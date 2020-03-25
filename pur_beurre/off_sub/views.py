from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import json
# from django.views.generic import ListView, TemplateView, DetailView

from auth.views import sign
from .models import Product, Category


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
        data ['product_id'] = product.id
    return JsonResponse(data)


def ajax_save_product(request):
    """
    This view is used to save a product as a user's favorite.
    This is not linked to a template.
    """
    pass

def ajax_unsave_product(request):
    """
    This view is used to unsave a product from the user's favorites.
    This is not linked to a template.
    """
    pass

@login_required
def favorites(request):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    context['user_authenticated'] = request.user.is_authenticated # bool
    context['user_favorites'] = request.user.favorites.all() # QuerySet
    return render(
        request, 
        'off_sub/favorites.html',
        context,
    )

def food(request, product_id):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    context['user_authenticated'] = request.user.is_authenticated # bool
    product = get_object_or_404(Product, id=product_id)
    context['product'] = product
    return render(
        request, 
        'off_sub/food.html',
        context,
    )

def index(request):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    context['user_authenticated'] = request.user.is_authenticated # bool
    return render(
        request, 
        'off_sub/index.html',
        context,
    )

def legal(request):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    context['user_authenticated'] = request.user.is_authenticated # bool
    return render(
        request, 
        'off_sub/legal.html',
        context,
    )

def results(request, product_id):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    context['user_authenticated'] = request.user.is_authenticated # bool
    if context['user_authenticated']:
        context['user_favorites'] = request.user.favorites.all() # QuerySet
    product = Product.objects.get(id=product_id)
    # number of substitutes: 6
    subs = product.get_best_subs(6)
    context['products_list'] = subs # type is queryset
    context['initial_product'] = product
    return render(
        request, 
        'off_sub/results.html',
        context,
    )
