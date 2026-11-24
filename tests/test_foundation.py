import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_foundation", ROOT / "tools/verify_foundation.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class Foundation(unittest.TestCase):
    def sandbox(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dst = Path(tmp.name) / "hq"
        shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return dst

    def test_valid(self):
        v.validate(ROOT)

    def test_altered_law(self):
        dst = self.sandbox()
        path = dst / "CONSTITUTION.md"
        path.write_text(path.read_text().replace("Independence:", "Dependence:"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "law blob changed"):
            v.validate(dst)

    def test_altered_archive(self):
        dst = self.sandbox()
        path = dst / "evidence/imported/2026-11-24/HISTORICAL-DOGFOODING.md"
        path.write_bytes(path.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "archive blob mismatch"):
            v.validate(dst)

    def test_missing_product(self):
        dst = self.sandbox()
        path = dst / "products/registry.json"
        data = json.loads(path.read_text())
        data["products"].pop()
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "six unique products"):
            v.validate(dst)

    def test_duplicate_json(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            json.loads('{"a":1,"a":2}', object_pairs_hook=v.no_duplicates)

    def test_broken_navigation(self):
        dst = self.sandbox()
        path = dst / "README.md"
        path.write_bytes(path.read_bytes() + b"\n[missing](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "broken local link"):
            v.validate(dst)

if __name__ == "__main__":
    unittest.main()
