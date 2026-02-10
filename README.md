# Django GREP (Generic Reusable Enhanced Plugins)

Django GREP is a powerful suite of reusable plugins and utilities designed to enhance Django and Wagtail projects with advanced component architecture, modular pipelines, and core system extensions.

## Features

### 🧩 Plugin Components (`django_grep.components`)
A robust plugin system for building modular page elements and layouts.
- **Pluggable Blocks**: Modular components like Hero, CTA, Features, and Testimonials that can be dropped into any StreamField.
- **Template Tag Plugins**: Extensible template tags for rendering complex logic with minimal boilerplate.
- **Frontend Assets**: Automated asset management for plugin-specific CSS/JS.

### 🚀 Pipelines (`django_grep.pipelines`)
Enhanced model workflows and data processing pipelines.
- **Base Models**: Abstract base models for enhanced content management (UUID PKs, timestamps, audit fields).
- **Signal Handling**: Streamlined signal dispatching and handling.
- **Routing**: Flexible class-based viewsets and URL routing (`django_grep.pipelines.routes`).

### 🛠️ Utilities (`django_grep.contrib`)
Essential utilities for everyday Django development.
- **Configuration**: Unified settings management.
- **Helpers**: String manipulation, date formatting, and more.

## Installation

Install the package via pip:

```bash
pip install django-grep
```

## Quick Start

### 1. Configure Settings

Add `django_grep` apps to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "django_grep.pipelines",
    "django_grep.components",
    # ...
]
```

### 2. Basic Usage

#### Using Components

In your Wagtail Page model:

```python
from wagtail.models import Page
from wagtail.fields import StreamField
from django_grep.components.blocks import streamBlocks

class ContentPage(Page):
    body = StreamField(streamBlocks, use_json_field=True)
```

#### Using Pipelines Models

```python
from django.db import models
from django_grep.pipelines.models import DefaultBase

class MyModel(DefaultBase):
    title = models.CharField(max_length=255)
    # Inherits created_at, updated_at, created_by, updated_by, live, etc.
```

## Documentation

For detailed documentation, please refer to the [docs](docs/) directory.

## License

This project is licensed under the MIT License.
