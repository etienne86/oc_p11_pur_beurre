"""This module contains the tests related to the 'MyUserManager' class."""

from django.test import TestCase

from auth.models import MyUser, MyUserManager
# from off_sub.views import request


class MyUserTestCase(TestCase):

    def setUp(self):
        self.user_a = MyUser.objects.create(
            email="toto@mail.com",
            first_name="Toto"
        )

    def test_create_user(self):
        """
        Test if one record has been added to the 'MyUser' table
        (my_auth_myuser).
        """
        # count the number of users
        old_users_records = MyUser.objects.count()
        # add a new user
        user_b = MyUser(email="titi@mail.com", first_name="Titi")
        user_b.save()
        # count the number of products again
        new_users_records = MyUser.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_users_records, old_users_records + 1)
