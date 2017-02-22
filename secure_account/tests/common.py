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

        cls.company = cls.env['res.company'].create({
            'name': 'My Testing Company',
        })

        cls.cad = cls.env['res.currency'].create({
            'name': 'CAD',
            'company_id': cls.company.id,
            'rate_ids': [
                (0, 0, {
                    'name': datetime.now().date(),
                    'rate': 1,
                }),
            ],
        })

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

        cls.analytic_journal = cls.env['account.analytic.journal'].create({
            'name': 'Journal 1',
            'code': 'TEST1',
            'company_id': cls.company.id,
        })

        cls.account_1 = cls.env['account.account'].create({
            'name': 'Cash',
            'code': '1000001',
            'user_type': cls.env.ref('account.data_account_type_cash').id,
            'type': 'liquidity',
            'company_id': cls.company.id,
        })

        cls.account_2 = cls.env['account.account'].create({
            'name': 'Expense',
            'code': '6000001',
            'user_type': cls.env.ref('account.data_account_type_expense').id,
            'type': 'other',
            'company_id': cls.company.id,
        })

        cls.account_3 = cls.env['account.account'].create({
            'name': 'Payable',
            'code': '2000001',
            'user_type': cls.env.ref('account.data_account_type_payable').id,
            'type': 'payable',
            'company_id': cls.company.id,
        })

        cls.account_tax = cls.env['account.account'].create({
            'name': 'Tax Account',
            'code': '2000002',
            'user_type': cls.env.ref('account.data_account_type_payable').id,
            'type': 'payable',
            'company_id': cls.company.id,
        })

        cls.journal = cls.env['account.journal'].create({
            'name': 'Journal 1',
            'code': 'TEST1',
            'type': 'cash',
            'analytic_journal_id': cls.analytic_journal.id,
            'company_id': cls.company.id,
        })

        now = datetime.now()
        cls.year = cls.env['account.fiscalyear'].create({
            'name': 'Current Year',
            'code': str(now.year),
            'date_start': now,
            'date_stop': now + relativedelta(month=12),
            'company_id': cls.company.id,
        })

        cls.year.create_period()
        cls.period = cls.year.period_ids[0]
        cls.period.company_id = cls.company

        cls.move = cls.env['account.move'].create({
            'period_id': cls.period.id,
            'journal_id': cls.journal.id,
            'partner_id': cls.partner_1.id,
            'company_id': cls.company.id,
        })

        cls.line_1 = cls.env['account.move.line'].create({
            'move_id': cls.move.id,
            'name': 'Test',
            'account_id': cls.account_1.id,
            'analytic_account_id': cls.analytic_acc_1.id,
            'debit': 100,
            'company_id': cls.company.id,
        })

        cls.line_2 = cls.env['account.move.line'].create({
            'move_id': cls.move.id,
            'name': 'Test',
            'account_id': cls.account_3.id,
            'credit': 100,
            'partner_id': cls.partner_1.id,
            'company_id': cls.company.id,
        })
