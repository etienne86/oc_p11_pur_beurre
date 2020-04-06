"""
This module contains the unit tests related to the views (app 'off_sub').
"""

from django.urls import reverse
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser

from pur_beurre.auth.models import MyUser
from pur_beurre.off_sub import views
from pur_beurre.off_sub.models import Product


class FavoritesPageTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            email="toto@mail.com",
            first_name="Toto"
        )

    def test_favorites_page_returns_200_with_an_authenticated_user(self):
        """
        Test that favorites page returns a 200 code
        if a user is authenticated.
        """
        # simulate a request with a logged-in user
        request = self.factory.get(reverse('off_sub:favorites'))
        request.user = self.user
        # get the response
        response = views.favorites(request)
        self.assertEqual(response.status_code, 200)

    def test_favorites_page_returns_302_with_no_user(self):
        """
        Test that favorites page returns a 302 code if no user is logged in.
        """
        # simulate a request with no user
        request = self.factory.get(reverse('off_sub:favorites'))
        request.user = AnonymousUser()
        # get the response
        response = views.favorites(request)
        self.assertEqual(response.status_code, 302)


class FoodPageTestCase(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            code='1234567890123',
            product_name="a superb product",
            nutriscore_grade='a',
            nutriscore_score=-1,
            url="https://fr.openfoodfacts.org/produit/1234567890123/"
            "a-superb-product",
            image_url="https://static.openfoodfacts.org/images/products/"
            "123/456/789/0123/front_fr.8.400.jpg",
        )

    def test_food_page_returns_200(self):
        """
        Test that food page returns a 200 code.
        """
        product_id = self.product.id
        response = self.client.get(reverse(
            'off_sub:food',
            args=(product_id,)
        ))
        self.assertEqual(response.status_code, 200)

    def test_food_page_returns_404(self):
        """
        Test that food page returns a 404 code if the item does not exist.
        """
        product_id = self.product.id + 1
        response = self.client.get(reverse(
            'off_sub:food',
            args=(product_id,)
        ))
        self.assertEqual(response.status_code, 404)


class IndexPageTestCase(TestCase):

    def test_index_page_returns_200(self):
        """
        Test that index page returns a 200 code.
        """
        response = self.client.get(reverse('off_sub:index'))
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):

    def test_legal_page_returns_200(self):
        """
        Test that legal page returns a 200 code.
        """
        response = self.client.get(reverse('off_sub:legal'))
        self.assertEqual(response.status_code, 200)


class ResultsPageTestCase(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            code='1234567890123',
            product_name="a superb product",
            nutriscore_grade='a',
            nutriscore_score=-1,
            url="https://fr.openfoodfacts.org/produit/1234567890123/"
            "a-superb-product",
            image_url="https://static.openfoodfacts.org/images/products/"
            "123/456/789/0123/front_fr.8.400.jpg",
        )

    def test_results_page_returns_200(self):
        """
        Test that results page returns a 200 code.
        """
        product_id = self.product.id
        response = self.client.get(reverse(
            'off_sub:results',
            args=(product_id,)
        ))
        self.assertEqual(response.status_code, 200)

    def test_results_page_returns_404(self):
        """
        Test that results page returns a 404 code if the item does not exist.
        """
        product_id = self.product.id + 1
        response = self.client.get(reverse(
            'off_sub:results',
            args=(product_id,)
        ))
        self.assertEqual(response.status_code, 404)
