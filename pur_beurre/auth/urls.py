from django.urls import path

from . import views


app_name = 'auth'
urlpatterns = [
    path('account/', views.account, name="account"),
    path('sign/', views.sign, name="sign"),
    path('log_out/', views.log_out, name="log_out"),
]
