# -*- coding: utf-8 -*-
# © 2011 Smile
# © 2017 Savoir-faire Linux
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from openerp.tests.common import TransactionCase


class TestUserProfile(TransactionCase):

    def setUp(self):
        super(TestUserProfile, self).setUp()
        self.group1 = self.env['res.groups'].create({'name': 'Group 1'})
        self.group2 = self.env['res.groups'].create({'name': 'Group 2'})
        self.group3 = self.env['res.groups'].create({'name': 'Group 3'})
        self.user_profile1 = self.env['res.users'].create({
            'name': 'Profile 1',
            'login': 'profile1',
            'user_profile': True,
            'groups_id': [(6, 0, [self.group1.id])],
        })
        self.user_profile2 = self.env['res.users'].create({
            'name': 'Profile 2',
            'login': 'profile2',
            'user_profile': True,
            'groups_id': [(6, 0, (self.group1 | self.group2).ids)],
        })
        self.user_profile3 = self.env['res.users'].create({
            'name': 'Profile 3',
            'login': 'profile3',
            'user_profile': True,
            'groups_id': [(6, 0, [self.group3.id])],
        })
        self.user = self.env['res.users'].create({
            'name': 'Demo User',
            'login': 'demouser',
            'user_profile_ids': [(6, 0, self.user_profile1.ids)],
        })

    def test_1_user_create(self):
        """
        Test create method
        We create a dictionary of values
        We create a user from these values, he has a user profile
        We check that that the new user has been created with his name
        """
        user = self.env['res.users'].create({
            'name': 'User Test 1',
            'login': 'usertest1',
            'user_profile_ids': [(6, 0, self.user_profile2.ids)],
        })
        self.assertEqual(user.name, 'User Test 1')
        self.assertEqual(user.groups_id, self.group1 | self.group2)

    def test_2_user_write(self):
        """
        Test write method
        We use the user created in the first method
        We change his user_profile_ids
        We check if the update has been done
        """
        self.user.user_profile_ids = self.user_profile2
        self.assertEqual(self.user.groups_id, self.group1 | self.group2)

        self.user.user_profile_ids = self.user_profile1
        self.assertEqual(self.user.groups_id, self.group1)

        self.user.user_profile_ids = self.user_profile3
        self.assertEqual(self.user.groups_id, self.group3)

    def test_3_group_implied_ids(self):
        self.assertEqual(self.user.groups_id, self.group1)
        self.group1.write({'implied_ids': [(4, self.group3.id)]})
        self.assertEqual(self.user.groups_id, self.group1 | self.group3)

    def test_4_group_users(self):
        self.assertEqual(self.user.groups_id, self.group1)

        self.group1.write({'users': [(3, self.user_profile1.id)]})
        self.assertEqual(self.user.groups_id, self.env['res.groups'])

        self.group3.users |= self.user_profile1
        self.assertEqual(self.user.groups_id, self.group3)

    def test_5_profile_write(self):
        self.assertEqual(self.user.groups_id, self.group1)
        self.user_profile1.groups_id |= self.group3
        self.assertEqual(self.user.groups_id, self.group1 | self.group3)

    def test_6_profile_create(self):
        self.assertEqual(self.user.groups_id, self.group1)
        self.env['res.users'].create({
            'name': 'New Profile',
            'login': 'new_profile_login',
            'user_profile': True,
            'user_ids': [(4, self.user.id)],
            'groups_id': [(6, 0, [self.group3.id])],
        })
        self.assertEqual(self.user.groups_id, self.group1 | self.group3)
