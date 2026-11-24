import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
try:
    import graphify_hq as g
except ModuleNotFoundError as e:
    if e.name != 'graphify': raise
    raise unittest.SkipTest('Graphify dependency only installed in dedicated graph job')
class Graph(unittest.TestCase):
    def setUp(self):
        self.data=g.source_inputs()
        self.s=g.project(self.data)
    def test_valid(self): g.validate_projection(self.s,g.project(self.data))
    def test_fabricated_edge(self):
        self.s["edges"].pop()
        with self.assertRaisesRegex(ValueError,"projection differs"): g.validate_projection(self.s,g.project(self.data))
    def test_missing_case(self):
        key="evidence/imported/2026-11-24/dogfooding-evidence.json"
        d=json.loads(self.data[key]);d["cases"].pop();self.data[key]=json.dumps(d).encode()
        with self.assertRaisesRegex(ValueError,"coverage mismatch"): g.project(self.data)
    def test_duplicate_case(self):
        key="evidence/imported/2026-11-24/dogfooding-evidence.json"
        d=json.loads(self.data[key]);d["cases"].append(d["cases"][0]);self.data[key]=json.dumps(d).encode()
        with self.assertRaisesRegex(ValueError,"duplicate case"): g.project(self.data)
