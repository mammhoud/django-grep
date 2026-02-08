"""
📦 Django + Wagtail Template Tags
=================================

Provides utilities for:
- 🌐 Site and page navigation (site roots, menus, breadcrumbs)
- 🧩 Form rendering via ComponentsFormRenderer
- 🔁 Viewset-based URL reversing
- 🎨 Theme variable injection (light/dark)
- 🧭 Wagtail layout utilities

Usage in templates:
-------------------
    {% load core_tags %}
    {% get_site_root as site_root %}
    {% top_menu site_root %}
    {% render_component_form form %}
    {% viewset_url my_viewset 'detail' pk=obj.pk %}
    {% get_theme_variables 'light' %}
"""

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

# ---------------------------------------------------------------------
# 🌍 Site & Navigation Tags
# ---------------------------------------------------------------------
@register.simple_tag(takes_context=True)
def get_site_root(context: Context) -> Page | None:
    """
    Get the Wagtail root page for the current request.
    Works with or without Wagtail SiteMiddleware.
    """
    try:
        request = context.get("request")

        if not request:
            # Try to get from context directly if no request
            return context.get("site_root")

        # Method 1: Try to get site from request
        if hasattr(request, "site"):
            site = request.site
            if site and hasattr(site, "root_page"):
                return site.root_page

        # Method 2: Use Site.find_for_request
        try:
            site = Site.find_for_request(request)
            return site.root_page if site else None
        except (Site.DoesNotExist, AttributeError):
            pass

        # Method 3: Try to get from cached context
        return context.get("site_root")

    except Exception:
        return None


@register.simple_tag
def has_children(page: Page) -> bool:
    """Check if a Wagtail page has live children."""
    return page.get_children().live().exists()


@register.simple_tag
def is_active(page: Page, current_page: Page | None) -> bool:
    """Determine whether a page is active (for menu highlighting)."""
    return current_page.url_path.startswith(page.url_path) if current_page else False

@register.inclusion_tag("landing/partials/navigations.html", takes_context=True)
def top_menu(
    context: Context,
    parent=None,
    calling_page: Page | None = None,
    max_depth: int = 1,
    show_root: bool = False
):
    """
    Render a top navigation menu from Wagtail live children.
    
    Args:
        parent: The parent page to get children from. If None, uses site root.
        calling_page: The current page for highlighting active items.
        max_depth: How many levels of navigation to show (1 = immediate children only).
        show_root: Whether to include the root page in the menu.
    """
    request = context.get("request")

    # Get the appropriate parent page
    if not parent:
        try:
            site = Site.find_for_request(request)
            parent = site.root_page if site else None
        except Exception:
            parent = None

    if not parent:
        # No parent page found
        return {
            "calling_page": calling_page,
            "menuitems": [],
            "request": request,
        }

    # Start with either root or its children
    if show_root:
        # Include the root page itself
        menuitems = [parent]
        # Add immediate children
        children = parent.get_children().live().in_menu()
        menuitems.extend(children)
    else:
        # Only show children of the root
        menuitems = parent.get_children().live().in_menu()

    # Mark active items
    for item in menuitems:
        if calling_page:
            # Multiple ways to determine active state
            item.active = (
                calling_page.url_path.startswith(item.url_path) or
                calling_page.id == item.id or
                (hasattr(item, 'specific') and
                 calling_page.id == getattr(item.specific, 'id', None))
            )
        else:
            item.active = False

    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        "request": request,
        "parent_page": parent,
    }

# ---------------------------------------------------------------------
# 🧩 Form Rendering
# ---------------------------------------------------------------------

# @register.simple_tag
# def render_component_form(form: Form, layout: Optional[Any] = None) -> str:
#     """
#     Render a Django form using the ComponentsFormRenderer or a custom layout.

#     Usage:
#         {% render_component_form form %}
#         {% render_component_form form custom_layout %}
#     """
#     try:
#         if layout:
#             return layout.render(form)
#         return form.render(
#             renderer=ComponentsFormRenderer(),
#             template_name="components/django/forms/div.html"
#         )
#     except Exception as e:
#         logger.warning(f"[render_component_form] Error rendering form: {e}")
#         return ""

# ---------------------------------------------------------------------
# 🔁 Viewset-Based URL Utilities
# ---------------------------------------------------------------------

@register.simple_tag(takes_context=True)
def viewset_url(context: Context, viewset: Viewset, view_name: str, *args, **kwargs) -> str:
    """
    Reverse a URL from a registered viewset.

    Usage:
        {% viewset_url viewset 'detail' pk=object.id %}
    """
    if not viewset:
        return ""

    if not isinstance(viewset, Viewset):
        raise template.TemplateSyntaxError(
            f"viewset_url: expected Viewset instance, got '{type(viewset)}'"
        )

    try:
        current_app = getattr(context.request, "current_app", None) or \
                      getattr(context.request.resolver_match, "namespace", None)
    except Exception:
        current_app = None

    try:
        return viewset.reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)
    except NoReverseMatch:
        return ""

# ---------------------------------------------------------------------
# 🌐 Request URL Helpers
# ---------------------------------------------------------------------

@register.simple_tag
def absolute_request_url(request: HttpRequest) -> str:
    """Return the absolute URI of the current request."""
    return request.build_absolute_uri()

# ---------------------------------------------------------------------
# 🎨 Theme System Tags
# ---------------------------------------------------------------------

@register.simple_tag
def get_theme_variables(scope: str) -> str:
    """
    Retrieve theme CSS variables for a given scope ('light' or 'dark').
    """
    try:
        with suppress(ImportError):
            from core.setup.theme.settings import LayoutHelper  # type: ignore

        theme_vars = LayoutHelper.get_theme_variables(scope)
        return mark_safe(theme_vars) if theme_vars else ""
    except Exception as e:
        logger.warning(f"[get_theme_variables] Error: {e}")
        return ""



@register.inclusion_tag("layout/front/includes/breadcrumbs.html", takes_context=True)
def wagtail_breadcrumbs(context: Context):
    """
    Render Wagtail breadcrumbs with a front-end layout template.
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



@register.filter
def multiply(value, arg):
    """Multiply the value by the arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Add the arg to the value"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return value
