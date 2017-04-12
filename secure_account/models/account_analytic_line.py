# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    PROTECTED_FIELDS = {
        'account_id',
        'amount',
        'amount_currency',
        'company_id',
        'currency_id',
        'date',
        'general_account_id',
        'journal_id',
        'move_id',
        'product_id',
        'product_uom_id',
        'unit_amount',
    }

    PROTECTED_STATES = {
        'posted',
    }

    @classmethod
    def get_protected_fields(cls):
        return set(cls.PROTECTED_FIELDS)

    @classmethod
    def get_protected_states(cls):
        return set(cls.PROTECTED_STATES)

    @api.multi
    def unlink(self):
        for line in self:
            if line.move_id.move_id.state in self.get_protected_states():
                raise ValidationError(_(
                    "You may not delete the analytic line "
                    "%(line)s because it is bound to a posted "
                    "accounting entry (%(entry)s).") % {
                    'line': line.name,
                    'entry': line.move_id.move_id.name,
                })
        return super(AccountAnalyticLine, self).unlink()

    @api.multi
    def write(self, vals):
        protected_fields = self.get_protected_fields()
        protected_written = protected_fields.intersection(vals)
        if protected_written:
            for line in self:
                if line.move_id.move_id.state in self.get_protected_states():
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the analytic line "
                        "%(line)s because it is bound to a posted "
                        "accounting entry (%(entry)s).") % {
                        'field': protected_written.pop(),
                        'line': line.name,
                        'entry': line.move_id.move_id.name,
                    })
        return super(AccountAnalyticLine, self).write(vals)
