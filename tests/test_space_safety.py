"""Enforce strict boundaries for the hosted illustrative Space."""
import ast
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[1]


class PublicSpaceSafetyTests(unittest.TestCase):
    def test_hosted_demo_is_synthetic_only(self):
        text = (BASE / "hf-space" / "app.py").read_text(encoding="utf-8")
        ast.parse(text)
        for forbidden in ("gr.File(", "gr.Textbox(", "gr.UploadButton(",
                          "gr.DownloadButton(", "interactive=True", ".to_csv(",
                          "read_csv(", ".change(", ".click(", "tempfile"):
            with self.subTest(pattern=forbidden):
                self.assertNotIn(forbidden, text)
        self.assertIn("interactive=False", text)
        self.assertIn("EXAMPLE_RESULTS", text)

    def test_static_fixture_agrees_with_local_authoritative_rules(self):
        import pandas as pd
        from scripts.modules.clean_and_categorize import categorize_title
        from scripts.modules.analyze_and_decide import action_recommendation
        from scripts.modules.engagement_priority import compute_priority_score, assign_priority
        tree = ast.parse((BASE / "hf-space" / "app.py").read_text(encoding="utf-8"))
        fixtures = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ("SAMPLE", "EXAMPLE_RESULTS"):
                        fixtures[target.id] = ast.literal_eval(node.value.args[0])
        self.assertEqual(len(fixtures["SAMPLE"]), len(fixtures["EXAMPLE_RESULTS"]))
        for contact, result in zip(fixtures["SAMPLE"], fixtures["EXAMPLE_RESULTS"]):
            role = categorize_title(contact["Position"])
            self.assertEqual(role, result["Category"])
            self.assertEqual(action_recommendation(role), result["Recommendation"])
            score = compute_priority_score(pd.Series({**contact, "Category": role}))
            self.assertEqual(score, result["Priority Score"])
            self.assertEqual(assign_priority(score), result["Priority"])

    def test_space_deployment_requires_explicit_owner_consent(self):
        text = (BASE / ".github/workflows/sync-huggingface.yml").read_text(encoding="utf-8")
        triggers = text.split("jobs:", 1)[0]
        self.assertIn("workflow_dispatch:", triggers)
        self.assertIn("confirm_publication:", triggers)
        self.assertIn("default: false", triggers)
        self.assertNotIn("  push:", triggers)
        self.assertIn("inputs.confirm_publication == true", text)
        self.assertIn("persist-credentials: false", text)

    def test_legacy_removal_entry_point_is_not_shipped(self):
        self.assertFalse((BASE / "linkedin_remove_connections.py").exists())
