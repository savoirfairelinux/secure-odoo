# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo.addons.action_access_control_list.controllers.main import \
    ProtectedEnvironment
from odoo.exceptions import AccessError
from odoo.tests import SavepointCase


class TestInvoice(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestInvoice, cls).setUpClass()

        cls.company = cls.env.ref('base.main_company')
        cls.test_user = cls.env.ref('base.user_demo')

        cls.env['ir.action.protected'].search([]).unlink()

        cls.journal = cls.env['account.journal'].create({
            'name': 'Journal 1',
            'code': 'TEST1',
            'type': 'sale',
            'company_id': cls.company.id,
        })

        cls.receivable = cls.env['account.account'].create({
            'name': 'Receivable',
            'code': '1111111',
            'user_type_id': cls.env.ref(
                'account.data_account_type_receivable').id,
            'company_id': cls.company.id,
            'reconcile': True,
        })

        cls.expense = cls.env['account.account'].create({
            'name': 'Expense',
            'code': '6111111',
            'user_type_id': cls.env.ref(
                'account.data_account_type_expenses').id,
            'company_id': cls.company.id,
        })

        cls.partner = cls.env['res.partner'].create({'name': 'Customer'})

        cls.out_invoice = cls.env['account.invoice'].create({
            'account_id': cls.receivable.id,
            'partner_id': cls.partner.id,
            'journal_id': cls.journal.id,
            'type': 'out_invoice',
        })

        cls.account_invoice_line_1 = cls.env['account.invoice.line'].create({
            'invoice_id': cls.out_invoice.id,
            'name': 'Line 1',
            'account_id': cls.expense.id,
            'price_unit': 20,
        })

        cls.env['ir.model.access'].search(
            [('group_id.users', '=', cls.test_user.id)]).unlink()

        cls.env['ir.action.protected'].search([]).unlink()

        cls.action = cls.env['ir.action.protected'].create({
            'name': 'Validate Invoices',
            'type': 'python',
            'technical_name': 'action_invoice_open',
            'model_id': cls.env.ref('account.model_account_invoice').id,
        })

    def test_01_invoice_validate(self):
        env = ProtectedEnvironment(self.env.cr, self.test_user.id, {})
        inv = env['account.invoice'].browse(self.out_invoice.id)
        inv.action_invoice_open()
        self.assertTrue(inv.move_id)

    def test_02_invoice_validate_not_secured(self):
        inv = self.out_invoice.sudo(self.test_user)
        with self.assertRaises(AccessError):
            inv.action_invoice_open()

    def _add_action_access(self, domain=None):
        self.env['ir.action.access'].create({
            'action_id': self.action.id,
            'group_id': self.test_user.groups_id[0].id,
            'model_id': self.env.ref('account.model_account_invoice').id,
            'filter_ids': [(0, 0, {
                'name': 'Custom Filter',
                'model_id': self.env.ref('account.model_account_invoice').id,
                'domain': domain,
            })] if domain is not None else None,
        })

    def test_10_check_access_success(self):
        self._add_action_access()
        self.action.check_access(self.test_user, [self.out_invoice.id])

    def test_11_check_access_no_access(self):
        with self.assertRaises(AccessError):
            self.action.check_access(self.test_user, [self.out_invoice.id])

    def test_12_check_access_with_domain(self):
        self._add_action_access("[('type', '=', 'out_invoice')]")
        self.action.check_access(self.test_user, [self.out_invoice.id])

    def test_13_check_access_wrong_domain(self):
        self._add_action_access("[('type', '=', 'in_invoice')]")
        with self.assertRaises(AccessError):
            self.action.check_access(self.test_user, [self.out_invoice.id])

    def test_14_check_access_both_domain(self):
        self._add_action_access("[('type', '=', 'out_invoice')]")
        self._add_action_access("[('type', '=', 'in_invoice')]")
        self.action.check_access(self.test_user, [self.out_invoice.id])

    def test_15_check_access_dynamic_domain(self):
        self.out_invoice.user_id = self.test_user
        self._add_action_access("[('user_id', '=', ${user.id})]")
        self.action.check_access(self.test_user, [self.out_invoice.id])

    def test_16_check_access_dynamic_wrong_domain(self):
        self.out_invoice.user_id = self.test_user
        self._add_action_access("[('user_id', '!=', ${user.id})]")
        with self.assertRaises(AccessError):
            self.action.check_access(self.test_user, [self.out_invoice.id])

    def _add_read_access(self):
        self.env['ir.model.access'].create({
            'name': 'Invoice Access',
            'group_id': self.test_user.groups_id[0].id,
            'model_id': self.env.ref('account.model_account_invoice').id,
            'perm_read': 1,
            'perm_write': 0,
            'perm_create': 0,
            'perm_unlink': 0,
        })

    def test_20_invoice_read(self):
        self.out_invoice.action_invoice_open()
        self._add_read_access()
        env = ProtectedEnvironment(self.env.cr, self.test_user.id, {})
        env._bypass_exception = 'account.invoice'
        inv = env['account.invoice'].browse(self.out_invoice.id)
        inv.read(fields=['outstanding_credits_debits_widget'])

    def test_21_invoice_read_not_secured(self):
        self.out_invoice.action_invoice_open()
        self._add_read_access()
        inv = self.out_invoice.sudo(self.test_user)
        with self.assertRaises(AccessError):
            inv.read(fields=['outstanding_credits_debits_widget'])

    def test_22_invoice_read_no_access(self):
        self.out_invoice.action_invoice_open()
        env = ProtectedEnvironment(self.env.cr, self.test_user.id, {})
        env._bypass_exception = 'account.invoice'
        inv = env['account.invoice'].browse(self.out_invoice.id)
        with self.assertRaises(AccessError):
            inv.read(fields=['outstanding_credits_debits_widget'])

    def _compate_access_dicts(self, item1, item2):
        self.assertEquals(item1['model'], item2['model'])
        self.assertEquals(item1['technical_name'], item2['technical_name'])
        self.assertEquals(item1['domain'], item2['domain'])

    def test_30_get_action_access_no_access(self):
        res = self.env['res.users'].sudo(self.test_user).get_action_access()
        self._compate_access_dicts(res[0], {
            'model': 'account.invoice',
            'technical_name': 'action_invoice_open',
            'domain': False,
        })

    def test_31_get_action_access_no_domain(self):
        self._add_action_access()
        res = self.env['res.users'].sudo(self.test_user).get_action_access()
        self._compate_access_dicts(res[0], {
            'model': 'account.invoice',
            'technical_name': 'action_invoice_open',
            'domain': True,
        })

    def test_32_get_action_access_with_domain(self):
        self._add_action_access("[('type', '=', 'out_invoice')]")
        res = self.env['res.users'].sudo(self.test_user).get_action_access()
        self._compate_access_dicts(res[0], {
            'model': 'account.invoice',
            'technical_name': 'action_invoice_open',
            'domain': [('type', '=', 'out_invoice')],
        })

    def test_33_get_action_access_user_not_in_group(self):
        self._add_action_access()
        self.test_user.write({'groups_id': [(5, 0)]})
        res = self.env['res.users'].sudo(self.test_user).get_action_access()
        self._compate_access_dicts(res[0], {
            'model': 'account.invoice',
            'technical_name': 'action_invoice_open',
            'domain': False,
        })
