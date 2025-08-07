---
applyTo: "**"
---

# Data Science Project: {{cookiecutter.project_name}} Coding Standards

## What this project is about
{{ cookiecutter.description }}

## General Guidelines
- Always use type hints for function signatures and variables.
- Use numpy format for docstrings.
- Think critically and challenge ideas to ensure robustness and innovation.

## Naming Conventions
- Use `snake_case` for variables, functions, and methods.
- Use `PascalCase` for class names.
- Use `ALL_CAPS` for constants.
- Avoid single-character variable names unless in a loop or mathematical context.

## Documentation
- Always include docstrings for functions, classes, and modules.
- Use numpy format for docstrings. Example:

```python
def calculate_mean(data: List[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers.

    Parameters
    ----------
    data : List[float]
        List of numerical values.

    Returns
    -------
    float
        The arithmetic mean of the input data.
    """
    return sum(data) / len(data)
```

## Type Hints
- Always use type hints for function parameters and return values.
- Use `List`, `Dict`, `Tuple`, etc., from the `typing` module for complex types.

```python
from typing import List, Dict, Tuple

def process_data(data: List[Dict[str, float]]) -> Tuple[float, float]:
    """Process a list of dictionaries and return a tuple of summary statistics.

    Parameters
    ----------
    data : List[Dict[str, float]]
        List of dictionaries containing numerical data.

    Returns
    -------
    Tuple[float, float]
        A tuple containing the mean and standard deviation of the data.
    """
    # Processing logic here
    pass
```

## Code Quality
- Write unit tests for all functions and classes.
- Use meaningful variable names that reflect their purpose.
- Avoid hardcoding values; use constants or configuration files instead.
- Challenge assumptions and think critically about the problem and solution.

## Error Handling
- Use try/except blocks to handle exceptions gracefully.
- Log errors with sufficient context to aid in debugging.
- Validate input data to ensure it meets expected criteria.

```python
import logging

def safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers and handle potential errors.

    Parameters
    ----------
    numerator : float
        The numerator in the division.
    denominator : float
        The denominator in the division.

    Returns
    -------
    float
        The result of the division.

    Raises
    ------
    ValueError
        If the denominator is zero.
    """
    try:
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        return numerator / denominator
    except Exception as e:
        logging.error(f"Error in safe_divide: {e}")
        raise
```

## Collaboration
- Review and provide constructive feedback on pull requests.
- Document your thought process and decisions in code comments and commit messages.
- Be open to feedback and willing to refactor code for improvement.
