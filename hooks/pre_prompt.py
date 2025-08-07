"""
Utility functions and classes for pre-prompt checks.

This module provides:
- check_uv_installed: checks if uv is installed.
"""
import shutil
import sys


def check_uv_installed():
    """Check if the 'uv' command is available in the system."""
    return shutil.which("uv") is not None

if __name__ == "__main__":
    if not check_uv_installed():
        print("uv is not installed. Please install uv to continue.", file=sys.stderr)
        exit(1)

    print("uv is installed and ready to use.")