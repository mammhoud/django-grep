"""
Authentication forms module exports with  styling support.
"""

# Code request forms
from .code import (
    RequestLoginCodeForm,
    VerifyCodeForm,
)

# Code confirmation forms
from .confirm import (
    BaseConfirmCodeForm,
    ConfirmEmailVerificationCodeForm,
    ConfirmLoginCodeForm,
    ConfirmPasswordResetCodeForm,
)

# Authentication forms
from .login import LoginForm

# Password forms
from .password import (
    ChangePasswordForm,
    PasswordField,
    PasswordVerificationMixin,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordField,
    SetPasswordForm,
)

# Phone forms
from .phone import (
    ChangePhoneForm,
    PhoneVerificationRequestForm,
    VerifyPhoneForm,
)
from .signup import SignupForm

__all__ = [
    # Authentication
    'LoginForm',
    'SignupForm',
    
    # Password forms
    'ChangePasswordForm',
    'SetPasswordForm',
    'ResetPasswordForm',
    'ResetPasswordKeyForm',
    'PasswordField',
    'SetPasswordField',
    'PasswordVerificationMixin',
    
    # Code confirmation
    'BaseConfirmCodeForm',
    'ConfirmLoginCodeForm',
    'ConfirmEmailVerificationCodeForm',
    'ConfirmPasswordResetCodeForm',
    
    # Code request
    'RequestLoginCodeForm',
    'VerifyCodeForm',
    
    # Phone forms
    'VerifyPhoneForm',
    'ChangePhoneForm',
    'PhoneVerificationRequestForm',
    
]
