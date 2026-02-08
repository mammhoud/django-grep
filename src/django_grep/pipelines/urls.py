from __future__ import annotations

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.i18n import set_language
from django.views.static import serve
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import index, sitemap
from wagtail.documents import urls as wagtaildocs_urls

from django_grep.pipelines.site import *

from .apps import PipelinesConfig

app_name = PipelinesConfig.label

urlpatterns = [
    path("auth/sign-in/", view=LoginView.as_view(), name="login"),
    path("auth/sign-up/", view=RegisterView.as_view(), name="register"),
    path("auth/sign-out/", view=LogoutView.as_view(), name="logout"),
    path(
        "auth/reset-password/", view=ResetPasswordView.as_view(), name="password_reset"
    ),  # getting by email
    path(
        "auth/forgot-password/", view=ForgotPasswordView.as_view(), name="password_forgot"
    ),  # search with email
    path("auth/verify-email/", view=VerifyEmailView.as_view(), name="verify-email-page"),  #
    path("notifications/", NotificationView.as_view(), name="notifications"),
]
