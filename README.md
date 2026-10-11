# Python Data Analyzer

A lightweight Python tool for analyzing sales data from CSV files.

## Features

- Reads sales data from CSV files
- Validates required columns and input values
- Detects and reports invalid rows
- Calculates total revenue and units sold
- Generates product-level revenue summaries
- Generates monthly sales reports
- Exports reports to JSON and CSV
- Includes automated unit tests
- Uses only the Python standard library

## Requirements

- Python 3.9 or newer
- No external packages required

## Usage

Place your sales data in `data/sales.csv`.

Run the main analyzer:

    python analyzer.py

Generate the monthly report:

    python monthly_report.py

Run the tests:

    python -m unittest discover -s tests -v

## Output Files

Reports are generated in the `output/` directory:

- `summary.json` — overall sales statistics
- `product_summary.csv` — revenue summary by product
- `invalid_rows.csv` — invalid records and error messages
- `monthly_sales.csv` — monthly order counts, units sold, and revenue

## Input Data Format

The CSV file must contain these columns: `date`, `product`, `quantity`, `unit_price`.

Dates should use the `YYYY-MM-DD` format.

## Limitations

This is a demonstration project using sample data. Validate business requirements before using it in production.

## License

MIT
