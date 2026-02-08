from django.utils.translation import gettext_lazy as _

from django_grep.pipelines.models import SocialSettings

from ..base import BaseSnippetViewSet


class SocialSettingsViewSet(BaseSnippetViewSet):
    """Manage simple Person records via the Wagtail Snippet interface."""

    model = SocialSettings
    menu_label = _("Social Links")
    icon = "globe"
    menu_order = 200
