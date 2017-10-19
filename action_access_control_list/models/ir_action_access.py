# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import api, models, fields


class IrActionAccess(models.Model):
    """Action Access Rule"""

    _name = 'ir.action.access'
    _description = __name__

    group_id = fields.Many2one(
        'res.groups',
        'Group',
        required=True,
        index=True,
        ondelete='cascade',
    )

    model_id = fields.Many2one(
        'ir.model',
        'Model',
        required=True,
        index=True,
        ondelete='cascade',
    )

    model_technical_name = fields.Char(
        'Model Technical Name',
        related='model_id.model',
        store=True,
        readonly=True,
        index=True,
    )

    action_id = fields.Many2one(
        'ir.action.protected',
        'Action',
        required=True,
        index=True,
        domain="[('model_id', '=', model_id)]"
    )

    action_technical_name = fields.Char(
        'Action Technical Name',
        related='action_id.technical_name',
        store=True,
        readonly=True,
        index=True,
    )

    filter_ids = fields.Many2many(
        'ir.action.access.filter', string='Domain Filters')

    active = fields.Boolean('Active', default=True)

    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.action_id.model_id != self.model_id:
            self.action_id = None

        self.filter_ids = self.filter_ids.filtered(
            lambda f: f.model_id == self.model_id)
