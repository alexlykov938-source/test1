"""Base class and registry for reports."""

from abc import ABC, abstractmethod


class BaseReport(ABC):
    """Abstract base class for all report types."""

    @abstractmethod
    def filter(self, rows: list[dict]) -> list[dict]:
        """Filter rows relevant for this report."""

    @abstractmethod
    def sort(self, rows: list[dict]) -> list[dict]:
        """Sort filtered rows."""

    @property
    @abstractmethod
    def columns(self) -> list[str]:
        """Columns to display in the report."""

    def generate(self, rows: list[dict]) -> list[dict]:
        """Run filter + sort and return report rows."""
        return self.sort(self.filter(rows))


# Registry mapping report name -> report class
_REGISTRY: dict[str, type[BaseReport]] = {}


def register(name: str):
    """Decorator to register a report class under a given name."""
    def decorator(cls: type[BaseReport]) -> type[BaseReport]:
        _REGISTRY[name] = cls
        return cls
    return decorator


def get_report(name: str) -> BaseReport:
    """Return an instance of the report for the given name."""
    if name not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY))
        raise ValueError(
            f"Unknown report '{name}'. Available reports: {available}"
        )
    return _REGISTRY[name]()
