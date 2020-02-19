"""
Please execute this module first, to build
and fill in the database 'pur_beurre_db'.
Pre-requisite: the database 'pur_beurre_db' has to be created.
"""


import re

import django
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
        categ = Category.objects.create(name=categ_name)
        # add the category to the database
        categ.add_category_to_db()
        # execute the HTTP request to get products with API
        categ_1k = requests.get(categ.get_url_1k_products())
        categ_1k_dict = categ_1k.json()
        if (categ_1k.status_code == 200) and (categ_1k_dict["count"]):
            api_return = categ_1k.json() # type is dict
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
                    prod.product_name = item["product_name"]
                    prod.nutriscore_grade = item["nutrition_grade_fr"]
                    prod.nutriscore_score = \
                        int(item["nutriments"]["nutrition-score-fr_100g"])
                    prod.url = item["url"]
                    prod.image_url = item["image_url"]
                    # add the product to the database, if necessary
                    prod.add_product_to_db()
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
                        shop = Store(name=shop_name)
                        # add the store to the database, if necessary
                        shop.add_store_to_db()
                        # update the database (table ProductStore)
                        prod.add_product_store_to_db(shop)
    print("Installation terminée !")

if __name__ == "__main__":
    main()
