# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountInvoiceTax(models.Model):

    _inherit = 'account.invoice.tax'

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

    @classmethod
    def get_protected_fields(cls):
        return cls.PROTECTED_FIELDS

    @api.multi
    def unlink(self):
        for tax in self:
            invoice = tax.invoice_id
            if invoice.state in invoice.get_protected_states():
                raise ValidationError(_(
                    "You may not delete the invoice tax %(tax)s "
                    "because the invoice (%(invoice)s) "
                    "is validated.") % {
                    'invoice': tax.invoice_id.name,
                    'tax': tax.name,
                })
        return super(AccountInvoiceTax, self).unlink()

    @api.multi
    def write(self, vals):
        protected_fields = self.get_protected_fields()
        if protected_fields.intersection(vals):
            for tax in self:
                invoice = tax.invoice_id
                if invoice.state in invoice.get_protected_states():
                    field = tuple(protected_fields.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the invoice tax %(tax)s "
                        "because the invoice (%(invoice)s) "
                        "is validated.") % {
                        'field': field,
                        'invoice': tax.invoice_id.name,
                        'tax': tax.name,
                    })
        return super(AccountInvoiceTax, self).write(vals)
