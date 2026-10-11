import csv
import subprocess
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPORT = BASE / "output" / "monthly_sales.csv"


class MonthlyReportTests(unittest.TestCase):
    def test_monthly_report_matches_sample_data(self):
        result = subprocess.run(
            [sys.executable, str(BASE / "monthly_report.py")],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Invalid rows skipped: 0", result.stdout)

        with REPORT.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["month"], "2026-10")
        self.assertEqual(rows[0]["orders"], "7")
        self.assertEqual(rows[0]["units_sold"], "18")
        self.assertEqual(rows[0]["revenue"], "685.50")


if __name__ == "__main__":
    unittest.main(verbosity=2)
