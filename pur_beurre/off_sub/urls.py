from django.urls import path
from django.conf.urls import url, include
# from django.views.generic import TemplateView

from . import views


app_name = 'off_sub'
urlpatterns = [
    path('', views.index, name="index"),
    path('favorites/', views.favorites, name="favorites"),
    path('food/<product_id>', views.food, name="food"),
    path('legal/', views.legal, name="legal"),
    path('results/', views.results, name="results"),
]
