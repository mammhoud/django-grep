# Pipelines Framework

The Pipelines framework in Django GREP provides enhanced Django models, signals, and routing capabilities for building robust, logical application structures.

## Base Models

### `DefaultBase`

`django_grep.pipelines.models.DefaultBase` is an abstract base model that provides common fields needed for most content models:

-   `id`: UUID primary key.
-   `created_at`: Auto-timestamp on creation.
-   `updated_at`: Auto-timestamp on modification.
-   `created_by`: Foreign key to the user who created the record.
-   `updated_by`: Foreign key to the user who last updated the record.
-   `is_active`: Boolean flag for soft activation/deactivation.
-   `live`: Boolean flag indicating if the content is published.
-   `first_published_at`: Timestamp of first publication.
-   `last_published_at`: Timestamp of last publication.

```python
from django_grep.pipelines.models import DefaultBase

class BlogPost(DefaultBase):
    title = models.CharField(max_length=255)
    content = models.TextField()
```

### `EnhancedBase`

`django_grep.pipelines.models.EnhancedBase` extends `DefaultBase` with additional SEO and metadata fields, suitable for models requiring extensive metadata.

### `ContentBase`

`django_grep.pipelines.models.ContentBase` is designed specifically for content-heavy models, potentially including fields for associated media or complex relationships.

### `TaggableBase`

`django_grep.pipelines.models.TaggableBase` provides tagging capabilities integration with `taggit`.

## Signal Handling

Pipelines streamline signal handling. Use the provided decorators or mixins to hook into model lifecycle events (pre_save, post_save, etc.) in a predictable manner.

## Routing System (`django_grep.routes`)

The routing system simplifies class-based URL configurations.

### `BaseViewset` / `Viewset`

Create modular viewsets that encapsulated related views and URL patterns.

```python
from django_grep.pipelines.routes.base import Viewset, route
from django.urls import path

class MyViewset(Viewset):
    url_prefix = "my-app"

    @route(path("detail/<int:pk>/", name="detail"))
    def detail_view(self, request, pk):
        # Implementation
        pass

    def get_urlpatterns(self):
        return super().get_urlpatterns() + [
            # additional patterns
        ]
```

### `menu_path`

Helper for defining menu structure directly alongside URL definitions.

## Tags

The package includes a tagging system (`django_grep.pipelines.models.tags`) with advanced features like categorization, visibility controls, and color coding for tags.
