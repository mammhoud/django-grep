"""
Utility functions.
"""

from .cache import (
    cache_get_or_set,
    generate_cache_key,
    invalidate_cache_pattern,
    is_redis_available,
)
from .token import (
    decode_token,
    generate_token,
    validate_token,
)
from .validation import (
    validate_email,
    validate_password,
    validate_phone,
    validate_uuid,
)

__all__ = [
    "generate_cache_key",
    "cache_get_or_set",
    "invalidate_cache_pattern",
    "is_redis_available",
    "validate_token",
    "generate_token",
    "decode_token",
    "validate_email",
    "validate_phone",
    "validate_password",
    "validate_uuid",
]
