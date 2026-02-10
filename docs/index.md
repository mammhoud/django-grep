# Django GREP Documentation

Welcome to the documentation for **Django GREP** (Generic Reusable Enhanced Plugins).

## Overview

Django GREP is a collection of enhancing plugins, utilities, and components for Django and Wagtail projects. It aims to simplify common development patterns by providing reusable logic for components, models, and modular workflows.

## Table of Contents

- [General Usage Guide](usage.md)
- [Component System](./components/index.md)
- [Advanced Features](./components/features.md)
- [Pipelines & Plugins](./pipelines/pipelines.md)
- [Models Reference](./pipelines/models.md)
- [Managers Reference](./pipelines/managers.md)
- [Services Reference](./pipelines/services.md)
- [Filters Reference](./pipelines/filters.md)
- [Forms Reference](forms.md)
- [Authentication Backends](backends.md)
- [Core Utilities](utils.md)
- [Routing (Routes)](routes.md)

## Key Concepts

- **Plugin Components**: Reusable, atomic pieces of functionality (like UI blocks).
- **Plugins & Pipelines**: Workflow-driven model behaviors (signals, events).
- **Contrib**: Generic utilities and helpers.

## Getting Started

1.  **Install**: `pip install django-grep`
2.  **Configure**: Add `django_grep.components` and `django_grep.pipelines` to `INSTALLED_APPS`.
3.  **Use**: Import from `django_grep.*`.

See [Usage Guide](usage.md) for detailed instructions.
