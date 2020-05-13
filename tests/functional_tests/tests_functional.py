"""
This module contains the functional tests for the project, using two classes:
- TestWithAnonymousUser, where no user is initially logged in
- TestWithAuthenticatedUser, where a user is initially logged in
"""

import random
import re

from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
import selenium
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    url_changes, url_to_be, visibility_of
)
from seleniumlogin import force_login

from auth.models import MyUser
from off_sub.models import Product, Category
import pur_beurre.settings as settings


class TestWithAnonymousUser(StaticLiveServerTestCase):
    """
    This class contains functional tests with anonymous user.
    Use Firefox as web browser.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # initialize a webdriver
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()
        # set home_url
        cls.home_url = f"{cls.live_server_url}/"

    @classmethod
    def tearDownClass(cls):
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
            first_name="Toto",
            password="TopSecret"
        )

    ##################
    # basic scenarii #
    ##################

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

    #################################
    # scenarii with chained actions #
    #################################

    def test_look_for_a_product_from_home_with_masthead_form_enter(self):
        """
        Test for User Story US02: scenario #1.
        """
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
        """
        Test for User Story US02: scenario #2.
        """
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
            ".group-autocompletion-1 > .btn"
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
        """
        Test for User Story US02: scenario #3.
        """
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
        Test for User Story US02: scenario #4.
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
        # click on "Chercher" button (unavailable on L and wider screens)
        search_btn = self.selenium.find_element_by_css_selector(
            ".group-autocompletion-0 > .btn"
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
        Test for User Story US03: scenario #1.
        Click on the searched product, i.e. in the masthead section.
        """
        # start from results page
        product_id = self.product_c.id
        start_url = f"{self.live_server_url}/results/{product_id}"
        self.selenium.get(start_url)
        # click on product picture
        product_picture = self.selenium.find_element_by_id("masthead_picture")
        product_picture.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "food" page
        expected_url = f"{self.live_server_url}/food/" + \
            f"{product_id}?next=/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_click_on_product_name_to_consult_details_results_page(self):
        """
        Test for User Story US03: scenario #2.
        Click on the searched product, i.e. in the masthead section.
        """
        # start from results page
        product_id = self.product_c.id
        start_url = f"{self.live_server_url}/results/{product_id}"
        self.selenium.get(start_url)
        # click on product name
        product_subtitle = self.selenium.find_element_by_id(
            "masthead_subtitle"
        )
        product_subtitle.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "food" page
        expected_url = f"{self.live_server_url}/food/" + \
            f"{product_id}?next=/results/{product_id}"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_create_user_account_success(self):
        """
        Test for User Story US04: scenario #1.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        sign_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/"))
        # select the tab "Nous rejoindre"
        signup_tab = self.selenium.find_element_by_id("nous-rejoindre")
        signup_tab.click()
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
            self.selenium.find_element_by_id("logout-icon")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            authenticated = True
        self.assertTrue(home_sweet_home and authenticated)

    def test_create_user_account_failure_already_used_email(self):
        """
        Test for User Story US04: scenario #2.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        sign_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/"))
        # select the tab "Nous rejoindre"
        signup_tab = self.selenium.find_element_by_id("nous-rejoindre")
        signup_tab.click()
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
        actions.send_keys("toto@mail.com")  # already used email
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
        message = "Un compte est déjà créé avec ce courriel."
        expected_error = (error_message.text == message)
        # stay on current page: True or False?
        current_page = (self.selenium.current_url == f"{start_url}auth/sign/")
        self.assertTrue(expected_error and current_page)

    def test_create_user_account_failure_two_different_passwords(self):
        """
        Test for User Story US04: scenario #3.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        sign_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/"))
        # select the tab "Nous rejoindre"
        signup_tab = self.selenium.find_element_by_id("nous-rejoindre")
        signup_tab.click()
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
        actions.send_keys("un_autre_toto@mail.com")
        password1_field = self.selenium.find_element_by_id("id_password1")
        actions.click(password1_field)
        actions.send_keys("Password123")
        password2_field = self.selenium.find_element_by_id("id_password2")
        actions.click(password2_field)
        actions.send_keys("WrongPassword!")  # wrong password
        # click on the "Créer un compte" button
        actions.click(submit_button)
        # wait for seeing the error message
        actions.pause(1)
        # compile chained actions
        actions.perform()
        # get an error message: True or False?
        error_message = self.selenium.find_element_by_class_name("text-danger")
        message = "Les deux mots de passe ne correspondent pas"
        expected_error = (error_message.text == message)
        # stay on current page: True or False?
        current_page = (self.selenium.current_url == f"{start_url}auth/sign/")
        self.assertTrue(expected_error and current_page)

    def test_login_success(self):
        """
        Test for User Story US05: scenario #1.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        sign_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/"))
        # select the tab "Se connecter"
        login_tab = self.selenium.find_element_by_id("se-connecter")
        login_tab.click()
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        submit_button = self.selenium.find_element_by_name("login_form")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(submit_button))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill the login form
        email_field = self.selenium.find_elements_by_id("id_email")[0]
        actions.click(email_field)
        actions.send_keys("toto@mail.com")
        password_field = self.selenium.find_element_by_id("id_password")
        actions.click(password_field)
        actions.send_keys("TopSecret")
        # click on the "Se connecter" button
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
            self.selenium.find_element_by_id("logout-icon")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            authenticated = True
        self.assertTrue(home_sweet_home and authenticated)

    def test_login_failure_wrong_email(self):
        """
        Test for User Story US05: scenario #2.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        sign_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(f"{self.live_server_url}/"))
        # select the tab "Se connecter"
        login_tab = self.selenium.find_element_by_id("se-connecter")
        login_tab.click()
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        submit_button = self.selenium.find_element_by_name("login_form")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(submit_button))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill the login form
        email_field = self.selenium.find_elements_by_id("id_email")[0]
        actions.click(email_field)
        actions.send_keys("oops@mail.com")
        password_field = self.selenium.find_element_by_id("id_password")
        actions.click(password_field)
        actions.send_keys("TopSecret")
        # click on the "Se connecter" button
        actions.click(submit_button)
        # wait for seeing the error message
        actions.pause(1)
        # compile chained actions
        actions.perform()
        # get an error message: True or False?
        error_message = self.selenium.find_element_by_class_name("text-danger")
        message = "Merci de saisir un email et un mot de passe valides SVP."
        expected_error = (error_message.text == message)
        # stay on current page: True or False?
        current_page = (self.selenium.current_url == f"{start_url}auth/sign/")
        self.assertTrue(expected_error and current_page)

    def test_login_failure_wrong_password(self):
        """
        Test for User Story US05: scenario #3.
        """
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
        # select the tab "Se connecter"
        login_tab = self.selenium.find_element_by_id("se-connecter")
        login_tab.click()
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        submit_button = self.selenium.find_element_by_name("login_form")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(submit_button))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill the login form
        email_field = self.selenium.find_elements_by_id("id_email")[0]
        actions.click(email_field)
        actions.send_keys("toto@mail.com")
        password_field = self.selenium.find_element_by_id("id_password")
        actions.click(password_field)
        actions.send_keys("Oops")
        # click on the "Se connecter" button
        actions.click(submit_button)
        # wait for seeing the error message
        actions.pause(1)
        # compile chained actions
        actions.perform()
        # get an error message: True or False?
        error_message = self.selenium.find_element_by_class_name("text-danger")
        message = "Merci de saisir un email et un mot de passe valides SVP."
        expected_error = (error_message.text == message)
        # stay on current page: True or False?
        current_page = (self.selenium.current_url == f"{start_url}auth/sign/")
        self.assertTrue(expected_error and current_page)

    def test_sign_from_results_page_without_losing_results(self):
        """
        Test for User Story US12: unique scenario.
        """
        # start from results page
        product_id = self.product_c.id
        start_url = f"{self.live_server_url}/results/{product_id}"
        self.selenium.get(start_url)
        # click on "Se Connecter" button
        login_button = self.selenium.find_element_by_id("btn-login")
        login_button.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # select the tab "Se connecter"
        login_tab = self.selenium.find_element_by_id("se-connecter")
        login_tab.click()
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        submit_button = self.selenium.find_element_by_name("login_form")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(submit_button))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill the login form
        email_field = self.selenium.find_elements_by_id("id_email")[0]
        actions.click(email_field)
        actions.send_keys("toto@mail.com")
        password_field = self.selenium.find_element_by_id("id_password")
        actions.click(password_field)
        actions.send_keys("TopSecret")
        # click on the "Se connecter" button
        actions.click(submit_button)
        # compile chained actions
        actions.perform()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_to_be(f"{self.live_server_url}/results_/{product_id}"))
        # redirect to results page: True or False?
        results_url = f"{self.live_server_url}/results_/{product_id}"
        redirection_to_results = (self.selenium.current_url == results_url)
        # user authenticated: True or False?
        authenticated = False
        try:
            self.selenium.find_element_by_id("logout-icon")
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            authenticated = True
        self.assertTrue(redirection_to_results and authenticated)

    def test_reset_password_success(self):
        """
        Test for User Story US14: scenario #1.
        Standard process:
        1. click on "forgotten password" link
        2. fill in the form with no error (provide email)
        3. check the received email
        4. enter the given link to the web browser
        5. fill in the form with no error (provide new password)
        """
        # start from sign page
        start_url = f"{self.live_server_url}/auth/sign/"
        self.selenium.get(start_url)
        #########################################
        # 1. click on "forgotten password" link #
        #########################################
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        reset_pwd_button = self.selenium.find_element_by_id("forgotten_pwd")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(reset_pwd_button))
        # click on "forgotten password" link
        reset_pwd_button.click()
        #####################################################
        # 2. fill in the form with no error (provide email) #
        #####################################################
        # wait for page loading
        reset_pwd_url = f"{self.live_server_url}/auth/reset_password/"
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_to_be(reset_pwd_url))
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        email_field = self.selenium.find_element_by_id("id_email")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(email_field))
        # change the site in the email
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = self.live_server_url
        site.name = self.live_server_url
        site.save()
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on field "Courriel"
        actions.click(email_field)
        # enter the mail address
        actions.send_keys("toto@mail.com")
        # press "Return" key
        actions.send_keys(Keys.RETURN)
        # compile chained actions
        actions.perform()
        ###############################
        # 3. check the received email #
        ###############################
        # wait for email receiving
        actions = ActionChains(self.selenium)
        actions.pause(1)
        actions.perform()
        # test that one message has been sent
        email_received = (len(mail.outbox) == 1)
        # get the mail content
        mail_content = mail.outbox[0].body
        # extract "reset password link"
        match = re.search(
            "choisir un nouveau mot de passe :\n(.*)\nPour mémoire",
            mail_content
        )
        if not match:
            password_reset_ok = False
        else:
            reset_pwd_link = match.group(1)
            ##############################################
            # 4. enter the given link to the web browser #
            ##############################################
            self.selenium.get(reset_pwd_link)
            ############################################################
            # 5. fill in the form with no error (provide new password) #
            ############################################################
            edit_new_pwd_url = self.selenium.current_url
            # scroll down
            self.selenium.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # wait for scrolling
            new_pwd_field1 = self.selenium.find_element_by_id(
                "id_new_password1"
            )
            WebDriverWait(
                self.selenium,
                timeout=2
            ).until(visibility_of(new_pwd_field1))
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on field "Nouveau mot de passe"
            actions.click(new_pwd_field1)
            # enter the new password
            actions.send_keys("TopSecret123")
            # click on field "Confirmation du nouveau mot de passe"
            new_pwd_field2 = self.selenium.find_element_by_id(
                "id_new_password2"
            )
            actions.click(new_pwd_field2)
            # enter the new password
            actions.send_keys("TopSecret123")
            # press "Return" key
            actions.send_keys(Keys.RETURN)
            # compile chained actions
            actions.perform()
            # wait for page loading
            WebDriverWait(
                self.selenium,
                timeout=2
            ).until(url_changes(edit_new_pwd_url))
            # check final url
            ok_url = f"{self.live_server_url}/auth/reset_password_complete/"
            password_reset_ok = (self.selenium.current_url == ok_url)
        self.assertTrue(email_received and password_reset_ok)

    def test_reset_password_failure_wrong_email(self):
        """
        Test for User Story US14: scenario #2.
        Alternative process:
        1. click on "forgotten password" link
        2. fill in the form with an error: unrecognized email
        3. no email is received
        """
        # start from sign page
        start_url = f"{self.live_server_url}/auth/sign/"
        self.selenium.get(start_url)
        #########################################
        # 1. click on "forgotten password" link #
        #########################################
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        reset_pwd_button = self.selenium.find_element_by_id("forgotten_pwd")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(reset_pwd_button))
        # click on "forgotten password" link
        reset_pwd_button.click()
        #########################################################
        # 2. fill in the form with an error: unrecognized email #
        #########################################################
        # wait for page loading
        reset_pwd_url = f"{self.live_server_url}/auth/reset_password/"
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_to_be(reset_pwd_url))
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        email_field = self.selenium.find_element_by_id("id_email")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(email_field))
        # change the site in the email
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = self.live_server_url
        site.name = self.live_server_url
        site.save()
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on field "Courriel"
        actions.click(email_field)
        # enter the mail address
        actions.send_keys("error@mail.com")
        # press "Return" key
        actions.send_keys(Keys.RETURN)
        # compile chained actions
        actions.perform()
        ###########################
        # 3. no email is received #
        ###########################
        # wait for email receiving
        actions = ActionChains(self.selenium)
        actions.pause(1)
        actions.perform()
        # test that no message has been sent
        email_received = (len(mail.outbox) == 0)
        self.assertTrue(email_received)

    def test_reset_password_failure_different_new_passwords(self):
        """
        Test for User Story US14: scenario #2.
        Alternative process:
        1. click on "forgotten password" link
        2. fill in the form with no error (provide email)
        3. check the received email
        4. enter the given link to the web browser
        5. fill in the form with an error: different two passwords
        """
        # start from sign page
        start_url = f"{self.live_server_url}/auth/sign/"
        self.selenium.get(start_url)
        #########################################
        # 1. click on "forgotten password" link #
        #########################################
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        reset_pwd_button = self.selenium.find_element_by_id("forgotten_pwd")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(reset_pwd_button))
        # click on "forgotten password" link
        reset_pwd_button.click()
        #####################################################
        # 2. fill in the form with no error (provide email) #
        #####################################################
        # wait for page loading
        reset_pwd_url = f"{self.live_server_url}/auth/reset_password/"
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_to_be(reset_pwd_url))
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        email_field = self.selenium.find_element_by_id("id_email")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(email_field))
        # change the site in the email
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = self.live_server_url
        site.name = self.live_server_url
        site.save()
        # start chained actions
        actions = ActionChains(self.selenium)
        # click on field "Courriel"
        actions.click(email_field)
        # enter the mail address
        actions.send_keys("toto@mail.com")
        # press "Return" key
        actions.send_keys(Keys.RETURN)
        # compile chained actions
        actions.perform()
        ###############################
        # 3. check the received email #
        ###############################
        # wait for email receiving
        actions = ActionChains(self.selenium)
        actions.pause(1)
        actions.perform()
        # test that one message has been sent
        email_received = (len(mail.outbox) == 1)
        # get the mail content
        mail_content = mail.outbox[0].body
        # extract "reset password link"
        match = re.search(
            "choisir un nouveau mot de passe :\n(.*)\nPour mémoire",
            mail_content
        )
        if not match:
            self.assertTrue(False)
        else:
            reset_pwd_link = match.group(1)
            ##############################################
            # 4. enter the given link to the web browser #
            ##############################################
            self.selenium.get(reset_pwd_link)
            ##############################################################
            # 5. fill in the form with an error: different two passwords #
            ##############################################################
            edit_new_pwd_url = self.selenium.current_url
            # scroll down
            self.selenium.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # wait for scrolling
            new_pwd_field1 = self.selenium.find_element_by_id(
                "id_new_password1"
            )
            WebDriverWait(
                self.selenium,
                timeout=2
            ).until(visibility_of(new_pwd_field1))
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on field "Nouveau mot de passe"
            actions.click(new_pwd_field1)
            # enter the new password
            actions.send_keys("TopSecret123")
            # click on field "Confirmation du nouveau mot de passe"
            new_pwd_field2 = self.selenium.find_element_by_id(
                "id_new_password2"
            )
            actions.click(new_pwd_field2)
            # enter the new password
            actions.send_keys("TopSecret456")  # different from password #1
            # press "Return" key
            actions.send_keys(Keys.RETURN)
            # wait for seeing the error message
            actions.pause(1)
            # compile chained actions
            actions.perform()
            # get an error message: True or False?
            error_message = self.selenium.find_element_by_class_name(
                "text-danger"
            )
            # msg = "Les deux mots de passe ne correspondent pas."
            msg = _(
                "The two password fields didn’t match."
            )
            expected_error = (_(error_message.text) == msg)
            # stay on current page: True or False?
            current_page = (self.selenium.current_url == edit_new_pwd_url)
        self.assertTrue(email_received and expected_error and current_page)


class TestWithAuthenticatedUser(StaticLiveServerTestCase):
    """
    This class contains functional tests with an authenticated user.
    Use Firefox as web browser.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # initialize a webdriver
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()
        # set home_url
        cls.home_url = f"{cls.live_server_url}/"

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        # a test user
        self.user = MyUser.objects.create_user(
            email="toto@mail.com",
            first_name="Toto",
            password="TopSecret"
        )
        # force login for this test user
        force_login(self.user, self.selenium, self.live_server_url)
        # some products in database
        self.product_a = Product.objects.create(
            code='1234567890123',
            product_name="a superb product",
            nutriscore_grade='a',
            nutriscore_score=-1,
        )
        self.product_b = Product.objects.create(
            code='2222222222222',
            product_name="product_b",
            nutriscore_grade='b',
            nutriscore_score=1,
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
        # add some of these products as favorites for the test user
        self.user.favorites.add(self.product_a)
        self.user.favorites.add(self.product_b)

    ##################
    # basic scenarii #
    ##################

    def test_display_account(self):
        """
        Display account page.
        """
        self.selenium.get(f"{self.live_server_url}/auth/account")
        expected_url = f"{self.live_server_url}/auth/account/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_display_favorites(self):
        """
        Display favorites page.
        """
        self.selenium.get(f"{self.live_server_url}/favorites")
        expected_url = f"{self.live_server_url}/favorites/"
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
        Display home page.
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
        Display logout page.
        """
        self.selenium.get(f"{self.live_server_url}/auth/log_out")
        expected_url = f"{self.live_server_url}/auth/log_out/"
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

    #################################
    # scenarii with chained actions #
    #################################

    def test_logout_success(self):
        """
        Test for User Story US06: unique scenario.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on "logout" icon
        logout_icon = self.selenium.find_element_by_id("logout-icon")
        logout_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "logout" page
        expected_url = f"{self.live_server_url}/auth/log_out/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_save_a_product_as_favorite(self):
        """
        Test for User Story US07: scenario #1.
        Standard process:
        1. click on the button to save the product
        2. check that the button state switches
        3. check on the favorites page that the product is well saved
        """
        result = True
        # start from results page
        product_id = self.product_c.id
        start_url = f"{self.live_server_url}/results/{product_id}"
        self.selenium.get(start_url)
        # is/are there a/some product(s) savable as favorite(s)?
        savable = self.selenium.find_elements_by_class_name("saveProduct")
        savable_quantity = len(savable)
        # # on the contrary, is/are there a/some unsavable product(s)?
        # unsavable = self.selenium.find_elements_by_class_name(
        #     "unsaveProduct"
        # )
        # unsavable_quantity = len(unsavable)
        if savable_quantity > 0:  # at least one product is savable
            ##############################################
            # 1. click on the button to save the product #
            ##############################################
            # randomly choose a favorite
            index = random.randint(0, savable_quantity - 1)
            save_button = savable[index]
            # which product will be saved?
            saved_product_id = save_button.get_attribute("property")
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on "Sauvegarder" button
            actions.click(save_button)
            # wait for the button switch
            actions.pause(1)
            # compile chained actions
            actions.perform()
            ###########################################
            # 2. check that the button state switches #
            ###########################################
            # has the product saved button switched to "unsavable"?
            button = self.selenium.find_element_by_id(saved_product_id)
            switch_button_status = (button.text == "Retirer des favoris")
            # update result
            result *= switch_button_status
            #################################################################
            # 3. check on the favorites page that the product is well saved #
            #################################################################
            # switch to favorites page
            favorites_icon = self.selenium.find_element_by_id("favorites-icon")
            favorites_icon.click()
            # wait for page loading
            WebDriverWait(
                self.selenium,
                timeout=2
            ).until(url_changes(start_url))
            expected_url = f"{self.live_server_url}/favorites/"
            redirect_status = (expected_url == self.selenium.current_url)
            # update result
            result *= redirect_status
            # is the saved product among the favorites?
            saved = self.selenium.find_elements_by_class_name(
                "unsaveProduct"
            )
            found = False
            # loop on all saved products
            counter = 0
            while ((not found) and (counter < len(saved))):
                button = saved[counter]
                if (button.get_attribute("property") == saved_product_id):
                    found = True
                counter += 1
            saved_product_status = found
            # update result
            result *= saved_product_status
        else:  # no product is savable as favorite
            pass
        self.assertTrue(result)

    def test_save_a_product_as_favorite_immediate_reverse(self):
        """
        Test for User Story US07: scenario #2.
        Alternative process:
        1. click on the button to save the product
        2. check that the button state switches
        3. reverse clicking to cancel product saving
        4. check that the button state switches back to original
        5. check on the favorites page that the product is NOT saved
        """
        result = True
        # start from results page
        product_id = self.product_c.id
        start_url = f"{self.live_server_url}/results/{product_id}"
        self.selenium.get(start_url)
        # is/are there a/some product(s) savable as favorite(s)?
        savable = self.selenium.find_elements_by_class_name("saveProduct")
        savable_quantity = len(savable)
        # on the contrary, is/are there a/some unsavable product(s)?
        unsavable = self.selenium.find_elements_by_class_name(
            "unsaveProduct"
        )
        # click process
        if savable_quantity > 0:  # at least one product is savable
            ##############################################
            # 1. click on the button to save the product #
            ##############################################
            # randomly choose a favorite
            index = random.randint(0, savable_quantity - 1)
            save_button = savable[index]
            # which product will be saved?
            saved_product_id = save_button.get_attribute("property")
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on "Sauvegarder" button
            actions.click(save_button)
            # wait for the button switch
            actions.pause(1)
            # compile chained actions
            actions.perform()
            ###########################################
            # 2. check that the button state switches #
            ###########################################
            # has the product saved button switched to "unsavable"?
            button = self.selenium.find_element_by_id(saved_product_id)
            switch_button_status = (button.text == "Retirer des favoris")
            # update result
            result *= switch_button_status
            ################################################
            # 3. reverse clicking to cancel product saving #
            ################################################
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on "Retirer des favoris" button (updated)
            updated_button = self.selenium.find_element_by_id(saved_product_id)
            actions.click(updated_button)
            # wait for the button switch
            actions.pause(1)
            # compile chained actions
            actions.perform()
            ############################################################
            # 4. check that the button state switches back to original #
            ############################################################
            # has the product unsaved button switched to "savable"?
            reverse_button = self.selenium.find_element_by_id(saved_product_id)
            switch_button_status = (reverse_button.text == "Sauvegarder")
            # update result
            result *= switch_button_status
            # double check: are we well back to the beginning of the story?
            unsaved = self.selenium.find_elements_by_class_name("saveProduct")
            saved = self.selenium.find_elements_by_class_name("unsaveProduct")
            back_status = ((unsaved is savable) and (saved is unsavable))
            # update result
            result *= back_status
            ################################################################
            # 5. check on the favorites page that the product is NOT saved #
            ################################################################
            # switch to favorites page
            favorites_icon = self.selenium.find_element_by_id("favorites-icon")
            favorites_icon.click()
            # wait for page loading
            WebDriverWait(
                self.selenium,
                timeout=2
            ).until(url_changes(start_url))
            expected_url = f"{self.live_server_url}/favorites/"
            redirect_status = (expected_url == self.selenium.current_url)
            # update result
            result *= redirect_status
            found = False
            # is the saved product among the favorites?
            saved = self.selenium.find_elements_by_class_name(
                "unsaveProduct"
            )
            # loop on all saved products
            counter = 0
            while ((not found) and (counter < len(saved))):
                button = saved[counter]
                if (button.get_attribute("property") == saved_product_id):
                    found = True
                counter += 1
            saved_product_status = not found
            # update result
            result *= saved_product_status
        else:  # no product is savable as favorite
            pass
        self.assertTrue(result)

    def test_go_to_favorites_page(self):
        """
        Test for User Story US08: unique scenario.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on the favorites icon
        favorites_icon = self.selenium.find_element_by_id("favorites-icon")
        favorites_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        expected_url = f"{self.live_server_url}/favorites/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_unsave_product_from_favorites(self):
        """
        Test for User Story US09: scenario #1.
        Standard process:
        1. click on the button to unsave the product
        2. check that the button state switches
        3. refresh the page to check that the product "disappeared"
        """
        result = True
        # start from favorites page
        start_url = f"{self.live_server_url}/favorites/"
        self.selenium.get(start_url)
        # is/are there a/some product(s) registered as favorites?
        saved = self.selenium.find_elements_by_class_name("unsaveProduct")
        saved_quantity = len(saved)
        # click process
        if saved_quantity > 0:  # at least one favorite is registered
            ################################################
            # 1. click on the button to unsave the product #
            ################################################
            # scroll down
            self.selenium.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # wait for scrolling
            legal_link = self.selenium.find_element_by_id("legal-footer")
            WebDriverWait(
                self.selenium,
                timeout=2
            ).until(visibility_of(legal_link))
            # randomly choose a favorite
            index = random.randint(0, saved_quantity - 1)
            unsave_button = saved[index]
            # which product will be unsaved?
            saved_product_id = unsave_button.get_attribute("property")
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on "Retirer des favoris" button
            actions.click(unsave_button)
            # wait for the button switch
            actions.pause(1)
            # compile chained actions
            actions.perform()
            ###########################################
            # 2. check that the button state switches #
            ###########################################
            # has the "unsavable" button switched to "savable"?
            button = self.selenium.find_element_by_id(saved_product_id)
            switch_button_status = (button.text == "Sauvegarder")
            # update result
            result *= switch_button_status
            ###############################################################
            # 3. refresh the page to check that the product "disappeared" #
            ###############################################################
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on a "refresh" button
            refresh_button = self.selenium.find_elements_by_class_name(
                "btn-refresh"
            )[1]
            actions.click(refresh_button)
            # wait for page reloading
            actions.pause(2)
            # compile chained actions
            actions.perform()
            # check that we are still on the favorites page
            expected_url = f"{self.live_server_url}/favorites/"
            page_status = self.selenium.current_url.startswith(expected_url)
            # update result
            result *= page_status
            found = False
            # is the saved product among the favorites?
            saved = self.selenium.find_elements_by_class_name(
                "unsaveProduct"
            )
            # loop on all saved products
            counter = 0
            while ((not found) and (counter < len(saved))):
                button = saved[counter]
                if (button.get_attribute("property") == saved_product_id):
                    found = True
                counter += 1
            saved_product_status = not found
            # update result
            result *= saved_product_status
        else:  # no product is savable as favorite
            pass
        self.assertTrue(result)

    def test_unsave_product_from_favorites_immediate_reverse(self):
        """
        Test for User Story US09: scenario #2.
        Alternative process:
        1. click on the button to unsave the product
        2. check that the button state switches
        3. reverse clicking to cancel product unsaving (keep saved)
        4. check that the button state switches back to original
        5. refresh the page to check that the product is still here
        """
        result = True
        # start from favorites page
        start_url = f"{self.live_server_url}/favorites/"
        self.selenium.get(start_url)
        # is/are there a/some product(s) registered as favorites?
        saved = self.selenium.find_elements_by_class_name("unsaveProduct")
        saved_quantity = len(saved)
        # click process
        if saved_quantity > 0:  # at least one favorite is registered
            ################################################
            # 1. click on the button to unsave the product #
            ################################################
            # scroll down
            self.selenium.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # wait for scrolling
            legal_link = self.selenium.find_element_by_id("legal-footer")
            WebDriverWait(
                self.selenium,
                timeout=2
            ).until(visibility_of(legal_link))
            # randomly choose a favorite
            index = random.randint(0, saved_quantity - 1)
            unsave_button = saved[index]
            # which product will be unsaved?
            saved_product_id = unsave_button.get_attribute("property")
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on "Retirer des favoris" button
            actions.click(unsave_button)
            # wait for the button switch
            actions.pause(1)
            # compile chained actions
            actions.perform()
            ###########################################
            # 2. check that the button state switches #
            ###########################################
            # has the "unsavable" button switched to "savable"?
            button = self.selenium.find_element_by_id(saved_product_id)
            switch_button_status = (button.text == "Sauvegarder")
            # update result
            result *= switch_button_status
            ###############################################################
            # 3. reverse clicking to cancel product unsaving (keep saved) #
            ###############################################################
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on "Retirer des favoris" button (updated)
            updated_button = self.selenium.find_element_by_id(saved_product_id)
            actions.click(updated_button)
            # wait for the button switch
            actions.pause(1)
            # compile chained actions
            actions.perform()
            ############################################################
            # 4. check that the button state switches back to original #
            ############################################################
            # has the "savable" button switched back to "unsavable"?
            reverse_button = self.selenium.find_element_by_id(saved_product_id)
            switch_button_status = (
                reverse_button.text == "Retirer des favoris"
            )
            # update result
            result *= switch_button_status
            ###############################################################
            # 5. refresh the page to check that the product is still here #
            ###############################################################
            # start chained actions
            actions = ActionChains(self.selenium)
            # click on a "refresh" button
            refresh_button = self.selenium.find_elements_by_class_name(
                "btn-refresh"
            )[1]
            actions.click(refresh_button)
            # wait for page reloading
            actions.pause(2)
            # compile chained actions
            actions.perform()
            # check that we are still on the favorites page
            expected_url = f"{self.live_server_url}/favorites/"
            page_status = self.selenium.current_url.startswith(expected_url)
            # update result
            result *= page_status
            found = False
            # is the saved product among the favorites?
            saved = self.selenium.find_elements_by_class_name(
                "unsaveProduct"
            )
            # loop on all saved products
            counter = 0
            while ((not found) and (counter < len(saved))):
                button = saved[counter]
                if (button.get_attribute("property") == saved_product_id):
                    found = True
                counter += 1
            saved_product_status = found
            # update result
            result *= saved_product_status
        else:  # no product is savable as favorite
            pass
        self.assertTrue(result)

    def test_go_to_account_page(self):
        """
        Test for User Story US10: unique scenario.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # click on the account icon
        account_icon = self.selenium.find_element_by_id("account-icon")
        account_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        expected_url = f"{self.live_server_url}/auth/account/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_go_to_legal_page(self):
        """
        Test for User Story US11: unique scenario.
        """
        # start from index (home) page
        start_url = f"{self.live_server_url}/"
        self.selenium.get(start_url)
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        legal_link = self.selenium.find_element_by_id("legal-footer")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(legal_link))
        # click on the "Mentions légales" link
        legal_link.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        expected_url = f"{self.live_server_url}/legal/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_change_password_success(self):
        """
        Test for User Story US13: scenario #1.
        Standard process:
        1. click on "change password" button
        2. fill in the form with no error
        """
        # start from account page
        start_url = f"{self.live_server_url}/auth/account/"
        self.selenium.get(start_url)
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        change_pwd_btn = self.selenium.find_element_by_id("change_pwd_btn")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(change_pwd_btn))
        # click on the "change pawword" button
        change_pwd_btn.click()
        # wait for page loading
        change_pwd_url = f"{self.live_server_url}/auth/change_password/"
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_to_be(change_pwd_url))
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        legal_link = self.selenium.find_element_by_id("legal-footer")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(legal_link))
        # fill in the form
        old_pwd_field = self.selenium.find_element_by_id("id_old_password")
        old_pwd_field.send_keys("TopSecret")
        new_pwd_field1 = self.selenium.find_element_by_id("id_new_password1")
        new_pwd_field1.send_keys("TopSecret123")
        new_pwd_field2 = self.selenium.find_element_by_id("id_new_password2")
        new_pwd_field2.send_keys("TopSecret123")
        # submit the form
        pwd_submit = self.selenium.find_element_by_id("pwd_submit")
        pwd_submit.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(change_pwd_url))
        expected_url = f"{self.live_server_url}/auth/change_password/done/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_change_password_failure_wrong_old_password(self):
        """
        Test for User Story US13: scenario #2.
        Alternative process:
        1. click on "change password" button
        2. fill in the form with wrong old password
        """
        # start from account page
        start_url = f"{self.live_server_url}/auth/account/"
        self.selenium.get(start_url)
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        change_pwd_btn = self.selenium.find_element_by_id("change_pwd_btn")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(change_pwd_btn))
        # click on the "change pawword" button
        change_pwd_btn.click()
        # wait for page loading
        change_pwd_url = f"{self.live_server_url}/auth/change_password/"
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_to_be(change_pwd_url))
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        legal_link = self.selenium.find_element_by_id("legal-footer")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(legal_link))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill in the form
        old_pwd_field = self.selenium.find_element_by_id("id_old_password")
        actions.click(old_pwd_field)
        actions.send_keys("WrongPassword")
        new_pwd_field1 = self.selenium.find_element_by_id("id_new_password1")
        actions.click(new_pwd_field1)
        actions.send_keys("TopSecret123")
        new_pwd_field2 = self.selenium.find_element_by_id("id_new_password2")
        actions.click(new_pwd_field2)
        actions.send_keys("TopSecret123")
        # submit the form
        pwd_submit = self.selenium.find_element_by_id("pwd_submit")
        actions.click(pwd_submit)
        # wait for seeing the error message
        actions.pause(1)
        # compile chained actions
        actions.perform()
        # get an error message: True or False?
        error_message = self.selenium.find_element_by_class_name("text-danger")
        # msg = "
        #   Votre ancien mot de passe est incorrect. Veuillez le rectifier.
        # "
        msg = _(
            "Your old password was entered incorrectly. Please enter it again."
        )
        expected_error = (_(error_message.text) == msg)
        # stay on current page: True or False?
        current_page = (
            self.selenium.current_url ==
            f"{self.live_server_url}/auth/change_password/"
        )
        self.assertTrue(expected_error and current_page)

    def test_change_password_failure_different_new_passwords(self):
        """
        Test for User Story US13: scenario #3.
        Alternative process:
        1. click on "change password" button
        2. fill in the form with two different new passwords
        """
        # start from account page
        start_url = f"{self.live_server_url}/auth/account/"
        self.selenium.get(start_url)
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        change_pwd_btn = self.selenium.find_element_by_id("change_pwd_btn")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(change_pwd_btn))
        # click on the "change pawword" button
        change_pwd_btn.click()
        # wait for page loading
        change_pwd_url = f"{self.live_server_url}/auth/change_password/"
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_to_be(change_pwd_url))
        # scroll down
        self.selenium.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        # wait for scrolling
        legal_link = self.selenium.find_element_by_id("legal-footer")
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(visibility_of(legal_link))
        # start chained actions
        actions = ActionChains(self.selenium)
        # fill in the form
        old_pwd_field = self.selenium.find_element_by_id("id_old_password")
        actions.click(old_pwd_field)
        actions.send_keys("TopSecret")
        new_pwd_field1 = self.selenium.find_element_by_id("id_new_password1")
        actions.click(new_pwd_field1)
        actions.send_keys("TopSecret123")
        new_pwd_field2 = self.selenium.find_element_by_id("id_new_password2")
        actions.click(new_pwd_field2)
        actions.send_keys("TopSecret456")  # different from password #1
        # submit the form
        pwd_submit = self.selenium.find_element_by_id("pwd_submit")
        actions.click(pwd_submit)
        # wait for seeing the error message
        actions.pause(1)
        # compile chained actions
        actions.perform()
        # get an error message: True or False?
        error_message = self.selenium.find_element_by_class_name("text-danger")
        # msg = "Les deux mots de passe ne correspondent pas."
        msg = _(
            "The two password fields didn’t match."
        )
        expected_error = (_(error_message.text) == msg)
        # stay on current page: True or False?
        current_page = (
            self.selenium.current_url ==
            f"{self.live_server_url}/auth/change_password/"
        )
        self.assertTrue(expected_error and current_page)
