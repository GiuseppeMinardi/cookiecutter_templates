"""Post generation script to install data science packages using uv."""

import json
import subprocess
import sys
from pathlib import Path
from random import choice
from typing import Optional

# Define the root folder as the current working directory
root_folder: Path = Path.cwd()

other_packages = ["pydantic", "pydantic-settings", "cool-styles"]

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


def main():
    """Main function to execute post-generation tasks."""
    if "{{cookiecutter.setup_environment}}" == "y":
        print("Installing packages...")
        install_packages(data_science_packages)

        print("Installing packages...")
        install_packages(other_packages)

        print("Installing dev packages...")
        install_packages(dev_packages, dev=True)
    else:
        print("Not setting up the environment...")

    print("Customizing VSCode...")
    customize_titlebar_color()


if __name__ == "__main__":
    main()
