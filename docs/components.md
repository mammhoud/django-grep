# Components System

The Components system in Django GREP provides a rich set of Wagtail StreamField blocks for building modular, maintainable, and interactive page layouts.

## Core Components

The following components are readily available for use:

### Layout Components

- **Section (`SectionBlock`)**: A full-width section with optional background colors and padding.
- **Container (`ContainerBlock`)**: A Bootstrap-like container block to restrain content width.
- **Card (`CardBlock`)**: A versatile card component for content display.

### Media Components

- **Image (`ImageBlock`)**: A simple image block with caption support.
- **Video (`VideoBlock`)**: An embeddable video block (YouTube, Vimeo, internal).
- **Gallery (`GalleryBlock`)**: A collection of images with grid layout options.

### Content Components

- **RichText (`RichTextBlock`)**: Enhanced rich text editor block.
- **Heading (`HeadingBlock`)**: Customizable headings (H1, H2, H3, H4, H5, H6).
- **Quote (`QuoteBlock`)**: Block for displaying quotes or citations.
- **Button (`ButtonBlock`)**: Standard button with multiple styles (primary, secondary, outline).

## Extending Components

You can easily extend or create new components by inheriting from `wagtail.blocks.StructBlock` or using the provided base classes in `django_grep.components.blocks.base`.

```python
from wagtail import blocks
from django_grep.components.blocks.base import BaseStructBlock

class CustomCardBlock(BaseStructBlock):
    title = blocks.CharBlock()
    description = blocks.RichTextBlock()

    class Meta:
        template = "blocks/custom_card.html"
        icon = "doc-full"
```

## Template Integration

Components are designed to render using their associated templates. When adding components to a StreamField, they automatically render according to their specified `template` meta attribute.

Example template usage (`models.py`):

```python
from django_grep.components.blocks import streamBlocks

class ContentPage(Page):
    body = StreamField(streamBlocks, use_json_field=True)
```

Example template (`content_page.html`):

```html
{% load wagtailcore_tags %}

{% for block in page.body %}
    {% include_block block %}
{% endfor %}
```
