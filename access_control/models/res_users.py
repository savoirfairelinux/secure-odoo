# -*- coding: utf-8 -*-
# © 2011 Smile
# © 2017 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from collections import defaultdict
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError


class ResUsers(models.Model):

    _inherit = 'res.users'

    user_profile = fields.Boolean('Is User Profile')
    user_profile_ids = fields.Many2many(
        'res.users',
        'res_user_profile_rel',
        'profile_id',
        'user_id',
        'User Profile',
        domain=[
            ('id', '!=', SUPERUSER_ID), ('user_profile', '=', True),
            '|', ('active', '=', True), ('active', '=', False),
        ])

    user_ids = fields.Many2many(
        'res.users',
        'res_user_profile_rel',
        'user_id',
        'profile_id',
        'Users',
        domain=[('user_profile', '=', False)],
        copy=False)

    @api.multi
    def update_from_profile(self):
        users_by_profile = defaultdict(set)

        group_erp = self.env.ref('base.group_erp_manager')

        if group_erp in self.mapped('user_profile_ids.groups_id'):
            if group_erp not in self.env.user.groups_id:
                raise AccessError(_(
                    'You are not allowed to grant administration access '
                    'to a user.'))

        for user in self:
            users_by_profile[tuple(user.user_profile_ids.ids)].add(user.id)

        for profile_ids, user_ids in users_by_profile.items():
            users = self.browse(list(user_ids))
            profiles = self.browse(profile_ids)
            group_ids = list(set(profiles.mapped('groups_id').ids))
            users.sudo().with_context(updating_groups=True).write(
                {'groups_id': [(6, 0, group_ids)]})

    @api.multi
    def update_users_linked_to_profile(self):
        self = self.with_context(active_test=False)
        self.mapped('user_ids').update_from_profile()

    @api.model
    def create(self, vals):
        record = super(ResUsers, self).create(vals)
        if record.user_profile_ids:
            record.update_from_profile()
        if record.user_profile:
            record.update_users_linked_to_profile()
        return record

    @api.multi
    def write(self, vals):
        vals = self._remove_reified_groups(vals)
        if 'user_profile_ids' in vals and 'groups_id' in vals:
            del vals['groups_id']

        # Prevent any standard user from adding groups directly to a
        # user. Do not raise an exception, because Odoo automatically
        # adds groups when creating a user.
        group_erp = self.env.ref('base.group_erp_manager')
        if 'groups_id' in vals and group_erp not in self.env.user.groups_id:
            del vals['groups_id']

        res = super(ResUsers, self).write(vals)
        if vals.get('user_profile_ids'):
            self.update_from_profile()

        profiles = self.filtered(lambda u: u.user_profile)
        if profiles:
            if group_erp not in self.env.user.groups_id:
                raise AccessError(_(
                    'You are not allowed to modify a user profile.'))
            profiles.update_users_linked_to_profile()

        return res
