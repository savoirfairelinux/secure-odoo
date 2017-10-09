# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import models, fields


class IrProtectedAction(models.Model):

    """
    Secured action
    """

    _name = 'ir.protected.action'

    name = fields.Char(
        required=True,
    )

    technical_name = fields.Char(
        string='Technical Name',
        required=True,
        help='Name of the python method corresponding to the action'
    )

    model_id = fields.Many2one(
        comodel_name='ir.model',
    )

    model_technical_name = fields.Char(
        related='model_id.model',
        store=True,
        readonly=True,
        index=True
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )
