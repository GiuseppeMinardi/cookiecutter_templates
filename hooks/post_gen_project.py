import subprocess
from pathlib import Path

root_folder = Path(".").resolve()


def run(command, cwd=None):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True, cwd=cwd)


def main():
    env_file = root_folder / "environment.yml"

    if not env_file.exists():
        print("⚠️  No environment.yml found. Skipping Conda environment creation.")
        return

    # Check if conda is available
    try:
        if (
            subprocess.call(
                "conda --version",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            != 0
        ):
            print(
                "❌ Conda not found. Please install Miniconda or Anaconda and create the environment manually:"
            )
            print(f"    conda env create -f {env_file}")

        print("🔧 Creating Conda environment from environment.yml...")
        run("conda env create -f environment.yml")

    except Exception as e:
        print(f"ERROR: couldn't compplete the environment creation: {e}")

    remote_repo = "{{ cookiecutter.remote_repository }}".strip()

    if remote_repo:
        print(f"🔧 Initializing git repository and connecting to remote: {remote_repo}")

        # Initialize git repo
        subprocess.call("git init", shell=True)

        # Add all files
        subprocess.call("git add .", shell=True)

        # Initial commit
        subprocess.call('git commit -m "Initial commit from cookiecutter"', shell=True)

        # Add remote origin
        subprocess.call(f"git remote add origin {remote_repo}", shell=True)

        # Set main branch and push (create remote branch if needed)
        subprocess.call("git branch -M main", shell=True)
        subprocess.call("git push -u origin main", shell=True)

        print("✅ Git repo initialized, connected, and pushed to remote.")
    else:
        print("No remore repository provided")


if __name__ == "__main__":
    # main()
    pass
