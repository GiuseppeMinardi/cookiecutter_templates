"""Package initialization for the generated project.

Expose the most useful symbols from the package so notebooks can import
directly from the package without modifying `sys.path`.
"""

import logging

from .project_configs import LoggerConfiguration, ProjectPaths

_project_paths = ProjectPaths()
_logger_config = LoggerConfiguration()
_loggerdict_config = _logger_config.generate(log_dir=_project_paths.logger_folder)
logger = logging.getLogger(_logger_config.log_name)
logger.setLevel(_logger_config.log_level)

__all__ = ["ProjectPaths", "logger"]