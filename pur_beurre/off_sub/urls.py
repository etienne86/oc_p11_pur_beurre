from django.urls import path

from pur_beurre.off_sub import ajax_views, views


app_name = 'off_sub'
urlpatterns = [
    path('', views.index, name="index"),
    path('favorites/', views.favorites, name="favorites"),
    path('food/<product_id>', views.food, name="food"),
    path('legal/', views.legal, name="legal"),
    path('results/<product_id>', views.results, name="results"),
    path('results_/<product_id>', views.results_login, name="results_login"),

    path(
        'ajax_find_product',
        ajax_views.ajax_find_product,
        name="ajax_find_product"
    ),
    path(
        'ajax_save_product',
        ajax_views.ajax_save_product,
        name="ajax_save_product"
    ),
    path(
        'ajax_unsave_product',
        ajax_views.ajax_unsave_product,
        name="ajax_unsave_product"
    ),
]
