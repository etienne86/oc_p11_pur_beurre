from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
# from django.views.generic import ListView, TemplateView, DetailView


def account(request):
    return render(
        request, 
        'off_sub/account.html', 
    )

def favorites(request):
    return render(
        request, 
        'off_sub/favorites.html', 
    )

def food(request):
    return render(
        request, 
        'off_sub/food.html', 
    )

def index(request):
    return render(
        request, 
        'off_sub/index.html', 
    )

def legal(request):
    return render(
        request, 
        'off_sub/legal.html', 
    )

def results(request):
    return render(
        request, 
        'off_sub/results.html', 
    )

def sign(request):
    return render(
        request, 
        'off_sub/sign.html', 
    )

def sign_in(request):
    return render(
        request, 
        'off_sub/sign_in.html', 
    )

def sign_up(request):
    return render(
        request, 
        'off_sub/sign_up.html', 
    )