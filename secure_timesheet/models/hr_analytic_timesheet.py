# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError
from openerp.addons.secure_account.models.account_analytic_line import (
    PROTECTED_FIELDS)


class HrAnalyticTimesheet(models.Model):

    _inherit = 'hr.analytic.timesheet'

    line_id = fields.Many2one(ondelete='restrict')

    @api.multi
    def check_unlink_access(self):
        for line in self:
            if line.sheet_id.state in ('confirm', 'done'):
                raise ValidationError(_(
                    "You may not delete the timesheet line "
                    "%(line)s because it is bound to a confirmed "
                    "timesheet (%(timesheet)s).") % {
                    'line': line.name,
                    'timesheet': "%s - %s" % (
                        line.sheet_id.employee_id.name, line.sheet_id.name
                    ),
                })

    @api.multi
    def unlink(self):
        self.check_unlink_access()
        return super(HrAnalyticTimesheet, self).unlink()

    @api.multi
    def check_write_access(self, vals):
        if PROTECTED_FIELDS.intersection(vals):
            for line in self:
                if line.sheet_id.state in ('confirm', 'done'):
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the timesheet line "
                        "%(line)s because it is bound to a confirmed "
                        "timesheet (%(timesheet)s).") % {
                        'field': field,
                        'line': line.name,
                        'timesheet': "%s - %s" % (
                            line.sheet_id.employee_id.name, line.sheet_id.name
                        ),
                    })

    @api.multi
    def write(self, vals):
        self.check_write_access(vals)
        return super(HrAnalyticTimesheet, self).write(vals)
