import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / "data" / "sales.csv"
OUTPUT = BASE / "output"
REPORT = OUTPUT / "summary.json"
INVALID = OUTPUT / "invalid_rows.csv"
PRODUCTS = OUTPUT / "product_summary.csv"

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    totals = defaultdict(lambda: {
        "quantity": 0,
        "revenue": Decimal("0")
    })
    invalid_rows = []
    rows_read = 0
    valid_rows = 0
    total_revenue = Decimal("0")

    if not INPUT.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT}")

    with INPUT.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"date", "product", "quantity", "unit_price"}

        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV must contain columns: {sorted(required)}")

        for line_number, row in enumerate(reader, start=2):
            rows_read += 1

            try:
                date = (row.get("date") or "").strip()
                product = (row.get("product") or "").strip()
                quantity_text = (row.get("quantity") or "").strip()
                price_text = (row.get("unit_price") or "").strip()

                if not date or not product:
                    raise ValueError("Date and product are required")

                try:
                    quantity = int(quantity_text)
                except ValueError:
                    raise ValueError("Quantity must be a whole number")

                try:
                    price = Decimal(price_text)
                except InvalidOperation:
                    raise ValueError("Unit price must be a valid number")

                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
                if not price.is_finite() or price < 0:
                    raise ValueError("Unit price must be finite and non-negative")

                revenue = price * quantity
                totals[product]["quantity"] += quantity
                totals[product]["revenue"] += revenue
                total_revenue += revenue
                valid_rows += 1

            except (ValueError, InvalidOperation, TypeError) as error:
                invalid_rows.append({
                    "line_number": line_number,
                    "date": row.get("date", ""),
                    "product": row.get("product", ""),
                    "quantity": row.get("quantity", ""),
                    "unit_price": row.get("unit_price", ""),
                    "error": str(error)
                })

    with INVALID.open("w", newline="", encoding="utf-8") as file:
        fields = [
            "line_number", "date", "product",
            "quantity", "unit_price", "error"
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(invalid_rows)

    with PRODUCTS.open("w", newline="", encoding="utf-8") as file:
        fields = ["product", "quantity_sold", "revenue"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for product, values in sorted(totals.items()):
            writer.writerow({
                "product": product,
                "quantity_sold": values["quantity"],
                "revenue": f"{values['revenue']:.2f}"
            })

    report = {
        "input_file": str(INPUT.relative_to(BASE)),
        "rows_read": rows_read,
        "valid_rows": valid_rows,
        "invalid_rows": len(invalid_rows),
        "products_count": len(totals),
        "units_sold": sum(v["quantity"] for v in totals.values()),
        "total_revenue": f"{total_revenue:.2f}",
        "top_product_by_revenue": (
            max(totals, key=lambda p: totals[p]["revenue"])
            if totals else None
        )
    }

    REPORT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=" * 40)
    print("PYTHON DATA ANALYZER")
    print("=" * 40)
    for key, value in report.items():
        print(f"{key}: {value}")
    print("\nReports saved:")
    print(REPORT)
    print(PRODUCTS)
    print(INVALID)

if __name__ == "__main__":
    main()
