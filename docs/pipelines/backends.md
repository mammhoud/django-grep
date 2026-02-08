# Authentication Backends

## Overview

The backends module (`django_grep.pipelines.backends`) provides custom authentication backends to extend Django's default behavior, particularly for multi-identifier login (Email, Username, ID, Code).

## `EmailOrUsernameModelBackend`

**Location:** `django_grep.pipelines/backends/auth.py`

**Purpose:** A flexible authentication backend that allows users to log in using multiple identifiers. It extends `allauth.account.auth_backends.AuthenticationBackend`.

### Features

- **Multi-Identifier Login**: Authenticate using:
    - Email address
    - Username
    - User ID (UUID)
    - Custom `code` field (e.g., specific employee ID or reference code)
- **Performance Optimization**: Uses `select_related` and `prefetch_related` to fetch the user's profile, groups, and permissions in a single query upon authentication.
- **Security**: Inherits timing attack mitigation and password throttling from `django-allauth`.

### Installation

Add the backend to your `AUTHENTICATION_BACKENDS` setting in `settings.py`:

```python
AUTHENTICATION_BACKENDS = [
    # ...
    "django_grep.pipelines.backends.auth.EmailOrUsernameModelBackend",
    "django.contrib.auth.backends.ModelBackend", # Optional fallback
    # ...
]
```

### Usage

Once configured, standard Django authentication functions will utilize this backend.

```python
from django.contrib.auth import authenticate, login

# User can enter email, username, or ID
user = authenticate(request, username="user@example.com", password="secret_password")

if user:
    login(request, user)
```

### Extension

To add more identifiers (e.g., phone number), extend the class:

```python
from django_grep.pipelines.backends.auth import EmailOrUsernameModelBackend
from django.db.models import Q

class ExtendedAuthBackend(EmailOrUsernameModelBackend):
    def authenticate(self, request, **credentials):
        username = credentials.get("username")
        # Add phone number query
        # ... logic to include Q(phone_number=username) ...
        return super().authenticate(request, **credentials)
```
