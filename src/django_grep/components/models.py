from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Site
from wagtail.snippets.models import register_snippet

from django_grep.components.conf import SystemComponentName


@register_snippet
class CustomComponent(models.Model):
    """
    🧩 Custom HTML Component Snippet
    Allows administrators to upload custom HTML templates that can be
    rendered dynamically using the `django-grep` component system.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Display Name"),
        help_text=_("Human-readable name for the component."),
    )
    identifier = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("Variable Name"),
        help_text=_("Space-less identifier used in templates (e.g., 'primary_banner')."),
    )
    component_type = models.CharField(
        max_length=50,
        choices=SystemComponentName.choices(),
        default=SystemComponentName.DYNAMIC,
        verbose_name=_("Component Type"),
        help_text=_("The system trigger this component responds to."),
    )
    html_file = models.FileField(
        upload_to="components/custom/",
        verbose_name=_("HTML Template File"),
        help_text=_("Upload a .html file containing the component structure."),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("identifier"),
        FieldPanel("component_type"),
        FieldPanel("html_file"),
    ]

    def __str__(self):
        return f"{self.name} ({self.identifier})"

    class Meta:
        verbose_name = _("Custom Component")
        verbose_name_plural = _("Custom Components")


@register_setting
class CustomComponentSettings(BaseSiteSetting):
    """
    ⚙️ Global settings for custom components.
    Allows selecting uploaded components for specific site sections.
    """

    custom_header = models.ForeignKey(
        "components.CustomComponent",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Custom Header Component"),
    )
    custom_footer = models.ForeignKey(
        "components.CustomComponent",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Custom Footer Component"),
    )
    trigger_mode = models.CharField(
        max_length=50,
        choices=SystemComponentName.choices(),
        default=SystemComponentName.DYNAMIC,
        verbose_name=_("Global Trigger Mode"),
        help_text=_("Sets the default trigger behavior for custom components."),
    )

    panels = [
        FieldPanel("custom_header"),
        FieldPanel("custom_footer"),
        FieldPanel("trigger_mode"),
    ]

    class Meta:
        verbose_name = _("Custom Component Settings")
