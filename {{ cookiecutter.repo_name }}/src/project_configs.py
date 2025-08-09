"""
Project configuration settings for the data science project.

This module defines paths to various folders and sets up the project
configuration using Pydantic settings.
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
    BaseSettings,
    SettingsConfigDict,
)


class DataFolderSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    data_root: DirectoryPath = Field(
        description="Root of the folder containing all the data"
    )
    external: DirectoryPath | None = Field(
        default=None, description="Folder containing data from external sources."
    )
    interim: DirectoryPath | None = Field(
        default=None, description="Folder containing intermediate data sources."
    )
    processed: DirectoryPath | None = Field(
        default=None, description="Folder containing data ready to be used."
    )
    raw: DirectoryPath | None = Field(
        default=None, description="Folder containing raw data"
    )

    @field_serializer(
        "data_root", "external", "interim", "processed", "raw", when_used="json"
    )
    def paths_serializer(self, path: Path | None):
        return path.as_posix() if path else None

    @model_validator(mode="before")
    @classmethod
    def validate_after(cls, values):
        root_folder: str | Path = values.get("data_root")
        if not root_folder:
            raise ValueError("data_root folder cannot be None")
        elif isinstance(root_folder, str):
            root_folder = Path(root_folder)
        elif not isinstance(root_folder, Path):
            raise ValueError("Data root folder can only be of type str or Path.")

        for folder_name in ["external", "interim", "processed", "raw"]:
            if not values.get(folder_name):
                values[folder_name] = root_folder.joinpath(folder_name)
        return values


class ReportFolderSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    report_root: DirectoryPath = Field(
        description="Root of the folder containing the reports"
    )
    figures: DirectoryPath | None = Field(
        default=None, description="Folder containing the figures"
    )
    tables: DirectoryPath | None = Field(
        default=None, description="Folder containing the tables"
    )

    @field_serializer("*", when_used="json")
    def paths_serializer(self, path: Path | None):
        return path.as_posix() if path else None

    @model_validator(mode="before")
    @classmethod
    def validate_after(cls, values):
        root_folder: str | Path = values.get("report_root")
        if not root_folder:
            raise ValueError("data_root folder cannot be None")
        elif isinstance(root_folder, str):
            root_folder = Path(root_folder)
        elif not isinstance(root_folder, Path):
            raise ValueError("Data root folder can only be of type str or Path.")

        for folder_name in ["figures", "tables"]:
            if not values.get(folder_name):
                values[folder_name] = root_folder.joinpath(folder_name)
        return values


class ProjectPaths(BaseSettings):
    """Project configuration settings for the data science project."""

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
                "matplotlib": {
                    "level": "WARNING",
                    "handlers": ["console"],
                    "propagate": False,
                },
                "urllib3": {
                    "level": "WARNING",
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }


if __name__ == "__main__":
    conf = ProjectPaths()
    print(conf.model_dump_json(indent=4))
