from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import json
# from django.views.generic import ListView, TemplateView, DetailView

from .forms import UserCreationForm, AuthenticationForm
from .models import MyUser
from off_sub.models import Product


@login_required
def account(request):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    context['user_authenticated'] = request.user.is_authenticated # bool
    context['user'] = request.user
    return render(
        request, 
        'auth/account.html',
        context,
    )

@login_required
def log_out(request):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    logout(request)
    return render(
        request, 
        'auth/log_out.html',
        context,
    )

def sign(request):
    prod_list = list(Product.objects.all())
    context = {'all_products': json.dumps([str(prod) for prod in prod_list])}
    context['user_authenticated'] = request.user.is_authenticated # bool
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        authentication_form = AuthenticationForm(request, request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            first_name = user_creation_form.cleaned_data['first_name']
            email = user_creation_form.cleaned_data['email']
            password = user_creation_form.cleaned_data['password1']
        if authentication_form.is_valid():
            email = authentication_form.cleaned_data['email']
            password = authentication_form.cleaned_data['password']
        print(authentication_form.errors)
        if user_creation_form.is_valid() or authentication_form.is_valid():
            # try to log in the user
            try:
                with transaction.atomic():
                    user = MyUser.objects.get(email=email)
                    account = authenticate(
                        email=email,
                        password=password
                    )
                    if account is not None:
                        # log in the user
                        login(request, account)
            except IntegrityError:
                pass
            # redirect to home page
            return redirect('/')
    else: # GET request
        user_creation_form = UserCreationForm()
        authentication_form = AuthenticationForm()
    context['user_creation_form'] = user_creation_form
    context['authentication_form'] = authentication_form
    return render(
        request, 
        'auth/sign.html',
        context
    )
