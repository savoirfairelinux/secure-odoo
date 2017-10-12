# -*- coding: utf-8 -*-
# © 2011 Smile
# © 2017 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo.tests import HttpCase

class TestActionAccessControlList(HttpCase):

    def setUp(self):
        super(TestActionAccessControlList, self).setUp()
        self.test_user = self.env['res.users'].create({
            'name': 'acme_user',
            'login': 'acme_user',
            'active': True,
        })
        self.protected_action = self.env['ir.protected.action'].create({
            'name': 'invoice_validate',
            'technical_name': 'action_invoice_open',
            'model_id': self.env['account.invoice'],
        })
        self.journal = self.env['account.journal'].create({
            'name': 'acme_journal',
        })
        self.partner = self.env['res.partner'].create({
            'name': 'acme_partner',
        })
        self.account = self.env['account.account'].create({
            'name': 'acme_account',
        })
        self.out_invoice = self.env['account.invoice'].create({
            'account_id': self.account,
            'partner_id': self.partner,
        })

    def test_01_invoice_validate(self):
        """No Access"""
        self.phantom_js("/web#action=account_invoice.action_invoice_open",
                        "", login="acme_user")
        self.assertTrue(False)

    def test_02_invoice_validate(self):
        """Access without domain"""
        self.assertFalse(True)

    def test_03_invoice_validate(self):
        """Access with domain"""
        self.assertFalse(True)

    def test_04_invoice_validate(self):
        """Access with another domain"""
        self.assertTrue(False)
