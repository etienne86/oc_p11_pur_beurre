"""
This module contains the unit tests related to
the db_init custom command (app 'off_sub').
"""

from django.test import TestCase
from unittest.mock import patch

from django.core.management import call_command

from off_sub.models import Product, Category, Store


class MockCategory:

    CATEGORIES_LIST = ["desserts"]

    objects = Category.objects

    def __init__(self, name):
        pass

    def add_category_to_db(self):
        Category.add_category_to_db()

    @classmethod
    def get_categories_list(cls):
        return cls.CATEGORIES_LIST

    def get_url_250_products(self):
        return "a_fictive_url"


class MockRequestsGet:

    OFF_API_RESULT = {
        "count": 123,
        "products": [
            # an ideal product (product a)
            {
                "countries": "France",
                "code": '1234567890123',
                "product_name": "a superb product",
                "nutriscore_grade": 'a',
                "nutriscore_score": -20,  # fictive (not calculated)
                "url": "a_superb_url",
                "image_url": "a_superb_image_url",
                "nutriments": {
                    "fat_value": 0,
                    "fat_unit": "g",
                    "saturated-fat_value": 0,
                    "saturated-fat_unit": "g",
                    "sugars_value": 0,
                    "sugars_unit": "g",
                    "salt_value": 0,
                    "salt_unit": "mg"
                },
                "stores": "Aux champignons,Le clair de lune,Bio coupe"
            },
            # a product with missing information (product b)
            {
                "countries": "France",
                "code": '3210987654321',
                "nutriscore_grade": 'b',
                "nutriscore_score": 1,
            }
        ]
    }

    def __init__(self, url, params=None):
        self.status_code = 200

    def json(self):
        return self.OFF_API_RESULT


@patch(target='off_sub.models.Category', new=MockCategory)
@patch(target='requests.get', new=MockRequestsGet)
class DatabaseInitialization(TestCase):

    @classmethod
    @patch(target='off_sub.models.Category', new=MockCategory)
    @patch(target='requests.get', new=MockRequestsGet)
    def setUpClass(cls):
        super().setUpClass()
        # initialize the database
        call_command('db_init')
        # get the products
        cls.all_products = Product.objects.all()
        cls.prod_a = cls.all_products[0]
        cls.prod_b = cls.all_products[1]
        # get the stores
        cls.all_stores = Store.objects.all()
        cls.store_a = cls.all_stores[0]
        cls.store_b = cls.all_stores[1]
        cls.store_c = cls.all_stores[2]

    def test_get_all_products(self):
        self.assertEqual(len(self.all_products), 2)

    def test_get_code_product_a_and_product_b(self):
        self.assertTrue(
            self.prod_a.code == '1234567890123' and
            self.prod_b.code == '3210987654321'
        )

    def test_get_product_name_product_a(self):
        self.assertEqual(self.prod_a.product_name, "a superb product")

    def test_get_product_name_product_b(self):
        self.assertEqual(self.prod_b.product_name, "[Produit sans nom]")

    def test_nutriscore_grade_product_a_and_product_b(self):
        self.assertTrue(
            self.prod_a.nutriscore_grade == "a" and
            self.prod_b.nutriscore_grade == "b"
        )

    def test_nutriscore_score_product_a_and_product_b(self):
        self.assertTrue(
            self.prod_a.nutriscore_score == -20 and
            self.prod_b.nutriscore_score == 1
        )

    def test_get_url_product_a(self):
        self.assertEqual(self.prod_a.url, "a_superb_url")

    def test_get_url_product_b(self):
        self.assertEqual(self.prod_b.url, "")

    def test_get_image_url_product_a(self):
        self.assertEqual(self.prod_a.image_url, "a_superb_image_url")

    def test_get_image_url_product_b(self):
        self.assertEqual(self.prod_b.image_url, "")

    def test_get_fat_product_a(self):
        self.assertEqual(self.prod_a.fat, "0g")

    def test_get_fat_product_b(self):
        self.assertEqual(self.prod_b.fat, "donnée inconnue")

    def test_get_saturated_fat_product_a(self):
        self.assertEqual(self.prod_a.saturated_fat, "0g")

    def test_get_saturated_fat_product_b(self):
        self.assertEqual(self.prod_b.saturated_fat, "donnée inconnue")

    def test_get_sugars_product_a(self):
        self.assertEqual(self.prod_a.sugars, "0g")

    def test_get_sugars_product_b(self):
        self.assertEqual(self.prod_b.sugars, "donnée inconnue")

    def test_get_salt_product_a(self):
        self.assertEqual(self.prod_a.salt, "0mg")

    def test_get_salt_product_b(self):
        self.assertEqual(self.prod_b.salt, "donnée inconnue")

    def test_get_all_stores(self):
        self.assertEqual(len(self.all_stores), 3)

    def test_get_stores_names(self):
        store_a_bool = (self.store_a.name == "Aux champignons")
        store_b_bool = (self.store_b.name == "Le clair de lune")
        store_c_bool = (self.store_c.name == "Bio coupe")
        stores_bool = (store_a_bool and store_b_bool and store_c_bool)
        self.assertTrue(stores_bool)

    def test_stores_linked_to_product_a(self):
        prod_a_store_a_bool = (self.store_a in self.prod_a.stores.all())
        prod_a_store_b_bool = (self.store_b in self.prod_a.stores.all())
        prod_a_store_c_bool = (self.store_c in self.prod_a.stores.all())
        products_stores_bool = (
            prod_a_store_a_bool and
            prod_a_store_b_bool and
            prod_a_store_c_bool
        )
        self.assertTrue(products_stores_bool)

    def test_no_store_linked_to_product_b(self):
        self.assertEqual(len(self.prod_b.stores.all()), 0)
