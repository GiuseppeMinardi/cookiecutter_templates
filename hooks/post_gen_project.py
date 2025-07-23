#!/usr/bin/env python3
"""
Post-generation script for cookiecutter template.
Handles conda environment creation and git repository initialization.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional


class ProjectSetup:
    """Handles post-generation project setup tasks."""

    def __init__(self, root_path: Optional[Path] = None):
        self.root_folder = root_path or Path(".").resolve()
        self.success_count = 0
        self.total_tasks = 0

    def run_command(
        self, command: str, cwd: Optional[Path] = None, capture_output: bool = False
    ) -> subprocess.CompletedProcess:
        """
        Run a shell command with proper error handling.

        Args:
            command: Command to execute
            cwd: Working directory for command
            capture_output: Whether to capture stdout/stderr

        Returns:
            CompletedProcess result

        Raises:
            subprocess.CalledProcessError: If command fails
        """
        print(f"  Running: {command}")

        return subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True if capture_output else None,
        )

    def check_command_available(self, command: str) -> bool:
        """Check if a command is available in the system PATH."""
        try:
            subprocess.run(
                f"{command} --version",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def setup_conda_environment(self) -> bool:
        """
        Create conda environment from environment.yml if it exists.

        Returns:
            True if successful or skipped, False if failed
        """
        print("\n🐍 Setting up Conda environment...")
        self.total_tasks += 1

        env_file = self.root_folder / "environment.yml"

        if not env_file.exists():
            print("  ⚠️  No environment.yml found. Skipping conda environment creation.")
            self.success_count += 1
            return True

        # Check if conda is available
        if not self.check_command_available("conda"):
            print("  ❌ Conda not found. Please install Miniconda or Anaconda.")
            print(f"  📋 Manual setup: conda env create -f {env_file.name}")
            return False

        try:
            print(f"  🔧 Creating conda environment from {env_file.name}...")
            self.run_command(
                f"conda env create -f {env_file.name}", cwd=self.root_folder
            )
            print("  ✅ Conda environment created successfully!")
            self.success_count += 1
            return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to create conda environment: {e}")
            print(f"  📋 Manual setup: conda env create -f {env_file.name}")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error during environment creation: {e}")
            return False

    def setup_git_repository(self, remote_repo: str) -> bool:
        """
        Initialize git repository and connect to remote.

        Args:
            remote_repo: Remote repository URL

        Returns:
            True if successful, False if failed
        """
        print("\n📦 Setting up Git repository...")
        self.total_tasks += 1

        if not remote_repo or remote_repo.strip() == "":
            print("  ⚠️  No remote repository provided. Skipping git setup.")
            self.success_count += 1
            return True

        remote_repo = remote_repo.strip()

        # Check if git is available
        if not self.check_command_available("git"):
            print(
                "  ❌ Git not found. Please install Git and set up the repository manually."
            )
            print("  📋 Manual setup commands:")
            print("    git init")
            print("    git add .")
            print("    git commit -m 'Initial commit from cookiecutter'")
            print(f"    git remote add origin {remote_repo}")
            print("    git branch -M main")
            print("    git push -u origin main")
            return False

        try:
            print("  🔧 Initializing git repository...")

            # Initialize git repo
            self.run_command("git init", cwd=self.root_folder)

            # Add all files
            print("  📁 Adding files to git...")
            self.run_command("git add .", cwd=self.root_folder)

            # Check if there are any files to commit
            try:
                result = self.run_command(
                    "git diff --cached --quiet",
                    cwd=self.root_folder,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                # There are staged changes, proceed with commit
                pass
            else:
                print("  ⚠️  No changes to commit. Repository may be empty.")
                return False

            # Initial commit
            print("  💾 Creating initial commit...")
            self.run_command(
                'git commit -m "Initial commit from cookiecutter"', cwd=self.root_folder
            )

            # Add remote origin
            print(f"  🔗 Adding remote origin: {remote_repo}")
            self.run_command(
                f"git remote add origin {remote_repo}", cwd=self.root_folder
            )

            # Set main branch and push
            print("  🚀 Pushing to remote repository...")
            self.run_command("git branch -M main", cwd=self.root_folder)
            self.run_command("git push -u origin main", cwd=self.root_folder)

            print("  ✅ Git repository initialized and pushed to remote!")
            self.success_count += 1
            return True

        except subprocess.CalledProcessError as e:
            print(f"  ❌ Git setup failed: {e}")
            print("  📋 You may need to set up the repository manually.")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error during git setup: {e}")
            return False

    def run_setup(self) -> int:
        """
        Run all setup tasks.

        Returns:
            Exit code (0 for success, 1 for partial failure, 2 for complete failure)
        """
        print("🚀 Starting project setup...")
        print(f"📁 Working directory: {self.root_folder}")

        # Setup conda environment
        self.setup_conda_environment()

        # Get remote repository from cookiecutter context
        remote_repo = "{{ cookiecutter.remote_repository }}"
        self.setup_git_repository(remote_repo)

        # Print summary
        print("\n📊 Setup Summary:")
        print(f"  ✅ Successful tasks: {self.success_count}/{self.total_tasks}")

        if self.success_count == self.total_tasks:
            print("🎉 All setup tasks completed successfully!")
            return 0
        elif self.success_count > 0:
            print(
                "⚠️  Some tasks failed. Check the output above for manual setup instructions."
            )
            return 1
        else:
            print("❌ All setup tasks failed. Manual setup required.")
            return 2


def main():
    """Main entry point for the post-generation script."""
    setup = ProjectSetup()
    exit_code = setup.run_setup()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
