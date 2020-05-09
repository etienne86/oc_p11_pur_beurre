from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import forms, views


app_name = 'auth'
urlpatterns = [
    path('account/', views.account, name="account"),
    path(
        'change_password/',
        auth_views.PasswordChangeView.as_view(
            template_name='auth/change_password.html',
            success_url='done',
            form_class=forms.PasswordChangeForm,
        ),
        name="change_password"
    ),
    path(
        'change_password/done/',
        auth_views.TemplateView.as_view(
            template_name='auth/password_changed.html',
        ),
        name="change_password_done"
    ),
    path('log_out/', views.log_out, name="log_out"),
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/reset_password/password_reset_form.html',
            form_class=forms.PasswordResetForm,
            subject_template_name='auth/reset_password/password_reset_subject.txt',
            email_template_name='auth/reset_password/password_reset_email.html',
            success_url='done',
        ),
        name="reset_password"
    ),
    path(
        'reset_password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth/reset_password/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset_password_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/reset_password/password_reset_confirm.html',
            form_class=forms.SetPasswordForm,
            success_url=reverse_lazy('auth:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/reset_password/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('sign/', views.sign, name="sign"),
]
