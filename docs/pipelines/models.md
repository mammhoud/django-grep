# Models Documentation

## Base Models

### `DefaultBase`

**Location:** `django_grep.pipelines/models/default.py`

**Purpose:** Enhanced abstract base model with UUID, timestamps, audit fields, and Wagtail admin integration.

**When to Use:**
- ✅ Most common use case for business entities.
- ✅ Need audit trails (`created_by`, `updated_by`).
- ✅ Need soft delete functionality (`is_active`).
- ✅ Need publication workflow (`published`, `published_at`).
- ✅ Standard CRUD operations with UUID primary keys.

**Includes:**
- UUID primary key (UUID4).
- Timestamps (`created_at`, `updated_at`).
- Soft delete flag.
- Audit fields (ForeignKeys to User).
- Wagtail admin integration (automatic panels).

#### Fields
| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `id` | UUIDField | Primary key | auto-generated UUID4 |
| `created_at` | DateTimeField | Record creation timestamp | auto_now_add |
| `updated_at` | DateTimeField | Last update timestamp | auto_now |
| `is_active` | BooleanField | Soft delete flag | `True` |
| `created_by` | ForeignKey(User) | User who created record | nullable |
| `updated_by` | ForeignKey(User) | User who last updated | nullable |
| `published` | BooleanField | Publication status | `False` |
| `published_at` | DateTimeField | Publication timestamp | nullable |
| `unpublished_at` | DateTimeField | Unpublication timestamp | nullable |

#### Key Methods

```python
# Soft Delete
def soft_delete(self):
    """Soft delete by setting is_active to False."""

# Restore
def restore(self):
    """Restore a soft-deleted record."""

# Publish
def publish(self):
    """Publish the record."""

# Unpublish
def unpublish(self):
    """Unpublish the record."""
```

### `EnhancedBase`

**Location:** `django_grep.pipelines/models/default.py`

**Purpose:** Enhanced base model combining `DefaultBase` and `TemplateRenderMixin` with versioning.

**When to Use:**
- ✅ Need version tracking and revision history.
- ✅ Email template rendering (`TemplateRenderMixin`).
- ✅ Compliance/audit requirements (knowing what changed and when).
- ✅ Document management (contracts, agreements).

**Includes:**
- All `DefaultBase` features.
- Version tracking and revision creation.
- Template rendering logic.
- Email sending integration.

#### Additional Fields
| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `version` | PositiveIntegerField | Record version number | `1` |

#### Key Methods

```python
# Auto-increment version
def save(self, *args, **kwargs):
    """Increment version on save"""

# Create revision
def create_revision(self):
    """Create a revision/snapshot of the object"""

# Render template
def render_template(self, template_name, context=None):
    """Render an email template for this object"""

# Send email
def send_template_email(self, template_name, recipients, context=None):
    """Send email using a template"""
```

---

## User Models

### `Person` (Profile Model)

**Location:** `django_grep.pipelines/models/users/users.py`

**Purpose:** Comprehensive profile model extending the Django User system with one-to-one relationship.

#### Key Fields

| Category | Fields |
|----------|--------|
| **Identity** | `id` (UUID), `user` (OneToOne), `slug` |
| **Personal** | `first_name`, `last_name`, `full_name`, `display_name`, `birth_date`, `gender` |
| **Contact** | `email`, `phone_number`, `alternate_email`, `alternate_phone` |
| **Location** | `address`, `country`, `city`, `postal_code`, `location` |
| **Professional** | `job_title`, `company`, `department`, `position`, `industry`, `bio` |
| **Social** | `website`, `linkedin_url`, `github_url`, `twitter_url`, `facebook_url`, `instagram_url` |
| **Privacy** | `public_profile`, `profile_visibility`, `share_usage_data`, `show_email`, `allow_contact` |
| **Status** | `profile_type`, `status`, `is_registered`, `registration_date` |
| **Verification** | `is_email_verified`, `email_verified_at`, `is_phone_verified`, `phone_verified_at` |
| **Preferences** | `language`, `timezone`, `email_notifications`, `newsletter_notifications` |
| **UI** | `dark_mode`, `high_contrast`, `reduce_animations`, `ui_density` |
| **Subscription** | `subscription_plan`, `billing_cycle`, `payment_method`, `auto_renew` |
| **Activity** | `last_active`, `last_profile_update`, `login_count`, `profile_completion` |
| **Media** | `profile_image`, `cover_image`, `profile_content` (StreamField) |

#### Enums

```python
class ProfileType(models.TextChoices):
    EMPLOYEE = "EMP", "Employee"
    STUDENT = "STU", "Student"
    CUSTOMER = "CUS", "Customer"
    SUPPLIER_CONTACT = "SUP", "Supplier Contact"
    PARTNER_CONTACT = "PRT", "Partner Contact"
    CONTACT = "CON", "Contact Person"
    GUEST = "GST", "Guest"
    ADMINISTRATOR = "ADM", "Administrator"
    OTHER = "OTH", "Other"

class Status(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    SUSPENDED = "SUSPENDED", "Suspended"
    PENDING = "PENDING", "Pending Approval"
    INVITED = "INVITED", "Invited"
    ARCHIVED = "ARCHIVED", "Archived"
```

---

## Contact Models

### `BaseContact`

**Location:** `django_grep.pipelines/models/contacts/base.py`

**Purpose:** Base model for all contact-related models.

#### Key Features

- Extends `ClusterableModel` (Wagtail)
- Includes contact validation
- Phone and email validators
- Address fields

---

## Cache Mixins

### `ModelCacheMixin`

**Location:** `django_grep.pipelines/models/cache.py`

**Purpose:** Mixin to add caching capabilities to Django models.

#### Methods

```python
# Cache this instance
def cache_set(self, timeout: int | None = None) -> bool

# Get cached instance by identifier
@classmethod
def cache_get(cls, identifier: Any) -> Any | None

# Get from cache or fetch from database
@classmethod
def get_or_cache(cls, identifier: Any, **kwargs) -> Any | None

# Invalidate all cache for this model
def invalidate_all_cache(self) -> int
```


---

## Workspace Models

### `Workspace`

**Location:** `django_grep.pipelines/models/workspace.py`

**Purpose:** Multi-tenancy workspace management.

#### Key Fields

- `name`: Workspace name
- `slug`: URL-friendly identifier
- `owner`: ForeignKey to User
- `members`: ManyToMany to User
- `settings`: JSONField for workspace settings
- `is_active`: Status flag
