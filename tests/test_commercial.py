import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Commercial(unittest.TestCase):
    def test_rights_inventory(self):
        r=json.loads((ROOT/"commercial/rights-inventory.json").read_text())
        p=json.loads((ROOT/"products/registry.json").read_text())["products"]
        self.assertEqual({(x["id"],x["repository"],x["commit"]) for x in r["entries"]},{(x["id"],x["repo"],x["sha"]) for x in p})
        self.assertEqual({x["id"] for x in r["entries"] if not x["notice"]},{"vib","readme-hq"})
        self.assertFalse(r["distribution_approved"])
    def test_scope(self):
        s=(ROOT/"commercial/README.md").read_text()
        self.assertIn("No sales or launch authorized",s)
        self.assertIn("not universal agent support",s)
        self.assertIn("not forecast revenue",s)
