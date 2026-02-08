"""Enhanced utility functions for Django applications."""

import json
import re
from collections.abc import Callable, Iterator
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from functools import wraps
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

from .utils import *

# Constants
TRUE_VALUES = {
    "1",
    "true",
    "True",
    "TRUE",
    "on",
    "yes",
    "active",
    "Active",
    "ok",
    "OK",
    "success",
    "Success",
    "enable",
    "Enable",
    "enabled",
    "Enabled",
    "y",
    "Y",
}

FALSE_VALUES = {
    "0",
    "false",
    "False",
    "FALSE",
    "off",
    "no",
    "inactive",
    "Inactive",
    "disabled",
    "Disabled",
    "n",
    "N",
    "none",
    "None",
}

NULL_VALUES = {"null", "Null", "NULL", "nil", "Nil", "NIL", "undefined"}


class MARKER:
    """A sentinel value marker for special placeholder values."""

    __slots__ = ("marker",)

    def __init__(self, marker: str):
        self.marker = marker

    def __iter__(self) -> Iterator:
        return iter(())

    def __repr__(self) -> str:
        return f"<MARKER: {self.marker}>"

    def __str__(self) -> str:
        return self.marker

    def __bool__(self) -> bool:
        return False

    def __lt__(self, other: Any) -> bool:
        return self.marker < str(other)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MARKER) and self.marker == other.marker

    def __hash__(self) -> int:
        return hash(self.marker)


DEFAULT = MARKER("DEFAULT")
MISSING = MARKER("MISSING")
NOT_SET = MARKER("NOT_SET")


# Type variables for generic functions
T = TypeVar("T")
E = TypeVar("E", bound=Enum)
ModelType = TypeVar("ModelType", bound=models.Model)


# Environment variable utilities
def env_to_enum(enum_cls: type[E], value: Any, default: E | None = None) -> E:
    """
    Convert environment variable value to enum instance.

    Args:
        enum_cls: Enum class to convert to
        value: Value to convert
        default: Default value if conversion fails (optional)

    Returns:
        Enum instance

    Raises:
        ImproperlyConfigured: If value not found in enum and no default provided
    """
    if value is None:
        if default is not None:
            return default
        raise ImproperlyConfigured(
            f"Value is None and no default provided for {enum_cls.__name__}"
        )

    # Handle enum instances
    if isinstance(value, enum_cls):
        return value

    # Try to match by value
    for enum_member in enum_cls:
        if enum_member.value == value:
            return enum_member

    # Try to match by name (case-insensitive)
    value_str = str(value).upper()
    for enum_member in enum_cls:
        if enum_member.name.upper() == value_str:
            return enum_member

    if default is not None:
        return default

    valid_values = [member.value for member in enum_cls]
    raise ImproperlyConfigured(
        f"Env value {value!r} could not be found in {enum_cls.__name__}. "
        f"Valid values: {valid_values}"
    )


def env_to_bool(value: Any, default: bool = False) -> bool:
    """
    Convert environment variable to boolean.

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        Boolean value
    """
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    value_str = str(value).strip()

    if value_str in TRUE_VALUES:
        return True
    elif value_str in FALSE_VALUES:
        return False
    elif value_str in NULL_VALUES:
        return default

    try:
        # Try numeric conversion
        num_val = float(value_str)
        return bool(num_val)
    except (ValueError, TypeError):
        return default


def env_to_list(value: Any, separator: str = ",", strip: bool = True) -> list[str]:
    """
    Convert environment variable to list of strings.

    Args:
        value: Value to convert
        separator: Separator character (default: ",")
        strip: Whether to strip whitespace from items

    Returns:
        List of strings
    """
    if value is None:
        return []

    if isinstance(value, list):
        return value

    value_str = str(value).strip()
    if not value_str:
        return []

    items = value_str.split(separator)

    if strip:
        items = [item.strip() for item in items if item.strip()]
    else:
        items = [item for item in items if item]

    return items


def env_to_int(value: Any, default: int | None = None) -> int | None:
    """
    Convert environment variable to integer.

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        Integer value or default

    Raises:
        ImproperlyConfigured: If value cannot be converted and no default provided
    """
    if value is None:
        if default is not None:
            return default
        raise ImproperlyConfigured("Value is None and no default provided")

    try:
        return int(value)
    except (ValueError, TypeError):
        if default is not None:
            return default
        raise ImproperlyConfigured(f"Cannot convert {value!r} to integer")


# Boolean utilities
def is_true(val: str | bool | int | None) -> bool:
    """
    Check if a value represents True.

    Supports strings, booleans, integers, and None.
    Integer 0 is False, any other integer is True.

    Args:
        val: Value to check

    Returns:
        True if value represents a truthy value
    """
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return bool(val)
    if isinstance(val, str):
        return val.strip().lower() in TRUE_VALUES
    return bool(val)


def parse_boolean(value: Any, strict: bool = False) -> bool | None:
    """
    Parse a value to boolean with support for None.

    Args:
        value: Value to parse
        strict: If True, raise ValueError for unparsable values

    Returns:
        Boolean value or None

    Raises:
        ValueError: If strict=True and value cannot be parsed
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return bool(value)

    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in TRUE_VALUES:
            return True
        elif value_lower in FALSE_VALUES:
            return False
        elif value_lower in NULL_VALUES:
            return None

    if strict:
        raise ValueError(f"Cannot parse {value!r} as boolean")

    return None


# String manipulation utilities
def camel_case_to_underscore(name: str) -> str:
    """
    Convert camel-cased string to underscore-separated string.

    Examples:
        >>> camel_case_to_underscore('SomeString')
        'some_string'
        >>> camel_case_to_underscore('HTMLParser')
        'html_parser'
        >>> camel_case_to_underscore('URLHelper')
        'url_helper'
    """
    if not name:
        return name

    # Handle acronyms at the beginning
    name = re.sub(r"^([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    # Handle rest of the string
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", name)

    return name.lower()


def camel_case_to_title(name: str) -> str:
    """
    Convert camel-cased string to title-cased string.

    Examples:
        >>> camel_case_to_title('SomeString')
        'Some String'
        >>> camel_case_to_title('getHTMLContent')
        'Get HTML Content'
    """
    if not name:
        return name

    # Insert spaces before capital letters
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    name = re.sub(r"([A-Z])([A-Z][a-z])", r"\1 \2", name)

    return name.title()


def title_from_name(name: str) -> str:
    """
    Convert various naming conventions to title case.

    Examples:
        >>> title_from_name('some_string')
        'Some String'
        >>> title_from_name('some-string')
        'Some String'
        >>> title_from_name('SomeString')
        'Some String'
    """
    if not name:
        return name

    # Replace underscores and hyphens with spaces
    name = re.sub(r"[_-]", " ", name)
    # Add spaces for camel case
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)

    return name.title()


def strip_suffixes(word: str, suffixes: list[str]) -> str:
    """
    Strip specified suffixes from a word.

    Never strips the entire word. Suffixes are stripped in the order provided.

    Args:
        word: Word to strip suffixes from
        suffixes: List of suffixes to strip

    Returns:
        Word with suffixes stripped
    """
    if not word or not suffixes:
        return word

    for suffix in sorted(suffixes, key=len, reverse=True):
        if word == suffix:
            continue
        if word.endswith(suffix):
            word = word[: -len(suffix)]
            break

    return word


def truncate_string(value: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.

    Args:
        value: String to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncated

    Returns:
        Truncated string
    """
    if len(value) <= max_length:
        return value

    if max_length <= len(suffix):
        return suffix[:max_length]

    return value[: max_length - len(suffix)] + suffix


# Object and model utilities
def has_object_perm(
    user,
    short_perm_name: str,
    model: type[ModelType],
    obj: ModelType | None = None,
) -> bool:
    """
    Check if user has permission for a model or object.

    Checks model-level permission first, then object-level permission if obj is provided.

    Args:
        user: User to check permissions for
        short_perm_name: Short permission name (e.g., 'add', 'change', 'delete', 'view')
        model: Django model class
        obj: Optional object instance for object-level permission

    Returns:
        True if user has permission
    """
    if not user or not user.is_authenticated:
        return False

    perm_name = (
        f"{model._meta.app_label}."
        f"{auth.get_permission_codename(short_perm_name, model._meta)}"
    )

    # Check model-level permission
    if user.has_perm(perm_name):
        return True

    # Check object-level permission if obj provided
    if obj is not None and user.has_perm(perm_name, obj=obj):
        return True

    return False


def get_object_data(obj: ModelType) -> Iterator[tuple[models.Field, str, Any]]:
    """
    Generate field data for an object with choice fields expanded.

    Returns:
        Iterator of (field, label, value) tuples
    """
    for field in obj._meta.fields:
        # Skip auto fields and auto-created fields
        if isinstance(field, models.AutoField) or field.auto_created:
            continue

        # Get field value with choice expansion
        if hasattr(obj, f"get_{field.name}_display"):
            value = getattr(obj, f"get_{field.name}_display")()
        else:
            value = getattr(obj, field.name)

        # Skip None values
        if value is None:
            continue

        yield (field, field.verbose_name.capitalize(), value)


def model_field_names(model_class: type[ModelType]) -> list[str]:
    """
    Get all field names for a model.

    Args:
        model_class: Django model class

    Returns:
        List of field names
    """
    return [field.name for field in model_class._meta.fields]


def validate_required_fields(
    data: dict[str, Any],
    required_fields: list[str],
    error_class: type[Exception] = ValidationError,
) -> None:
    """
    Validate that required fields are present in data.

    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        error_class: Exception class to raise

    Raises:
        error_class: If any required field is missing
    """
    missing_fields = [
        field for field in required_fields if field not in data or data[field] is None
    ]

    if missing_fields:
        raise error_class(f"Missing required fields: {', '.join(missing_fields)}")


# Path and URL utilities
PATH_PARAMETER_COMPONENT_RE = re.compile(
    r"<(?:(?P<converter>[^>:]+):)?(?P<parameter>[^>]+)>"
)


def list_path_components(route: str) -> list[str]:
    """
    Extract parameter names from Django path expression.

    Examples:
        >>> list_path_components('/prefix/<str:pk>')
        ['pk']
        >>> list_path_components('<str:pk>/<int:id>/<slug:slug>')
        ['pk', 'id', 'slug']
    """
    return [match["parameter"] for match in PATH_PARAMETER_COMPONENT_RE.finditer(route)]


def extract_path_params(route: str) -> list[tuple[str, str | None]]:
    """
    Extract converters and parameters from Django path expression.

    Returns:
        List of (parameter, converter) tuples
    """
    return [
        (match["parameter"], match["converter"])
        for match in PATH_PARAMETER_COMPONENT_RE.finditer(route)
    ]


# Value selection utilities
def first_not_default(*args: Any, default: Any = DEFAULT) -> Any:
    """
    Return the first argument that is not the `DEFAULT` marker.

    Args:
        *args: Arguments to check
        default: Default marker to skip (default: DEFAULT)

    Returns:
        First non-default argument or last argument if all are default
    """
    if not args:
        return None

    for arg in args:
        if arg is not default:
            return arg

    return args[-1] if args else None


def first_truthy(*args: Any, default: Any = None) -> Any:
    """
    Return the first truthy argument.

    Args:
        *args: Arguments to check
        default: Default value if no truthy argument found

    Returns:
        First truthy argument or default
    """
    for arg in args:
        if arg:
            return arg

    return default


def coalesce(*args: Any, skip_none: bool = True) -> Any:
    """
    Return the first non-None (or non-skipped) value.

    Args:
        *args: Arguments to check
        skip_none: Whether to skip None values

    Returns:
        First non-skipped value or None
    """
    for arg in args:
        if arg is not None or not skip_none:
            return arg

    return None


# JSON utilities
def safe_json_loads(
    json_string: str,
    default: Any = None,
    raise_exception: bool = False,
) -> Any:
    """
    Safely load JSON string with error handling.

    Args:
        json_string: JSON string to parse
        default: Default value if parsing fails
        raise_exception: Whether to raise exception on failure

    Returns:
        Parsed JSON or default value

    Raises:
        json.JSONDecodeError: If raise_exception=True and parsing fails
    """
    if not json_string:
        return default

    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        if raise_exception:
            raise
        return default


def json_serializer(obj: Any) -> Any:
    """
    Extended JSON serializer supporting common Python types.

    Supports: datetime, date, Decimal, Enum, MARKER
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, MARKER):
        return str(obj)
    elif hasattr(obj, "__dict__"):
        return obj.__dict__

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class viewprop:
    """
    A property that can be overridden.

    The viewprop class is a descriptor that works similarly to the built-in
    `property` decorator but allows its value to be overridden on instances
    of the class it is used in.
    """

    def __init__(self, func: Any):
        self.__doc__ = func.__doc__
        self.fget = func
        self.__name__ = func.__name__

    def __get__(self, obj: Any | None, objtype: type[Any] | None = None) -> Any:
        if obj is None:
            return self
        if self.fget.__name__ not in obj.__dict__:
            obj.__dict__[self.fget.__name__] = self.fget(obj)
        return obj.__dict__[self.fget.__name__]

    def __set__(self, obj: Any, value: Any) -> None:
        obj.__dict__[self.fget.__name__] = value

    def __delete__(self, obj: Any) -> None:
        obj.__dict__.pop(self.fget.__name__, None)

    def __repr__(self) -> str:
        return f"<view_property func={self.fget}>"


# Type checking utilities
def is_optional_type(type_hint: Any) -> bool:
    """
    Check if a type hint is Optional (Union with None).

    Args:
        type_hint: Type hint to check

    Returns:
        True if type is Optional
    """
    origin = get_origin(type_hint)
    if origin is Union:
        args = get_args(type_hint)
        return type(None) in args
    return False


def get_optional_type(type_hint: Any) -> Any:
    """
    Get the non-None type from Optional type hint.

    Args:
        type_hint: Type hint to extract from

    Returns:
        Non-None type or original type
    """
    if is_optional_type(type_hint):
        args = get_args(type_hint)
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return non_none_args[0]
    return type_hint


# Decoration utilities
def memoize(func: Callable) -> Callable:
    """
    Memoization decorator for functions.

    Caches results based on function arguments.
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """
    Retry decorator for functions that may fail.

    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts in seconds
        backoff: Multiplier for delay after each attempt
        exceptions: Exception types to catch and retry
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        import time

                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception

        return wrapper

    return decorator


# Greetings
GREETINGS = lazy(
    lambda: [
        _("Fantastic!"),
        _("That looks awesome!"),
        _("You are looking very well today!"),
        _("I totally admire your spontaneity."),
        _("I like your new haircut."),
        _("What a beautiful costume!"),
        _("You look very good in that suit"),
        _("I love your style."),
        _("I love your hair today"),
        _("What a beautiful outfit!"),
        _("That color is perfect on you!"),
        _("You have a great smile!"),
        _("Your positivity is infectious!"),
        _("You're doing an amazing job!"),
        _("I appreciate your hard work."),
        _("You make a difference!"),
        _("Your effort is paying off!"),
        _("You're crushing it!"),
        _("Keep up the excellent work!"),
        _("You're inspiring!"),
    ],
    list,
)()
