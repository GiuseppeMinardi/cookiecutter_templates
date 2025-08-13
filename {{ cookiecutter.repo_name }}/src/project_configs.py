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
    Settings for data folder structure in the project.

    This class stores paths for different categories of data folders, such as
    raw, processed, and external data. It validates that the main `data_root`
    folder is provided and automatically generates default subfolder paths
    if they are not explicitly set.

    Attributes
    ----------
    data_root : DirectoryPath
        Root of the folder containing all data.
    external : DirectoryPath or None
        Folder containing data from external sources. Defaults to `data_root/external`.
    interim : DirectoryPath or None
        Folder containing intermediate data. Defaults to `data_root/interim`.
    processed : DirectoryPath or None
        Folder containing processed data ready for use. Defaults to `data_root/processed`.
    raw : DirectoryPath or None
        Folder containing raw, unprocessed data. Defaults to `data_root/raw`.
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
        """
        Serialize `Path` objects to POSIX-style strings for JSON output.

        Parameters
        ----------
        path : Path or None
            The path to serialize.

        Returns
        -------
        str or None
            The POSIX string representation of the path, or None if path is None.
        """
        return path.as_posix() if path else None

    @model_validator(mode="before")
    @classmethod
    def validate_after(cls, values: dict) -> dict:
        """
        Validate and populate missing subfolder paths based on `data_root`.

        Parameters
        ----------
        values : dict
            Dictionary of provided settings values.

        Returns
        -------
        dict
            Updated dictionary with missing subfolder paths set.

        Raises
        ------
        ValueError
            If `data_root` is missing or of the wrong type.
        """
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
    """
    Settings for report folder structure in the project.

    This class stores paths for different categories of report-related
    folders, such as figures and tables. It validates that the main
    `report_root` folder is provided and automatically generates default
    subfolder paths if they are not explicitly set.

    Attributes
    ----------
    report_root : DirectoryPath
        Root of the folder containing reports.
    figures : DirectoryPath or None
        Folder containing figure files. Defaults to `report_root/figures`.
    tables : DirectoryPath or None
        Folder containing table files. Defaults to `report_root/tables`.
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
        """
        Serialize `Path` objects to POSIX-style strings for JSON output.

        Parameters
        ----------
        path : Path or None
            The path to serialize.

        Returns
        -------
        str or None
            The POSIX string representation of the path, or None if path is None.
        """
        return path.as_posix() if path else None

    @model_validator(mode="before")
    @classmethod
    def validate_after(cls, values: dict) -> dict:
        """
        Validate and populate missing subfolder paths based on `report_root`.

        Parameters
        ----------
        values : dict
            Dictionary of provided settings values.

        Returns
        -------
        dict
            Updated dictionary with missing subfolder paths set.

        Raises
        ------
        ValueError
            If `report_root` is missing or of the wrong type.
        """
        root_folder: str | Path = values.get("report_root")
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
