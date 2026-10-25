"""Verify the public Space is static, fictional, and not a contact service."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

BASE = Path(__file__).resolve().parents[1]


class Tables(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = {}
        self.active = None
        self.current = None
        self.cell = None
        self.tags = []

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        self.tags.append((tag, props))
        if tag == "table":
            self.active = props["id"]
            self.ids[self.active] = []
        if tag == "tr":
            self.current = []
        if tag in ("td", "th"):
            self.cell = ""

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.current is not None:
            self.current.append(self.cell.strip())
            self.cell = None
        if tag == "tr" and self.active is not None and self.current is not None:
            self.ids[self.active].append(self.current)
            self.current = None
        if tag == "table":
            self.active = None


class PublicSpaceSafetyTests(unittest.TestCase):
    def setUp(self):
        self.html = (BASE / "hf-space" / "index.html").read_text(encoding="utf-8")
        self.parsed = Tables()
        self.parsed.feed(self.html)

    def test_only_reviewed_static_files_are_present(self):
        self.assertEqual(
            {f.name for f in (BASE / "hf-space").iterdir() if f.is_file()},
            {"README.md", "index.html"},
        )
        meta = (BASE / "hf-space" / "README.md").read_text(encoding="utf-8")
        self.assertIn("sdk: static", meta)
        self.assertIn("app_file: index.html", meta)
        self.assertNotIn("sdk: gradio", meta)

    def test_no_processing_controls_or_external_assets(self):
        for forbidden in ("script", "form", "input", "button", "textarea", "select",
                          "iframe", "object", "embed", "img", "link"):
            with self.subTest(tag=forbidden):
                self.assertNotIn(forbidden, [tag for tag, _ in self.parsed.tags])
        for _, attrs in self.parsed.tags:
            self.assertNotIn("src", attrs)
            self.assertNotIn("action", attrs)
            self.assertFalse(any(key.startswith("on") for key in attrs))
        self.assertIn("default-src 'none'", self.html)
        self.assertIn("form-action 'none'", self.html)
        self.assertEqual(len(re.findall(r"<tr>", self.html)), 12)

    def test_fictional_tables_match_authoritative_cli_rules(self):
        from scripts.modules.clean_and_categorize import categorize_title
        from scripts.modules.analyze_and_decide import action_recommendation
        from scripts.modules.engagement_priority import compute_priority_score, assign_priority
        import pandas as pd
        raw = self.parsed.ids["synthetic-input"][1:]
        processed = self.parsed.ids["synthetic-analysis"][1:]
        self.assertEqual(len(raw), len(processed))
        self.assertEqual(len(raw), 5)
        for (name, title, company), (out_name, role, recommendation, score, priority) in zip(raw, processed):
            self.assertEqual(name, out_name)
            self.assertTrue(name.endswith("Example"))
            self.assertEqual(categorize_title(title), role)
            self.assertEqual(action_recommendation(role), recommendation)
            row = pd.Series({"Category":role,"Position":title,"Company":company,"URL":"https://example.invalid"})
            self.assertEqual(compute_priority_score(row), int(score))
            self.assertEqual(assign_priority(int(score)), priority)

    def test_deployment_is_opt_in_and_prunes_only_old_runtime_files(self):
        text = (BASE / ".github/workflows/sync-huggingface.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("confirm_publication:", text)
        self.assertIn("default: false", text)
        self.assertNotIn("  push:", text.split("jobs:", 1)[0])
        self.assertIn("inputs.confirm_publication == true", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn("--delete app.py --delete requirements.txt", text)

    def test_remover_not_shipped(self):
        self.assertFalse((BASE / "linkedin_remove_connections.py").exists())
