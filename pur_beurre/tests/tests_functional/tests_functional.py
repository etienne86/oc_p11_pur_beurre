"""
This module contains the functional tests for the project.
"""

import os
import time

import django
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.test import LiveServerTestCase
from django.contrib.auth.models import AnonymousUser
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import url_changes
from selenium.webdriver.firefox.options import Options
from seleniumlogin import force_login

django.setup()

from auth.models import MyUser
from off_sub.models import Product
from pur_beurre.settings import BASE_DIR




class TestWithAnonymousUser(StaticLiveServerTestCase):
    """
    This class contains functional tests with anonymous user.
    User Firefox as web browser.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # initialize a webdriver
        cls.selenium = WebDriver(
            executable_path=os.path.join(
                BASE_DIR, 'drivers/geckodriver'
            )
        )
        cls.driver = Firefox(
            executable_path=os.path.join(
                BASE_DIR, 'drivers/geckodriver'
            )
        )
        # set home_url
        cls.home_url = f"{cls.live_server_url}/"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        # a product in database
        self.product_a = Product.objects.create(
            code='1234567890123',
            product_name="a superb product",
            nutriscore_grade='a',
            nutriscore_score=-1,
            url="https://fr.openfoodfacts.org/produit/1234567890123/"
            "a-superb-product",
            image_url="https://static.openfoodfacts.org/images/products/"
            "123/456/789/0123/front_fr.8.400.jpg",
        )

    # basic scenarii

    def test_display_account(self):
        """
        Try to display account page, redirect to sign page.
        """
        self.selenium.get(f"{self.live_server_url}/auth/account")
        expected_url = f"{self.live_server_url}/auth/sign/?next=/auth/account/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_favorites(self):
        """
        Try to display favorites page, redirect to sign page.
        """
        self.selenium.get(f"{self.live_server_url}/favorites")
        expected_url = f"{self.live_server_url}/auth/sign/?next=/favorites/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_food(self):
        """
        Display food page.
        """
        product_id = 17
        self.selenium.get(f"{self.live_server_url}/food/{product_id}")
        expected_url = f"{self.live_server_url}/food/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_index(self):
        """
        Display index (home) page.
        """
        self.selenium.get(f"{self.live_server_url}")
        expected_url = f"{self.live_server_url}/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_legal(self):
        """
        Display legal page.
        """
        self.selenium.get(f"{self.live_server_url}/legal")
        expected_url = f"{self.live_server_url}/legal/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_log_out(self):
        """
        Try to display log_out page, redirect to sign page.
        """
        self.selenium.get(f"{self.live_server_url}/auth/log_out")
        expected_url = f"{self.live_server_url}/auth/sign/?next=/auth/log_out/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_results(self):
        """
        Display results page.
        """
        product_id = 17
        self.selenium.get(f"{self.live_server_url}/results/{product_id}")
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_sign(self):
        """
        Display sign page.
        """
        self.selenium.get(f"{self.live_server_url}/auth/sign")
        expected_url = f"{self.live_server_url}/auth/sign/"
        self.assertEqual(self.selenium.current_url, expected_url)

    # scenarii with chained actions

    def test_look_for_a_product_from_home_with_masthead_form_enter(self):
        actions = ActionChains(self.selenium)
        # start from index (home) page
        self.selenium.get(f"{self.live_server_url}")
        # click on field "Produit" (select field)
        product_field = self.selenium.find_element_by_id("autocompletion-1")
        actions.click(product_field)
        # enter the product name
        actions.send_keys(str(self.product_a))
        # press "Return" key
        actions.send_keys(Keys.RETURN)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(self.selenium, timeout=2).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_home_with_masthead_form_click_btn(self):
        actions = ActionChains(self.selenium)
        # start from index (home) page
        self.selenium.get(f"{self.live_server_url}")
        # click on field "Produit" (select field)
        product_field = self.selenium.find_element_by_id("autocompletion-1")
        actions.click(product_field)
        # enter the product name
        actions.send_keys(str(self.product_a))
        # click on "Chercher" button
        search_btn = self.selenium.find_element_by_css_selector(
            "#autocompletion-1 + .btn"
        )
        actions.click(search_btn)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(self.selenium, timeout=2).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_home_navbar_form_enter(self):
        actions = ActionChains(self.selenium)
        # start from index (home) page
        self.selenium.get(f"{self.live_server_url}")
        # click on field "Produit" (select field)
        product_field = self.selenium.find_element_by_id("autocompletion-0")
        actions.click(product_field)
        # enter the product name
        actions.send_keys(str(self.product_a))
        # press "Return" key
        actions.send_keys(Keys.RETURN)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(self.selenium, timeout=2).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_home_navbar_form_click_btn(self):
        """
        Available on XS, S and M screens only (L and XL screens excluded).
        """
        actions = ActionChains(self.selenium)
        # start from index (home) page
        self.driver.get(f"{self.live_server_url}")
        # click on field "Produit" (select field)
        product_field = self.driver.find_element_by_id("autocompletion-0")
        actions.click(product_field)
        # enter the product name
        actions.send_keys(str(self.product_a))
        # click on "Chercher" button (unavailable only on L and wider screens)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(640, 480)
        navbar_toggler = self.driver.find_element_by_css_selector(".navbar-toggler-icon")
        actions.click(navbar_toggler)
        search_btn = self.driver.find_element_by_css_selector(
            "#autocompletion-0 + .btn"
        )
        actions.click(search_btn)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(self.driver, timeout=2).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.driver.current_url, expected_url)



# class TestWithAuthenticatedUser(LiveServerTestCase):
#     """
#     This class contains functional tests with a user.
#     User Firefox as web browser.
#     """

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver(
#             executable_path=os.path.join(
#                 BASE_DIR, 'drivers/geckodriver'
#             )
#         )

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def setUp(self):
#         """
#         Create a test user.
#         """
#         self.user =  MyUser.objects.create_user(
#             email="toto@mail.com",
#             first_name="Toto"
#         )

#     def test_display_account(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         self.selenium.get(f"{self.live_server_url}/auth/account")
#         expected_url = f"{self.live_server_url}/auth/account/"
#         self.assertEqual(self.selenium.current_url, expected_url)

#     def test_display_favorites(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         self.selenium.get(f"{self.live_server_url}/favorites")
#         expected_url = f"{self.live_server_url}/favorites/"
#         self.assertEqual(self.selenium.current_url, expected_url)

#     def test_display_food(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         product_id = 17
#         self.selenium.get(f"{self.live_server_url}/food/{product_id}")
#         expected_url = f"{self.live_server_url}/food/{product_id}"
#         self.assertEqual(self.selenium.current_url, expected_url)

#     def test_display_index(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         self.selenium.get(f"{self.live_server_url}")
#         expected_url = f"{self.live_server_url}/"
#         self.assertEqual(self.selenium.current_url, expected_url)

#     def test_display_legal(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         self.selenium.get(f"{self.live_server_url}/legal")
#         expected_url = f"{self.live_server_url}/legal/"
#         self.assertEqual(self.selenium.current_url, expected_url)

#     def test_display_log_out(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         self.selenium.get(f"{self.live_server_url}/auth/log_out")
#         expected_url = f"{self.live_server_url}/auth/log_out/"
#         self.assertEqual(self.selenium.current_url, expected_url)

#     def test_display_results(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         product_id = 17
#         self.selenium.get(f"{self.live_server_url}/results/{product_id}")
#         expected_url = f"{self.live_server_url}/results/{product_id}"
#         self.assertEqual(self.selenium.current_url, expected_url)

#     def test_display_sign(self):
#         force_login(self.user, self.selenium, self.live_server_url)
#         self.selenium.get(f"{self.live_server_url}/auth/sign")
#         expected_url = f"{self.live_server_url}/auth/sign/"
#         self.assertEqual(self.selenium.current_url, expected_url)
