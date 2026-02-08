# Routing System (Routes)

The Routing System in Django GREP provides a structured, class-based approach to defining URL patterns and views.

## Introduction

Instead of scattering URL definitions across `urls.py` files, the Routes system allows you to encapsulate related views and their URL patterns within a `Viewset` class. This mimics the structure of libraries like `django-rest-framework` but for standard Django views.

## Basic Usage

### Defining a Viewset

```python
from django_grep.pipelines.routes.base import Viewset, route
from django.urls import path
from django.shortcuts import render

class MyBlogViewset(Viewset):
    url_prefix = "blog"

    @route(path("", name="index"))
    def index(self, request):
        return render(request, "blog/index.html")

    @route(path("<slug:slug>/", name="detail"))
    def detail(self, request, slug):
        return render(request, "blog/detail.html", {"slug": slug})
```

### Registering URLs

In your project's main `urls.py`:

```python
from django.urls import path, include
from .views import MyBlogViewset

urlpatterns = [
    # ...
    path("blog/", include(MyBlogViewset().urls)),
    # ...
]
```

## Features

- **Namespace Support**: `Viewset` handles namespacing automatically based on `url_prefix` or explicitly provided namespace.
- **Route Decorator**: Use the `@route` decorator to define patterns directly on methods.
- **Menu Integration**: Use `menu_path` to mark routes that should appear in generated menus.
- **URL Reversing**: Simplifies reversing URLs within the viewset using `self.reverse("name")`.
- **Automatic Pattern Collection**: Automatically collects all decorated methods into the `urlpatterns` list.
