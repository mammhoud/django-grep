# Django GREP

Django GREP (Generic Reusable Enhanced Pipelines) is a powerful utility library designed to enhance Django and Wagtail projects with a suite of reusable components, advanced pipelines, and core utilities.

It was originally developed as part of the CTC website project (`wagtail-ctc`) and has evolved into a standalone package for broader reuse.

## Features

### 🧩 Components (`django_grep.components`)
A robust component system for Wagtail StreamFields, providing a structured way to build complex page layouts.
- **Pre-built Blocks**: Includes common blocks like Hero, CTA, Features, Testimonials, and more.
- **Template Tag Integration**: Easily render blocks in templates using custom template tags.
- **Manifest Management**: Automatic asset manifest generation for component-specific CSS/JS.

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
