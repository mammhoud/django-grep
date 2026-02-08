# Core Utilities

A collection of utility functions and classes to streamline Django development.

## Generic Utilities (`django_grep.contrib.utils`)

This module includes helpers for common tasks such as:

-   `unique_ordered(seq)`: deduplicates sequences while preserving order.
-   `slugify(text)`: robust slug generation beyond standard Django slugify.
-   `get_object_or_none(model, **kwargs)`: exception-safe model retrieval.

## Enums (`django_grep.contrib.enums`)

A set of reusable enums for common choices in models/application logic:

-   `Environment`: Development, Staging, Production.
-   `LogLevel`: Standard logging levels.
-   `Direction`: Enum for orientation/direction (LTR/RTL).
-   `Workflow`: State workflow definition (Draft, Review, Published).
-   `Module`: Component modularity helpers.
-   `Runtime`: Runtime environment detection.

These enums can be used across your models for consistent choices.

## Application Settings (`django_grep.conf_utils`)

A centralized way to manage application-specific settings, defaulting to sensible values but overrideable via Django settings.

```python
from django_grep.conf_utils import app_settings

if app_settings.ENABLE_FEATURE_X:
    # Feature X logic
```

## Typing (`django_grep.typing`)

Type aliases and generic types for modern Python type hinting support, compliant with correct `typing` or `typing_extensions` imports based on Python version.

## Testing Setup

Testing utilities are also provided, simplifying test case creation (e.g., creating test users, mocking requests).
