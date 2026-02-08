from django import template

register = template.Library()

"""modal.html
<div class="modal" id="{{ modal_id }}" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{{ modal_title }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                {{ modal_body }}
            </div>
        </div>
    </div>
</div>


"""


@register.inclusion_tag("modal.html")
def generate_modal(modal_id, modal_title, modal_body):
    """
    Template tag to generate a modal dialog.

    Usage:
        {% generate_modal modal_id="myModal" modal_title="Modal Title" modal_body="This is the body of the modal" %}
    """
    return {"modal_id": modal_id, "modal_title": modal_title, "modal_body": modal_body}
