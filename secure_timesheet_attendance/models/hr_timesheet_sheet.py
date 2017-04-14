# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import models


class HrTimesheetSheet(models.Model):

    _inherit = 'hr_timesheet_sheet.sheet'

    # Bypass simple check from hr_attendance module.
    # Superseded by check_write_access in secure_timesheet
    def _check(self):
        return True
