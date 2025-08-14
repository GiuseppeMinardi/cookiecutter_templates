"""Pre generation script for validating cookiecutter parameters."""

import re
import sys
import urllib.error
import urllib.request
from urllib.parse import quote

# Get cookiecutter parameters
repo_name = "{{ cookiecutter.repo_name }}"
project_name = "{{ cookiecutter.project_name }}"
author_email = "{{ cookiecutter.author_email }}"
description = "{{ cookiecutter.description }}"
setup_environment = "{{ cookiecutter.setup_environment }}"

# Constants
MAX_DESCRIPTION_LENGTH = 100
PYPI_API_URL = "https://pypi.org/pypi/{package}/json"
MIN_PYTHON_VERSION = (3, 12)


def error(message: str) -> None:
    """Print error message and exit with non-zero status.

    Args:
        message: The error message to display
    """
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def warning(message: str) -> None:
    """Print warning message but don't exit.

    Args:
        message: The warning message to display
    """
    print(f"WARNING: {message}", file=sys.stderr)


def validate_repo_name(name: str) -> None:
    """Validate repository name follows Python package naming conventions.

    Args:
        name: The repository name to validate

    Raises
    ------
        SystemExit: If validation fails
    """
    if not name:
        error("Repository name cannot be empty")

    # Check if repo_name follows Python package naming conventions
    # (alphanumeric with underscores, no hyphens)
    if not re.match(r"^[a-zA-Z0-9_]+$", name):
        error(
            f"Repository name '{name}' is not valid. "
            "It must contain only letters, numbers, and underscores."
        )

    # Check if repo_name starts with a letter or underscore (as per Python conventions)
    if not re.match(r"^[a-zA-Z_]", name):
        error(
            f"Repository name '{name}' is not valid. "
            "It must start with a letter or underscore."
        )


def validate_project_name(name: str) -> None:
    """Validate project name is not empty and doesn't contain problematic characters.

    Args:
        name: The project name to validate

    Raises
    ------
        SystemExit: If validation fails
    """
    if not name or name.strip() == "":
        error("Project name cannot be empty")

    # Check for characters that might cause issues in file paths
    problematic_chars = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    for char in problematic_chars:
        if char in name:
            warning(
                f"Project name '{name}' contains character '{char}' "
                "which might cause issues in file paths"
            )


def validate_author_email(email: str) -> None:
    """Validate author email format if provided.

    Args:
        email: The email to validate

    Raises
    ------
        SystemExit: If validation fails
    """
    if not email:
        return  # Email is optional

    # Simple email validation using regex
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        error(f"Author email '{email}' is not a valid email address")


def validate_description(desc: str) -> None:
    """Validate project description is not too long.

    Args:
        desc: The description to validate

    Raises
    ------
        SystemExit: If validation fails
    """
    if len(desc) > MAX_DESCRIPTION_LENGTH:
        error(
            f"Description is too long ({len(desc)} characters). "
            f"Maximum allowed is {MAX_DESCRIPTION_LENGTH} characters."
        )


def validate_setup_environment(setup: str) -> None:
    """Validate setup_environment is either 'y' or 'n'.

    Args:
        setup: The setup_environment value to validate

    Raises
    ------
        SystemExit: If validation fails
    """
    if setup not in ["y", "n"]:
        error(f"Setup environment must be 'y' or 'n', got '{setup}'")


def check_python_version() -> None:
    """Check if the Python version meets the minimum requirement.

    Raises
    ------
        SystemExit: If Python version is less than required
    """
    current_version = sys.version_info

    if current_version < MIN_PYTHON_VERSION:
        error(
            f"Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ is required. "
            f"You're using Python {current_version.major}.{current_version.minor}"
        )


def check_pypi_name_conflict(name: str) -> None:
    """Check if the repository name already exists in PyPI.

    Args:
        name: The repository name to check

    Raises
    ------
        SystemExit: If name already exists in PyPI
    """
    try:
        # URL encode the package name for safety
        encoded_name = quote(name)
        url = PYPI_API_URL.format(package=encoded_name)

        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                warning(
                    f"Repository name '{name}' already exists in PyPI. "
                    "Consider choosing a different name to avoid conflicts."
                )
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Package not found in PyPI, which is good
            pass
        else:
            # There was an error checking PyPI
            warning(f"Could not check PyPI for package name conflicts: {e}")
    except Exception as e:
        warning(f"Could not check PyPI for package name conflicts: {e}")


def main() -> None:
    """Main function to execute pre-generation validation.

    Raises
    ------
        SystemExit: If any validation fails
    """
    print("Validating cookiecutter parameters...")

    # Validate required parameters
    validate_repo_name(repo_name)
    validate_project_name(project_name)
    validate_author_email(author_email)
    validate_description(description)
    validate_setup_environment(setup_environment)

    # Additional checks
    check_python_version()
    check_pypi_name_conflict(repo_name)

    print("All parameters are valid!")


if __name__ == "__main__":
    main()
