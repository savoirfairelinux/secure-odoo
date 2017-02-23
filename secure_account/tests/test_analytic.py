# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.exceptions import ValidationError
from . import common


class TestAnalytic(common.TestAccountBase):

    def test_01_delete_analytic_line_draft(self):
        self.assertEqual(len(self.line_1.analytic_lines), 1)
        self.line_1.analytic_lines.unlink()
        self.assertEqual(len(self.line_1.analytic_lines), 0)

    def test_02_delete_analytic_line_posted(self):
        self.move.post()
        self.assertEqual(len(self.line_1.analytic_lines), 1)
        with self.assertRaises(ValidationError):
            self.line_1.analytic_lines.unlink()

    def test_03_write_analytic_line_draft(self):
        self.assertEqual(len(self.line_1.analytic_lines), 1)
        self.assertEqual(self.line_1.analytic_lines.amount, -100)
        self.line_1.analytic_lines.amount = -200
        self.assertEqual(self.line_1.analytic_lines.amount, -200)

    def test_04_write_analytic_line_posted(self):
        self.move.post()
        self.assertEqual(len(self.line_1.analytic_lines), 1)
        with self.assertRaises(ValidationError):
            self.line_1.analytic_lines.amount = -200
