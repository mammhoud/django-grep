import django_tables2 as tables
from django.db.models import Model


class BaseTable(tables.Table):
	check_box = tables.columns.CheckBoxColumn()
	model: Model = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if hasattr(model, "category"):
			self.base_columns["category"] = tables.Column(
				accessor="category", verbose_name="Category", orderable=True
			)
