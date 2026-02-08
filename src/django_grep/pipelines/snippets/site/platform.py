# wagtail_hooks.py
from django.utils.translation import gettext_lazy as _
from wagtail.admin.ui.tables import BooleanColumn, DateColumn, TitleColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from django_grep.pipelines.models import SiteSettings
from django_grep.pipelines.snippets.base import BaseSnippetViewSet


class SiteSettingsViewSet(BaseSnippetViewSet):
    """
    Custom ViewSet for SiteSettings with enhanced functionality.
    """
    model = SiteSettings
    icon = "cog"  # Wagtail icon name
    menu_label = _("Site Settings")
    menu_name = "site-settings"
    menu_order = 1000
    # add_to_settings_menu = True  # Show in Settings menu
    # add_to_admin_menu = False    # Don't show in main menu
    
    # list_display = [
    #     TitleColumn("site_name", label=_("Site Name"), url_name='edit'),
    #     "get_language_display",
    #     BooleanColumn("active", label=_("Active")),
    #     DateColumn("last_published_at", label=_("Last Published")),
    # ]
    
    # list_filter = [
    #     "language",
    #     "active",
    # ]
    
    # search_fields = [
    #     "site_name",
    #     "company_name",
    #     "tagline",
    #     "meta_description",
    # ]
    
    ordering = ["language", "-active"]
    
#     list_export = [
#         "site_name",
#         "language",
#         "active",
#         "company_name",
#         "primary_email",
#         "primary_phone",
#         "last_published_at",
#     ]
    
#     # Custom permissions
#     def user_can_access(self, user):
#         """Only superusers and editors can access settings."""
#         return user.is_superuser or user.groups.filter(name__in=['Editors', 'Site Managers']).exists()
    
#     def user_can_create(self, user):
#         """Only superusers can create new settings."""
#         return user.is_superuser
    
#     def get_queryset(self, request):
#         """Filter queryset based on user permissions."""
#         qs = super().get_queryset(request)
#         if not request.user.is_superuser:
#             # Non-superusers can only see active settings
#             qs = qs.filter(active=True)
#         return qs
    
#     # Custom actions
#     def get_list_actions(self):
#         actions = super().get_list_actions()
        
#         # Add custom action to activate a language
#         from django.utils.html import format_html
#         from wagtail.admin.ui.components import Button
        
#         class ActivateLanguageButton(Button):
#             def __init__(self, instance):
#                 if not instance.active:
#                     super().__init__(
#                         label=_("Activate"),
#                         url=f"/admin/site-settings/activate/{instance.pk}/",
#                         icon_name="tick",
#                         priority=10,
#                     )
#                 else:
#                     super().__init__(
#                         label=_("Active"),
#                         url="#",
#                         icon_name="tick-inverse",
#                         priority=10,
#                         attrs={'disabled': 'disabled', 'class': 'button-secondary'}
#                     )
        
#         return actions
    
#     # Custom templates
#     edit_template_name = "settings/edit.html"
#     create_template_name = "settings/create.html"


# # # Register the snippet with custom ViewSet
# # register_snippet(SiteSettings, viewset=SiteSettingsViewSet)


# # # -----------------------------------------------------------------------------
# # # TEMPLATE TAGS FOR SETTINGS ACCESS
# # # -----------------------------------------------------------------------------

# # from django import template
# # from django.utils.safestring import mark_safe
# # from ..models import SiteSettings

# # register = template.Library()


# # @register.simple_tag(takes_context=True)
# # def get_site_settings(context, language_code=None):
# #     """
# #     Get site settings for the current request or specified language.
# #     Usage in templates: {% get_site_settings as settings %}
# #     """
# #     request = context.get('request')
# #     if language_code:
# #         return SiteSettings.get_for_language(language_code)
# #     return SiteSettings.get_for_request(request)


# # @register.inclusion_tag('includes/social_links.html', takes_context=True)
# # def social_links(context):
# #     """
# #     Render social media links.
# #     Usage: {% social_links %}
# #     """
# #     settings = SiteSettings.get_for_request(context.get('request'))
# #     return {
# #         'social_links': settings.get_social_links() if settings else [],
# #         'request': context.get('request'),
# #     }


# # @register.inclusion_tag('includes/contact_info.html', takes_context=True)
# # def contact_info(context):
# #     """
# #     Render contact information.
# #     Usage: {% contact_info %}
# #     """
# #     settings = SiteSettings.get_for_request(context.get('request'))
# #     return {
# #         'settings': settings,
# #         'request': context.get('request'),
# #     }


# # # -----------------------------------------------------------------------------
# # # CONTEXT PROCESSOR
# # # -----------------------------------------------------------------------------

# # def site_settings(request):
# #     """
# #     Add site settings to template context.
# #     """
# #     settings = SiteSettings.get_for_request(request)
# #     if settings:
# #         return {
# #             'site_settings': settings,
# #             'brand': settings.get_brand_context(),
# #             'contact': settings.get_contact_context(),
# #             'seo': settings.get_seo_context(),
# #             'social_links': settings.get_social_links(),
# #         }
# #     return {}