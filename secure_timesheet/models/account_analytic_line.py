# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    # TODO: should we protect project.project? protect analytic lines
    # attached to projects in a certain state?

    @api.multi
    def check_unlink_access(self):
        for line in self:
            sheet = line.sheet_id
            # TODO: what do we do if there is no associated timesheet?
            # Is that ever the case?
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
        if protected_fields.intersection(vals):
            for line in self:
                sheet = line.sheet_id
                # TODO: what do we do if there is no associated timesheet?
                # Is that ever the case?
                if sheet.state in sheet.get_protected_states():
                    field = tuple(protected_fields.intersection(vals))[0]
                    raise ValidationError(_(
                        "You may not modify the field %(field)s "
                        "of the timesheet line "
                        "%(line)s because it is bound to a confirmed "
                        "timesheet (%(timesheet)s).") % {
                        'field': field,
                        'line': line.name,
                        'timesheet': "%s - %s" % (
                            sheet.employee_id.name, sheet.name
                        ),
                    })

    @api.multi
    def write(self, vals):
        self.check_write_access(vals)
        return super(AccountAnalyticLine, self).write(vals)
