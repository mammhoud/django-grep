import json
import time
from typing import Dict

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from apps import logger
from django_grep.components.site import PageHandler

from .mixins import *

User = get_user_model()


class LoginView(AuthPageBase):
    """Login page component."""
    
    page_title = "Login"
    page_icon = "bi-box-arrow-in-right"  # Bootstrap icon class
    fragment_name = "auth.login"

    def get(self, request, *args, **kwargs):
        """Handle GET request for login page."""
        # Redirect if already authenticated
        if request.user.is_authenticated:
            return self.handle_already_authenticated(request)
        
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Handle POST request for login."""
        # Redirect if already authenticated
        if request.user.is_authenticated:
            return self.handle_already_authenticated(request)
        
        # Process login
        return self.process_login(request)
    
    def get_context_data(self, **kwargs):
        """Add login-specific context."""
        context = super().get_context_data(**kwargs)
        
        # # Form field values for re-population
        # context.update({
        #     'identifier': request.POST.get('email-username', ''),
        #     'remember_me': request.POST.get('remember_me') == 'off',
        # })
        
        return context



class LogoutView(AuthPageBase):
    """Logout page component."""
    
    page_title = "Logout"
    page_icon = "bi-box-arrow-right"  # Bootstrap icon class
    template_name = "auth/logout.html"
    fragment_name = "auth.logout"
    
    def get(self, request, *args, **kwargs):
        """Handle GET request for logout."""
        return self.process_logout(request)
    
    def post(self, request, *args, **kwargs):
        """Handle POST request for logout."""
        return self.process_logout(request)

