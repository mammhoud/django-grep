import logging
import uuid

from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from .mixins import ResponsiveBlockMixin, StyledBlockMixin

logger = logging.getLogger(__name__)


class BaseBlock(StyledBlockMixin, ResponsiveBlockMixin, blocks.StructBlock):
    """
    Enhanced base block class with built-in styling and responsive support.
    Provides common functionality for all blocks.
    """

    # Common fields for all blocks
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

    # Visibility controls
    is_visible = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Visible"),
        help_text=_("Toggle visibility of this block."),
    )

    # visibility_conditions = blocks.ChoiceBlock(
    #     required=False,
    #     choices=[
    #         ('always', _('Always Visible')),
    #         ('desktop', _('Desktop Only')),
    #         ('mobile', _('Mobile Only')),
    #         ('logged_in', _('Logged-in Users Only')),
    #         ('logged_out', _('Logged-out Users Only')),
    #     ],
    #     default='always',
    #     label=_("Visibility Conditions"),
    # )

    # # Responsive configuration
    # responsive_config = blocks.StructBlock(
    #     [
    #         (
    #             "width",
    #             blocks.ChoiceBlock(
    #                 required=False,
    #                 choices=[
    #                     ("full", _("Full Width")),
    #                     ("container", _("Container Width")),
    #                     ("narrow", _("Narrow Width")),
    #                 ],
    #                 default="container",
    #                 label=_("Container Width"),
    #             ),
    #         ),
    #         (
    #             "padding",
    #             blocks.ChoiceBlock(
    #                 required=False,
    #                 choices=[
    #                     ("none", _("No Padding")),
    #                     ("small", _("Small Padding")),
    #                     ("default", _("Default Padding")),
    #                     ("large", _("Large Padding")),
    #                 ],
    #                 default="default",
    #                 label=_("Padding Size"),
    #             ),
    #         ),
    #         (
    #             "background",
    #             blocks.ChoiceBlock(
    #                 required=False,
    #                 choices=[
    #                     ("none", _("No Background")),
    #                     ("light", _("Light Background")),
    #                     ("dark", _("Dark Background")),
    #                     ("gradient", _("Gradient Background")),
    #                     ("pattern", _("Pattern Background")),
    #                 ],
    #                 default="none",
    #                 label=_("Background Style"),
    #             ),
    #         ),
    #     ],
    #     required=False,
    #     label=_("Responsive Configuration"),
    # )

    def get_block_classes(self, value):
        """Get CSS classes for the block container."""
        base_classes = self.get_styling_config().get("container", "")
        responsive_classes = self.get_responsive_classes(value)
        custom_classes = value.get("custom_css_class", "")

        # Add visibility classes
        visibility_class = ""
        if value.get("visibility_conditions") != "always":
            visibility_class = f"visible-{value['visibility_conditions']}"

        classes = [base_classes, responsive_classes, custom_classes, visibility_class]
        return " ".join(filter(None, classes))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        # Add framework info
        context["framework"] = self.style_framework
        context["css_prefix"] = self.css_prefix

        # Generate unique block ID
        block_id = value.get("custom_css_id") or f"block-{uuid.uuid4().hex[:8]}"
        context["block_id"] = block_id
        context["block_classes"] = self.get_block_classes(value)

        return context

    def render(self, value, context=None):
        # Skip rendering if block is not visible
        if not value.get("is_visible", True):
            return ""

        return super().render(value, context)
