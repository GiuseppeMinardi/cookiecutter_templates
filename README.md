# Statistical Analysis Project Template

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for statistical analysis projects that follows best practices for organization, reproducibility, and documentation.

## Features

- **Comprehensive Statistical Environment**: Pre-configured with powerful libraries for both frequentist and Bayesian analysis
- **Professional LaTeX Reporting**: Ready-to-use LaTeX template with automated PDF building via GitHub Actions
- **Organized Project Structure**: Clear separation of data, code, and documentation
- **Modern Python Package Management**: Automatic package installation using uv
- **VSCode Integration**: Custom workspace settings including titlebar color customization
- **Plotting Style**: Custom matplotlib style configuration for consistent visualizations
- **Structured Configuration**: Pydantic-based project configuration and logging setup
- **Code Quality Tools**: Integration of linting with Ruff

## Requirements

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) >= 2.1.1
- [uv](https://github.com/astral-sh/uv) - Modern Python package installer and resolver
- Python >= 3.12
- LaTeX distribution (for report generation)

## Installation

```bash
pip install cookiecutter
pip install uv
```

## Usage

### Creating a New Project

```bash
cookiecutter https://github.com/yourusername/cookiecutter_templates.git
```

You'll be prompted to enter information about your project:

- `repo_git_ssh_url`: Git SSH URL (optional, used to automatically set repo name)
- `project_name`: Name of your statistical project
- `author_name`: Your name
- `author_email`: Your email (auto-generated if not provided)
- `description`: Brief description of the project
- `version`: Initial version number (default: 0.1.0)

### Project Structure

```plain
my_statistical_project/
├── .github/
│   └── workflows/
│       └── build-report.yml    # GitHub Action for LaTeX report building
├── .vscode/
│   └── settings.json           # VSCode workspace settings
├── data/                       # Data storage with clear organization
│   ├── external/               # Data from external sources
│   ├── interim/                # Intermediate data processing results
│   ├── processed/              # Cleaned/transformed data
│   └── raw/                    # Original, immutable data
├── logs/                       # Logging directory
├── notebooks/                  # Jupyter notebooks for exploration and analysis
│   ├── __setup.py              # Notebook setup helper
│   └── exploratory_analysis.ipynb  # Template notebook
├── report/                     # LaTeX reporting
│   ├── figures/                # Generated plots and visualizations
│   ├── tables/                 # Generated tables
│   └── report.tex              # LaTeX template for formal reporting
├── src/                        # Python package for reusable code
│   ├── __init__.py
│   └── project_configs.py      # Pydantic-based project configuration
├── plot_style.mlpstyle         # Custom matplotlib style configuration
├── pyproject.toml              # Python project configuration
├── README.md                   # Project documentation
└── ruff.toml                   # Ruff linting configuration
```

### Getting Started

After generating your project:

1. The required packages will be automatically installed using uv if available
2. Begin your analysis in the `notebooks/` directory
3. Store your data in the appropriate `data/` subdirectories
4. Write reusable functions in the `src/` directory
5. Generate your report using LaTeX in the `report/` directory
6. Push your changes to GitHub to trigger automatic report building (PDF generation)

### Statistical Capabilities

The template includes these key libraries:

- **PyMC**: Probabilistic programming for Bayesian modeling
- **ArviZ**: Exploratory analysis of Bayesian models
- **NumPy, SciPy, pandas**: Core data manipulation libraries
- **scikit-learn**: Machine learning algorithms
- **Matplotlib, Seaborn**: Visualization libraries with custom styling
- **statsmodels**: Statistical models and tests
- **openpyxl**: Excel file support

### LaTeX Reporting with GitHub Actions

The template includes a complete LaTeX setup:

- Professional report template with proper formatting
- GitHub Actions workflow that automatically:
  - Builds the PDF report on each push to main
  - Commits the generated PDF back to the repository
  - Makes the latest report easily accessible

### Project Configuration and Logging

The project uses Pydantic for configuration:

- `ProjectPaths`: Manages project directory structure
- `LoggerConfiguration`: Configurable logging setup with:
  - Timestamped log files
  - Rotating file handler
  - Console output
  - Customizable log levels

### VSCode Integration

The template includes VSCode-specific features:

- Random titlebar color assignment for easy project identification
- Workspace settings automatically configured

### Data Visualization

- Custom matplotlib style configuration (`plot_style.mlpstyle`)
- Professional color scheme for visualizations
- Consistent plot styling throughout the project

## Customization

- Modify `pyproject.toml` to add/remove Python packages
- Adjust `ruff.toml` to change linting configurations
- Edit `report.tex` to customize the LaTeX template
- Customize `plot_style.mlpstyle` for different visualization styling

## License

This project is licensed under the terms of the MIT license.
