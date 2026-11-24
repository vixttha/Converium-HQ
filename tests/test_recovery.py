"""Mechanical knowledge recovery checks, not an agent trial."""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
class Recovery(unittest.TestCase):
    def test_entry_points(self):
        agent = (ROOT/"AGENTS.md").read_text()
        for name in ("CONSTITUTION.md","STATE.md","history/DECISIONS.md","products/README.md","evidence/README.md","handoffs/LATEST.md","roadmap/README.md"):
            self.assertIn(name,agent)
            self.assertTrue((ROOT/name).is_file())
    def test_accepted_foundation(self):
        state=(ROOT/"STATE.md").read_text()
        self.assertIn("dc77ba9abe1e18fb9d27a12814213ce9acded31a",state)
        self.assertIn("45376454437",state)
        self.assertIn("PR #2",state)
    def test_evidence_bounds(self):
        m=json.loads((ROOT/"evidence/manifest.json").read_text())
        self.assertEqual(m["counts"]["cases"],23)
        self.assertEqual(m["counts"]["internal_cross_product_operational_edges"],14)
        self.assertEqual(m["verification"]["configuration_count"],64)
        self.assertEqual(m["verification"]["native_smokes"],192)
        self.assertIn("not established",(ROOT/"STATE.md").read_text())
    def test_independent_products(self):
        p=json.loads((ROOT/"products/registry.json").read_text())["products"]
        self.assertEqual(len({x["repo"] for x in p}),6)
        self.assertNotIn("vixttha/Converium-HQ",{x["repo"] for x in p})
