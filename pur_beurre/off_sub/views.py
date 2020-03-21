from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# from django.views.generic import ListView, TemplateView, DetailView

from auth.views import authenticated, sign
from .models import Product, Category

# @login_required(login_url=reverse_lazy(sign))
@login_required
def favorites(request):
    context = authenticated(request)
    return render(
        request, 
        'off_sub/favorites.html',
        context,
    )

def food(request, product_id):
    context = authenticated(request)
    product = get_object_or_404(Product, id=product_id)
    context['product'] = product
    return render(
        request, 
        'off_sub/food.html',
        context,
    )

def index(request):
    context = authenticated(request)
    prod_list = list(Product.objects.all())
    context['all_products'] = [
        f"{prod.code} - {prod.product_name}" for prod in prod_list
    ]
    return render(
        request, 
        'off_sub/index.html',
        context,
    )

def legal(request):
    context = authenticated(request)
    return render(
        request, 
        'off_sub/legal.html',
        context,
    )

def results(request):
    context = authenticated(request)
    product = Product.objects.get(id=489)
    # number of substitutes: 6
    subs = product.get_best_subs(6)
    context['products_list'] = subs # type is queryset
    context['initial_product'] = product
    return render(
        request, 
        'off_sub/results.html',
        context,
    )
