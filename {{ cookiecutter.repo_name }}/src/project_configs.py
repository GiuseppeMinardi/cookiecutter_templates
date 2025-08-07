"""
Project configuration settings for the data science project.

This module defines paths to various folders and sets up the project
configuration using Pydantic settings.
"""

from datetime import datetime
from pathlib import Path

from pydantic import DirectoryPath, Field, PositiveInt
from pydantic_settings import BaseSettings


class ProjectPaths(BaseSettings):
    """
    Project configuration settings for the data science project.

    This module defines paths to various folders and sets up the project
    configuration using Pydantic settings.
    """

    root: DirectoryPath = Path(__file__).resolve().parents[1]

    logger_folder: DirectoryPath = root.joinpath("logs")

    # Data paths
    data_folder: DirectoryPath = root.joinpath("data")
    raw_data_folder: DirectoryPath = data_folder.joinpath("raw")
    external_data_folder: DirectoryPath = data_folder.joinpath("external")
    processed_data_folder: DirectoryPath = data_folder.joinpath("processed")

    # Report paths
    report_folder: DirectoryPath = root.joinpath("report")
    figures_output_folder: DirectoryPath = report_folder.joinpath("figures")
    tables_output_folder: DirectoryPath = report_folder.joinpath("tables")


class LoggerConfiguration(BaseSettings):
    """
    Logger configuration settings for the data science project.

    This class defines the configuration for logging, including log level,
    log file name, maximum file size, and backup count. It provides a method
    to generate a logging configuration dictionary compatible with Python's
    logging module.
    """

    log_level: str = Field(default="INFO")
    log_name: str = Field(default="{{cookiecutter.repo_name}}")
    log_file_name: str = Field(default="{{cookiecutter.repo_name}}.log")
    max_bytes: PositiveInt = Field(default=5_000_000)  # 5 MB
    backup_count: PositiveInt = Field(default=5)

    def generate(self, log_dir: Path) -> dict:
        """
        Generate a logging configuration dictionary.

        Parameters
        ----------
        log_dir : Path
            The directory where the log file will be stored.

        Returns
        -------
        dict
            A dictionary suitable for configuring Python's logging module.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_name = f"{timestamp}_{self.log_file_name}"
        log_path = log_dir / log_file_name

        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": self.log_level,
                    "formatter": "standard",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": self.log_level,
                    "formatter": "standard",
                    "filename": log_path.as_posix(),
                    "maxBytes": self.max_bytes,
                    "backupCount": self.backup_count,
                    "encoding": "utf8",
                },
            },
            "root": {
                "level": self.log_level,
                "handlers": ["console", "file"],
            },
            "loggers": {
                "matplotlib": {"level": "WARNING", "handlers": ["console"], "propagate": False},
                "urllib3": {"level": "WARNING", "handlers": ["console"], "propagate": False},
            },
        }
