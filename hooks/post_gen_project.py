"""Post generation script to install data science packages using uv."""
import json
import re
import subprocess
import sys
from pathlib import Path
from random import choice
from typing import Optional

# Define the root folder as the current working directory
root_folder: Path = Path.cwd()

# Regex pattern for validating GitHub URLs
github_url_pattern: re.Pattern[str] = re.compile(
    pattern=r"^(https?://)?(www\.)?github\.com/.*$"
)

# Lists of packages to install
data_science_packages = [
    "pymc",
    "arviz",
    "matplotlib",
    "numpy",
    "openpyxl",
    "pandas",
    "scikit-learn",
    "scipy",
    "seaborn",
    "setuptools",
    "statsmodels",
]

dev_packages = [
    "ipykernel",
    "tqdm",
]


def customize_titlebar_color(color_to_use: Optional[str] = None) -> None:
    """Customize the titlebar of VSCode."""
    possible_colors = ["#001524", "#15616d", "#ffecd1", "#ff7d00", "#78290f"]
    if not color_to_use:
        color_to_use = choice(possible_colors)

    vscode_folder: Path = root_folder.joinpath(".vscode")
    vscode_folder.mkdir(exist_ok=True, parents=True)

    vscode_workspace_settings = vscode_folder.joinpath("settings.json")
    settings = {
        "workbench.colorCustomizations": {
            "titleBar.inactiveBackground": color_to_use,
            "titleBar.inactiveForeground": "#DDDDDD",
        }
    }

    with vscode_workspace_settings.open("w") as f:
        json.dump(settings, f, indent=4)


def install_packages(packages: list[str], dev: bool = False):
    """Install packages using uv."""
    try:
        commands = ["uv", "add"]
        if dev:
            commands.append("--dev")
        commands.extend(packages)

        subprocess.run(
            args=commands,
            check=True,
            stdout=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}", file=sys.stderr)
        sys.exit(1)


def setup_git_repository(git_url: str):
    """Set up a Git repository and push to the remote."""
    if not github_url_pattern.match(git_url):
        print("Error: The provided URL is not a valid GitHub URL.")
        sys.exit(1)

    try:
        subprocess.run(["git", "init"], cwd=root_folder.as_posix(), check=True)
        subprocess.run(
            ["git", "remote", "add", "origin", git_url],
            cwd=root_folder.as_posix(),
            check=True,
        )
        print("Git repository initialized and remote origin set.")

        subprocess.run(
            ["git", "checkout", "-b", "develop"],
            cwd=root_folder.as_posix(),
            check=True,
        )
        print("Develop branch created.")

        subprocess.run(
            ["git", "add", "."],
            cwd=root_folder.as_posix(),
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "first commit"],
            cwd=root_folder.as_posix(),
            check=True,
        )
        subprocess.run(
            ["git", "push", "-u", "origin", "develop"],
            cwd=root_folder.as_posix(),
            check=True,
        )
        print("Pushed to remote develop branch.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during Git operations: {e}")
        sys.exit(1)


def main():
    """Main function to execute post-generation tasks."""
    git_repo_url = "{{cookiecutter.repo_git_ssh_url}}"
    if git_repo_url:
        print("Initializing Git repo.")
        setup_git_repository(git_repo_url)
    else:
        print("No GitHub repo provided.")

    print("Installing packages...")
    install_packages(data_science_packages)

    print("Installing dev packages...")
    install_packages(dev_packages, dev=True)

    print("Customizing VSCode...")
    customize_titlebar_color()

if __name__ == "__main__":
    main()