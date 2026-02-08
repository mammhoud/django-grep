from contextlib import suppress
from typing import Any, Optional

from django import template
from django.forms import Form
from django.http import HttpRequest
from django.template.context import Context
from django.urls import NoReverseMatch
from django.utils.safestring import mark_safe
from wagtail.models import Page, Site

from core import logger

# from django_grep.components.forms import ComponentsFormRenderer
from django_grep.pipelines.routes.base import Viewset

register = template.Library()


@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context: Context):
    """
    Render breadcrumbs for current Wagtail page.
    """
    self = context.get("self")
    if not self or self.depth <= 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }
