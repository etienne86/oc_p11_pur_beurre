"""
This module contains the context_processors (app 'off_sub').
"""

import json

from .models import Product


def pur_beurre_all_products(request):
    """
    Return a dict, usable in the apps views as context, with
    all products available in database.
    """
    prod_list = list(Product.objects.all())
    kwargs = {
        'all_products': json.dumps([str(prod) for prod in prod_list])
    }
    return kwargs


def pur_beurre_user_authenticated(request):
    """
    Return a dict, usable in the apps views as context, with
    a boolean indicating if the user is authenticated of not.
    """
    kwargs = {
        'user_authenticated': request.user.is_authenticated  # bool
    }
    return kwargs
