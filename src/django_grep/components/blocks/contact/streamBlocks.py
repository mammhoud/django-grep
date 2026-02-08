import logging
import uuid

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from .contactMethods import ContactMethodBlock

# from .socialLinks import SocialLinkBlock
from .websiteLinks import ContactProfileBlock

logger = logging.getLogger(__name__)

# =============================================================================
# BASE CONTENT STREAM BLOCK (for general content)
# =============================================================================


class ContactMethodsStreamBlock(blocks.StreamBlock):
    """
    StreamBlock container for all contact method types.
    """

    contact_method = ContactMethodBlock()
    # website_link = ContactProfileBlock()

    class Meta:
        label = _("Contact Methods")
        icon = "phone"
        block_counts = {
            "contact_method": {"min_num": 0, "max_num": 20},
            "social_media": {"min_num": 0, "max_num": 15},
            "website_link": {"min_num": 0, "max_num": 10},
        }
