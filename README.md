# Statistical Analysis Project Template

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for statistical analysis projects that follows best practices for organization, reproducibility, and documentation.

## Features

- **Comprehensive Statistical Environment**: Pre-configured with powerful libraries for both frequentist and Bayesian analysis
- **Professional LaTeX Reporting**: Ready-to-use LaTeX template for publication-quality documentation
- **Organized Project Structure**: Clear separation of data, code, and documentation
- **Automated Environment Setup**: Automatic conda environment creation during project generation
- **Code Quality Tools**: Integration of linting with Ruff

## Requirements

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) >= 2.1.1
- [Conda](https://docs.conda.io/en/latest/) (Miniconda or Anaconda)
- LaTeX distribution (for report generation)

## Installation

```bash
pip install cookiecutter
```

## Usage

### Creating a New Project

```bash
cookiecutter https://github.com/yourusername/cookiecutter_templates.git
```

You'll be prompted to enter information about your project:

- `project_name`: Name of your statistical project
- `author_name`: Your name
- `description`: Brief description of the project
- `version`: Initial version number (default: 0.1.0)

### Project Structure

```plain
my_statistical_project/
├── data/                 # Data storage with clear organization
│   ├── external/         # Data from external sources
│   ├── processed/        # Cleaned/transformed data
│   ├── raw/              # Original, immutable data
├── notebooks/            # Jupyter notebooks for exploration and analysis
├── report/               # LaTeX reporting
│   ├── figures/          # Generated plots and visualizations
│   ├── tables/           # Generated tables
│   └── report.tex        # LaTeX template for formal reporting
├── my_statistical_project/  # Python package for reusable code
├── environment.yml       # Conda environment definition
├── pyproject.toml        # Python project configuration
└── README.md             # Project documentation
```

### Getting Started

After generating your project:

1. The conda environment will be automatically created if conda is available
2. Activate the environment: `conda activate my_statistical_project`
3. Begin your analysis in the `notebooks/` directory
4. Store your data in the appropriate `data/` subdirectories
5. Write reusable functions in the Python package directory
6. Generate your report using LaTeX in the `report/` directory

### Statistical Capabilities

The template includes these key libraries:

- **PyMC (v5.23.0)**: Probabilistic programming for Bayesian modeling
- **ArviZ (v0.21.0)**: Exploratory analysis of Bayesian models
- **NumPy, SciPy, pandas**: Core data manipulation libraries
- **scikit-learn**: Machine learning algorithms
- **Matplotlib, Seaborn**: Visualization libraries
- **statsmodels**: Statistical models and tests

### LaTeX Reporting

The `report.tex` file is pre-configured with:

- Professional formatting and styling
- Code listings with syntax highlighting
- Table and figure support with proper captioning
- Mathematical formula support via amsmath
- Customized colors and styling

## Customization

- Modify `environment.yml` to add/remove Python packages
- Adjust `pyproject.toml` to change Poetry and linting configurations
- Edit `report.tex` to customize the LaTeX template

## License

This project is licensed under the terms of the MIT license.