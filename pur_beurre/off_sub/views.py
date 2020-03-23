from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import json
# from django.views.generic import ListView, TemplateView, DetailView

from auth.views import sign
from .models import Product, Category


@login_required
def favorites(request):
    context = {}
    context['user_authenticated'] = request.user.is_authenticated # bool
    context['user_favorites'] = request.user.favorites.all() # QuerySet
    return render(
        request, 
        'off_sub/favorites.html',
        context,
    )

def food(request, product_id):
    context = {}
    context['user_authenticated'] = request.user.is_authenticated # bool
    product = get_object_or_404(Product, id=product_id)
    context['product'] = product
    return render(
        request, 
        'off_sub/food.html',
        context,
    )

def index(request):
    context = {}
    context['user_authenticated'] = request.user.is_authenticated # bool
    prod_list = list(Product.objects.all())
    context['all_products'] = json.dumps([str(prod) for prod in prod_list])
    return render(
        request, 
        'off_sub/index.html',
        context,
    )
    '"coucou c\'est moi c\'est pas moi"'

def legal(request):
    context = {}
    context['user_authenticated'] = request.user.is_authenticated # bool
    return render(
        request, 
        'off_sub/legal.html',
        context,
    )

def results(request):
    context = {}
    context['user_authenticated'] = request.user.is_authenticated # bool
    if context['user_authenticated']:
        context['user_favorites'] = request.user.favorites.all() # QuerySet
    product = Product.objects.get(id=50)
    # number of substitutes: 6
    subs = product.get_best_subs(6)
    context['products_list'] = subs # type is queryset
    context['initial_product'] = product
    return render(
        request, 
        'off_sub/results.html',
        context,
    )

def save_product(request):
    pass

def unsave_product(request):
    pass
