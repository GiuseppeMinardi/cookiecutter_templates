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
    BaseSettings,
    SettingsConfigDict,
)


class DataFolderSettings(BaseSettings):
    """
    Configuration for data directory structure.
    
    Defines paths to various data folders (raw, processed, interim, external)
    with automatic validation and default subfolder creation from a root path.
    """

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
    def paths_serializer(self, path: Path | None) -> str | None:
        """Serialize Path objects to POSIX-formatted strings.
        
        Args:
            path: Path object or None to serialize.
            
        Returns
        -------
            POSIX-formatted string representation of the path, or None.
        """
        return path.as_posix() if path else None

    @model_validator(mode="before")
    @classmethod
    def validate_after(cls, values: dict) -> dict:
        """Validate and populate default data folder paths.
        
        Args:
            values: Dictionary of field values to validate.
            
        Returns
        -------
            Validated values dictionary with default subfolders populated.
            
        Raises
        ------
            ValueError: If data_root is missing or invalid type.
        """
        root_folder: str | Path | None = values.get("data_root")
        if not root_folder:
            raise ValueError("Root folder should be present.")

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
    """
    Configuration for report directory structure.
    
    Defines paths to various report folders (figures, tables)
    with automatic validation and default subfolder creation from a root path.
    """
    
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
    def paths_serializer(self, path: Path | None) -> str | None:
        """Serialize Path objects to POSIX-formatted strings.
        
        Args:
            path: Path object or None to serialize.
            
        Returns
        -------
            POSIX-formatted string representation of the path, or None.
        """
        return path.as_posix() if path else None

    @model_validator(mode="before")
    @classmethod
    def validate_after(cls, values: dict) -> dict:
        """Validate and populate default report folder paths.
        
        Args:
            values: Dictionary of field values to validate.
            
        Returns
        -------
            Validated values dictionary with default subfolders populated.
            
        Raises
        ------
            ValueError: If report_root is missing or invalid type.
        """
        root_folder: str | Path | None = values.get("report_root")
        if not root_folder:
            raise ValueError("report_root folder cannot be None")
        elif isinstance(root_folder, str):
            root_folder = Path(root_folder)
        elif not isinstance(root_folder, Path):
            raise ValueError("Report root folder can only be of type str or Path.")

        for folder_name in ["figures", "tables"]:
            if not values.get(folder_name):
                values[folder_name] = root_folder.joinpath(folder_name)
        return values


class ProjectPaths(BaseSettings):
    """
    Configuration for project-level paths and directories.
    
    Centralizes access to all project folder settings including data, reports,
    and logs directories. Automatically initializes default data and report
    folder configurations based on the project root directory.
    """
    
    root: DirectoryPath = Path(__file__).resolve().parents[2]
    logger_folder: DirectoryPath = root.joinpath("logs")

    data_folder: DataFolderSettings | None = Field(
        default=None, description="Folder containing the data."
    )
    report_folder: ReportFolderSettings | None = Field(
        default=None, description="Folder containing the reports."
    )

    @model_validator(mode="before")
    @classmethod
    def _fill_fields(cls, values: dict) -> dict:
        if not (root_folder := values.get("root")):
            root_folder = Path(__file__).resolve().parents[2]
            values["root"] = root_folder
        values["data_folder"] = DataFolderSettings(
            data_root=root_folder.joinpath("data")
        )
        values["report_folder"] = ReportFolderSettings(
            report_root=root_folder.joinpath("report")
        )
        return values


class LoggerConfiguration(BaseSettings):
    log_level: str = Field(default="INFO")
    log_name: str = Field(default="{{cookiecutter.repo_name}}")
    log_file_name: str = Field(default="{{cookiecutter.repo_name}}.log")
    max_bytes: PositiveInt = Field(default=5_000_000)
    backup_count: PositiveInt = Field(default=5)

    def generate(self, log_dir: Path) -> dict:
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
