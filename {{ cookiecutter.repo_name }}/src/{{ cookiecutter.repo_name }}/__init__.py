"""Package initialization for the generated project.

Expose the most useful symbols from the package so notebooks can import
directly from the package without modifying `sys.path`.
"""

from .project_configs import ProjectPaths
from .project_logger import logger

__all__ = ["ProjectPaths", "logger"]
