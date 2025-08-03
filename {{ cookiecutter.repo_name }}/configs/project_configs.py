"""
Project configuration settings for the data science project.

This module defines paths to various folders and sets up the project
configuration using Pydantic settings.
"""
from pathlib import Path

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectPaths(BaseSettings):
    """
    Project configuration settings for the data science project.

    This module defines paths to various folders and sets up the project
    configuration using Pydantic settings.
    """

    settings_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra fields not defined in the model
    )
    root: DirectoryPath = Path(__file__).parent.parent.parent

    data_folder: DirectoryPath = root / "data"
    external_data_folder: DirectoryPath =  data_folder / "external"
    processed_data_folder: DirectoryPath = data_folder / "processed"
    raw_data_folder: DirectoryPath = data_folder / "raw"

    figures_output_folder: DirectoryPath = root / "reports" / "figures"
    tables_output_folder: DirectoryPath = root / "reports" / "tables"
