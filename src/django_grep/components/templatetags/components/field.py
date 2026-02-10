from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def get_field_value(obj, field_name):
    """
    Custom filter to get the value of a field dynamically from a model instance.

    Usage:
        {{ row|get_field_value:'field_name' }}

    Example:
        {{ row|get_field_value:'first_name' }}
    """
    try:
        return getattr(obj, field_name, "")
    except AttributeError:
        return ""


@register.simple_tag
def render_field(field, label=None):
    """
    Template tag to render a form field with optional custom labels.

    Usage:
        {% render_field field %}
        {% render_field field label="Custom Label" %}
    """
    return {"field": field, "label": label if label else field.label}
@register.simple_tag
def render_unhandled_fields(unhandled_fields):
    """
    Renders unhandled model fields as a list of hidden spans for JavaScript consumption.
    """
    if not unhandled_fields:
        return ""

    parts = ['<div class="unhandled-model-fields" style="display:none;">']
    for key, value in unhandled_fields.items():
        parts.append(format_html('<span data-field="{}">{}</span>', key, value))
    parts.append('</div>')

    return mark_safe("".join(parts))
