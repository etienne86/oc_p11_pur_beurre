from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# from django.views.generic import ListView, TemplateView, DetailView

from auth.views import authenticated, sign

# @login_required(login_url=reverse_lazy(sign))
@login_required
def favorites(request):
    context = authenticated(request)
    return render(
        request, 
        'off_sub/favorites.html',
        context,
    )

def food(request):
    context = authenticated(request)
    return render(
        request, 
        'off_sub/food.html',
        context,
    )

def index(request):
    context = authenticated(request)
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
    return render(
        request, 
        'off_sub/results.html',
        context,
    )
