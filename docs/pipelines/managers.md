# Managers Documentation

## User Manager

### `UserManager`

**Location:** `django_grep.pipelines/managers/user.py`

**Purpose:** Enhanced user manager with authentication, caching, and automatic profile/person creation.

**Extends:** `CachedManager`, `BaseUserManager`

#### Key Methods

##### User Creation

```python
def create_user(self, email, password=None, **extra_fields)
    """Create regular user with automatic person and profile creation."""

def create_superuser(self, email, password=None, **extra_fields)
    """Create superuser with person and profile creation."""
```

##### Authentication

```python
def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[models.Model], str]
    """Authenticate user with security checks."""
```

##### Cached Queries

```python
def get_by_email_cached(self, email: str) -> Optional[models.Model]
    """Get user by email with caching."""

def get_by_id_cached(self, user_id: str) -> Optional[models.Model]
    """Get user by ID with caching."""
```

##### Profile Management

```python
def update_user_profile(self, user_id: str, updates: Dict[str, Any])
    -> Tuple[bool, Optional[models.Model], str]
    """Update user profile with validation and sync with person."""

def get_user_profile_context(self, user_id: str) -> Dict[str, Any]
    """Get comprehensive user information for profile context."""
```

#### Security Features

##### Login Attempt Tracking

The manager automatically tracks failed login attempts:

- **After 5 failed attempts:** Account is locked for 15 minutes
- **Successful login:** Resets failed attempt counter
- **Auto-unlock:** Account automatically unlocks after lock period

**Fields Used:**
- `failed_login_attempts` (IntegerField)
- `account_locked_until` (DateTimeField)

##### Cache Invalidation

User caches are automatically invalidated on:
- Profile updates
- Login/logout
- Email changes
- Permission changes

---

## Cache Support

### `CacheSupportMixin`

**Location:** `django_grep.pipelines/managers/base.py`

**Purpose:** Adds universal caching to BaseManager.

#### Configuration

```python
CACHE_PREFIX = "cache_manager"
DEFAULT_CACHE_TIMEOUT = 3600  # 1 hour
```

#### Key Methods

##### Cache Detection

```python
@staticmethod
def is_redis_available() -> bool
    """Check if Redis cache backend is available."""
```

##### Cached Queries

```python
# Get with cache
def get_cached(self, identifier: Any, field: str = None,
               include_related=False, force_refresh=False, **kwargs)

# Filter with cache
def filter_cached(self, filters: Dict[str, Any], ordering: List[str] = None,
                  limit: int = None, offset: int = 0,
                  include_related: bool = False, force_refresh: bool = False, **kwargs)
```

##### Cache Management

```python
# Invalidate specific cache
def invalidate_object_cache(self, obj: models.Model) -> bool

# Clear all cache for this manager
def invalidate_all_cache(self) -> bool
```
