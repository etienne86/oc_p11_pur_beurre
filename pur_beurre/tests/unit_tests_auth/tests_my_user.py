"""
This module contains the unit tests related to the 'MyUserManager' class.
"""

from django.test import TestCase

from pur_beurre.auth.models import MyUser


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

    def test_create_user_without_email(self):
        """
        Test if a ValueError is raised if no email is provided.
        """
        text = ""
        try:
            MyUser.objects.create_user(email="", first_name="Titi")
        except ValueError as e:
            text = str(e)
        self.assertEqual(text, "Le courriel est requis pour s'inscrire.")

    def test_str_user(self):
        """
        Test if user printing is correct.
        """
        self.assertEqual(str(self.user_a), "Toto (toto@mail.com)")

    def test_user_has_perm(self):
        """
        Test if user method 'has_perm' is correct.
        """
        perm = "a perm value"
        self.assertEqual(self.user_a.has_perm(perm), True)

    def test_user_has_module_perms(self):
        """
        Test if user method 'has_module_perms' is correct.
        """
        app_label = "an app label"
        self.assertEqual(self.user_a.has_module_perms(app_label), True)

    def test_user_is_not_staff(self):
        """
        Test if user is not admin.
        """
        self.assertFalse(self.user_a.is_staff)
