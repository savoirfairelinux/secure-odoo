# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import api, models


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.model
    def get_action_access(self):
        actions = self.env['ir.action.protected'].sudo().search([])
        return actions.get_user_access(self.env.user)
