"""
Combined media gallery blocks for images and videos.
"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from ..base import BaseBlock
from .image import ImageBlock
from .video import VideoBlock


class MediaGalleryItemBlock(BaseBlock):
    """
    Individual media item for mixed galleries (image or video).
    """
    
    media_type = blocks.ChoiceBlock(
        required=True,
        choices=[
            ('image', _('Image')),
            ('video', _('Video')),
        ],
        default='image',
        label=_("Media Type"),
    )
    
    image = ImageBlock(
        required=False,
        label=_("Image Content"),
    )
    
    video = VideoBlock(
        required=False,
        label=_("Video Content"),
    )
    
    caption = blocks.RichTextBlock(
        required=False,
        label=_("Caption"),
        features=['bold', 'italic', 'link'],
    )
    
    category = blocks.CharBlock(
        required=False,
        max_length=50,
        label=_("Category"),
        help_text=_("Optional category for filtering."),
    )
    
    featured = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Featured Item"),
        help_text=_("Highlight this item in the gallery."),
    )
    
    class Meta:
        icon = "media"
        label = _("Media Gallery Item")
        template = "blocks/media_gallery_item.html"
        group = _("Media")
    
    def get_media_content(self, value):
        """Get the appropriate media content based on type."""
        if value.get('media_type') == 'image' and value.get('image'):
            return value['image']
        elif value.get('media_type') == 'video' and value.get('video'):
            return value['video']
        return None


class MediaGalleryBlock(BaseBlock):
    """
     gallery for mixed media content (images and videos).
    """
    
    gallery_title = blocks.CharBlock(
        required=False,
        max_length=200,
        label=_("Gallery Title"),
    )
    
    gallery_description = blocks.RichTextBlock(
        required=False,
        label=_("Gallery Description"),
        features=['bold', 'italic', 'link'],
    )
    
    layout_style = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('masonry', _('Masonry Layout')),
            ('grid', _('Uniform Grid')),
            ('justified', _('Justified Grid')),
            ('carousel', _('Carousel')),
            ('lightbox', _('Lightbox Gallery')),
        ],
        default='masonry',
        label=_("Layout Style"),
    )
    
    filterable = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Enable Filtering"),
        help_text=_("Allow users to filter by media type or category."),
    )
    
    filter_by = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('type', _('Media Type')),
            ('category', _('Category')),
            ('both', _('Both Type and Category')),
        ],
        default='type',
        label=_("Filter By"),
    )
    
    items_per_page = blocks.IntegerBlock(
        required=False,
        default=12,
        min_value=1,
        max_value=100,
        label=_("Items Per Page"),
        help_text=_("Number of items to show before pagination."),
    )
    
    lightbox_enabled = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Enable Lightbox"),
    )
    
    lazy_loading = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Lazy Loading"),
    )
    
    media_items = blocks.ListBlock(
        MediaGalleryItemBlock(),
        label=_("Media Items"),
        help_text=_("Add images and videos to the gallery."),
    )
    
    # Display Options
    show_captions = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('never', _('Never')),
            ('hover', _('On Hover')),
            ('always', _('Always')),
            ('lightbox', _('In Lightbox Only')),
        ],
        default='hover',
        label=_("Show Captions"),
    )
    
    show_thumbnails = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show Thumbnails"),
    )
    
    thumbnail_size = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('small', _('Small (150px)')),
            ('medium', _('Medium (250px)')),
            ('large', _('Large (350px)')),
        ],
        default='medium',
        label=_("Thumbnail Size"),
    )
    
    class Meta:
        icon = "image"
        label = _(" Media Gallery")
        template = "blocks/enhanced_media_gallery.html"
        group = _("Media")
    
    def get_gallery_config(self, value):
        """Get gallery configuration for JavaScript."""
        import json
        
        config = {
            'layout': value.get('layout_style', 'masonry'),
            'filterable': value.get('filterable', False),
            'filterBy': value.get('filter_by', 'type'),
            'lightbox': value.get('lightbox_enabled', True),
            'lazyLoading': value.get('lazy_loading', True),
            'itemsPerPage': value.get('items_per_page', 12),
            'captions': value.get('show_captions', 'hover'),
            'thumbnails': value.get('show_thumbnails', True),
            'thumbnailSize': value.get('thumbnail_size', 'medium'),
        }
        return json.dumps(config)
    
    def get_categories(self, value):
        """Extract unique categories from media items."""
        categories = set()
        for item in value.get('media_items', []):
            category = item.value.get('category')
            if category:
                categories.add(category)
        return sorted(list(categories))