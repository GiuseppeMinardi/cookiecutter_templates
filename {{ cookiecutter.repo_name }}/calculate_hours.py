"""
Calculate work hours and associated costs from a CSV log file.

This module reads a CSV file containing work session start and end times,
calculates the duration of each session, computes the associated cost based
on an hourly rate, and exports the results to a formatted Excel file.
"""

import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import pandas as pd

path_file = Path(__file__).parent.joinpath("ore_lavorate.csv")
output_file = Path(__file__).parent.joinpath("ore_lavorate_calcolate.xlsx")

hourly_fee = 25

if not path_file.exists():
    path_file.touch()  # Create an empty file if it doesn't exist
    with path_file.open("w") as f:
        f.write("start,end,note\n")  # Write header for the CSV
    sys.exit(
        f"Created empty CSV at {path_file}. Please populate it with data and rerun the script."
    )

# --- 1. Data Processing ---
dataset = pd.read_csv(path_file).assign(
    start=lambda df_: pd.to_datetime(df_.start, format="%d/%m/%Y_%H:%M"),
    end=lambda df_: pd.to_datetime(df_.end, format="%d/%m/%Y_%H:%M"),
)

dataset["duration_hrs"] = (
    dataset["end"].sub(dataset["start"]).dt.total_seconds().div(3600)
)
dataset["cost_eur"] = dataset["duration_hrs"] * hourly_fee

dataset.to_excel(output_file, index=False)

# --- 2. Styling (openpyxl) ---
wb = load_workbook(output_file)
ws = wb.active
last_row = ws.max_row

# Styles
header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
summary_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
white_font = Font(color="FFFFFF", bold=True)
bold_font = Font(bold=True)
thin_border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)

# Format Main Table Headers
for cell in ws[1]:
    cell.fill = header_fill
    cell.font = white_font
    cell.alignment = Alignment(horizontal="center")
    cell.border = thin_border

# Format Data Body
for row in ws.iter_rows(min_row=2, max_row=last_row):
    row[2].number_format = '0.00 "hrs"'  # Column C (index 2)
    row[3].number_format = "€ #,##0.00"  # Column D (index 3)
    for cell in row:
        cell.border = thin_border

# --- 3. Dedicated Summary Section (Top Right) ---
# Placing Summary in G1:I2 area
summary_row = 2
total_hours_col = 8  # H
total_cost_col = 9  # I

# Labels
ws.cell(row=1, column=total_hours_col, value="TOTAL HOURS").font = bold_font
ws.cell(row=1, column=total_cost_col, value="TOTAL COST").font = bold_font
ws.cell(row=summary_row, column=7, value="TOTAL DUE:").font = bold_font

# Formulas (Summing columns C and D)
total_hrs_cell: Cell = ws.cell(
    row=summary_row, column=total_hours_col, value=f"=SUM(D2:D{last_row})"
)
total_cost_cell: Cell = ws.cell(
    row=summary_row, column=total_cost_col, value=f"=SUM(E2:E{last_row})"
)

# Styling Summary Area
for col in range(7, 10):
    for r in range(1, 3):
        cell = ws.cell(row=r, column=col)
        if r == summary_row and col >= 8:
            cell.fill = summary_fill
            cell.font = bold_font
        cell.border = thin_border

total_hrs_cell.number_format = '0.00 "hrs"'
total_cost_cell.number_format = "€ #,##0.00"

# Adjust Column Widths
widths: dict[str, int] = {"A": 20, "B": 20, "C": 15, "D": 15, "G": 15, "H": 15, "I": 15}
for col, width in widths.items():
    ws.column_dimensions[col].width = width

wb.save(output_file)
print("Client-ready Excel generated with side-summary.")
