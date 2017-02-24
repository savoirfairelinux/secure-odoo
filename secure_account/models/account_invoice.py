# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError

PROTECTED_FIELDS = {
    'account_id',
    'company_id',
    'currency_id',
    'date_due',
    'date_invoice',
    'fiscal_position',
    'internal_number',
    'invoice_line',
    'journal_id',
    'name',
    'partner_id',
    'payment_term',
    'period_id',
    'tax_line',
    'type',
}


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def check_next_state(self, next_state):
        if next_state in ('open', 'paid'):
            return

        for invoice in self:
            if invoice.journal_id.update_posted:
                continue

            if invoice.state in ('open', 'paid'):
                raise ValidationError(_(
                    "The invoice %(invoice)s may not be "
                    "cancelled or set to draft because "
                    "it is validated."
                ) % {'invoice': invoice.name})

    @api.multi
    def write(self, vals):
        if vals.get('state'):
            self.check_next_state(vals['state'])

        if PROTECTED_FIELDS.intersection(vals):
            for invoice in self:
                if invoice.state in ('open', 'paid'):
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the invoice %(invoice)s "
                        "because it is validated") % {
                        'field': field,
                        'invoice': invoice.name,
                    })
        return super(AccountInvoice, self).write(vals)
