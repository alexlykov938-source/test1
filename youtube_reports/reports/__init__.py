"""
Reports package.

Each module in this package registers its report class via the @register
decorator. Import them here so the registry is populated when the package
is loaded.
"""

from . import clickbait  # noqa: F401
from .base import get_report, register  # noqa: F401

__all__ = ["get_report", "register"]
