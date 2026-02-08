from django.utils.translation import gettext_lazy as _

from django_grep.pipelines.models import Person

from ..base import BaseSnippetViewSet


class PersonViewSet(BaseSnippetViewSet):
    """Manage simple Person records via the Wagtail Snippet interface."""

    model = Person
    menu_label = _("People")
    icon = "user"
    menu_order = 200
    # search_fields = ["first_name", "last_name", "email", "phone", "organization__name"]
    # list_display = [
    #     "full_name",
    #     "email",
    #     "phone",
    #     "organization",
    #     "type",
    #     "is_active",
    # ]
    # list_export = [
    #     "first_name",
    #     "last_name",
    #     "email",
    #     "phone",
    #     "organization",
    #     "type",
    #     "is_active",
    # ]
    # csv_filename = "people.csv"

    # @staticmethod
    # def type_display(obj):
    #     return obj.get_type_display()

    # type_display.short_description = _("Type")

    # # def get_queryset(self, request):
    # #     qs = super().get_queryset(request)
    # #     return qs.select_related("organization", "department").prefetch_related("tags", "contact_methods")

