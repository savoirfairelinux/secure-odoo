# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.exceptions import ValidationError
from . import common


class TestAnalytic(common.TestAccountBase):

    def test_01_delete_analytic_line_draft(self):
        self.line_1.create_analytic_lines()
        self.assertEqual(len(self.line_1.analytic_line_ids), 1)
        self.line_1.analytic_line_ids.unlink()
        self.assertEqual(len(self.line_1.analytic_line_ids), 0)

    def test_02_delete_analytic_line_posted(self):
        self.move.post()
        self.assertEqual(len(self.line_1.analytic_line_ids), 1)
        with self.assertRaises(ValidationError):
            self.line_1.analytic_line_ids.unlink()

    def test_03_write_analytic_line_draft(self):
        self.line_1.create_analytic_lines()
        self.assertEqual(len(self.line_1.analytic_line_ids), 1)
        self.assertEqual(self.line_1.analytic_line_ids.amount, -100)
        self.line_1.analytic_line_ids.amount = -200
        self.assertEqual(self.line_1.analytic_line_ids.amount, -200)

    def test_04_write_analytic_line_posted(self):
        self.move.post()
        self.assertEqual(len(self.line_1.analytic_line_ids), 1)
        with self.assertRaises(ValidationError):
            self.line_1.analytic_line_ids.amount = -200
