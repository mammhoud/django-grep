# Routes Module Usage

This module provides the core routing and viewset functionality for building dynamic interfaces in Django and Wagtail.

## Classes

### BaseViewset
- **File**: `base.py`
- **Description**: The base class for all viewsets. Provides basic routing logic.

### Viewset
- **File**: `base.py`
- **Description**: Standard Viewset class for handling common view operations.

### Route
- **File**: `base.py`
- **Description**: Represents a defined route within a viewset.

### IndexViewMixin
- **File**: `base.py`
- **Description**: Mixin to add index view capabilities to a viewset.

### Application
- **File**: `sites.py`
- **Description**: Represents an application structure with multiple sites/routes.

### Site
- **File**: `sites.py`
- **Description**: Represents a site configuration within an application.

### AppMenuMixin
- **File**: `sites.py`
- **Description**: Mixin for handling application menus.

## Planned/Future Viewsets & Mixins

The following components were previously commented out in `__init__.py` and are preserved here for future implementation:

### Model-Based Viewsets and Mixins
```python
# from .model import (
# 	# BaseModelViewset,
# 	# CreateViewMixin,
# 	# DeleteViewMixin,
# 	# DetailViewMixin,
# 	# ListBulkActionsMixin,
# 	# ModelViewset,
# 	# ReadonlyModelViewset,
# 	# UpdateViewMixin,
# )
```

### Module Exports (__all__)
```python
# __all__ = [
# 	"BaseModelViewset",
# 	"BaseViewset",
# 	# "DeleteViewMixin",
# 	# "DetailViewMixin",
# 	# "CreateViewMixin",
# 	# "UpdateViewMixin",
# 	# "ListBulkActionsMixin",
# 	# "ModelViewset",
# 	# "ReadonlyModelViewset",
# 	"Viewset",
# 	"ViewsetMeta",
# 	"IndexViewMixin",
# 	"route",
# 	"Route",
# 	"Site",
# 	"Application",
# 	"AppMenuMixin",
# 	"menu_path",
# ]
```
