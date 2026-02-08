# Forms Documentation

## Overview

The forms module (`django_grep.pipelines.forms`) provides enhanced form classes with built-in styling support for multiple frameworks (Bootstrap 5, Tailwind CSS), security features, and layout management.

## Base Forms

### `BaseStyledForm`

**Location:** `django_grep.pipelines/forms/base.py`

**Purpose:** Base class providing styling configuration for both Bootstrap and Tailwind.

#### Features
- **Dual-Framework Support**: Switch between Bootstrap 5 and Tailwind CSS via settings.
- **Auto-Styling**: Automatically detects field types (e.g., password, email, date) and applies appropriate classes.
- **Validation Styling**: Helpers for valid/invalid states and feedback messages.
- **Button Styling**: Configurable button styles (primary, secondary, outline, etc.).

#### Configuration

To configure the styling framework globally, add to your `settings.py`:

```python
STYLES_FRAMEWORK = "bootstrap"  # or "tailwind"
STYLES_PREFIX = ""  # transform "btn" to "prefix-btn" if needed
```

#### Usage

```python
from django_grep.pipelines.forms.base import BaseStyledForm

class MyForm(BaseStyledForm):
    name = forms.CharField()
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fields are automatically styled on init
        self.apply_button_styling()
```

---

## Form Mixins

### `SecurityMixin`

**Location:** `django_grep.pipelines/forms/mixins.py`

**Purpose:** Adds security features to forms to prevent spam and replay attacks.

**Features:**
- **Honeypot Field**: `security_check` field hidden from users but visible to bots.
- **Timestamp Hash**: Prevents replay attacks by validating form submission time.

### `LayoutMixin`

**Location:** `django_grep.pipelines/forms/mixins.py`

**Purpose:** Provides layout configuration using `crispy-forms`.

**Methods:**
- `setup_layout(fields, submit_text=None, show_links=True)`: Quick setup for common form layouts.
- `get_form_helper()`: Returns a configured `FormHelper`.

### `ValidationMixin`

**Location:** `django_grep.pipelines/forms/mixins.py`

**Purpose:** Enhanced validation feedback.

**Methods:**
- `add_error_highlighting()`: Adds CSS error classes to invalid fields.
- `get_field_with_errors()`: Renders field with attached error message.

---

## Authentication Forms

**Location:** `django_grep.pipelines/forms/authentication/`

Pre-built forms for common authentication flows.

### Available Forms

| Form | Purpose |
|------|---------|
| `LoginForm` | User login with support for multiple backends |
| `SignupForm` | User registration |
| `ChangePasswordForm` | Password change for authenticated users |
| `ResetPasswordForm` | Request password reset email |
| `SetPasswordForm` | Set new password (after reset) |
| `VerifyCodeForm` | Verify MFA or login code |
| `VerifyPhoneForm` | Verify phone number |

### Usage Example

```python
from django_grep.pipelines.forms.authentication import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        login(request, form.user)
        return redirect("home")
    return render(request, "login.html", {"form": form})
```
