# Python Data Analyzer

A lightweight Python tool for analyzing sales data from CSV files.

## Features

- Reads CSV files
- Validates input data
- Detects invalid rows
- Calculates total revenue and units sold
- Creates a product summary report
- Exports results to JSON and CSV

## Requirements

Python 3.9 or newer.
No external packages required.

## Usage

1. Put your sales data in `data/sales.csv`.
2. Run:

   python analyzer.py

3. Check the generated reports in the `output/` directory.

## Output Files

- `summary.json`: Overall statistics
- `product_summary.csv`: Revenue by product
- `invalid_rows.csv`: Invalid records and error messages

## Limitations

This is a demonstration project using sample data.
Validate business requirements before using it in production.

## License

MIT
