# Filters Documentation

The `django-grep` filter system provides high-level abstractions for model querying, ranging from auto-detecting identifier lookups to universal dynamic filtersets.

---

## 🔍 Identifiers & Lookups

### `BaseFilterMethod`

**Location:** `django_grep.pipelines/filters/base.py`

**Purpose:** Single-value lookups with automatic field type detection.

**Auto-Detection Logic:**
- **UUID**: If value matches UUID format, targets `uuid` or `id` fields.
- **Email**: If value contains `@`, targets `email` fields.
- **Slug**: If value is a string without `@`, targets `code` or `slug` fields.
- **Primary Key**: If value is an integer, targets `pk`.

**Example:**
```python
from django_grep.pipelines.filters import BaseFilterMethod

# Auto-detects that this is an email lookup
filter = BaseFilterMethod(User, "user@example.com")
user = filter.get()

# Explicit field override
filter = BaseFilterMethod(Person, "john-doe", filter_field="slug")
person = filter.get()
```

---

## 📋 Complex Filtering

### `DictFilterMethod`

**Location:** `django_grep.pipelines/filters/base.py`

**Purpose:** Running complex queries using a dictionary of filter parameters.

**When to Use:**
- ✅ Multi-field filtering (e.g., from a search form).
- ✅ Dynamic query generation.
- ✅ List views with optional filters.

**Example:**
```python
from django_grep.pipelines.filters import DictFilterMethod

filter = DictFilterMethod(
    model_class=Person,
    filters={
        'is_active': True,
        'city': 'New York',
        'age__gte': 25
    },
    ordering=['-created_at']
)
persons = filter.run()
```

---

## 🛠️ Universal Filtering

### `UniversalFilter`

**Location:** `django_grep.pipelines/filters/base.py`

**Purpose:** Bridge to `django-filter` providing automatic FilterSet generation.

**When to Use:**
- ✅ Generic views or API endpoints where any field can be filtered.
- ✅ Reducing boilerplate for standard FilterSet creation.

#### Key Methods

```python
# Generate a FilterSet class for a model on-the-fly
PersonFilterSet = UniversalFilter.create_filterset_for_model(Person)

# filter a queryset directly using a data dictionary
results = UniversalFilter.filter_model(
    model_class=Person,
    filter_data={'city__icontains': 'new', 'is_active': True}
)
```
