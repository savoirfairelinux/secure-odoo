# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import api
from odoo.addons.sale.models.sale_analytic import AccountAnalyticLine


create_original = AccountAnalyticLine.create
write_original = AccountAnalyticLine.write
unlink_original = AccountAnalyticLine.unlink


def is_module_installed(env):
    return 'disable_sale_analytic' in env.registry._init_modules


@api.model
def create(self, vals):
    if is_module_installed(self.env):
        return super(AccountAnalyticLine, self).create(vals)
    else:
        create_original(self, vals)


@api.multi
def write(self, vals):
    if is_module_installed(self.env):
        return super(AccountAnalyticLine, self).write(vals)
    else:
        write_original(self, vals)


@api.multi
def unlink(self):
    if is_module_installed(self.env):
        return super(AccountAnalyticLine, self).unlink()
    else:
        unlink_original(self)


AccountAnalyticLine.create = create
AccountAnalyticLine.write = write
AccountAnalyticLine.unlink = unlink
