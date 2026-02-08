# Services Documentation

## Base Service

### `BaseService`

**Location:** `django_grep.pipelines/services/base.py`

**Purpose:** Abstract base service providing standard CRUD operations and hooks.

#### Class Attributes

```python
model_class: Type[models.Model] = None  # Model this service operates on
service_name: str = None  # Name for service registry (optional)
```

#### Initialization

```python
def __init__(self, model_class: Type[models.Model] = None):
    """
    Initialize service with model class.
    Auto-registers if service_name is set.
    """
```

#### Core Methods

##### Get

```python
def get(self, identifier: Any, **kwargs) -> Optional[models.Model]:
    """Get object by identifier."""
```

##### Create

```python
def create(self, data: Dict[str, Any], **kwargs) -> models.Model:
    """Create new object."""
```

##### Update

```python
def update(self, identifier: Any, data: Dict[str, Any], **kwargs) -> Optional[models.Model]:
    """Update existing object."""
```

##### Delete

```python
def delete(self, identifier: Any, **kwargs) -> bool:
    """Delete object."""
```

##### List

```python
def list(self, filters: Dict[str, Any] = None, ordering: List[str] = None,
         limit: int = None, offset: int = 0, **kwargs) -> Dict[str, Any]:
    """List objects with pagination."""
```

---

## CRUD Service

### `CRUDService`

**Location:** `django_grep.pipelines/services/crud.py`

**Purpose:** Enhanced CRUD service with validation and error handling.

**Additional Features:**
- Input validation
- Field-level permissions
- Bulk operations
- Transaction support

**Usage:**
```python
from django_grep.pipelines.services import CRUDService

class PersonService(CRUDService):
    model_class = Person

    # Define allowed fields for create/update
    create_fields = ['first_name', 'last_name', 'email', 'phone']
    update_fields = ['first_name', 'last_name', 'phone', 'location']

    def validate_input(self, data, operation):
        """Custom validation."""
        if operation == 'create' and 'email' not in data:
            return {'valid': False, 'errors': ['email is required']}
        return {'valid': True, 'data': data}
```

---

## Service Hooks

### Hook Lifecycle

```
run() called
    ↓
    before_execute() - Pre-execution hook
    ↓
    execute() - Main operation
    ↓
    after_execute() - Post-execution hook
    ↓
    Return result
```

### Hook Methods

#### before_execute

```python
def before_execute(self, operation: str, **kwargs) -> Dict[str, Any]:
    """
    Hook executed before service operation.
    Can modify kwargs before execution.
    """
```

#### after_execute

```python
def after_execute(self, operation: str, result: Any, **kwargs) -> Any:
    """
    Hook executed after service operation.
    Can modify result before returning.
    """
```

#### handle_error

```python
def handle_error(self, error: Exception, operation: str, **kwargs) -> Any:
    """
    Handle service errors.
    Can transform or log errors.
    """
```
