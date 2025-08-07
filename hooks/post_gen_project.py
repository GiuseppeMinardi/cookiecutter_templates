"""Post generation script to install data science packages using uv."""
import subprocess
import sys

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
    "scipy"
]

dev_packages = [
    "ipykernel",
    "tqdm",
]

def install_packages(packages: list[str], dev: bool = ""):
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
    """Install data science packages using uv."""
    install_packages(data_science_packages)
    install_packages(dev_packages, dev=True)

if __name__ == "__main__":
    main()