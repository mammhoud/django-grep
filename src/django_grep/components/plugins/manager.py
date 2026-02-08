from __future__ import annotations

import importlib

import pluggy

from ..plugins import hookspecs

pm = pluggy.PluginManager("django_grep.components")
pm.add_hookspecs(hookspecs)

pm.load_setuptools_entrypoints("django-block")

DEFAULT_PLUGINS: list[str] = [
    "core.conf",
    "django_grep.components.staticfiles",
    "django_grep.components.templates",
]

for plugin in DEFAULT_PLUGINS:
    mod = importlib.import_module(plugin)
    pm.register(mod, plugin)
