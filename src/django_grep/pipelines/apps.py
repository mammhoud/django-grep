from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PipelinesConfig(AppConfig):
    label = "pipelines"
    name = "django_grep.pipelines"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Pipelines")
    verbose_name_plural = _("Pipelines")

    def ready(self): ...
