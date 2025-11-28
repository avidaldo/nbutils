"""NBUtils - A command-line utility for managing Jupyter notebooks.

This package provides utilities for:
- Converting between Jupyter notebooks, Python files, and Markdown
- Batch processing notebooks and Python files
- Adjusting heading levels in notebooks and markdown files

The package uses nbformat for reliable notebook manipulation.
"""

__version__ = "0.1.0"

from .core import NBUtils

__all__ = ["NBUtils"]