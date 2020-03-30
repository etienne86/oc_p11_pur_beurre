"""
This module contains the unit tests related to the 'MyUserManager' class.
"""

from django.test import TestCase

from auth.models import MyUser


class MyUserTestCase(TestCase):

    def setUp(self):
        self.user_a = MyUser.objects.create_user(
            email="toto@mail.com",
            first_name="Toto"
        )

    def test_create_superuser(self):
        """
        Test if one record has been added to the 'MyUser' table
        (my_auth_myuser) with superuser permissions.
        """
        # count the number of users
        old_users_records = MyUser.objects.count()
        # add a new user
        user_b = MyUser.objects.create_superuser(
            email="super_titi@mail.com",
            password="Password123"
        )
        # count the number of products again
        new_users_records = MyUser.objects.count()
        # compare the two numbers (after and before)
        user_creation = (new_users_records == old_users_records + 1)
        # is this user admin ?
        user_is_admin = user_b.is_admin
        # union statement
        self.assertTrue(user_creation and user_is_admin)

    def test_create_user(self):
        """
        Test if one record has been added to the 'MyUser' table
        (my_auth_myuser).
        """
        # count the number of users
        old_users_records = MyUser.objects.count()
        # add a new user
        MyUser.objects.create_user(
            email="titi@mail.com",
            first_name="Titi"
        )
        # count the number of products again
        new_users_records = MyUser.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_users_records, old_users_records + 1)
