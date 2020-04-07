"""
This module defines some functions called in the apps.
"""

import json

from pur_beurre.off_sub.models import Product


def get_all_products():
    """
    Return all products in a dict, usable in the apps views as context.
    """
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    return context
