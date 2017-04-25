# -*- coding: utf-8 -*-
# © 2011 Smile
# © 2017 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from openerp import api, models


class ResGroups(models.Model):

    _inherit = 'res.groups'

    @api.multi
    def write(self, vals):
        old_users = self.users
        res = super(ResGroups, self).write(vals)
        new_users = self.users
        all_users = old_users | new_users
        all_users.filtered(
            lambda u: u.user_profile).update_users_linked_to_profile()
        return res

    @api.model
    def create(self, vals):
        res = super(ResGroups, self).create(vals)
        res.users.filtered(
            lambda u: u.user_profile).update_users_linked_to_profile()
        return res
