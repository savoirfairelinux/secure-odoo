# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class HrTimesheetSheet(models.Model):

    _inherit = 'hr_timesheet_sheet.sheet'

    # TODO? ondelete=restrict on timesheet_ids field

    PROTECTED_FIELDS = {
        'date_from',
        'date_to',
        'employee_id',
    }

    PROTECTED_STATES = {
        'confirm',
        'done',
    }

    @classmethod
    def get_protected_fields(cls):
        return cls.PROTECTED_FIELDS

    @classmethod
    def get_protected_states(cls):
        return cls.PROTECTED_STATES

    @api.multi
    def check_unlink_access(self):
        for sheet in self:
            if sheet.state in self.get_protected_states():
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
        protected_fields = self.get_protected_fields()
        if protected_fields.intersection(vals):
            for sheet in self:
                if sheet.state in ('confirm', 'done'):
                    field = tuple(protected_fields.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the timesheet %(timesheet)s "
                        "because it is already confirmed.") % {
                        'field': field,
                        'timesheet': "%s - %s" % (
                            sheet.employee_id.name, sheet.name
                        ),
                    })

    # Bypass simple check from hr_timesheet_sheet module.
    # Superseded by check_write_access
    def _check_state(self):
        return True

    @api.multi
    def write(self, vals):
        self.check_write_access(vals)
        return super(HrTimesheetSheet, self).write(vals)
