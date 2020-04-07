"""
This module contains the unit tests related to the 'Product' class.
"""

from django.test import TestCase

from pur_beurre.off_sub.models import Product, Category, Store


class ProductTestCase(TestCase):

    def setUp(self):
        # create a product
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
        # create two categories and link them to the product
        self.category_1 = Category.objects.create(name="Category #1")
        self.product_a.categories.add(self.category_1)
        self.category_2 = Category.objects.create(name="Category #2")
        self.product_a.categories.add(self.category_2)
        # create two stores and link them to the product
        store_1 = Store.objects.create(name="Store #1")
        self.product_a.stores.add(store_1)
        store_2 = Store.objects.create(name="Store #2")
        self.product_a.stores.add(store_2)

    def create_4_other_products(self):
        # create 4 other products
        self.product_b = Product(
            code='2222222222222',
            product_name="product b",
            nutriscore_grade='b',
            nutriscore_score=1,
            url="b-url",
            image_url="b-image-url",
        )
        self.product_b.add_product_to_db()
        self.product_c = Product(
            code='3333333333333',
            product_name="product c",
            nutriscore_grade='c',
            nutriscore_score=6,
            url="c-url",
            image_url="c-image-url",
        )
        self.product_c.add_product_to_db()
        self.product_d = Product(
            code='4444444444444',
            product_name="product d",
            nutriscore_grade='d',
            nutriscore_score=14,
            url="d-url",
            image_url="d-image-url",
        )
        self.product_d.add_product_to_db()
        self.product_e = Product(
            code='5555555555555',
            product_name="product e",
            nutriscore_grade='e',
            nutriscore_score=25,
            url="e-url",
            image_url="e-image-url",
        )
        self.product_e.add_product_to_db()
        # create categories and link them to the products
        self.product_b.categories.add(self.category_1)
        self.product_c.categories.add(self.category_1)
        self.product_d.categories.add(self.category_2)
        self.product_e.categories.add(self.category_2)

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
            code='2222222222222',
            product_name="a new product",
            nutriscore_grade='b',
            nutriscore_score=1,
            url="https://fr.openfoodfacts.org/produit/2222222222222/"
            "a-new-product",
            image_url="https://static.openfoodfacts.org/images/products/"
            "222/222/222/2222/front_fr.8.400.jpg",
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
            url="https://fr.openfoodfacts.org/produit/1234567890123/"
            "a-superb-product",
            image_url="https://static.openfoodfacts.org/images/products/"
            "123/456/789/0123/front_fr.8.400.jpg",
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
            url="https://fr.openfoodfacts.org/produit/1234567890123/"
            "a-fake-product",
            image_url="https://static.openfoodfacts.org/images/products/"
            "123/456/789/0123/front_fr.8.400.jpg",
        )
        product_a_bis.add_product_to_db()
        # count the number of products again
        new_products_records = Product.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_products_records, old_products_records)

    def test_get_best_subs_with_good_product(self):
        """
        Test if the substitution program returns the best products.
        In this test case, the selected product SHOULD BE returned.
        """
        # test with 2 subs
        nb_sub = 2
        # create 4 other products
        self.create_4_other_products()
        # get 2 subs for 'product_d'
        subs_qs = self.product_b.get_best_subs(nb_sub)
        # collect the nutriscore of the 2 subs
        subs_nutri = [sub.nutriscore_score for sub in subs_qs]
        # what is the worst nutriscore in the list of subs?
        sub_nutri_max = max(subs_nutri)
        # is the selected product in the subs?
        good_product = (sub_nutri_max >= self.product_b.nutriscore_score)
        # are the other products worse?
        all_list = Product.objects.all()
        all_nutri = [prod.nutriscore_score for prod in all_list]
        all_nutri.sort()
        best_of_other_nutri = all_nutri[nb_sub]
        other_product = (sub_nutri_max <= best_of_other_nutri)
        # union statement
        self.assertTrue(good_product and other_product)

    def test_get_best_subs_without_good_product(self):
        """
        Test if the substitution program returns the best products.
        In this test case, the selected product SHOULD NOT BE returned.
        """
        # test with 2 subs
        nb_sub = 2
        # create 4 other products
        self.create_4_other_products()
        # get 2 subs for 'product_e'
        subs_qs = self.product_e.get_best_subs(nb_sub)
        # collect the nutriscore of the 2 subs
        subs_nutri = [sub.nutriscore_score for sub in subs_qs]
        # what is the worst nutriscore in the list of subs?
        sub_nutri_max = max(subs_nutri)
        # is the selected product worse?
        bad_product = (sub_nutri_max <= self.product_e.nutriscore_score)
        # are the other products worse?
        all_prods = Product.objects.filter(categories__name="Category #2")
        all_nutri = [prod.nutriscore_score for prod in all_prods]
        all_nutri.sort()
        # focus on the best among the other ones
        best_of_other_nutri = all_nutri[nb_sub]
        other_product = (sub_nutri_max <= best_of_other_nutri)
        # union statement
        self.assertTrue(bad_product and other_product)
