# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    PROTECTED_FIELDS = {
        'account_id',
        'company_id',
        'currency_id',
        'date_due',
        'date_invoice',
        'fiscal_position',
        'internal_number',
        'invoice_line_ids',
        'journal_id',
        'name',
        'partner_id',
        'payment_term',
        'period_id',
        'tax_line_ids',
        'type',
    }

    PROTECTED_STATES = {
        'open',
        'paid',
    }

    @classmethod
    def get_protected_fields(cls):
        return cls.PROTECTED_FIELDS

    @classmethod
    def get_protected_states(cls):
        return cls.PROTECTED_STATES

    @api.multi
    def check_next_state(self, next_state):
        if next_state in self.get_protected_states():
            return

        for invoice in self:
            if invoice.journal_id.update_posted:
                continue

            if invoice.state in self.get_protected_states():
                raise ValidationError(_(
                    "The invoice %(invoice)s may not be "
                    "cancelled or set to draft because "
                    "it is validated."
                ) % {'invoice': invoice.name})

    @api.multi
    def write(self, vals):
        if vals.get('state'):
            self.check_next_state(vals['state'])

        protected_fields = self.get_protected_fields()
        if protected_fields.intersection(vals):
            for invoice in self:
                if invoice.state in self.get_protected_states():
                    field = tuple(protected_fields.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the invoice %(invoice)s "
                        "because it is validated") % {
                        'field': field,
                        'invoice': invoice.name,
                    })
        return super(AccountInvoice, self).write(vals)
