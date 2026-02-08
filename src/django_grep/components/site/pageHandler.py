"""
Page Components & Smart Views
=============================
Production-ready component views with integrated:
- Template context management
- Fragment handling
- HTMX/SSE support
- Notification system
"""

from typing import Any, List

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core import logger

from .context import *
from .notifications import *
from .paginators import *
from .plugins import *
from .response import *


class ComponentViews(FragmentHandlerMixin, TemplateView):
    """
    Smart Component View with integrated features:
    - Template rendering with context
    - Fragment handling for HTMX/UnPoly
    - HTMX response support
    - Notification system
    - Error handling
    """

    # Configuration
    component_name: str | None = None
    require_auth: bool = False
    login_url: str | None = None
    cache_timeout: int = 0

    def setup(self, request: HttpRequest, *args, **kwargs):
        """Initialize view with request."""
        super().setup(request, *args, **kwargs)

        # Set request on instance
        self.request = request

        # Determine rendering strategy
        self.strategy = self.resolve_strategy(request)

        # Set template name based on strategy
        self.template_name = self.resolve_template_name()

        # Check authentication if required
        if self.require_auth and not request.user.is_authenticated:
            self.handle_unauthenticated()

    def handle_unauthenticated(self):
        """Handle unauthenticated access."""
        if hasattr(self.request, "htmx") and self.request.htmx:
            # HTMX response for unauthenticated
            from django.http import HttpResponse

            response = HttpResponse(status=401)
            response["HX-Redirect"] = self.login_url or "/login/"
            return response
        else:
            # Traditional redirect
            return redirect(self.login_url or "/login/")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle GET requests with strategy-based rendering."""
        try:
            # Build context
            context = self.get_context_data(request=request, *args, **kwargs)

            # Add notifications to context
            if hasattr(self, "get_notifications"):
                context["notifications"] = self.get_notifications(request)

            # Strategy-based rendering
            if self.strategy == "fragment":
                return self.render_fragment(request, context, title=self.page_title)
            else:
                return self.render_layout(context)

        except Exception as e:
            logger.error(f"[SmartComponent] GET failed: {e}")
            return self.handle_error(request, e)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle POST requests with HTMX/SSE support."""
        try:
            # Process form/data
            result = self.process_post(request, *args, **kwargs)

            # If result is a response, return it
            if isinstance(result, HttpResponse):
                return result

            # Default success handling
            return self.handle_success(request, result)

        except Exception as e:
            logger.error(f"[SmartComponent] POST failed: {e}")
            return self.handle_error(request, e)

    def process_post(self, request: HttpRequest, *args, **kwargs) -> Any:
        """Process POST data. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement process_post")

    def handle_success(self, request: HttpRequest, result: Any) -> HttpResponse:
        """Handle successful POST processing."""
        # Try to get redirect URL from result
        redirect_url = getattr(result, "get_absolute_url", None)
        if callable(redirect_url):
            redirect_url = redirect_url()

        # Determine response type
        if hasattr(request, "htmx") and request.htmx:
            # HTMX response
            if redirect_url:
                return HttpResponseClientRedirect(redirect_url)
            else:
                # Refresh the current view
                response = self.get(request)
                response["HX-Trigger"] = json.dumps({"refresh": True})
                return response
        else:
            # Traditional response
            if redirect_url:
                return redirect(redirect_url)
            else:
                # Re-render GET
                return self.get(request)

    def handle_error(self, request: HttpRequest, error: Exception) -> HttpResponse:
        """Handle errors gracefully."""
        error_message = str(error)

        # Send notification
        notification_response = self.add_error(f"Error: {error_message}", request=request)

        if notification_response:
            return notification_response

        # Fallback error response
        if hasattr(request, "htmx") and request.htmx:
            return JsonResponse({"error": error_message, "status": "error"}, status=400)
        else:
            # Re-render with error in context
            context = self.get_context_data(request=request)
            context["error"] = error_message
            return self.render_layout(context)

    def render_to_response(self, context: dict[str, Any], **response_kwargs):
        """Override to add HTMX headers if needed."""
        response = super().render_to_response(context, **response_kwargs)

        # Add HTMX headers for fragment responses
        if self.strategy == "fragment" and hasattr(self.request, "htmx"):
            # Don't swap entire page for fragments
            response["HX-Reswap"] = "innerHTML"

            # Set retarget if needed
            if hasattr(self, "fragment_target"):
                response["HX-Retarget"] = self.fragment_target

        return response


class PageHandler(NotificationMixin, ComponentViews):
    """
    Page-level component for full page rendering.
    Extends SmartComponentView with page-specific features.
    """

    show_breadcrumbs = False
    show_sidebar = False
    full_width = False

    def get_context_data(self, **kwargs):
        """Add page-specific context."""
        context = super().get_context_data(**kwargs)

        # Page layout context
        context.update(
            {
                "show_breadcrumbs": self.show_breadcrumbs,
                "show_sidebar": self.show_sidebar,
                "full_width": self.full_width,
                "current_page": self.__class__.page_title,
            }
        )

        # Add breadcrumbs if enabled
        if self.show_breadcrumbs:
            context["breadcrumbs"] = self.get_breadcrumbs()

        return context

    def get_breadcrumbs(self) -> List[dict[str, str]]:
        """Get breadcrumb trail for current page."""
        return [
            {"title": "Home", "url": "/"},
            {"title": self.page_title, "url": self.request.path, "active": True},
        ]

    def get_sidebar_context(self) -> dict[str, Any]:
        """Get sidebar data. Override in subclasses."""
        return {}


class ModalComponent(ComponentViews):
    """
    Component for modal dialogs.
    Renders as fragment with modal wrapper.
    """

    fragment_template = "base_modal.html"
    modal_size = "md"  # sm, md, lg, xl
    modal_title = ""
    close_button = True
    backdrop = True

    def get_context_data(self, **kwargs):
        """Add modal-specific context."""
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "modal_size": self.modal_size,
                "modal_title": self.modal_title or self.page_title,
                "close_button": self.close_button,
                "backdrop": self.backdrop,
                "is_modal": True,
            }
        )

        return context


class PaginatedComponentView(HTMXPaginationMixin, ComponentViews):
    """
    Smart component view with built-in pagination.

    Features:
    - Automatic pagination setup
    - HTMX pagination support
    - Multiple pagination styles
    - Integration with component system
    """

    # Pagination configuration
    pagination_template: str = "components/pagination/default.html"
    items_template: str = "components/items/list.html"

    # Fragment configuration
    fragment_name: str | None = None
    items_fragment_selector: str = "#items-container"
    pagination_fragment_selector: str = "#pagination-container"

    def setup(self, request: HttpRequest, *args, **kwargs):
        """Initialize view with pagination."""
        super().setup(request, *args, **kwargs)

        # Set up pagination based on request
        self.setup_pagination(request)

    def setup_pagination(self, request: HttpRequest):
        """Configure pagination based on request parameters."""
        # Detect pagination style from request
        if request.GET.get("pagination_style"):
            self.pagination_style = request.GET.get("pagination_style")

        # Detect HTMX triggers
        if hasattr(request, "htmx") and request.htmx:
            if request.headers.get("HX-Trigger") == "load-more":
                self.pagination_style = "load_more"
                self.load_more_enabled = True
            elif request.headers.get("HX-Trigger") == "infinite-scroll":
                self.pagination_style = "infinite"
                self.infinite_scroll_enabled = True

    def get_queryset(self) -> list:
        """Get queryset for pagination."""
        # Override in subclasses
        return super().get_queryset()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get context with pagination data."""
        context = super().get_context_data(**kwargs)

        # Add pagination context
        context = self.get_paginated_context_with_htmx(self.request, context)

        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle GET requests with pagination."""
        # Check for HTMX pagination request
        htmx_response = self.get_htmx_response(request, {})
        if htmx_response:
            return htmx_response

        # Regular request handling
        context = self.get_context_data(**kwargs)

        # Render based on strategy
        if self.strategy == "fragment":
            return self.render_fragment(request, context)
        else:
            return self.render_layout(context)

    def render_items_fragment(self, context: dict[str, Any]) -> str:
        """Render items fragment for HTMX responses."""
        try:
            return render_to_string(self.items_template, context)
        except Exception as e:
            logger.error(f"Failed to render items fragment: {e}")
            return ""

    def serialize_items(self, items: List[Any]) -> List[dict[str, Any]]:
        """Serialize items for JSON responses."""
        # Default implementation - override in subclasses
        return [
            {"id": getattr(item, "id", idx), "repr": str(item)} for idx, item in enumerate(items)
        ]

    def get_pagination_urls(self) -> dict[str, str]:
        """Get pagination URLs for template."""
        if not hasattr(self, "request"):
            return {}

        base_url = self.request.path
        page = self.get_page_number(self.request)

        urls = {
            "first": f"{base_url}?{self.page_kwarg}=1",
            "last": f"{base_url}?{self.page_kwarg}={self.paginator.num_pages}",
        }

        if page > 1:
            urls["prev"] = f"{base_url}?{self.page_kwarg}={page - 1}"

        if page < self.paginator.num_pages:
            urls["next"] = f"{base_url}?{self.page_kwarg}={page + 1}"

        return urls


class PaginatedListView(PaginatedComponentView):
    """
    List view with pagination for displaying querysets.
    """

    # Template configuration
    template_name: str = "components/paginated_list.html"
    fragment_name: str = "components.paginated_list"

    # Model configuration (optional)
    model = None
    ordering: str | None = None

    def get_queryset(self):
        """Get queryset for the list."""
        if self.model:
            queryset = self.model.objects.all()

            # Apply ordering
            if self.ordering:
                queryset = queryset.order_by(self.ordering)

            return queryset

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Add model-specific context."""
        context = super().get_context_data(**kwargs)

        if self.model:
            context["model_name"] = self.model._meta.verbose_name_plural

        return context
