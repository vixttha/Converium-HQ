import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
class Baseline(unittest.TestCase):
    def test_integrated_receipt(self):
        x=load("baseline/receipt.json")
        self.assertEqual(x["merged_pr"],8)
        self.assertEqual(x["main"],"b913f99149d1e9ac44727a1226fafef2f2f1d9a1")
        self.assertEqual({r["id"] for r in x["runs"]},{45383486121,45383486118})
        self.assertEqual(sum(r["tests"] for r in x["runs"]),20)
        self.assertTrue(all(r["conclusion"]=="success" for r in x["runs"]))
        self.assertFalse(x["baseline_accepted"])
        self.assertIn("fresh-chatgpt",x["pending"])
    def test_rights_pins(self):
        x=load("commercial/audit-2026-11-24.json")
        old=load("commercial/rights-inventory.json")
        self.assertEqual({(p["id"],p["commit"]) for p in x["products"]},{(p["id"],p["commit"]) for p in old["entries"]})
        self.assertEqual({p["id"] for p in x["products"] if p["release"]},{"lydite","brand-identity"})
        self.assertEqual({p["id"] for p in x["products"] if not p["notice"]},{"vib","readme-hq"})
        self.assertFalse(x["ownership_verified"])
        self.assertFalse(x["distribution_approved"])
    def test_unapproved_decisions(self):
        self.assertFalse(load("brand/tokens.json")["approved"])
        self.assertIn("not a release",(ROOT/"baseline/ACCEPTANCE.md").read_text())
        self.assertIn("has not been executed",(ROOT/"recovery/FINAL-TRIAL.md").read_text())
        self.assertIn("No new coding trials executed",(ROOT/"benchmarks/README.md").read_text())
    def test_navigation(self):
        for p in ["baseline/ACCEPTANCE.md","baseline/receipt.json","commercial/LICENSING-AUDIT.md","commercial/READINESS.md","brand/NAME-REVIEW.md","recovery/FINAL-TRIAL.md","benchmarks/README.md"]:
            self.assertTrue((ROOT/p).is_file())
