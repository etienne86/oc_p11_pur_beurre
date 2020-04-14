from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from .models import Product


@login_required
def favorites(request):
    context = {}
    context['user_favorites'] = request.user.favorites.all()  # QuerySet
    context['products_list'] = context['user_favorites']
    current_url = request.get_full_path().strip(
        Site.objects.get_current().domain
    )
    context['current_url'] = current_url
    return render(
        request,
        'off_sub/favorites.html',
        context,
    )


def food(request, product_id):
    context = {}
    product = get_object_or_404(Product, id=product_id)
    context['product'] = product
    try:
        previous_url = request.get_full_path().split("?next=")[1]
    except IndexError:
        previous_url = request.get_full_path().strip(
            Site.objects.get_current().domain
        )
    context['previous_url'] = previous_url
    return render(
        request,
        'off_sub/food.html',
        context,
    )


def index(request):
    context = {}
    return render(
        request,
        'off_sub/index.html',
        context,
    )


def legal(request):
    context = {}
    return render(
        request,
        'off_sub/legal.html',
        context,
    )


def results(request, product_id):
    context = {}
    if request.user.is_authenticated:
        context['user_favorites'] = request.user.favorites.all()  # QuerySet
    product = get_object_or_404(Product, id=product_id)
    # number of suggested substitutes: 6
    subs = product.get_best_subs(6)
    context['products_list'] = subs  # QuerySet
    context['initial_product'] = product
    current_url = request.get_full_path().strip(
        Site.objects.get_current().domain
    )
    context['current_url'] = current_url
    return render(
        request,
        'off_sub/results.html',
        context,
    )


@login_required
def results_login(request, product_id):
    return results(request, product_id)
