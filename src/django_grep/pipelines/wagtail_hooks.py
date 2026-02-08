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
        PersonViewSet,
        SiteSettingsViewSet,
        SocialSettingsViewSet,
        EmailSettingsViewSet,
    )

# =============================================================================
# REGISTRATION
# =============================================================================
register_snippet(ManagementsSnippetGroup)



