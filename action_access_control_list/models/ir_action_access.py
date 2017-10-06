# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import api, models, fields

class IrActionAccess(models.Model):

    """
    Actions access rule
    """

    _name = 'ir.action.access'

    group_id = fields.Many2one(
        string='Group',
        comodel_name='res.groups',
        required=True,
        index=True,
        ondelete='cascade',
    )

    model_id = fields.Many2one(
        string='Model',
        comodel_name='ir.model',
        required=True,
        index=True,
        ondelete='cascade',
    )

    model_technical_name = fields.Char(
        string='Model Technical Name',
        related='model_id.model',
        store=True,
        readonly=True,
        index=True,
    )

    action_id = fields.Many2one(
        string='Action',
        comodel_name='ir.protected.action',
        required=True,
        index=True,
    )

    action_technical_name = fields.Char(
        string='Model Technical Name',
        related='action_id.technical_name',
        store=True,
        Readonly=True,
        index=True,
    )

    domain = fields.Char()

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    @api.onchange('model_id')
    def _onchange_model_id(self):
        """
        Empty the action_id field
        """
        if self.action_id.model_id != self.model_id:
            self.action_id = None
