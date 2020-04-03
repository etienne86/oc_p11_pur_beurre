"""
This module contains the unit tests related to the functions (app 'off_sub').
"""

from django.test import TestCase

from off_sub import functions as fct
from off_sub.models import Product


class GetAllProductsTestCase(TestCase):

    def setUp(self):
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

    def test_get_all_products_results_type_is_dict(self):
        """
        Test that the results is a dict.
        """
        self.assertIs(type(fct.get_all_products()), dict)

    def test_get_all_products_value_type_is_list_of_strings(self):
        """
        Test that, in the returned dict, the value for key 'all_products',
        is a list of strings.
        """
        context = fct.get_all_products()
        result = True
        try:
            products_list = context['all_products']
            for item in products_list:
                result = (result and (type(item) is str))
        except Exception:
            result = False
        self.assertTrue(result)

    def test_get_all_products_really_all(self):
        """
        Test that all products are in the returned dict,
        used as context in views.
        """
        # count the number of products in database
        products_counter = len(Product.objects.all())
        # count the number of products in the returned dict
        context_value = fct.get_all_products()['all_products']  # type is str
        # for one product, there are two double quotes
        double_quotes_counter = context_value.count('\"')
        # match
        self.assertEqual(products_counter * 2, double_quotes_counter)
