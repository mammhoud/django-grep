from django.conf import settings

from django_grep.pipelines.models import SiteSettings, SocialSettings


# =======================================
# TEMPLATE CONTEXT PROCESSOR HELPER
# =======================================
def SETTINGS(request=None):
    """
    Context processor to add active settings to all templates.
    Usage in templates: {{ site_settings.site_name }}, {{ social_settings.phone_number }}
    """
    context = {}

    # Get site settings
    site_settings = SiteSettings.get_active_for_request(request)
    context["site_settings"] = {}
    if site_settings:
        context["site_settings"] = site_settings

    # Get social settings
    social_settings = SocialSettings.get_active_for_request(request)
    context["social_settings"] = {}
    if social_settings:
        context["social_settings"] = social_settings

    # # Get email settings
    # email_settings = EmailSettings.get_active_for_request(request)
    # if email_settings:
    #     context['email_settings'] = email_settings

    return context
