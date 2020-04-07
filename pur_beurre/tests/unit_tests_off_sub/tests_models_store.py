"""
This module contains the unit tests related to the 'Store' class.
"""

from django.test import TestCase

from pur_beurre.off_sub.models import Store


class StoreTestCase(TestCase):

    def setUp(self):
        # one store already recorded
        self.store_1 = Store.objects.create(name="auchan")

    def test_add_store_to_db_one_new_record(self):
        """
        Test if one record has been added to the 'Store' table.
        """
        # count the number of stores
        old_stores_records = Store.objects.count()
        # add a new store
        store_2 = Store(name="carrefour")
        store_2.add_store_to_db()
        # count the number of stores again
        new_stores_records = Store.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_stores_records, old_stores_records + 1)

    def test_add_store_to_db_already_exists(self):
        """
        Test if the 'Store' table stays unchanged
        if the store is already recorded.
        """
        # count the number of stores
        old_stores_records = Store.objects.count()
        # add a store already recorded
        store_1_bis = Store(name="auchan")
        store_1_bis.add_store_to_db()
        # count the number of stores again
        new_stores_records = Store.objects.count()
        # compare the two numbers (after and before)
        self.assertEqual(new_stores_records, old_stores_records)
