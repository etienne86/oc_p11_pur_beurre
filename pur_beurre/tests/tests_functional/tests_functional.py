"""
This module contains the functional tests for the project.
"""

import os
import random

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import AnonymousUser
import selenium
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    url_changes, visibility_of
)
from seleniumlogin import force_login

from auth.models import MyUser
from off_sub.models import Product, Category
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
        # set home_url
        cls.home_url = f"{cls.live_server_url}/"
        # # set window_rect (i.e. window_position and window_size)
        # cls.selenium.set_window_rect(0, 0, 1200, 800)

    @classmethod
    def tearDownClass(cls):
        # cls.driver.quit()
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        # some products in database
        self.product_a = Product.objects.create(
            code='1234567890123',
            product_name="a superb product",
            nutriscore_grade='a',
            nutriscore_score=-1,
        )
        self.product_b1 = Product.objects.create(
            code='2222222222201',
            product_name="product_b1",
            nutriscore_grade='b',
            nutriscore_score=1,
        )
        self.product_b2 = Product.objects.create(
            code='2222222222202',
            product_name="product_b2",
            nutriscore_grade='b',
            nutriscore_score=2,
        )
        self.product_b3 = Product.objects.create(
            code='2222222222203',
            product_name="product_b3",
            nutriscore_grade='b',
            nutriscore_score=3,
        )
        self.product_c = Product.objects.create(
            code='3333333333333',
            product_name="product c",
            nutriscore_grade='c',
            nutriscore_score=6,
        )
        self.product_d = Product.objects.create(
            code='4444444444444',
            product_name="product d",
            nutriscore_grade='d',
            nutriscore_score=14,
        )
        self.product_e = Product.objects.create(
            code='5555555555555',
            product_name="product e",
            nutriscore_grade='e',
            nutriscore_score=25,
        )
        # a category for these products
        self.category_1 = Category.objects.create(name="Category #1")
        self.product_a.categories.add(self.category_1)
        self.product_b1.categories.add(self.category_1)
        self.product_b2.categories.add(self.category_1)
        self.product_b3.categories.add(self.category_1)
        self.product_c.categories.add(self.category_1)
        self.product_d.categories.add(self.category_1)
        self.product_e.categories.add(self.category_1)
        # a user in database
        self.user_a = MyUser.objects.create_user(
            email="toto@mail.com",
            first_name="Toto"
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
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
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
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_home_with_masthead_form_click_btn(self):
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
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
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_home_navbar_form_enter(self):
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
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
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_home_navbar_form_click_btn(self):
        """
        Available on XS, S and M screens only (L and XL screens excluded).
        """
        # save window_rect
        rect_0 = self.selenium.get_window_rect()
        # adjust window_position and window_size
        self.selenium.set_window_rect(0, 0, 800, 600)
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on field "Produit" (select field)
        navbar_toggler = self.selenium.find_element_by_css_selector(
            ".navbar-toggler-icon"
        )
        actions.click(navbar_toggler)
        product_field = self.selenium.find_element_by_id("autocompletion-0")
        actions.click(product_field)
        # enter the product name
        actions.send_keys(str(self.product_a))
        # click on "Chercher" button (unavailable only on L and wider screens)
        search_btn = self.selenium.find_element_by_css_selector(
            "#autocompletion-0 + .btn"
        )
        actions.click(search_btn)
        # compile chained actions
        actions.perform()
        # restore window_rect
        self.selenium.set_window_rect(0, 0, rect_0['width'], rect_0['height'])
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(self.home_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_click_on_product_picture_to_consult_details_results_page(self):
        """
        Click on the searched product, i.e. in the masthead section.
        """
        # start from results page
        product_id = self.product_c.id
        start_url = f"{self.live_server_url}/results/{product_id}"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on product picture
        product_picture = self.selenium.find_element_by_id("masthead_picture")
        actions.click(product_picture)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "food" page
        expected_url = f"{self.live_server_url}/food/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_click_on_product_name_to_consult_details_results_page(self):
        """
        Click on the searched product, i.e. in the masthead section.
        """
        # start from results page
        product_id = self.product_c.id
        start_url = f"{self.live_server_url}/results/{product_id}"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on product name
        product_subtitle = self.selenium.find_element_by_id("masthead_subtitle")
        actions.click(product_subtitle)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "food" page
        expected_url = f"{self.live_server_url}/food/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_create_user_account_success(self):
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        actions.click(sign_icon)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/"))
        # start chained actions
        actions = ActionChains(self.selenium)
        # select the tab "Nous rejoindre"
        signup_tab = self.selenium.find_element_by_id("nous-rejoindre")
        actions.click(signup_tab)
        # compile chained actions
        actions.perform()
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        submit_button = self.selenium.find_element_by_name("sign_up_form")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(submit_button))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill the "create account" form
        first_name_field = self.selenium.find_element_by_id("id_first_name")
        actions.click(first_name_field)
        actions.send_keys("Titi")
        email_field = self.selenium.find_elements_by_id("id_email")[1]
        actions.click(email_field)
        actions.send_keys("titi@mail.com")
        password1_field = self.selenium.find_element_by_id("id_password1")
        actions.click(password1_field)
        actions.send_keys("Password123")
        password2_field = self.selenium.find_element_by_id("id_password2")
        actions.click(password2_field)
        actions.send_keys("Password123")
        # click on the "Créer un compte" button
        actions.click(submit_button)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/auth/sign/"))
        # redirect to home page: True or False?
        home_sweet_home = (self.selenium.current_url == start_url)
        # user authenticated: True or False?
        authenticated = False
        try:
            logout_icon = self.selenium.find_element_by_id("logout-icon")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            authenticated = True
        self.assertTrue(home_sweet_home and authenticated)
 

    def test_create_user_account_failure(self):
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        actions.click(sign_icon)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/"))
        # start chained actions
        actions = ActionChains(self.selenium)
        # select the tab "Nous rejoindre"
        signup_tab = self.selenium.find_element_by_id("nous-rejoindre")
        actions.click(signup_tab)
        # compile chained actions
        actions.perform()
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        submit_button = self.selenium.find_element_by_name("sign_up_form")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(submit_button))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill the "create account" form
        first_name_field = self.selenium.find_element_by_id("id_first_name")
        actions.click(first_name_field)
        actions.send_keys("Toto")
        email_field = self.selenium.find_elements_by_id("id_email")[1]
        actions.click(email_field)
        actions.send_keys("toto@mail.com") #  already used email
        password1_field = self.selenium.find_element_by_id("id_password1")
        actions.click(password1_field)
        actions.send_keys("Password123")
        password2_field = self.selenium.find_element_by_id("id_password2")
        actions.click(password2_field)
        actions.send_keys("Password123")
        # click on the "Créer un compte" button
        actions.click(submit_button)
        # wait for seeing the error message
        actions.pause(1)
        # compile chained actions
        actions.perform()
        # get an error message: True or False?
        error_message = self.selenium.find_element_by_class_name("text-danger")
        expected_error = (
            error_message.text == "Un compte est déjà créé avec ce courriel."
        ) 
        # stay on current page: True or False?
        current_page = (self.selenium.current_url == f"{start_url}auth/sign/")
        self.assertTrue(error_message and current_page)


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
