from django.urls import path
from django.conf.urls import url, include
# from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('account/', views.account, name="account"), ### wrong app
    path('favorites/', views.favorites, name="favorites"),
    path('food/', views.food, name="food"),
    path('legal/', views.legal, name="legal"),
    path('results/', views.results, name="results"),
    path('sign/', views.sign, name="sign"), ### wrong app
]
