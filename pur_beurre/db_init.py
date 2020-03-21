"""
Please execute this module first, to build
and fill in the database 'pur_beurre_db'.
Pre-requisite: the database 'pur_beurre_db' has to be created.
"""


import os, re

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pur_beurre.settings")
django.setup()

import requests

from off_sub.models import Category, Product, Store


def main():
    """
    This function is the main function to be executed
    to build and fill in the database.
    """
    print("Installation en cours, veuillez patienter SVP...")
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
            api_return = categ_250.json() # type is dict
            products_list = api_return["products"] # type is list of dict
            # iterate on each product
            for item in products_list: # type is dict
                # initiate a new instance of product
                prod = Product()
                # filter on:
                # - products containing "France" in the list of countries
                # - products with 'nutrition_grade_fr' and 'code' completed
                regexp = "(.*)[Ff]rance(.*)"
                if (re.match(regexp, item["countries"]) is not None) \
                        and ("code" in item.keys()) \
                        and ("nutrition_grade_fr" in item.keys()):
                    # set the product attributes
                    prod.code = item["code"]
                    try:
                        prod.product_name = item["product_name"]
                    except KeyError:
                        prod.product_name = "[Produit sans nom]"    
                    prod.nutriscore_grade = item["nutrition_grade_fr"]
                    prod.nutriscore_score = \
                        int(item["nutriments"]["nutrition-score-fr_100g"])
                    try:
                        prod.url = item["url"]
                    except KeyError:
                        prod.url = ""
                    try:
                        prod.image_url = item["image_url"]
                    except KeyError:
                        prod.image_url = ""
                    # extract some key nutriments data as fat, sugars and salt
                    extract_nutriments_data(item, prod)
                    # add the product to the database, if necessary
                    prod_id = prod.add_product_to_db()
                    # cover the case where the product already exists
                    prod = Product.objects.get(id=prod_id)
                    # update the database (table ProductCategory), if necessary
                    prod.add_product_category_to_db(categ)
                    # if applicable, link the stores and the product
                    shop_names = []
                    try:
                        shop_names = [
                            shop.strip() for shop in item["stores"].split(",")
                        ]
                    except KeyError: # if no store mentioned here...
                        # ... then skip this step
                        continue
                    for shop_name in shop_names:
                        # create a new instance of store
                        shop = Store.objects.get_or_create(name=shop_name)[0]
                        # add the store to the database, if necessary
                        shop.add_store_to_db()
                        # update the database (table ProductStore)
                        prod.add_product_store_to_db(shop)
    print("Installation terminée !")


def extract_nutriments_data(item, prod):
    """
    This sub-function extracts some nutriments data from Open Food Facts.
    """
    try:
        prod.fat = str(item["nutriments"]["fat"]) + \
                        max(item["nutriments"]["fat_unit"], "g")
    except KeyError:
        prod.fat = "donnée inconnue"
    try:
        prod.saturated_fat = str(item["nutriments"]["saturated-fat"]) + \
                        max(item["nutriments"]["saturated-fat_unit"], "g")
    except KeyError:
        prod.saturated_fat = "donnée inconnue"
    try:
        prod.sugars = str(item["nutriments"]["sugars"]) + \
                        max(item["nutriments"]["sugars_unit"], "g")
    except KeyError:
        prod.sugars = "donnée inconnue"
    try:
        prod.salt = str({item["nutriments"]["salt"]}) + \
                        max(item["nutriments"]["salt_unit"], "g")
    except KeyError:
        prod.salt = "donnée inconnue"


if __name__ == "__main__":
    main()
