import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "data" / "sales.csv"
OUTPUT = BASE / "output"

class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.original = INPUT.read_bytes()

    def tearDown(self):
        INPUT.write_bytes(self.original)

    def run_analyzer(self):
        return subprocess.run(
            [sys.executable, str(BASE / "analyzer.py")],
            capture_output=True,
            text=True
        )

    def test_sample_data(self):
        result = self.run_analyzer()
        self.assertEqual(result.returncode, 0, result.stderr)

        report = json.loads(
            (OUTPUT / "summary.json").read_text(encoding="utf-8")
        )
        self.assertEqual(report["rows_read"], 7)
        self.assertEqual(report["valid_rows"], 7)
        self.assertEqual(report["invalid_rows"], 0)
        self.assertEqual(report["units_sold"], 18)
        self.assertEqual(report["total_revenue"], "685.50")

    def test_invalid_quantity_is_reported(self):
        with INPUT.open("a", encoding="utf-8") as file:
            file.write("2026-10-08,TestProduct,abc,10.00\n")

        result = self.run_analyzer()
        self.assertEqual(result.returncode, 0, result.stderr)

        report = json.loads(
            (OUTPUT / "summary.json").read_text(encoding="utf-8")
        )
        self.assertEqual(report["invalid_rows"], 1)

        with (OUTPUT / "invalid_rows.csv").open(
            newline="", encoding="utf-8"
        ) as file:
            invalid = list(csv.DictReader(file))

        self.assertEqual(len(invalid), 1)
        self.assertIn("Quantity", invalid[0]["error"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
