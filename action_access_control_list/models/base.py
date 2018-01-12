# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import api, models


class Base(models.AbstractModel):

    _inherit = 'base'

    @api.multi
    def check_access_rule(self, operation):
        if self._check_bypass_access():
            return

        return super(Base, self).check_access_rule(operation)

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        if self._check_bypass_access():
            return True

        return super(Base, self).check_access_rights(
            operation, raise_exception=raise_exception)

    @api.multi
    def check_field_access_rights(self, operation, fields):
        if self._check_bypass_access():
            if fields:
                return [f for f in fields if f in self._fields]
            else:
                return list(self._fields)

        return super(Base, self).check_field_access_rights(operation, fields)

    def _check_bypass_access(self):
        return (
            getattr(self.env, '_bypass_access', False) and
            self.env._bypass_exception != self._name
        )
