from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from scripts.modules.analyze_and_decide import action_recommendation
from scripts.modules.clean_and_categorize import categorize_title, read_connections_csv
from scripts.modules.engagement_priority import assign_priority, compute_priority_score


class CategorizationTests(unittest.TestCase):
    def test_expected_role_categories(self) -> None:
        self.assertEqual(categorize_title("Senior Product Manager"), "Product")
        self.assertEqual(categorize_title("Machine Learning Engineer"), "Developer")
        self.assertEqual(categorize_title("Technical Recruiter"), "HR / Recruiter")
        self.assertEqual(categorize_title("Founder"), "Other")

    def test_missing_title_is_other(self) -> None:
        self.assertEqual(categorize_title(None), "Other")

    def test_linkedin_style_preamble_is_detected(self) -> None:
        content = (
            "Notes: This is synthetic metadata before the export header.\n"
            "Generated for testing only.\n"
            "First Name,Last Name,Company,Position,URL\n"
            "Ava,Example,Example Labs,Product Manager,https://example.com/profile\n"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "Connections.csv"
            path.write_text(content, encoding="utf-8")
            dataframe = read_connections_csv(path)
        self.assertEqual(list(dataframe.columns), ["First Name", "Last Name", "Company", "Position", "URL"])
        self.assertEqual(dataframe.iloc[0]["Position"], "Product Manager")

    def test_missing_position_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad.csv"
            path.write_text("Name,Company\nExample,Example Co\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_connections_csv(path)


class RecommendationTests(unittest.TestCase):
    def test_other_requires_manual_review(self) -> None:
        self.assertEqual(action_recommendation("Other"), "Review manually")

    def test_unknown_category_requires_manual_review(self) -> None:
        self.assertEqual(action_recommendation("Unexpected"), "Review manually")


class PriorityTests(unittest.TestCase):
    def test_priority_score_is_deterministic(self) -> None:
        row = pd.Series(
            {
                "Category": "Product",
                "Company": "Example Labs",
                "Position": "Product Manager",
                "URL": "https://example.com/profile",
            }
        )
        first = compute_priority_score(row)
        second = compute_priority_score(row)
        self.assertEqual(first, 8)
        self.assertEqual(first, second)
        self.assertEqual(assign_priority(first), "High")

    def test_other_with_sparse_profile_is_low(self) -> None:
        row = pd.Series({"Category": "Other", "Company": "", "Position": "Founder", "URL": ""})
        self.assertEqual(compute_priority_score(row), 2)
        self.assertEqual(assign_priority(2), "Low")


if __name__ == "__main__":
    unittest.main()
