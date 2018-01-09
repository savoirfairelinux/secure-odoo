# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import models, fields, _
from odoo.osv.expression import AND, OR, normalize_domain
from odoo.exceptions import AccessError
from odoo.tools.safe_eval import safe_eval


class IrProtectedAction(models.Model):
    """Protected Action"""

    _name = 'ir.action.protected'
    _description = __name__

    name = fields.Char(required=True)

    type = fields.Selection([
        ('python', 'Python Method'),
        ('action', 'XML Action'),
    ], required=True, default='python')

    technical_name = fields.Char(
        'Technical Name',
        help='Name of the python method related to the action.'
    )

    action_id = fields.Many2one(
        'ir.actions.actions', 'Action', index=True,
        help='The XML action related to the secured action.')

    model_id = fields.Many2one(
        'ir.model', 'Model', index=True, required=True)

    model_technical_name = fields.Char(
        'Model Technical Name',
        related='model_id.model',
        store=True,
        readonly=True,
        index=True,
    )

    active = fields.Boolean('Active', default=True)
    error_message = fields.Text(translate=True)

    def check_access(self, user, ids):
        if not self._check_domain(user, ids):
            raise AccessError(self._get_error_message(ids))
        return True

    def _check_domain(self, user, ids):
        access = self.env['ir.action.access'].search([
            ('group_id.users', '=', user.id),
            ('action_id', '=', self.id),
        ])
        for line in access:
            if not line.filter_ids:
                return True

            if not ids:
                continue

            domain = [
                normalize_domain(safe_eval(f.get_server_domain(user)))
                for f in line.filter_ids
            ]
            domain.append([('id', 'in', ids)])
            domain = AND(domain)

            records = self.env[self.model_technical_name]\
                .sudo()\
                .with_context(active_test=False)\
                .search(domain)

            if set(ids).difference(records.ids):
                continue
            return True
        return False

    def _get_error_message(self, ids):
        if self.error_message:
            return self.error_message
        return _(
            'You are not allowed to trigger the action '
            '%(action)s on the records of model %(model)s '
            'with ids %(ids)s.') % {
            'action': self.technical_name,
            'model': self.model_technical_name,
            'ids': ids,
        }

    def get_user_access(self, user):
        # {action: [always_visible, restriction_domain]}
        action_values = {a: [False, []] for a in self}

        acl = self.env['ir.action.access'].search([
            ('action_id', 'in', self.ids),
            ('group_id.users', '=', user.id),
        ])

        for line in acl:
            if not line.filter_ids:
                action_values[line.action_id][0] = True
            else:
                domain = [
                    normalize_domain(safe_eval(f.get_client_domain(user)))
                    for f in line.filter_ids
                ]
                action_values[line.action_id][1].append(
                    AND(domain))

        res = []
        for a, vals in action_values.items():
            access = {
                'model': a.model_technical_name,
                'type': a.type,
                'technical_name': a.technical_name,
                'action_id': a.action_id.id,
                'domain': False,
            }
            if vals[0]:
                access['domain'] = True
            elif not vals[1]:
                access['domain'] = False
            else:
                access['domain'] = OR(vals[1])
            res.append(access)
        return res
