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

**When to Use:**
- ✅ Frequently accessed data.
- ✅ Performance critical queries.
- ✅ High read, low write operations.
- ✅ Expensive calculations.

**Cache Duration Guidelines:**
- User data: 30-60 minutes.
- Configuration: 1-24 hours.
- Static content: 24+ hours.
- Real-time data: 1-5 minutes.

#### Configuration

```python
CACHE_PREFIX = "cache_manager"
DEFAULT_CACHE_TIMEOUT = 3600  # 1 hour
```

#### Key Methods

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

---

## 🔍 Search Support

### `SearchManagerMixin`

**Location:** `django_grep.pipelines/managers/search.py`

**Purpose:** Adds full-text search and autocomplete capabilities to managers.

**When to Use:**
- ✅ Full-text search needed across multiple fields.
- ✅ Autocomplete features for UI inputs.
- ✅ Relevance scoring (PostgreSQL GIN indexes).

**Weighting & Minimum Score:**
```python
SEARCH_FIELDS = ['title', 'content', 'summary']
SEARCH_WEIGHTS = {'title': 2.0, 'summary': 1.5, 'content': 1.0}
SEARCH_MIN_SCORE = 0.3
```

#### Key Methods

```python
# Full-text search with scoring
def search(self, query: str, filters: Dict[str, Any] = None,
           limit: int = 20, offset: int = 0) -> QuerySet

# Autocomplete suggestions
def autocomplete(self, query: str, limit: int = 10) -> List[Dict]
```
