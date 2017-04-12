# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountMove(models.Model):

    _inherit = 'account.move'

    PROTECTED_FIELDS = {
        'company_id',
        'currency_id',
        'date',
        'journal_id',
        'line_id',
        'partner_id',
        'period_id',
        'name',
        'ref',
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
        for move in self:
            if move.state in self.get_protected_states():
                raise ValidationError(_(
                    "You may not delete the accounting entry %(entry)s "
                    "because it posted.") % {
                    'entry': move.name,
                })
        return super(AccountMove, self).unlink()

    @api.multi
    def write(self, vals):
        protected_fields = self.get_protected_fields()
        protected_written = protected_fields.intersection(vals)
        if protected_written:
            for move in self:
                if move.state in self.get_protected_states():
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the accounting entry %(entry)s "
                        "because it is posted.") % {
                        'field': protected_written.pop(),
                        'entry': move.name,
                    })
        return super(AccountMove, self).write(vals)
