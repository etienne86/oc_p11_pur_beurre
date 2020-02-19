"""This module contains the tests related to the 'Product' class."""

from django.test import TestCase

from off_sub.models import Product, Category, Store


class ProductTestCase(TestCase):

    def setUp(self):
        # create a product
        self.product_a = Product.objects.create(
            code='1234567890123',
            product_name="a superb product",
            nutriscore_grade='a',
            nutriscore_score=-1,
            url="https://fr.openfoodfacts.org/produit/1234567890123/a-superb-product",
            image_url="https://static.openfoodfacts.org/images/products/123/456/789/0123/front_fr.8.400.jpg",
        )
        # create two categories and link them to the product
        category_1 = Category.objects.create(name="Category #1")
        self.product_a.categories.add(category_1)
        category_2 = Category.objects.create(name="Category #2")
        self.product_a.categories.add(category_2)
        # create two stores and link them to the product
        store_1 = Store.objects.create(name="Store #1")
        self.product_a.stores.add(store_1)
        store_2 = Store.objects.create(name="Store #2")
        self.product_a.stores.add(store_2)

    def test_add_product_category_to_db_one_new_record(self):
        """
        Test if one record has been added to the 'ProductCategory' table
        (off_sub_product_categories).
        """
        # count the number of categories for product_a
        old_count = Category.objects.filter(products=self.product_a).count()
        # add a NEW category to product_a
        category_3 = Category.objects.create(name="Category #3")
        self.product_a.add_product_category_to_db(category_3)
        # count the number of categories for product_a again
        new_count = Category.objects.filter(products=self.product_a).count()
        # compare the two numbers (after and before)
        self.assertEqual(new_count, old_count + 1)

    def test_add_product_category_to_db_already_exists(self):
        """
        Test if the 'ProductCategory' table (off_sub_product_categories) stays
        unchanged if the link between product and category is already recorded.
        """
        # count the number of categories for product_a
        old_count = Category.objects.filter(products=self.product_a).count()
        # add a category already linked to product_a
        category_1_bis = Category.objects.get(name="Category #1")
        self.product_a.add_product_category_to_db(category_1_bis)
        # count the number of categories for product_a again
        new_count = Category.objects.filter(products=self.product_a).count()
        # compare the two numbers (after and before)
        self.assertEqual(new_count, old_count)

    def test_add_product_store_to_db_one_new_record(self):
        """
        Test if one record has been added to the 'ProductStore' table
        (off_sub_product_stores).
        """
        # count the number of stores for product_a
        old_count = Store.objects.filter(products=self.product_a).count()
        # add a NEW store to product_a
        store_3 = Store.objects.create(name="Store #3")
        self.product_a.add_product_store_to_db(store_3)
        # count the number of stores for product_a again
        new_count = Store.objects.filter(products=self.product_a).count()
        # compare the two numbers (after and before)
        self.assertEqual(new_count, old_count + 1)

    def test_add_product_store_to_db_already_exists(self):
        """
        Test if the 'ProductStore' table (off_sub_product_stores) stays
        unchanged if the link between product and store is already recorded.
        """
        # count the number of stores for product_a
        old_count = Store.objects.filter(products=self.product_a).count()
        # add a store already linked to product_a
        store_1_bis = Store.objects.get(name="Store #1")
        self.product_a.add_product_store_to_db(store_1_bis)
        # count the number of stores for product_a again
        new_count = Store.objects.filter(products=self.product_a).count()
        # compare the two numbers (after and before)
        self.assertEqual(new_count, old_count)

    def test_add_product_to_db_one_new_record(self):
        """
        Test if one record has been added to the 'Product' table
        (off_sub_product).
        """
        # count the number of products
        old_products_records = Product.objects.count()
        # add a new product
        product_b = Product(
            code='1111111111111',
            product_name="a new product",
            nutriscore_grade='b',
            nutriscore_score=2,
            url="https://fr.openfoodfacts.org/produit/1111111111111/a-new-product",
            image_url="https://static.openfoodfacts.org/images/products/111/111/111/1111/front_fr.8.400.jpg",
        )
        product_b.add_product_to_db()
        # count the number of products again
        new_products_records = Product.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_products_records, old_products_records + 1)

    def test_add_product_to_db_product_already_exists(self):
        """
        Test if the 'Product' table (off_sub_product) stays
        unchanged if the product is already recorded.
        """
        # count the number of products
        old_products_records = Product.objects.count()
        # add a product already recorded
        product_a_bis = Product(
            code='1234567890123',
            product_name="a superb product",
            nutriscore_grade='a',
            nutriscore_score=-1,
            url="https://fr.openfoodfacts.org/produit/1234567890123/a-superb-product",
            image_url="https://static.openfoodfacts.org/images/products/123/456/789/0123/front_fr.8.400.jpg",
        )
        product_a_bis.add_product_to_db()
        # count the number of products again
        new_products_records = Product.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_products_records, old_products_records)

    def test_add_product_to_db_same_code(self):
        """
        Test if the 'Product' table (off_sub_product) stays unchanged if
        the (fake) product has the same code as another one already recorded.
        """
        # count the number of products
        old_products_records = Product.objects.count()
        # add a product with a code already recorded
        product_a_bis = Product(
            code='1234567890123',
            product_name="a fake product",
            nutriscore_grade='a',
            nutriscore_score=-1,
            url="https://fr.openfoodfacts.org/produit/1234567890123/a-fake-product",
            image_url="https://static.openfoodfacts.org/images/products/123/456/789/0123/front_fr.8.400.jpg",
        )
        product_a_bis.add_product_to_db()
        # count the number of products again
        new_products_records = Product.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_products_records, old_products_records)