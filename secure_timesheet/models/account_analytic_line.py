# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from openerp import api, models


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    @api.multi
    def unlink(self):
        timesheet_lines = self.env['hr.analytic.timesheet'].search([
            ('line_id', 'in', self.ids),
        ])
        timesheet_lines.check_unlink_access()
        return super(AccountAnalyticLine, self).unlink()

    @api.multi
    def write(self, vals):
        timesheet_lines = self.env['hr.analytic.timesheet'].search([
            ('line_id', 'in', self.ids),
        ])
        timesheet_lines.check_write_access(vals)
        return super(AccountAnalyticLine, self).write(vals)
