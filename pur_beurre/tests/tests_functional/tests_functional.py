"""
This module contains the functional tests for the project.
"""

import os
import django
django.setup()

from django.urls import reverse
from django.test import Client, LiveServerTestCase
from django.contrib.auth.models import AnonymousUser
from selenium.webdriver.firefox.webdriver import WebDriver

from auth.models import MyUser
from pur_beurre.settings import BASE_DIR


class TestWithAnonymousUser(LiveServerTestCase):
    """
    This class contains functional tests with anonymous user.
    User Firefox as web browser.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(
            executable_path=os.path.join(
                BASE_DIR, 'drivers/geckodriver'
            )
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_display_account(self):
        self.selenium.get(f"{self.live_server_url}/auth/account")
        expected_url = f"{self.live_server_url}/auth/sign/?next=/auth/account/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_favorites(self):
        self.selenium.get(f"{self.live_server_url}/favorites")
        expected_url = f"{self.live_server_url}/auth/sign/?next=/favorites/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_food(self):
        product_id = 17
        self.selenium.get(f"{self.live_server_url}/food/{product_id}")
        expected_url = f"{self.live_server_url}/food/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_index(self):
        self.selenium.get(f"{self.live_server_url}")
        expected_url = f"{self.live_server_url}/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_legal(self):
        self.selenium.get(f"{self.live_server_url}/legal")
        expected_url = f"{self.live_server_url}/legal/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_log_out(self):
        self.selenium.get(f"{self.live_server_url}/auth/log_out")
        expected_url = f"{self.live_server_url}/auth/sign/?next=/auth/log_out/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_results(self):
        product_id = 17
        self.selenium.get(f"{self.live_server_url}/results/{product_id}")
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_sign(self):
        self.selenium.get(f"{self.live_server_url}/auth/sign")
        expected_url = f"{self.live_server_url}/auth/sign/"
        self.assertEqual(self.selenium.current_url, expected_url)

