# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError

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


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    @api.multi
    def unlink(self):
        for line in self:
            if line.move_id.move_id.state == 'posted':
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
        if PROTECTED_FIELDS.intersection(vals):
            for line in self:
                if line.move_id.move_id.state == 'posted':
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the analytic line "
                        "%(line)s because it is bound to a posted "
                        "accounting entry (%(entry)s).") % {
                        'field': field,
                        'line': line.name,
                        'entry': line.move_id.move_id.name,
                    })
        return super(AccountAnalyticLine, self).write(vals)
