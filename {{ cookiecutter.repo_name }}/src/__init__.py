import logging
from logging.config import dictConfig

from .project_configs import LoggerConfiguration, ProjectPaths

# Setup paths
project_paths: ProjectPaths = ProjectPaths()

# Configure logger
log_config: LoggerConfiguration = LoggerConfiguration()
dictConfig(log_config.generate(project_paths.logger_folder))

# Central logger instance, importable as `from my_project import logger`
logger: logging.Logger = logging.getLogger(log_config.log_name)