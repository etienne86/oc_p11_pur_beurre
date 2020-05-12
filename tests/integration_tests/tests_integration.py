"""
This module contains the integration tests for the project, using two classes:
- UnitTestCase, which contains unit tests
- TestWithAuthenticatedUser, which contains tests using the Firefox web browser
"""

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import url_changes
from seleniumlogin import force_login

from auth.models import MyUser
from off_sub.models import Product, Category


class UnitTestCase(TestCase):
    """
    This class contains unit tests.
    """

    def setUp(self):
        # initialize two users
        self.user_tic = MyUser.objects.create_user(
            email="tic@mail.com",
            first_name="Tic"
        )
        self.user_tac = MyUser.objects.create_user(
            email="tac@mail.com",
            first_name="Tac"
        )
        # initialize some products
        self.product_a = Product.objects.create(
            code='1234567890123',
            nutriscore_grade='a',
            nutriscore_score=-1,
        )
        self.product_b = Product.objects.create(
            code='2222222222222',
            nutriscore_grade='b',
            nutriscore_score=1,
        )
        self.product_c = Product.objects.create(
            code='3333333333333',
            nutriscore_grade='c',
            nutriscore_score=6,
        )
        self.product_d = Product.objects.create(
            code='4444444444444',
            nutriscore_grade='d',
            nutriscore_score=14,
        )
        # create some favorites for user "Tic"
        self.user_tic.favorites.add(self.product_a)
        self.user_tic.favorites.add(self.product_b)
        self.tic_favorites_start = self.user_tic.favorites.all()
        # create some favorites for user "Tac"
        self.user_tac.favorites.add(self.product_b)
        self.user_tac.favorites.add(self.product_c)
        self.tac_favorites_start = self.user_tac.favorites.all()

    def test_remove_common_favorite_no_change_on_other_user(self):
        """
        A product is registered as favorite for two different users.
        Test if removal of this favorite for one user
        has no impact on other user's favorites.
        """
        # remove the favorite from user "Tic"
        self.user_tic.favorites.remove(self.product_b)
        # update the favorites for user "Tac"
        tac_favorites = self.user_tac.favorites.all()
        # no change is expected for user "Tac"
        self.assertEqual(list(self.tac_favorites_start), list(tac_favorites))

    def test_add_a_favorite_no_change_on_other_user(self):
        """
        Test if adding a favorite to one user
        has no impact on other user's favorites.
        """
        # add a favorite to user "Tic"
        self.user_tic.favorites.add(self.product_d)
        # update the favorites for user "Tac"
        tac_favorites = self.user_tac.favorites.all()
        # no change is expected for user "Tac"
        self.assertEqual(list(self.tac_favorites_start), list(tac_favorites))


class TestWithAnonymousUser(StaticLiveServerTestCase):
    """
    This class contains an integration test with anonymous user.
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
        # initialize some products
        self.product_a = Product.objects.create(
            code='1234567890123',
            nutriscore_grade='a',
            nutriscore_score=-1,
        )
        self.product_b = Product.objects.create(
            code='2222222222222',
            nutriscore_grade='b',
            nutriscore_score=1,
        )
        self.product_c = Product.objects.create(
            code='3333333333333',
            nutriscore_grade='c',
            nutriscore_score=6,
        )
        self.product_d = Product.objects.create(
            code='4444444444444',
            nutriscore_grade='d',
            nutriscore_score=14,
        )
        # a category for these products
        self.category_1 = Category.objects.create(name="Category #1")
        self.product_a.categories.add(self.category_1)
        self.product_b.categories.add(self.category_1)
        self.product_c.categories.add(self.category_1)
        self.product_d.categories.add(self.category_1)

    def look_for_a_product_from_navbar(self, start_url):
        """
        This method is called in several tests (in this class, and other).
        """
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
        ).until(url_changes(start_url))
        # see "results" page
        product_id = self.product_a.id
        expected_url = f"{self.live_server_url}/results/{product_id}"
        return expected_url

    def test_look_for_a_product_from_navbar_in_sign_template(self):
        """
        Test if searching a product is also possible from 'sign' page.
        """
        # start from sign page
        start_url = f"{self.live_server_url}/auth/sign/"
        # execute the process
        expected_url = self.look_for_a_product_from_navbar(start_url)
        self.assertEqual(self.selenium.current_url, expected_url)


class TestWithAuthenticatedUser(StaticLiveServerTestCase):
    """
    This class contains integration tests with an authenticated user.
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
        # initialize a user
        self.user = MyUser.objects.create_user(
            email="tic@mail.com",
            first_name="Tic",
            password="Hazelnut"
        )
        # force login for this user
        force_login(self.user, self.selenium, self.live_server_url)
        # initialize some products
        self.product_a = Product.objects.create(
            code='1234567890123',
            nutriscore_grade='a',
            nutriscore_score=-1,
        )
        self.product_b = Product.objects.create(
            code='2222222222222',
            nutriscore_grade='b',
            nutriscore_score=1,
        )
        self.product_c = Product.objects.create(
            code='3333333333333',
            nutriscore_grade='c',
            nutriscore_score=6,
        )
        self.product_d = Product.objects.create(
            code='4444444444444',
            nutriscore_grade='d',
            nutriscore_score=14,
        )
        # a category for these products
        self.category_1 = Category.objects.create(name="Category #1")
        self.product_a.categories.add(self.category_1)
        self.product_b.categories.add(self.category_1)
        self.product_c.categories.add(self.category_1)
        self.product_d.categories.add(self.category_1)

    def look_for_a_product_from_navbar(self, start_url):
        return TestWithAnonymousUser.look_for_a_product_from_navbar(
            self,
            start_url
        )

    def test_navbar_click_from_logout_to_sign(self):
        """
        Test navigating from 'logout' page to 'sign' page.
        """
        # start from logout page
        start_url = f"{self.live_server_url}/auth/log_out/"
        self.selenium.get(start_url)
        # click on "sign" icon
        sign_icon = self.selenium.find_element_by_id("sign-icon")
        sign_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "sign" page
        expected_url = f"{self.live_server_url}/auth/sign/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_navbar_click_from_account_to_favorites(self):
        """
        Test navigating from 'account' page to 'favorites' page.
        """
        # start from account page
        start_url = f"{self.live_server_url}/auth/account/"
        self.selenium.get(start_url)
        # click on "favorites" icon
        favorites_icon = self.selenium.find_element_by_id("favorites-icon")
        favorites_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "favorites" page
        expected_url = f"{self.live_server_url}/favorites/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_navbar_click_from_account_to_logout(self):
        """
        Test navigating from 'account' page to 'logout' page.
        """
        # start from account page
        start_url = f"{self.live_server_url}/auth/account/"
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

    def test_navbar_click_from_favorites_to_account(self):
        """
        Test navigating from 'favorites' page to 'account' page.
        """
        # start from favorites page
        start_url = f"{self.live_server_url}/favorites/"
        self.selenium.get(start_url)
        # click on "account" icon
        account_icon = self.selenium.find_element_by_id("account-icon")
        account_icon.click()
        # wait for page loading
        WebDriverWait(
            self.selenium,
            timeout=2
        ).until(url_changes(start_url))
        # see "account" page
        expected_url = f"{self.live_server_url}/auth/account/"
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_navbar_click_from_favorites_to_logout(self):
        """
        Test navigating from 'favorites' page to 'logout' page.
        """
        # start from favorites page
        start_url = f"{self.live_server_url}/favorites/"
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

    def test_look_for_a_product_from_navbar_in_account_template(self):
        """
        Test if searching a product is also possible from 'account' page.
        """
        # start from account page
        start_url = f"{self.live_server_url}/auth/account/"
        # execute the process
        expected_url = self.look_for_a_product_from_navbar(start_url)
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_navbar_in_favorites_template(self):
        """
        Test if searching a product is also possible from 'favorites' page.
        """
        # start from favorites page
        start_url = f"{self.live_server_url}/favorites/"
        # execute the process
        expected_url = self.look_for_a_product_from_navbar(start_url)
        self.assertEqual(self.selenium.current_url, expected_url)

    def test_look_for_a_product_from_navbar_in_logout_template(self):
        """
        Test if searching a product is also possible from 'logout' page.
        """
        # start from logout page
        start_url = f"{self.live_server_url}/auth/log_out/"
        # execute the process
        expected_url = self.look_for_a_product_from_navbar(start_url)
        self.assertEqual(self.selenium.current_url, expected_url)
