# Pipelines Wagtail Hooks Usage

This directory contains the Wagtail admin integration hooks for the django-grep pipelines.

## Classes & Hooks

### ManagementsSnippetGroup
- **File**: `wagtail_hooks.py`
- **Description**: Groups management-related models (Person, Settings) together in the Wagtail admin menu.
- **Menu Label**: Manage
- **Menu Icon**: suitcase

### register_icons
- **Type**: `@hooks.register("register_icons")`
- **Description**: Registers custom FontAwesome SVG icons for use in the Wagtail admin.

## Planned/Future Integrations

The following snippet views and hooks were previously commented out in `wagtail_hooks.py` and are preserved here for future reference:

### Additional Viewsets in ManagementsSnippetGroup
```python
# CompanyViewSet,
# ContactViewSet,
# TagViewSet,
# ServiceViewSet,
# NewsletterViewSet,
# EmailTemplateViewSet,
```

### Accessibility Customization
```python
# class CustomAccessibilityItem(AccessibilityItem):
#     """
#     Custom accessibility checker for Wagtail user bar.
#     Extends the default accessibility item with custom configuration.
#     """
#     axe_run_only = None


# @hooks.register("construct_wagtail_userbar")
# def replace_userbar_accessibility_item(request, items):
#     """
#     Replace the default accessibility item in Wagtail user bar with custom implementation.
#     """
#     items[:] = [
#         CustomAccessibilityItem() if isinstance(item, AccessibilityItem) else item
#         for item in items
#     ]
```

### Menu & Dashboard Customization
```python
# @hooks.register('construct_main_menu')
# def hide_explorer_menu_item(request, menu_items):
#     # Hide explorer menu for non-staff
#     if not request.user.is_staff:
#         menu_items[:] = [item for item in menu_items if item.name != 'explorer']
#     return menu_items

# @hooks.register('register_admin_menu_item')
# def register_custom_menu_item():
#     # Register a 'Home Page' menu item
#     return MenuItem(_('Home Page'), reverse('index'), icon_name='home', order=1000)
```

### Page Serving Hooks
```python
# @hooks.register('before_serve_page')
# def check_page_permissions(page, request, serve_args, serve_kwargs):
#     # Custom logic before serving a page
#     pass
```

### Dashboard Panels
```python
# @hooks.register('construct_homepage_panels')
# def add_custom_dashboard_panels(request, panels):
#     # Add a 'Quick Stats' panel to the dashboard
#     pass
```
