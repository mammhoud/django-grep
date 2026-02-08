from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from django_grep.components.blocks.content.heading import AdvancedHeadingBlock
from django_grep.components.blocks.content.paragraph import ParagraphBlock
from django_grep.components.blocks.media.document import DocumentBlock
from django_grep.components.blocks.media.html import HTMLBlock

from ..base import BaseBlock
from ..content.quote import BlockQuote
from ..media.image import ImageBlock
from .tables import TableBlock


class SectionBlock(BaseBlock):
    """
     section block with multiple content types and layout options.
    """

    # Header
    section_title = blocks.CharBlock(
        required=False,
        max_length=200,
        label=_("Section Title"),
        help_text=_("Optional title for this content section."),
    )

    section_subtitle = blocks.CharBlock(
        required=False,
        max_length=400,
        label=_("Section Subtitle"),
    )

    # Layout
    layout_style = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('standard', _('Standard Flow')),
            ('grid', _('Grid Layout')),
            ('sidebar', _('Sidebar Layout')),
            ('cards', _('Card Layout')),
            ('alternating', _('Alternating Layout')),
        ],
        default='standard',
        label=_("Layout Style"),
    )

    columns = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('1', '1 Column'),
            ('2', '2 Columns'),
            ('3', '3 Columns'),
            ('4', '4 Columns'),
        ],
        default='1',
        label=_("Number of Columns"),
    )

    # Content
    content = blocks.StreamBlock([
        ('heading', AdvancedHeadingBlock()),
        ('paragraph', ParagraphBlock()),
        ('image', ImageBlock()),
        ('embed', EmbedBlock()),
        ('document', DocumentBlock()),
        ('table', TableBlock()),
        ('quote', BlockQuote()),
        ('html', HTMLBlock()),
        ('typed_table', TypedTableBlock([
            ('text', blocks.CharBlock()),
            ('numeric', blocks.FloatBlock()),
            ('rich_text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
        ], label=_("Typed Table"))),
    ], label=_("Section Content"), help_text=_("Add content blocks to this section."))

    # Styling
    background_style = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('none', _('No Background')),
            ('light', _('Light Background')),
            ('dark', _('Dark Background')),
            ('gradient', _('Gradient')),
            ('pattern', _('Pattern')),
            ('image', _('Background Image')),
        ],
        default='none',
        label=_("Background Style"),
    )

    background_image = ImageChooserBlock(
        required=False,
        label=_("Background Image"),
        help_text=_("Optional background image for the section."),
    )

    # Spacing
    padding_top = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('none', _('None')),
            ('small', _('Small')),
            ('medium', _('Medium')),
            ('large', _('Large')),
            ('xlarge', _('Extra Large')),
        ],
        default='medium',
        label=_("Top Padding"),
    )

    padding_bottom = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('none', _('None')),
            ('small', _('Small')),
            ('medium', _('Medium')),
            ('large', _('Large')),
            ('xlarge', _('Extra Large')),
        ],
        default='medium',
        label=_("Bottom Padding"),
    )

    class Meta:
        icon = "folder-open-inverse"
        label = _(" Section")
        group = _("Content")

    def get_section_classes(self, value):
        """Get CSS classes for the section."""
        classes = ['content-section']

        # Layout classes
        layout = value.get('layout_style', 'standard')
        classes.append(f'section-layout-{layout}')

        # Column classes
        columns = value.get('columns', '1')
        classes.append(f'columns-{columns}')

        # Background classes
        background = value.get('background_style', 'none')
        if background != 'none':
            classes.append(f'bg-{background}')

        # Padding classes
        padding_top = value.get('padding_top', 'medium')
        padding_bottom = value.get('padding_bottom', 'medium')
        classes.append(f'pt-{padding_top}')
        classes.append(f'pb-{padding_bottom}')

        return ' '.join(classes)
