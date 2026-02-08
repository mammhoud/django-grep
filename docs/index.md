# Django GREP Documentation

Welcome to the documentation for **Django GREP** (Generic Reusable Enhanced Pipelines).

## Overview

Django GREP is a collection of enhancing utilities and components for Django and Wagtail projects. It aims to simplify common development patterns by providing reusable logic for components, models, and workflows.

## Table of Contents

- [Integration Guide](usage.md)
- [Components System](components.md)
- [Pipelines & Models](pipelines.md)
- [Core Utilities](utils.md)
- [Routing (Routes)](routes.md)

## Key Concepts

- **Components**: Reusable, atomic pieces of functionality (like UI blocks).
- **Pipelines**: Workflow-driven model behaviors (signals, events).
- **Contrib**: Generic utilities and helpers.

## Getting Started

1.  **Install**: `pip install django-grep`
2.  **Configure**: Add `django_grep.components` and `django_grep.pipelines` to `INSTALLED_APPS`.
3.  **Use**: Import from `django_grep.*`.

See [Usage Guide](usage.md) for detailed instructions.
