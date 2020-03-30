from .admin import (
    AuthenticationForm as CustomAuthenticationForm,
    UserCreationForm as CustomUserCreationForm,
)


class UserCreationForm(CustomUserCreationForm):
    pass


class AuthenticationForm(CustomAuthenticationForm):
    pass
