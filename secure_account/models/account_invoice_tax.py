# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError

PROTECTED_FIELDS = {
    'account_analytic_id',
    'account_id',
    'amount',
    'base',
    'base_amount',
    'base_code_id',
    'company_id',
    'factor_base',
    'factor_tax',
    'invoice_id',
    'manual',
    'name',
    'sequence',
    'tax_amount',
    'tax_code_id',
}


class AccountInvoiceTax(models.Model):

    _inherit = 'account.invoice.tax'

    @api.multi
    def unlink(self):
        for tax in self:
            if tax.invoice_id.state in ('open', 'paid'):
                raise ValidationError(_(
                    "You may not delete the invoice tax %(tax)s "
                    "because the invoice (%(invoice)s) "
                    "is not in draft state.") % {
                    'invoice': tax.invoice_id.name,
                    'tax': tax.name,
                })
        return super(AccountInvoiceTax, self).unlink()

    @api.multi
    def write(self, vals):
        if PROTECTED_FIELDS.intersection(vals):
            for tax in self:
                if tax.invoice_id.state in ('open', 'paid'):
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the invoice tax %(tax)s "
                        "because the invoice (%(invoice)s) "
                        "is not in draft state.") % {
                        'field': field,
                        'invoice': tax.invoice_id.name,
                        'tax': tax.name,
                    })
        return super(AccountInvoiceTax, self).write(vals)
