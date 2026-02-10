import logging
import uuid

from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from .mixins import ResponsiveBlockMixin, StyledBlockMixin

logger = logging.getLogger(__name__)


class BaseBlock(blocks.StructBlock):
    """
    Base block class with minimal attributes.
    """
    is_visible = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Visible"),
        help_text=_("Toggle visibility of this block."),
    )

    class Meta:
        abstract = True

    def get_block_classes(self, value):
        """Get default CSS classes for the block."""
        return ""

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        # Generate unique block ID if not present
        context["block_id"] = f"block-{uuid.uuid4().hex[:8]}"
        context["block_classes"] = self.get_block_classes(value)
        return context

    def render(self, value, context=None):
        # Skip rendering if block is not visible
        if not value.get("is_visible", True):
            return ""
        return super().render(value, context)


class AttributeModelBlock(StyledBlockMixin, ResponsiveBlockMixin, BaseBlock):
    """
    Enhanced block class with styling, responsive support, and model attributes.
    Provides common functionality for complex blocks.
    """

    custom_css_id = blocks.CharBlock(
        required=False,
        max_length=50,
        label=_("Custom CSS ID"),
        help_text=_("Custom HTML ID for CSS targeting and JavaScript."),
    )

    custom_css_class = blocks.CharBlock(
        required=False,
        max_length=100,
        label=_("Custom CSS Class"),
        help_text=_("Additional CSS classes for custom styling."),
    )

    data_attributes = blocks.RawHTMLBlock(
        required=False,
        label=_("Data Attributes"),
        help_text=_("Custom data attributes for JavaScript interaction."),
    )

    unhandled_model_fields = blocks.ListBlock(
        blocks.StructBlock([
            ('field_name', blocks.CharBlock(required=True, label=_("Field Name"))),
            ('field_value', blocks.CharBlock(required=True, label=_("Field Value/Override"))),
            ('is_active', blocks.BooleanBlock(default=True, label=_("Active"))),
        ]),
        required=False,
        label=_("Unhandled Model Fields"),
        help_text=_("Manual mapping for model fields not explicitly defined in this block."),
    )

    def get_block_classes(self, value):
        """Get CSS classes for the block container."""
        base_classes = self.get_styling_config().get("container", "")
        responsive_classes = self.get_responsive_classes(value)
        custom_classes = value.get("custom_css_class", "")

        classes = [base_classes, responsive_classes, custom_classes]
        return " ".join(filter(None, classes))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        # Add framework info
        context["framework"] = self.style_framework
        context["css_prefix"] = self.css_prefix

        # Use custom ID if provided
        if value.get("custom_css_id"):
            context["block_id"] = value.get("custom_css_id")

        context["block_classes"] = self.get_block_classes(value)

        # Handle unhandled model fields
        unhandled = {}
        for item in value.get("unhandled_model_fields", []):
            if item.get("is_active", True):
                unhandled[item["field_name"]] = item["field_value"]
        context["unhandled_fields"] = unhandled

        return context

