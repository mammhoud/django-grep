# ====================================
# 🔧 Debug Toolbar - Main Exports
# ====================================

# Import new modular classes
from .base import *
from .config import *
from .core import DebugToolbarSetup
from .detection import INTERNAL_IPS, get_environment_info, get_internal_ips
from .development import DevelopmentEnvironment
from .middleware import MiddlewareConfig, configure_all_middleware
from .monitoring import MonitoringSetup
from .orchestrator import DevelopmentOrchestrator
from .prometheus import PrometheusSetup
from .sentry import SentrySetup
from .urls import configure_urls

# Create singleton instances for convenience
debug_toolbar_setup = DebugToolbarSetup()
development_env = DevelopmentEnvironment()
orchestrator = DevelopmentOrchestrator()

# ====================================
# 🔄 Condition Check Callbacks
# ====================================
try:
    from core import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

from configs.settings import settings

from .config import (
    DEBUG_TOOLBAR_ENABLED,
    LIVERELOAD_ENABLED,
    SILK_ENABLED,
)


# Convenience functions
def configure_all_development_tools(**kwargs):
    """Configure all development tools."""
    return development_env.configure_all(**kwargs)


def setup_complete_environment(**kwargs):
    """Setup complete development environment."""
    return orchestrator.setup_environment(**kwargs)


def get_development_status():
    """Get development tools status."""
    return debug_toolbar_setup.get_status()


def print_development_status():
    """Print development tools status."""
    debug_toolbar_setup.print_status()


def run_livereload_server(**kwargs):
    """Run livereload server."""
    debug_toolbar_setup.run_livereload_server(**kwargs)


__all__ = [
    # ====================================
    # 📋 Configuration Constants
    # ====================================
    "ENABLE_SILK_PROFILING",
    "SILK_ENABLED",
    "SILKY_PYTHON_PROFILER",
    "SILKY_PYTHON_PROFILER_BINARY",
    "SILKY_PYTHON_PROFILER_RESULT_PATH",
    "SILKY_META",
    "SILKY_AUTHENTICATION",
    "SILKY_AUTHORISATION",
    "SILKY_MAX_RECORDED_REQUESTS",
    "SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT",
    "SILKY_INTERCEPT_PERCENT",
    "SILKY_ANALYZE_QUERIES",
    "DEBUG_TOOLBAR_ENABLED",
    "DEBUG_TOOLBAR_CONFIG",
    "DEBUG_TOOLBAR_PANELS",
    "LIVERELOAD_ENABLED",
    "DEBUG_TOOLBAR_APP",
    "SILK_APP",
    "LIVERELOAD_APP",
    "PROMETHEUS_APP",
    "DEBUG_TOOLBAR_MIDDLEWARE",
    "SILK_MIDDLEWARE",
    "LIVERELOAD_MIDDLEWARE",
    "PROMETHEUS_BEFORE_MIDDLEWARE",
    "PROMETHEUS_AFTER_MIDDLEWARE",
    "DEFAULT_MIDDLEWARE_POSITIONS",
    "BASE_DIR",
    "AUTORELOAD_WATCH_PATHS",
    # ====================================
    # 🌐 Network Detection
    # ====================================
    "get_internal_ips",
    "INTERNAL_IPS",
    "get_environment_info",
    # ====================================
    # 🔄 Condition Callbacks
    # ====================================
    "show_toolbar",
    "enable_silk",
    "enable_livereload",
    "is_debug_mode",
    "is_testing",
    # ====================================
    # 🏗️ Base Classes
    # ====================================
    "BaseSetup",
    "DevelopmentTool",
    # ====================================
    # 🛠️ Individual Tools
    # ====================================
    "DebugToolbar",
    "Silk",
    "Livereload",
    # ====================================
    # 🔧 Core Setup Classes
    # ====================================
    "DebugToolbarSetup",
    "SentrySetup",
    "PrometheusSetup",
    "MonitoringSetup",
    "DevelopmentEnvironment",
    "DevelopmentOrchestrator",
    # ====================================
    # 🌐 URL Configuration
    # ====================================
    "configure_urls",
    # ====================================
    # 🔄 Auto-reload
    # ====================================
    "configure_autoreload",
    "AutoreloadSetup",
    # ====================================
    # 🔗 Middleware
    # ====================================
    "MiddlewareConfig",
    "configure_all_middleware",
    # ====================================
    # 🚀 Singleton Instances (Recommended)
    # ====================================
    "debug_toolbar_setup",
    "development_env",
    "orchestrator",
    # ====================================
    # ⚡ Convenience Functions
    # ====================================
    "configure_all_development_tools",
    "setup_complete_environment",
    "get_development_status",
    "print_development_status",
    "run_livereload_server",
]

# ====================================
# 📝 Version Information
# ====================================
__version__ = "1.0.0"
__author__ = "Xellent Research"
__description__ = "Comprehensive Django development tools and debugging utilities"


# ====================================
# 🎯 Quick Setup Function
# ====================================
def quick_setup(
    installed_apps=None, middleware=None, debug=None, sentry_dsn=None, **kwargs
):
    """
    Quick setup function for development environment.

    Usage:
        from configs.utils.debug_toolbar import quick_setup

        config = quick_setup(
            installed_apps=INSTALLED_APPS,
            middleware=MIDDLEWARE,
            debug=DEBUG,
            sentry_dsn=os.getenv('SENTRY_DSN')
        )
    """
    if installed_apps is None or middleware is None:
        raise ValueError("installed_apps, middleware, and templates are required")

    return orchestrator.setup_environment(
        installed_apps=installed_apps,
        middleware=middleware,
        debug=debug,
        sentry_dsn=sentry_dsn,
        **kwargs,
    )


# Add quick_setup to exports
__all__.append("quick_setup")


# ====================================
# 🎪 Development Mode Check
# ====================================
def is_development_mode() -> bool:
    """
    Check if development mode is fully enabled.

    Returns:
        True if all development tools are available and debug mode is enabled
    """
    if not is_debug_mode():
        return False

    # Check if essential packages are installed
    try:
        import debug_toolbar  # noqa
        import silk  # noqa
        import livereload  # noqa

        return True
    except ImportError:
        return False


# Add to exports
__all__.append("is_development_mode")


# ====================================
# 🧪 Test Environment Check
# ====================================
def is_test_environment() -> bool:
    """
    Check if running in test environment.

    Returns:
        True if running tests
    """
    return is_testing()


# Add to exports
__all__.append("is_test_environment")


# ====================================
# 📊 System Information
# ====================================
def get_system_info() -> dict:
    """
    Get comprehensive system information.

    Returns:
        Dictionary with system and development tools information
    """
    import platform
    import sys

    import django

    base_info = {
        "python": {
            "version": sys.version,
            "executable": sys.executable,
        },
        "system": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
        },
        "django": {
            "version": django.get_version(),
        },
        "development": {
            "debug_mode": is_debug_mode(),
            "development_mode": is_development_mode(),
            "test_environment": is_test_environment(),
        },
    }

    # Add development tools status
    try:
        status = get_development_status()
        base_info["tools"] = status.get("tools", {})
        base_info["paths"] = status.get("paths", {})
    except:
        pass

    return base_info


# Add to exports
__all__.append("get_system_info")
