"""
Please execute this module first, with "manage.py",
to build and fill in the database 'pur_beurre_db'.
Pre-requisite: the database 'pur_beurre_db' has to be created.
"""

import re

import requests
from django.core.management.base import BaseCommand

from off_sub.models import Category, Product, Store


class Command(BaseCommand):
    help = 'Initialize the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "Installation en cours, veuillez patienter SVP..."
        ))
        # fill in the database tables with products, categories and stores
        # iterate on each pre-selected category
        for categ_name in Category.get_categories_list():
            # initialize the category
            categ = Category.objects.get_or_create(name=categ_name)[0]
            # add the category to the database
            categ.add_category_to_db()
            # execute the HTTP request to get products with API
            categ_250 = requests.get(categ.get_url_250_products())
            categ_250_dict = categ_250.json()
            if (categ_250.status_code == 200) and (categ_250_dict["count"]):
                api_return = categ_250.json()  # type is dict
                products_list = api_return["products"]  # type is list of dict
                # iterate on each product
                for item in products_list:  # type is dict
                    # initiate a new instance of product
                    prod = Product()
                    # filter on:
                    # - products containing "France" in the list of countries
                    # - products with 'nutrition_grade_fr' and 'code' completed
                    regexp = "(.*)[Ff]rance(.*)"
                    if (re.match(regexp, item["countries"]) is not None) \
                            and ("code" in item.keys()) \
                            and ("nutriscore_grade" in item.keys()):
                        # set the product attributes
                        prod.code = item["code"]
                        try:
                            prod.product_name = item["product_name"]
                        except KeyError:
                            prod.product_name = "[Produit sans nom]"
                        prod.nutriscore_grade = item["nutriscore_grade"]
                        prod.nutriscore_score = \
                            int(item["nutriscore_score"])
                        try:
                            prod.url = item["url"]
                        except KeyError:
                            prod.url = ""
                        try:
                            prod.image_url = item["image_url"]
                        except KeyError:
                            prod.image_url = ""
                        # extract some nutriments data as fat, sugars and salt
                        extract_nutriments_data(item, prod)
                        # add the product to the database, if necessary
                        prod_id = prod.add_product_to_db()
                        # cover the case where the product already exists
                        prod = Product.objects.get(id=prod_id)
                        # update database (table ProductCategory), if necessary
                        prod.add_product_category_to_db(categ)
                        # if applicable, link the stores and the product
                        shop_names = []
                        try:
                            shops_list = item["stores"].split(",")
                            shop_names = [
                                shop.strip() for shop in shops_list
                            ]
                        except KeyError:  # if no store mentioned here...
                            # ... then skip this step
                            continue
                        for shop_name in shop_names:
                            # create a new instance of store
                            shop = Store.objects.get_or_create(
                                name=shop_name
                            )[0]
                            # add the store to the database, if necessary
                            shop.add_store_to_db()
                            # update the database (table ProductStore)
                            prod.add_product_store_to_db(shop)
        self.stdout.write(self.style.SUCCESS("Installation terminée !"))


# function called in the method 'Command.handle'
def extract_nutriments_data(item, prod):
    """
    This sub-function extracts some nutriments data from Open Food Facts.
    """
    try:
        prod.fat = str(item["nutriments"]["fat_value"]) + \
                        max(item["nutriments"]["fat_unit"], "g")
    except KeyError:
        prod.fat = "donnée inconnue"
    try:
        prod.saturated_fat = str(item["nutriments"]["saturated-fat_value"]) + \
                        max(item["nutriments"]["saturated-fat_unit"], "g")
    except KeyError:
        prod.saturated_fat = "donnée inconnue"
    try:
        prod.sugars = str(item["nutriments"]["sugars_value"]) + \
                        max(item["nutriments"]["sugars_unit"], "g")
    except KeyError:
        prod.sugars = "donnée inconnue"
    try:
        prod.salt = str(item["nutriments"]["salt_value"]) + \
                        max(item["nutriments"]["salt_unit"], "g")
    except KeyError:
        prod.salt = "donnée inconnue"
