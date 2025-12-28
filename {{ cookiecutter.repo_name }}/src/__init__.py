import logging
from logging.config import dictConfig

# Re-export package-level symbols from the real package folder so notebooks
# can `import {pkg}` after an editable install or when the package is available
# on sys.path. This top-level file keeps backward compatibility for code that
# does `from src import logger` while encouraging `from {pkg} import ...`.
from .{{ cookiecutter.repo_name }} import ProjectPaths, LoggerConfiguration  # ty: ignore

# Setup paths
project_paths: ProjectPaths = ProjectPaths()

# Configure logger
log_config: LoggerConfiguration = LoggerConfiguration()
dictConfig(log_config.generate(project_paths.logger_folder))

# Central logger instance
logger: logging.Logger = logging.getLogger(log_config.log_name)