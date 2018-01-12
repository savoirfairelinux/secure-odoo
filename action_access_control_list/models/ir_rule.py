# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import api, models


class IrRule(models.Model):

    _inherit = 'ir.rule'

    @api.model
    def _compute_domain(self, model_name, mode="read"):
        if getattr(self.env, '_bypass_access', False):
            if self.env._bypass_exception != model_name:
                return []
        return super(IrRule, self)._compute_domain(model_name, mode=mode)
