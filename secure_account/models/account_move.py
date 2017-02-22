# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models, _
from openerp.exceptions import ValidationError

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


class AccountMove(models.Model):

    _inherit = 'account.move'

    @api.multi
    def unlink(self):
        for move in self:
            if move.state == 'posted':
                raise ValidationError(_(
                    "You may not delete the accounting entry %(entry)s "
                    "because it posted.") % {
                    'entry': move.name,
                })
        return super(AccountMove, self).unlink()

    @api.multi
    def write(self, vals):
        if PROTECTED_FIELDS.intersection(vals):
            for move in self:
                if move.state == 'posted':
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the accounting entry %(entry)s "
                        "because it is posted.") % {
                        'field': field,
                        'entry': move.name,
                    })
        return super(AccountMove, self).write(vals)
