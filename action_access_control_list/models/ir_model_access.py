# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import api, models
from odoo.addons.base.ir.ir_model import IrModelAccess as BaseIrModelAccess


class IrModelAccess(models.Model):

    _inherit = 'ir.model.access'

    @api.model
    def check(self, model, mode='read', raise_exception=True):
        if getattr(self.env, '_bypass_access', False):
            if self.env._bypass_exception != model:
                return True

        return super(IrModelAccess, self).check(
            model, mode=mode, raise_exception=raise_exception)

    @api.model_cr
    def call_cache_clearing_methods(self):
        self.invalidate_cache()
        # Only the following line was modified from the original method
        BaseIrModelAccess.check.clear_cache(self)
        for model, method in self.__cache_clearing_methods:
            if model in self.env:
                getattr(self.env[model], method)()
