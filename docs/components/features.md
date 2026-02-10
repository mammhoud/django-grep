# Component System: Advanced Features

This document details the advanced features provided by the `django-grep` component system, including fragment rendering strategies and the notification mixin.

---

## 🧭 Render Strategy

`django-grep` provides a smart rendering strategy that automatically distinguishes between full document requests and partial updates (HTMX/UnPoly).

### Strategy Types
- **`document`**: Renders the full page layout (e.g., `landing/skeleton.html`). Used for first-time page loads.
- **`fragment`**: Renders only the component's internal template, skipping the global skeleton. Used for AJAX/HTMX request updates.

### Automatic Detection
The `PageHandler` and `FragmentHandlerMixin` automatically resolve the strategy based on the request headers (`HX-Request` or `X-Up-Target`).

### Force Resolution
You can manually override the strategy in your view or model:
```python
class MyPage(BasePage):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Force a specific strategy
        context["render_strategy"] = "fragment"
        return context
```

---

## 🔔 Unified Notification System

The `NotificationMixin` provides a unified interface for sending notifications across different request types.

### Initialization
Your views or models should inherit from `NotificationMixin`:
```python
from django_grep.components.site.pageHandler import PageHandler

class ContactPage(Page, PageHandler):
    # Already includes NotificationMixin via PageHandler
    pass
```

### Usage
```python
def post_success(self, request):
    # This works for traditional requests, HTMX, and SSE!
    self.notify(request, "Message sent successfully!", level="success")
```

### Delivery Modes
1.  **Traditional**: Injects messages into Django's `messages` framework.
2.  **HTMX**: Adds `HX-Trigger` headers to the response (e.g., `{"show_notification": {...}}`).
3.  **SSE (Server-Sent Events)**: Broadcats notifications through an active SSE stream if established.

### Customizing Events
You can customize the event name used for HTMX triggers:
```python
self.notify(request, "Task started", event_name="process_start")
```

---

## 🏗️ Structure Patterns

### The `PageHandler`
The `PageHandler` is the high-level entry point for full-page components. It combines:
- **`NotificationMixin`**: Unified feedback.
- **`ComponentViews`**: Logic for handling GET/POST within a component.
- **`BaseTemplateContextMixin`**: Smart context building.

Example of a minimal `PageHandler` implementation:
```python
class MyDashboard(PageHandler):
    template_name = "profile/dashboard.html"
    fragment_name = "profile.dashboard"

    def get_context_data(self, **kwargs):
        return {"stats": get_stats()}
```
