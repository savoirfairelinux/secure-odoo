# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError

PROTECTED_FIELDS = {
    'account_analytic_id',
    'account_id',
    'company_id',
    'discount',
    'invoice_id',
    'invoice_line_tax_id',
    'name',
    'origin',
    'partner_id',
    'price_subtotal',
    'price_unit',
    'product_id',
    'quantity',
    'sequence',
    'uos_id',
}


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    @api.multi
    def unlink(self):
        for line in self:
            if line.invoice_id.state in ('open', 'paid'):
                raise ValidationError(_(
                    "You may not delete the invoice line %(line)s "
                    "because the invoice (%(invoice)s) "
                    "is not in draft state.") % {
                    'invoice': line.invoice_id.name,
                    'line': line.name,
                })
        return super(AccountInvoiceLine, self).unlink()

    @api.multi
    def write(self, vals):
        if PROTECTED_FIELDS.intersection(vals):
            for line in self:
                if line.invoice_id.state in ('open', 'paid'):
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the invoice line %(line)s "
                        "because the invoice (%(invoice)s) "
                        "is not in draft state.") % {
                        'field': field,
                        'invoice': line.invoice_id.name,
                        'line': line.name,
                    })
        return super(AccountInvoiceLine, self).write(vals)
