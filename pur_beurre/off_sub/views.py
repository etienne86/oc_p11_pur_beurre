from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from pur_beurre.off_sub.models import Product
from pur_beurre.off_sub import functions as fct


@login_required
def favorites(request):
    # add all products to the context
    context = fct.get_all_products()
    context['user_authenticated'] = request.user.is_authenticated  # bool
    context['user_favorites'] = request.user.favorites.all()  # QuerySet
    context['products_list'] = context['user_favorites']
    return render(
        request,
        'off_sub/favorites.html',
        context,
    )


def food(request, product_id):
    # add all products to the context
    context = fct.get_all_products()
    context['user_authenticated'] = request.user.is_authenticated  # bool
    product = get_object_or_404(Product, id=product_id)
    context['product'] = product
    return render(
        request,
        'off_sub/food.html',
        context,
    )


def index(request):
    # add all products to the context
    context = fct.get_all_products()
    context['user_authenticated'] = request.user.is_authenticated  # bool
    return render(
        request,
        'off_sub/index.html',
        context,
    )


def legal(request):
    # add all products to the context
    context = fct.get_all_products()
    context['user_authenticated'] = request.user.is_authenticated  # bool
    return render(
        request,
        'off_sub/legal.html',
        context,
    )


def results(request, product_id):
    # add all products to the context
    context = fct.get_all_products()
    context['user_authenticated'] = request.user.is_authenticated  # bool
    if context['user_authenticated']:
        context['user_favorites'] = request.user.favorites.all()  # QuerySet
    product = get_object_or_404(Product, id=product_id)
    # number of suggested substitutes: 6
    subs = product.get_best_subs(6)
    context['products_list'] = subs  # QuerySet
    context['initial_product'] = product
    return render(
        request,
        'off_sub/results.html',
        context,
    )


@login_required
def results_login(request, product_id):
    return results(request, product_id)
