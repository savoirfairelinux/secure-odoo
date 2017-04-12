# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

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

    @classmethod
    def get_protected_fields(cls):
        return set(cls.PROTECTED_FIELDS)

    @api.multi
    def unlink(self):
        for line in self:
            move = line.move_id
            if move.state in move.get_protected_states():
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
        protected_fields = self.get_protected_fields()
        protected_written = protected_fields.intersection(vals)
        if protected_written:
            for line in self:
                move = line.move_id
                if move.state in move.get_protected_states():
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the accounting item "
                        "%(line)s because it is bound to a posted "
                        "accounting entry (%(entry)s).") % {
                        'field': protected_written.pop(),
                        'line': line.name,
                        'entry': line.move_id.name,
                    })
        return super(AccountMoveLine, self).write(vals)
