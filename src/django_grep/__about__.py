"""
@author Mahmoud Ezzat
@requires Python 3.11 or later

Copyright (c) 2024
All rights reserved.
"""

__version__ = "1.0.3"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)

__name__ = "django-grep"
__description__ = "Generic Reusable Enhanced Pipelines for Django and Wagtail"
