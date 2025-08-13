from pathlib import Path  # noqa: D100

import pytest
from cookiecutter.main import cookiecutter

template_directory: Path = Path(__file__).parents[1].resolve()


@pytest.mark.parametrize(
    argnames=[
        "repo_git_ssh_url",
        "project_name",
        "repo_name",
        "author_name",
        "author_email",
        "description",
        "version",
        "setup_environment",
    ],
    argvalues=[
        (
            "",
            "my statistical project",
            "",
            "giuseppe minardi",
            "giuseppe.minardi@gmail.com",
            "test description",
            "0.0.0",
            "n",
        ),
        (
            "",
            "my statistical project",
            "",
            "Mario Rossi",
            "",
            "test description",
            "0.0.0",
            "n",
        ),
        (
            "",
            "my statistical project",
            "",
            "Mario Rossi",
            "",
            "test description",
            "0.0.0",
            "y",
        ),
    ],
)
def test_project_creation(  # noqa: D103
    tmp_path: Path,
    repo_git_ssh_url: str,
    project_name: str,
    repo_name: str,
    author_name: str,
    author_email: str,
    description: str,
    version: str,
    setup_environment: str,
):
    if not repo_name and repo_git_ssh_url:
        repo_name = repo_git_ssh_url.split("/")[-1].replace(".git", "") 
    elif not repo_name and not repo_git_ssh_url:
        repo_name = project_name.replace(" ", "_").lower()
    
    if not author_email:
        author_email = author_name.title().replace(" ", "") + "@gmail.com"

    cookiecutter(
        template=template_directory.as_posix(),
        output_dir=str(tmp_path),
        no_input=True,
        extra_context={
            "repo_git_ssh_url": repo_git_ssh_url,
            "project_name": project_name,
            "repo_name": repo_name,
            "author_name": author_name,
            "author_email": author_email,
            "description": description,
            "version": version,
            "setup_environment": setup_environment,
        },
    )

    created_repo_path = tmp_path.joinpath(repo_name)
    assert created_repo_path.is_dir()

    expected_dirs = [
        [".vscode"],
        [".github"],
        [".github/workflows"],
        ["data"],
        ["data", "external"],
        ["data", "processed"],
        ["data", "raw"],
        ["data", "interim"],
        ["logs"],
        ["notebooks"],
        ["report"],
        ["report", "figures"],
        ["report", "tables"],
        ["src"],
    ]

    for rel_path in expected_dirs:
        folder = created_repo_path.joinpath(*rel_path)
        assert folder.is_dir(), f"Expected directory {folder} is missing or not a directory"

    with created_repo_path.joinpath("README.md").open("r") as f:
        readme = f.read()
        assert project_name in readme
        assert description in readme

    with created_repo_path.joinpath("pyproject.toml").open("r") as f:
        pyproject = f.read()
        assert author_name in pyproject
        assert author_email in pyproject
        assert description in pyproject
        assert version in pyproject
    
    with created_repo_path.joinpath("report", "report.tex").open("r") as f:
        report = f.read()
        assert author_name in report
        assert description in report
    
    if setup_environment == "y":
        uv_lock = created_repo_path.joinpath("uv.lock")
        assert uv_lock.is_file()



