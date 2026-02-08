"""Docstring for {{ cookiecutter.repo_name }} main file."""
import argparse

from {{ cookiecutter.repo_name }} import logger
from {{ cookiecutter.repo_name }}.project_configs import ProjectPaths

project_paths = ProjectPaths()
logger.info(f"Project root directory: {project_paths.root.as_posix()}")

def clean_raw_data(input_csv_path: str, output_csv_path: str) -> None:
    """Clean raw data and save to a new CSV file."""
    # Placeholder for data cleaning logic
    logger.info(f"Cleaning raw data from {input_csv_path} and saving to {output_csv_path}")
    # Example: Load CSV, clean data, and save cleaned CSV
    # df = pd.read_csv(input_csv_path)
    # cleaned_df = clean_data(df)
    # cleaned_df.to_csv(output_csv_path, index=False)
    raise NotImplementedError("Data cleaning function is not implemented yet.")

def run_analysis(cleaned_csv_path: str, report_output_path: str) -> None:
    """Run data analysis and generate report."""
    # Placeholder for analysis logic
    logger.info(f"Running analysis on {cleaned_csv_path} and saving report to {report_output_path}")
    # Example: Load cleaned CSV, perform analysis, and save report
    # df = pd.read_csv(cleaned_csv_path)
    # analysis_results = analyze_data(df)
    # save_report(analysis_results, report_output_path)
    raise NotImplementedError("Data analysis function is not implemented yet.")

def main():
    """Main Function."""  # noqa: D401
    print("Starting {{ cookiecutter.repo_name }} application...")
    parser = argparse.ArgumentParser(description="Breath Frequency MedThesis CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Clean Command ---
    clean_parser = subparsers.add_parser("clean", help="Clean raw data")
    clean_parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=Path,
        help="Path to raw data",
    )
    clean_parser.add_argument(
        "-o",
        "--output",
        required=False,
        default=project_paths.data_folder.interim.joinpath("cleaned_data.csv"),
        type=Path,
        help="Path for cleaned data",
    )

    # Parse the arguments and call the appropriate function
    args = parser.parse_args()

    if args.command == "clean":
        clean_raw_data(input_csv_path=args.input, output_csv_path=args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()