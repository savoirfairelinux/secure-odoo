# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.exceptions import ValidationError
from . import common


class TestAccountMove(common.TestAccountBase):

    def test_01_delete_move_line_draft(self):
        self.assertEqual(len(self.move.line_ids), 2)
        self.line_2.unlink()
        self.assertEqual(len(self.move.line_ids), 1)

    def test_02_delete_move_line_posted(self):
        self.move.post()
        self.assertEqual(len(self.move.line_ids), 2)
        with self.assertRaises(ValidationError):
            self.line_2.unlink()

    def test_03_write_move_line_draft(self):
        self.assertEqual(len(self.move.line_ids), 2)
        self.assertEqual(self.line_2.partner_id, self.partner_1)
        self.line_2.partner_id = self.partner_2
        self.assertEqual(self.line_2.partner_id, self.partner_2)

    def test_04_write_move_line_posted(self):
        self.move.post()
        self.assertEqual(len(self.move.line_ids), 2)
        self.assertEqual(self.line_2.partner_id, self.partner_1)
        with self.assertRaises(ValidationError):
            self.line_2.partner_id = self.partner_2

    def test_03_write_move_draft(self):
        self.assertEqual(self.move.partner_id, self.partner_1)
        self.move.partner_id = self.partner_2
        self.assertEqual(self.move.partner_id, self.partner_2)

    def test_04_write_move_posted(self):
        self.move.post()
        self.assertEqual(self.move.partner_id, self.partner_1)
        with self.assertRaises(ValidationError):
            self.move.partner_id = self.partner_2
