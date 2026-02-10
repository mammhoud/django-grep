"""
 video blocks with dual-framework styling support.
Includes video players, galleries, and advanced video features.
"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from ..base import AttributeModelBlock, BaseBlock
from .image import ImageBlock


class VideoBlock(AttributeModelBlock):
    """
     video block with multiple hosting options and advanced features.
    """

    # Video Source Options
    video_source = blocks.ChoiceBlock(
        required=True,
        choices=[
            ('embed', _('Embed URL (YouTube, Vimeo, etc.)')),
            ('html5', _('HTML5 Video File')),
            ('external', _('External Video URL')),
        ],
        default='embed',
        label=_("Video Source"),
    )

    # Embed Source
    embed_url = blocks.URLBlock(
        required=False,
        label=_("Embed URL"),
        help_text=_("URL from YouTube, Vimeo, or other embeddable video service."),
    )

    # HTML5 Video
    video_file = blocks.RawHTMLBlock(
        required=False,
        label=_("HTML5 Video"),
        help_text=_("HTML5 video tag with sources. Example: <video><source src='...'></video>"),
    )

    # External URL
    external_url = blocks.URLBlock(
        required=False,
        label=_("External Video URL"),
        help_text=_("Direct URL to video file or external player."),
    )

    # Content
    video_title = blocks.CharBlock(
        required=False,
        max_length=200,
        label=_("Video Title"),
        help_text=_("Title displayed above or with the video."),
    )

    video_description = blocks.RichTextBlock(
        required=False,
        label=_("Video Description"),
        features=['bold', 'italic', 'link'],
        help_text=_("Description displayed with the video."),
    )

    # Thumbnail & Preview
    thumbnail_image = ImageChooserBlock(
        required=False,
        label=_("Thumbnail Image"),
        help_text=_("Custom thumbnail image. If not provided, will use video service thumbnail."),
    )

    show_thumbnail = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show Thumbnail"),
        help_text=_("Display a thumbnail preview before playing."),
    )

    thumbnail_play_button = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show Play Button on Thumbnail"),
    )

    # Player Options
    autoplay = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Autoplay"),
        help_text=_("Automatically start playing the video."),
    )

    loop = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Loop"),
        help_text=_("Loop the video continuously."),
    )

    muted = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Muted"),
        help_text=_("Start video with muted audio."),
    )

    controls = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show Controls"),
        help_text=_("Display video player controls."),
    )

    # Display Options
    player_ratio = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('16:9', _('16:9 (Widescreen)')),
            ('4:3', _('4:3 (Standard)')),
            ('1:1', _('1:1 (Square)')),
            ('auto', _('Auto (Original)')),
        ],
        default='16:9',
        label=_("Player Aspect Ratio"),
    )

    player_size = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('small', _('Small')),
            ('medium', _('Medium')),
            ('large', _('Large')),
            ('full', _('Full Width')),
        ],
        default='medium',
        label=_("Player Size"),
    )

    alignment = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('left', _('Left Aligned')),
            ('center', _('Center Aligned')),
            ('right', _('Right Aligned')),
        ],
        default='center',
        label=_("Alignment"),
    )

    # Advanced
    custom_player_id = blocks.CharBlock(
        required=False,
        max_length=50,
        label=_("Custom Player ID"),
        help_text=_("Custom HTML ID for the video player."),
    )

    lazy_load = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Lazy Load"),
        help_text=_("Delay loading the video until it's visible."),
    )

    class Meta:
        icon = "media"
        label = _(" Video Player")
        template = "blocks/enhanced_video.html"
        group = _("Media")

    def get_player_attributes(self, value):
        """Get attributes for the video player."""
        attrs = {}

        # Embed-specific attributes
        if value.get('video_source') == 'embed' and value.get('embed_url'):
            # For embed services, we rely on oEmbed
            pass

        # HTML5 video attributes
        elif value.get('video_source') == 'html5':
            attrs['controls'] = value.get('controls', True)
            attrs['autoplay'] = value.get('autoplay', False)
            attrs['loop'] = value.get('loop', False)
            attrs['muted'] = value.get('muted', False)

        # External URL
        elif value.get('video_source') == 'external' and value.get('external_url'):
            attrs['src'] = value['external_url']

        # Lazy loading
        if value.get('lazy_load', True):
            attrs['loading'] = 'lazy'

        return attrs

    def get_player_classes(self, value):
        """Get CSS classes for the video player container."""
        classes = []

        # Size classes
        size = value.get('player_size', 'medium')
        if self.style_framework == 'tailwind':
            size_map = {
                'small': f"{self.css_prefix}max-w-md",
                'medium': f"{self.css_prefix}max-w-2xl",
                'large': f"{self.css_prefix}max-w-4xl",
                'full': f"{self.css_prefix}w-full",
            }
        else:  # Bootstrap
            size_map = {
                'small': 'col-md-6',
                'medium': 'col-md-8 col-lg-6',
                'large': 'col-md-10 col-lg-8',
                'full': 'col-12',
            }

        if size in size_map:
            classes.append(size_map[size])

        # Alignment classes
        alignment = value.get('alignment', 'center')
        if alignment == 'center':
            classes.append('mx-auto')
        elif alignment == 'left':
            classes.append('me-auto')
        elif alignment == 'right':
            classes.append('ms-auto')

        # Aspect ratio classes
        ratio = value.get('player_ratio', '16:9')
        if ratio == '16:9':
            classes.append('ratio ratio-16x9')
        elif ratio == '4:3':
            classes.append('ratio ratio-4x3')
        elif ratio == '1:1':
            classes.append('ratio ratio-1x1')

        return ' '.join(filter(None, classes))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['player_attributes'] = self.get_player_attributes(value)
        context['player_classes'] = self.get_player_classes(value)
        return context


class VideoGalleryBlock(AttributeModelBlock):
    """
    Gallery block for multiple videos with playlist functionality.
    """

    gallery_title = blocks.CharBlock(
        required=False,
        max_length=200,
        label=_("Gallery Title"),
    )

    layout_style = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('grid', _('Video Grid')),
            ('playlist', _('Video Playlist')),
            ('carousel', _('Video Carousel')),
        ],
        default='grid',
        label=_("Layout Style"),
    )

    show_playlist = blocks.BooleanBlock(
        required=False,
        default=True,
        label=_("Show Playlist"),
        help_text=_("Display a playlist of all videos."),
    )

    playlist_position = blocks.ChoiceBlock(
        required=False,
        choices=[
            ('side', _('Sidebar')),
            ('bottom', _('Bottom')),
            ('hidden', _('Hidden (Mobile Only)')),
        ],
        default='side',
        label=_("Playlist Position"),
    )

    autoplay_next = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Autoplay Next Video"),
        help_text=_("Automatically play next video when current ends."),
    )

    videos = blocks.ListBlock(
        VideoBlock(),
        label=_("Gallery Videos"),
        help_text=_("Add videos to the gallery."),
    )

    class Meta:
        icon = "media"
        label = _("Video Gallery")
        group = _("Media")
