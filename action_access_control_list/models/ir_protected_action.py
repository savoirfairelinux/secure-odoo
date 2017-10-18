# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import models, fields, _
from odoo.osv import expression
from odoo.exceptions import AccessError
from odoo.tools.safe_eval import safe_eval


class IrProtectedAction(models.Model):
    """Secured Action"""

    _name = 'ir.protected.action'
    _description = __name__

    name = fields.Char(required=True)

    technical_name = fields.Char(
        'Technical Name',
        required=True,
        help='Name of the python method corresponding to the action'
    )

    model_id = fields.Many2one('ir.model', 'Model', index=True)

    model_technical_name = fields.Char(
        'Model Technical Name',
        related='model_id.model',
        store=True,
        readonly=True,
        index=True
    )

    active = fields.Boolean('Active', default=True)
    error_message = fields.Text(translate=True)

    def check_access(self, ids):
        if not self._check_domain(ids):
            raise AccessError(self._get_error_message(ids))
        return True

    def _check_domain(self, ids):
        access = self.env['ir.action.access'].search([
            ('group_id.users', '=', self.env.user.id),
            ('action_id', '=', self.id),
        ])
        for line in access:
            if not line.domain:
                return True

            if not ids:
                return False

            domain = expression.normalize_domain(safe_eval(line.domain))
            domain = expression.AND([[('id', 'in', ids)], domain])

            records = self.env[self.model_technical_name]\
                .sudo()\
                .with_context(active_test=False)\
                .search(domain)

            if set(ids).difference(records.ids):
                return False
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
