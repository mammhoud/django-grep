from django import template

register = template.Library()


"""
<div class="card">
    {% if image %}
        <img src="{{ image }}" alt="{{ title }}"/>
    {% endif %}
    <div class="card-body">
        <h5 class="card-title">{{ title }}</h5>
        <p class="card-text">{{ content }}</p>
    </div>
</div>

"""


@register.inclusion_tag("card.html")
def generate_card(title, content, image=None):
    """
    Template tag to generate a card component with a title, content, and optional image.

    Usage:
        {% generate_card title="Card Title" content="Card content here" %}
        {% generate_card title="Card Title" content="Card content here" image="image_url.jpg" %}
    """
    return {"title": title, "content": content, "image": image}
