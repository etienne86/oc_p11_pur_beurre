from .admin import (
    AuthenticationForm as CustomAuthenticationForm,
    PasswordChangeForm as CustomPasswordChangeForm,
    PasswordResetForm as CustomResetChangeForm,
    SetPasswordForm as CustomSetPasswordForm,
    UserCreationForm as CustomUserCreationForm,
)


class AuthenticationForm(CustomAuthenticationForm):
    pass


class PasswordChangeForm(CustomPasswordChangeForm):
    pass


class PasswordResetForm(CustomResetChangeForm):
    pass


class SetPasswordForm(CustomSetPasswordForm):
    pass


class UserCreationForm(CustomUserCreationForm):
    pass
