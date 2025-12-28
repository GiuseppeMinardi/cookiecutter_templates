"""
Project configuration settings for the data science project.

This module defines the configuration for various paths and logging used
throughout the data science project. It leverages Pydantic `BaseSettings`
for environment-based configuration and validation.

The module contains:

- `DataFolderSettings`: Configuration for data directories (raw, processed, etc.).
- `ReportFolderSettings`: Configuration for report-related directories.
- `ProjectPaths`: Centralized access to all project folder settings.
- `LoggerConfiguration`: Logging configuration for the project.

All settings classes automatically validate paths and provide default
subfolder creation logic based on a given root folder.
"""

from datetime import datetime
from pathlib import Path

from pydantic import (
    DirectoryPath,
    Field,
    PositiveInt,
    field_serializer,
    model_validator,
)
from pydantic_settings import (
    """Compatibility shim: re-export package symbols from the package folder.

    This file keeps existing imports working for users who import from `src`.
    Prefer importing from the package name directly after running an editable
    install (e.g. `pip install -e .`).
    """

    from .{{ cookiecutter.repo_name }}.project_configs import ProjectPaths, LoggerConfiguration  # noqa: F401

    __all__ = ["ProjectPaths", "LoggerConfiguration"]


class ProjectPaths(BaseSettings):
    """
    Centralized project paths configuration.

    This class aggregates paths for:
    - Project root folder
    - Logger folder
    - Data folders (`DataFolderSettings`)
    - Report folders (`ReportFolderSettings`)

    It automatically populates default `DataFolderSettings` and
    `ReportFolderSettings` if not explicitly set.

    Attributes
    ----------
    root : DirectoryPath
        Root of the project.
    logger_folder : DirectoryPath
        Folder containing log files.
    data_folder : DataFolderSettings or None
        Settings for the data directories.
    report_folder : ReportFolderSettings or None
        Settings for the report directories.
    """

    root: DirectoryPath = Path(__file__).resolve().parents[1]
    logger_folder: DirectoryPath = root.joinpath("logs")

    data_folder: DataFolderSettings | None = Field(
        default=None, description="Folder containing the data."
    )
    report_folder: ReportFolderSettings | None = Field(
        default=None, description="Folder containing the reports."
    )

    @model_validator(mode="before")
    @classmethod
    def fill_fields(cls, values: dict) -> dict:
        """
        Populate default data and report folder settings if not provided.

        Parameters
        ----------
        values : dict
            Dictionary of provided settings values.

        Returns
        -------
        dict
            Updated dictionary with default folder settings populated.
        """
        if not (root_folder := values.get("root")):
            root_folder = Path(__file__).resolve().parents[1]
            values["root"] = root_folder
        values["data_folder"] = DataFolderSettings(
            data_root=root_folder.joinpath("data")
        )
        values["report_folder"] = ReportFolderSettings(
            report_root=root_folder.joinpath("report")
        )
        return values


class LoggerConfiguration(BaseSettings):
    """
    Logger configuration settings for the data science project.

    This class defines the configuration for logging, including:
    - Log level
    - Log file name
    - Maximum file size for rotation
    - Number of backup files to keep

    Methods
    -------
    generate(log_dir)
        Generate a Python logging configuration dictionary.

    Attributes
    ----------
    log_level : str
        Logging verbosity level (e.g., 'INFO', 'DEBUG').
    log_name : str
        Name of the logger.
    log_file_name : str
        File name for log storage.
    max_bytes : PositiveInt
        Maximum size in bytes before rotating the log file.
    backup_count : PositiveInt
        Number of backup log files to keep.
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
            Directory where the log file will be stored.

        Returns
        -------
        dict
            A dictionary suitable for configuring Python's `logging` module.
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
                "matplotlib": {
                    "level": "WARNING",
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
            },
        }


if __name__ == "__main__":
    conf = ProjectPaths()
    print(conf.model_dump_json(indent=4))
