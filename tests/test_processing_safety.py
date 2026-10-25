"""Synthetic security, reliability and privacy regression checks."""
from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
from openpyxl import load_workbook

from scripts.main import run_pipeline
from scripts.modules.clean_and_categorize import read_connections_csv
from scripts.modules.analyze_and_decide import analyze_and_decide
from scripts.modules.excel_safety import safe_for_excel


HEADER = "First Name,Last Name,Position,Company,URL\n"


class ProcessingBoundaryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.csv = self.dir / "synthetic.csv"
        self.out = self.dir / "results"

    def save(self, rows):
        self.csv.write_text(HEADER + rows, encoding="utf-8")

    def test_duplicate_columns_and_empty_files_fail(self):
        for text in ("", HEADER,
                     "First Name,Position,Position\nA,Product Manager,B\n"):
            with self.subTest(text=text):
                self.csv.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_connections_csv(self.csv)

    def test_input_limits_for_bytes_rows_and_columns(self):
        self.save("A,Example,Product Manager,Example Co,https://example.invalid\n")
        with patch("scripts.modules.clean_and_categorize.MAX_INPUT_BYTES", 5):
            with self.assertRaisesRegex(ValueError, "20 MiB"):
                read_connections_csv(self.csv)
        with patch("scripts.modules.clean_and_categorize.MAX_INPUT_ROWS", 0):
            with self.assertRaisesRegex(ValueError, "50000-row"):
                read_connections_csv(self.csv)
        with patch("scripts.modules.clean_and_categorize.MAX_COLUMNS", 2):
            with self.assertRaisesRegex(ValueError, "columns"):
                read_connections_csv(self.csv)

    def test_fresh_input_always_supersedes_stale_intermediates(self):
        self.save("A,Example,Product Manager,Example Co,https://example.invalid\n")
        run_pipeline(self.csv, self.out, "prioritize")
        before = pd.read_excel(self.out / "linkedin_priority.xlsx")
        self.assertEqual(before.iloc[0]["Category"], "Product")
        self.save("B,Example,Technical Recruiter,Example Co,https://example.invalid\n")
        run_pipeline(self.csv, self.out, "prioritize")
        after = pd.read_excel(self.out / "linkedin_priority.xlsx")
        self.assertEqual(after.iloc[0]["Category"], "HR / Recruiter")
        self.assertEqual(after.iloc[0]["First Name"], "B")

    def test_formula_like_values_are_never_written_as_excel_formulas(self):
        frame = pd.DataFrame([{
            "First Name": "=2+2", "Position": "Product Manager",
            "Company": " +SUM(1,2)", "URL": "@malicious",
            "Category": "Product",
        }])
        self.assertEqual(safe_for_excel(frame).iloc[0]["First Name"], "'=2+2")
        source = self.dir / "synthetic-categorized.csv"
        output = self.dir / "result.xlsx"
        frame.to_csv(source, index=False)
        analyze_and_decide(source, output)
        sheet = load_workbook(output).active
        self.assertEqual(sheet["A2"].data_type, "s")
        self.assertEqual(sheet["A2"].value, "'=2+2")
        self.assertEqual(sheet["C2"].data_type, "s")
        self.assertEqual(sheet["D2"].data_type, "s")

    def test_complete_report_pipeline_renders_six_charts(self):
        # Offline end-to-end coverage of both charting backends.
        self.save(
            "A,Example,Product Manager,Example Co,https://example.invalid/a\n"
            "B,Example,Technical Recruiter,Example Co,https://example.invalid/b\n"
            "C,Example,Backend Engineer,Example Co,https://example.invalid/c\n"
            "D,Example,Founder,Example Co,https://example.invalid/d\n"
        )
        run_pipeline(self.csv, self.out, "all")
        expected = (
            "reports/category_distribution_pie.png",
            "reports/action_recommendation_count.png",
            "reports/category_vs_action.png",
            "priority_reports/priority_distribution_pie.png",
            "priority_reports/category_vs_priority.png",
            "priority_reports/priority_score_boxplot.png",
        )
        for relative in expected:
            with self.subTest(file=relative):
                image = self.out / relative
                self.assertTrue(image.is_file())
                self.assertGreater(image.stat().st_size, 500)

    @unittest.skipUnless(os.name == "posix", "POSIX creation permissions")
    def test_new_files_not_world_readable(self):
        self.save("A,Example,Product Manager,Example Co,https://example.invalid\n")
        run_pipeline(self.csv, self.out, "prioritize")
        self.assertEqual(self.out.stat().st_mode & 0o077, 0)
        self.assertEqual((self.out / "linkedin_priority.xlsx").stat().st_mode & 0o077, 0)
