# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Project Structure

```
.
├── data/                 # Data storage
│   ├── external/         # Data from external sources
│   ├── processed/        # Cleaned/transformed data
│   ├── raw/              # Original, immutable data
├── notebooks/            # Jupyter notebooks for analysis
├── report/               # LaTeX reporting
│   ├── figures/          # Generated plots
│   ├── tables/           # Generated tables
│   └── report.tex        # LaTeX template
├── {{ cookiecutter.repo_name }}/  # Python package for reusable code
├── environment.yml       # Conda environment
└── pyproject.toml        # Python project configuration
```

## Setup

This project uses conda for environment management.

```bash
# Environment should be created automatically during project generation
# If not, create it manually:
conda env create -f environment.yml

# Activate the environment
conda activate {{ cookiecutter.repo_name }}
```

## Usage

1. **Data Storage**: 
   - Place raw data in `data/raw/`
   - Store external data in `data/external/`
   - Save processed datasets in `data/processed/`

2. **Analysis**:
   - Create Jupyter notebooks in `notebooks/` for exploration and analysis
   - Write reusable functions in the `{{ cookiecutter.repo_name }}/` package

3. **Reporting**:
   - Generate figures and tables from your analysis
   - Save figures to `report/figures/`
   - Save tables to `report/tables/`
   - Edit `report/report.tex` to document your findings
   - Compile the LaTeX report using your preferred LaTeX editor or command line:
     ```bash
     cd report
     pdflatex report.tex
     ```

## Statistical Tools

This project is set up with:
- PyMC and ArviZ for Bayesian modeling
- NumPy, SciPy, pandas for data manipulation
- scikit-learn for machine learning
- statsmodels for statistical models
- Matplotlib and Seaborn for visualization

## Author

{{ cookiecutter.author_name }}

## Version

{{ cookiecutter.version }}