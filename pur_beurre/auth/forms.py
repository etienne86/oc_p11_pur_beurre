from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm
)

from .admin import (
    AuthenticationForm as CustomAuthenticationForm,
    UserCreationForm as CustomUserCreationForm,
)
from .models import MyUser


class UserCreationForm(CustomUserCreationForm):
    pass

class AuthenticationForm(CustomAuthenticationForm):
    pass
