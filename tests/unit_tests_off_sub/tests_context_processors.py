"""
This module contains the unit tests related
to the context_processors (app 'off_sub').
"""

from django.test import TestCase
from django.test.client import RequestFactory

from off_sub import context_processors as off_sub_cp
from off_sub.models import Product


class ContextProcessorsTestCase(TestCase):

    def setUp(self):
        # some products
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
        self.product_b = Product.objects.create(
            code='2222222222222',
            product_name="a new product",
            nutriscore_grade='b',
            nutriscore_score=1,
            url="https://fr.openfoodfacts.org/produit/2222222222222/"
            "a-new-product",
            image_url="https://static.openfoodfacts.org/images/products/"
            "222/222/222/2222/front_fr.8.400.jpg",
        )
        # a request
        rf = RequestFactory()
        self.request = rf.get('foo/')

    def test_off_sub_cp_all_products_results_type_is_dict(self):
        """
        Test that the results is a dict.
        """
        context = off_sub_cp.pur_beurre_all_products(self.request)
        self.assertIs(type(context), dict)

    def test_off_sub_cp_all_products_value_type_is_list_of_strings(self):
        """
        Test that, in the returned dict, the value for key 'all_products',
        is a list of strings.
        """
        context = off_sub_cp.pur_beurre_all_products(self.request)
        result = True
        try:
            products_list = context['all_products']
            for item in products_list:
                result = (result and (type(item) is str))
        except Exception:
            result = False
        self.assertTrue(result)

    def test_off_sub_cp_all_products_really_all(self):
        """
        Test that all products are in the returned dict,
        used as context in views.
        """
        # count the number of products in database
        products_counter = len(Product.objects.all())
        # count the number of products in the returned dict
        context = off_sub_cp.pur_beurre_all_products(self.request)
        context_value = context['all_products']  # str
        # for one product, there are two double quotes
        double_quotes_counter = context_value.count('\"')
        # match
        self.assertEqual(products_counter * 2, double_quotes_counter)
