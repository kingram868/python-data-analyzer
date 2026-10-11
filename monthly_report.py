import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / "data" / "sales.csv"
OUTPUT = BASE / "output" / "monthly_sales.csv"


def main():
    monthly = defaultdict(
        lambda: {"orders": 0, "units_sold": 0, "revenue": Decimal("0")}
    )
    invalid_rows = 0

    with INPUT.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"date", "product", "quantity", "unit_price"}

        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV must contain columns: {sorted(required)}")

        for row in reader:
            try:
                sale_date = date.fromisoformat((row.get("date") or "").strip())
                product = (row.get("product") or "").strip()
                quantity = int(row.get("quantity") or "")
                price = Decimal((row.get("unit_price") or "").strip())

                if not product or quantity <= 0:
                    raise ValueError("Invalid product or quantity")
                if not price.is_finite() or price < 0:
                    raise ValueError("Invalid price")

                month = sale_date.strftime("%Y-%m")
                monthly[month]["orders"] += 1
                monthly[month]["units_sold"] += quantity
                monthly[month]["revenue"] += price * quantity

            except (ValueError, InvalidOperation, TypeError):
                invalid_rows += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        fields = ["month", "orders", "units_sold", "revenue"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for month, values in sorted(monthly.items()):
            writer.writerow({
                "month": month,
                "orders": values["orders"],
                "units_sold": values["units_sold"],
                "revenue": f"{values['revenue']:.2f}",
            })

    print(f"Monthly report saved: {OUTPUT}")
    print(f"Invalid rows skipped: {invalid_rows}")


if __name__ == "__main__":
    main()
