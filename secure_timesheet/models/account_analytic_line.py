# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    sheet_id = fields.Many2one(ondelete="restrict")
    project_id = fields.Many2one(ondelete="restrict")
    task_id = fields.Many2one(ondelete="restrict")

    @api.multi
    def check_unlink_access(self):
        for line in self:
            sheet = line.sheet_id
            if not sheet:
                continue
            if sheet.state in sheet.get_protected_states():
                raise ValidationError(_(
                    "You may not delete the timesheet line "
                    "%(line)s because it is bound to a confirmed "
                    "timesheet (%(timesheet)s).") % {
                    'line': line.name,
                    'timesheet': "%s - %s" % (
                        sheet.employee_id.name, sheet.name
                    ),
                })

    @api.multi
    def unlink(self):
        self.check_unlink_access()
        return super(AccountAnalyticLine, self).unlink()

    @api.multi
    def check_write_access(self, vals):
        protected_fields = self.get_protected_fields()
        protected_written = protected_fields.intersection(vals)
        if protected_written:
            for line in self:
                sheet = line.sheet_id
                if not sheet:
                    continue
                if sheet.state in sheet.get_protected_states():
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the timesheet line "
                        "%(line)s because it is bound to a confirmed "
                        "timesheet (%(timesheet)s).") % {
                        'field': protected_written.pop(),
                        'line': line.name,
                        'timesheet': "%s - %s" % (
                            sheet.employee_id.name, sheet.name
                        ),
                    })

    @api.multi
    def write(self, vals):
        self.check_write_access(vals)
        return super(AccountAnalyticLine, self).write(vals)

    # Bypass simple check from hr_timesheet_sheet module.
    # Superseded by check_write_access
    def _check_state(self):
        return True
