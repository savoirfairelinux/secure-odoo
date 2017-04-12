# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

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

    @classmethod
    def get_protected_fields(cls):
        return set(cls.PROTECTED_FIELDS)

    @classmethod
    def get_protected_states(cls):
        return set(cls.PROTECTED_STATES)

    @api.multi
    def unlink(self):
        for line in self:
            invoice = line.invoice_id
            if invoice.state in invoice.get_protected_states():
                raise ValidationError(_(
                    "You may not delete the invoice line %(line)s "
                    "because the invoice (%(invoice)s) "
                    "is validated.") % {
                    'invoice': line.invoice_id.name,
                    'line': line.name,
                })
        return super(AccountInvoiceLine, self).unlink()

    @api.multi
    def write(self, vals):
        protected_fields = self.get_protected_fields()
        protected_written = protected_fields.intersection(vals)
        if protected_written:
            for line in self:
                invoice = line.invoice_id
                if invoice.state in invoice.get_protected_states():
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the invoice line %(line)s "
                        "because the invoice (%(invoice)s) "
                        "is validated.") % {
                        'field': protected_written.pop(),
                        'invoice': line.invoice_id.name,
                        'line': line.name,
                    })
        return super(AccountInvoiceLine, self).write(vals)
