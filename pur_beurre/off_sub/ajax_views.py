from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from pur_beurre.off_sub.models import Product


def ajax_find_product(request):
    """
    This view is used to find the producted searched by the user.
    This is not linked to a template.
    """
    data = {}
    # get data from Javascript
    if request.method == 'POST':
        product_string = request.POST.get('product_string', "")
        # extract product code
        product_code = product_string.split('-')[0][:-1]
        # find the product id
        product = get_object_or_404(Product, code=product_code)
        data['product_id'] = product.id
    return JsonResponse(data)


def ajax_save_product(request):
    """
    This view is used to save a product as a user's favorite.
    This is not linked to a template.
    """
    data = {}
    # get data from Javascript
    if request.method == 'POST':
        product_id = request.POST.get('product_id', 0)
        product = get_object_or_404(Product, id=product_id)
        # add the product to the list of favorites for the user
        request.user.favorites.add(product)
        data['product_id'] = product_id
    return JsonResponse(data)


def ajax_unsave_product(request):
    """
    This view is used to unsave a product from the user's favorites.
    This is not linked to a template.
    """
    data = {}
    # get data from Javascript
    if request.method == 'POST':
        product_id = request.POST.get('product_id', 0)
        product = get_object_or_404(Product, id=product_id)
        # add the product to the list of favorites for the user
        request.user.favorites.remove(product)
        data['product_id'] = product_id
    return JsonResponse(data)
