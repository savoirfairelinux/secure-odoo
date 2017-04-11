# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.tests import common


class TestAccountBase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAccountBase, cls).setUpClass()

        yesterday = datetime.now() - relativedelta(days=1)
        cls.company = cls.env['res.company'].create({
            'name': 'My Testing Company',
            'fiscalyear_last_day': yesterday.day,
            'fiscalyear_last_month': yesterday.month,
        })

        cls.cad = cls.env['res.currency'].search(
            [('name', '=', 'CAD'), '|', ('active', '=', True),
             ('active', '=', False)])
        if not cls.cad:
            cls.cad = cls.env['res.currency'].create({
                'name': 'CAD',
                'symbol': '$',
                'rate_ids': [
                    (0, 0, {
                        'name': datetime.now().date(),
                        'rate': 1,
                    }),
                ],
            })
        cls.cad.active = True

        cls.company.currency_id = cls.cad

        cls.env.user.company_id = cls.company

        cls.partner_1 = cls.env['res.partner'].create({
            'name': 'Partner 1',
            'company_id': cls.company.id,
        })

        cls.partner_2 = cls.env['res.partner'].create({
            'name': 'Partner 2',
            'company_id': cls.company.id,
        })

        cls.analytic_acc_1 = cls.env['account.analytic.account'].create({
            'name': 'Analytic Account 1',
            'code': '1000001',
            'company_id': cls.company.id,
            'currency_id': cls.cad.id,
        })

        cls.analytic_acc_2 = cls.env['account.analytic.account'].create({
            'name': 'Analytic Account 2',
            'code': '1000002',
            'company_id': cls.company.id,
            'currency_id': cls.cad.id,
        })

        cls.account_1 = cls.env['account.account'].create({
            'name': 'Cash',
            'code': '1000001',
            'user_type_id': cls.env.ref(
                'account.data_account_type_liquidity').id,
            'company_id': cls.company.id,
        })

        cls.account_2 = cls.env['account.account'].create({
            'name': 'Expense',
            'code': '6000001',
            'user_type_id': cls.env.ref(
                'account.data_account_type_expenses').id,
            'company_id': cls.company.id,
        })

        cls.account_3 = cls.env['account.account'].create({
            'name': 'Payable',
            'code': '2000001',
            'user_type_id': cls.env.ref(
                'account.data_account_type_payable').id,
            'company_id': cls.company.id,
            'reconcile': True,
        })

        cls.account_4 = cls.env['account.account'].create({
            'name': 'Receivable',
            'code': '2000011',
            'user_type_id': cls.env.ref(
                'account.data_account_type_receivable').id,
            'company_id': cls.company.id,
            'reconcile': True,
        })

        cls.account_5 = cls.env['account.account'].create({
            'company_id': cls.company.id,
            'name': 'Income',
            'code': '600001',
            'user_type_id': cls.env.ref(
                'account.data_account_type_revenue').id,
        })

        cls.company.property_account_expense_categ_id = cls.account_2
        cls.company.property_account_payable_id = cls.account_3
        cls.company.property_account_receivable_id = cls.account_4
        cls.company.property_account_income_categ_id = cls.account_5

        cls.account_tax = cls.env['account.account'].create({
            'name': 'Tax Account',
            'code': '2000002',
            'user_type_id': cls.env.ref('account.data_account_type_payable').id,
            'company_id': cls.company.id,
            'reconcile': True,
        })

        cls.journal = cls.env['account.journal'].create({
            'name': 'Journal 1',
            'code': 'TEST1',
            'type': 'cash',
            'company_id': cls.company.id,
        })

        line_1_vals = {
            'name': 'Test',
            'account_id': cls.account_1.id,
            'analytic_account_id': cls.analytic_acc_1.id,
            'debit': 100,
            'company_id': cls.company.id,
        }

        line_2_vals = {
            'name': 'Test',
            'account_id': cls.account_3.id,
            'credit': 100,
            'partner_id': cls.partner_1.id,
            'company_id': cls.company.id,
        }

        cls.move = cls.env['account.move'].create({
            'journal_id': cls.journal.id,
            'partner_id': cls.partner_1.id,
            'company_id': cls.company.id,
            'line_ids': [(0, 0, line_1_vals), (0, 0, line_2_vals)],
        })

        cls.line_1 = cls.move.line_ids.filtered(lambda r: r.debit == 100)
        cls.line_2 = cls.move.line_ids.filtered(lambda r: r.credit == 100)
