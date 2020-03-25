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
    path('results/<product_id>', views.results, name="results"),
    path(
        'ajax_find_product',
        views.ajax_find_product,
        name="ajax_find_product"
    ),
    path(
        'ajax_save_product',
        views.ajax_save_product,
        name="ajax_save_product"
    ),
    path(
        'ajax_unsave_product',
        views.ajax_unsave_product,
        name="ajax_unsave_product"
    ),
]
