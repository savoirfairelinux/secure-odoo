# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError

PROTECTED_FIELDS = {
    'account_id',
    'amount_currency',
    'analytic_account_id',
    'credit',
    'currency_id',
    'date',
    'date_maturity',
    'debit',
    'journal_id',
    'move_id',
    'name',
    'partner_id',
    'period_id',
    'product_id',
    'product_tax_id',
    'product_uom_id',
    'quantity',
    'ref',
}


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    @api.multi
    def unlink(self):
        for line in self:
            if line.move_id.state == 'posted':
                raise ValidationError(_(
                    "You may not delete the accounting item "
                    "%(line)s because it is bound to a posted "
                    "accounting entry (%(entry)s).") % {
                    'line': line.name,
                    'entry': line.move_id.name,
                })
        return super(AccountMoveLine, self).unlink()

    @api.multi
    def write(self, vals):
        if PROTECTED_FIELDS.intersection(vals):
            for line in self:
                if line.move_id.state == 'posted':
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the accounting item "
                        "%(line)s because it is bound to a posted "
                        "accounting entry (%(entry)s).") % {
                        'field': field,
                        'line': line.name,
                        'entry': line.move_id.name,
                    })
        return super(AccountMoveLine, self).write(vals)
