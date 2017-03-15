# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from dateutil.relativedelta import relativedelta
from datetime import datetime
from openerp.exceptions import ValidationError
from openerp import fields
from . import common


class TestInvoice(common.TestAccountBase):

    @classmethod
    def setUpClass(cls):
        super(TestInvoice, cls).setUpClass()

        cls.customer = cls.env['res.partner'].create({
            'name': 'Customer 1',
            'customer': True,
            'company_id': cls.company.id,
        })

        cls.date_invoice = fields.Date.to_string(datetime.now())

        cls.invoice = cls.env['account.invoice'].create({
            'partner_id': cls.customer.id,
            'type': 'out_invoice',
            'currency_id': cls.cad.id,
            'date_invoice': cls.date_invoice,
            'account_id': cls.account_3.id,
            'company_id': cls.company.id,
        })

        cls.invoice_line = cls.env['account.invoice.line'].create({
            'invoice_id': cls.invoice.id,
            'name': 'Invoice Line 1',
            'price_unit': 20,
            'quantity': 5,
            'account_id': cls.account_2.id,
        })

        cls.tax_line = cls.env['account.invoice.tax'].create({
            'invoice_id': cls.invoice.id,
            'name': 'Tax Line 1',
            'amount': 15,
            'manual': True,
            'account_id': cls.account_tax.id,
        })

    def validate_invoice(self):
        self.invoice.action_invoice_open()

    def test_01_delete_invoice_line_draft(self):
        self.assertEqual(len(self.invoice.invoice_line_ids), 1)
        self.invoice.invoice_line_ids.unlink()
        self.assertEqual(len(self.invoice.invoice_line_ids), 0)

    def test_02_delete_invoice_line_posted(self):
        self.validate_invoice()
        self.assertEqual(len(self.invoice.invoice_line_ids), 1)
        with self.assertRaises(ValidationError):
            self.invoice.invoice_line_ids.unlink()

    def test_03_write_invoice_line_draft(self):
        self.assertEqual(len(self.invoice.invoice_line_ids), 1)
        self.assertEqual(self.invoice.invoice_line_ids.price_unit, 20)
        self.invoice.invoice_line_ids.price_unit = 30
        self.assertEqual(self.invoice.invoice_line_ids.price_unit, 30)

    def test_04_write_invoice_line_posted(self):
        self.validate_invoice()
        self.assertEqual(len(self.invoice.invoice_line_ids), 1)
        with self.assertRaises(ValidationError):
            self.invoice.invoice_line_ids.price_unit = 30

    def test_05_delete_tax_line_draft(self):
        self.assertEqual(len(self.invoice.tax_line_ids), 1)
        self.invoice.tax_line_ids.unlink()
        self.assertEqual(len(self.invoice.tax_line_ids), 0)

    def test_06_delete_tax_line_posted(self):
        self.validate_invoice()
        self.assertEqual(len(self.invoice.tax_line_ids), 1)
        with self.assertRaises(ValidationError):
            self.invoice.tax_line_ids.unlink()

    def test_07_write_tax_line_draft(self):
        self.assertEqual(len(self.invoice.tax_line_ids), 1)
        self.assertEqual(self.invoice.tax_line_ids.amount, 15)
        self.invoice.tax_line_ids.amount = 30
        self.assertEqual(self.invoice.tax_line_ids.amount, 30)

    def test_08_write_tax_line_posted(self):
        self.validate_invoice()
        self.assertEqual(len(self.invoice.tax_line_ids), 1)
        with self.assertRaises(ValidationError):
            self.invoice.tax_line_ids.amount = 30

    def test_09_write_invoice_draft(self):
        self.assertEqual(self.invoice.date_invoice, self.date_invoice)
        new_date = fields.Date.to_string(
            datetime.now() + relativedelta(days=1))
        self.invoice.date_invoice = new_date
        self.assertEqual(self.invoice.date_invoice, new_date)

    def test_10_write_invoice_posted(self):
        self.validate_invoice()
        self.assertEqual(self.invoice.date_invoice, self.date_invoice)
        new_date = fields.Date.to_string(
            datetime.now() + relativedelta(days=1))
        with self.assertRaises(ValidationError):
            self.invoice.date_invoice = new_date
