# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import api, models, fields, tools
from odoo.addons.mail.models.mail_template import mako_template_env


class IrActionAccessFilter(models.Model):
    """Action Access Filter"""

    _name = 'ir.action.access.filter'
    _description = __name__

    name = fields.Char(required=True)
    model_id = fields.Many2one(
        'ir.model', 'Model', required=True, ondelete='cascade')
    domain = fields.Text('Domain', required=True)
    different_domain = fields.Boolean(
        'Different Client/Server Side Domain',
        help="By default, the same domain will be used by "
        "both the client and the server side. If checked, "
        "a different domain will be used on the client side.")
    client_domain = fields.Text('Client Side Domain')
    active = fields.Boolean(default=True)

    @api.onchange('different_domain')
    def _onchange_different_domain(self):
        if not self.different_domain:
            self.client_domain = None

    def _eval_domain(self, domain, user):
        if '$' not in domain:
            return domain
        template = mako_template_env.from_string(tools.ustr(domain))
        return template.render({'user': user})

    def get_server_domain(self, user):
        return self._eval_domain(self.domain, user)

    def get_client_domain(self, user):
        domain = (
            self.client_domain if self.different_domain
            else self.domain)
        return self._eval_domain(domain, user)
