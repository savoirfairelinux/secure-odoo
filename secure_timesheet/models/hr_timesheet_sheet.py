# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from openerp import api, models, _
from openerp.exceptions import ValidationError

PROTECTED_FIELDS = {
    'date_from',
    'date_to',
    'employee_id',
}


class HrTimesheetSheet(models.Model):

    _inherit = 'hr_timesheet_sheet.sheet'

    @api.multi
    def check_unlink_access(self):
        for sheet in self:
            if sheet.state in ('confirm', 'done'):
                raise ValidationError(_(
                    "You may not delete the timesheet "
                    "%(timesheet)s because it is already confirmed.") % {
                    'timesheet': "%s - %s" % (
                        sheet.employee_id.name, sheet.name
                    ),
                })

    @api.multi
    def unlink(self):
        self.check_unlink_access()
        return super(HrTimesheetSheet, self).unlink()

    @api.multi
    def check_write_access(self, vals):
        if PROTECTED_FIELDS.intersection(vals):
            for sheet in self:
                if sheet.state in ('confirm', 'done'):
                    field = tuple(PROTECTED_FIELDS.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the timesheet %(timesheet)s"
                        "because it is already confirmed.") % {
                        'field': field,
                        'timesheet': "%s - %s" % (
                            sheet.employee_id.name, sheet.name
                        ),
                    })

    @api.multi
    def write(self, vals):
        self.check_write_access(vals)
        return super(HrTimesheetSheet, self).write(vals)
