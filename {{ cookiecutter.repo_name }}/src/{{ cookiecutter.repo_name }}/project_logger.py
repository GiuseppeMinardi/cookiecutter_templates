"""File where we generate the logger based on the configuration."""

import logging

from .project_logger import LoggerConfiguration, ProjectPaths

project_paths = ProjectPaths()
logger_config = LoggerConfiguration()
loggerdict_config = logger_config.generate(
    log_dir=project_paths.logger_folder
)
logger = logging.getLogger(logger_config.log_name)
logger.setLevel(logger_config.log_level)

