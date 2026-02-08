from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from .snippets import *


@hooks.register("register_icons")
def register_icons(icons):
    """
    Register custom SVG icons for use in Wagtail admin.
    Add any custom icons to the icons list.
    """
    return icons + [
        "wagtailfontawesomesvg/solid/suitcase.svg",
        "wagtailfontawesomesvg/solid/utensils.svg",
        "wagtailfontawesomesvg/solid/chart-line.svg",
        "wagtailfontawesomesvg/solid/users.svg",
        'wagtailfontawesomesvg/brands/facebook.svg',
        'wagtailfontawesomesvg/regular/face-laugh.svg',
        'wagtailfontawesomesvg/solid/yin-yang.svg',

    ]

class ManagementsSnippetGroup(SnippetViewSetGroup):
    """
    Groups people-related models together in the admin menu.
    Includes persons, students, and user management.
    """
    menu_label = _("Manage")
    menu_icon = "suitcase"
    menu_order = 300
    items = (
        # CompanyViewSet,
        PersonViewSet,
        # ContactViewSet,
        # TagViewSet,
        # ServiceViewSet,
        # NewsletterViewSet,
        # EmailTemplateViewSet,
        SiteSettingsViewSet,
        SocialSettingsViewSet,
        EmailSettingsViewSet,
    )

# =============================================================================
# REGISTRATION
# =============================================================================
register_snippet(ManagementsSnippetGroup)


# # =============================================================================
# # ADDITIONAL HOOKS
# # =============================================================================




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

# @hooks.register('construct_main_menu')
# def hide_explorer_menu_item(request, menu_items):
#     """
#     Customize the main menu by hiding or modifying menu items.
#     """
#     # Example: Hide the explorer menu for non-staff users
#     if not request.user.is_staff:
#         menu_items[:] = [item for item in menu_items if item.name != 'explorer']

#     return menu_items


# @hooks.register('register_admin_menu_item')
# def register_custom_menu_item():
#     """
#     Register custom menu items in the Wagtail admin.
#     """
#     from wagtail.admin.menu import MenuItem
#     from django.urls import reverse

#     return MenuItem(
#         _('Home Page'),
#         reverse('index'),
#         icon_name='home',
#         order=1000
#     )


# @hooks.register('before_serve_page')
# def check_page_permissions(page, request, serve_args, serve_kwargs):
#     """
#     Custom permission checks before serving pages.
#     Add any custom page serving logic here.
#     """
#     # Example: Log page access or add custom permissions
#     pass


# # Custom dashboard panels
# @hooks.register('construct_homepage_panels')
# def add_custom_dashboard_panels(request, panels):
#     """
#     Add custom panels to the Wagtail dashboard.
#     """
#     from wagtail.admin.ui.components import Component

#     class QuickStatsPanel(Component):
#         order = 10
#         template_name = 'admin/quick_stats_panel.html'

#         def get_context_data(self, request):
#             # Add context data for the panel
#             return {
#                 'total_people': Person.objects.count(),
#                 'total_newsletters': Newsletter.objects.count(),
#                 'recent_activity': [],  # Add recent activity data
#             }

#     panels.append(QuickStatsPanel())
#     return panels
