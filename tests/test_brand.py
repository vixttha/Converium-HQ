import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
NS="{http://www.w3.org/2000/svg}"
def luminance(s):
    rgb=[int(s[i:i+2],16)/255 for i in (1,3,5)]
    values=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in rgb]
    return sum(x*y for x,y in zip(values,[.2126,.7152,.0722]))
class Brand(unittest.TestCase):
    def test_contrast(self):
        t=json.loads((ROOT/"brand/tokens.json").read_text())
        for mode in ("light","dark"):
            for key in ("text","accent"):
                a,b=sorted([luminance(t[mode]["canvas"]),luminance(t[mode][key])])
                self.assertGreaterEqual((b+.05)/(a+.05),4.5)
        self.assertFalse(t["approved"])
    def test_three_safe_vectors(self):
        p=ROOT/"brand/concepts"
        self.assertEqual(len(list(p.glob("*.svg"))),3)
        for file in p.glob("*.svg"):
            root=ET.parse(file).getroot()
            self.assertEqual(root.attrib["viewBox"],"0 0 96 96")
            self.assertIsNotNone(root.find(NS+"title"))
            self.assertIsNotNone(root.find(NS+"desc"))
            self.assertTrue(all(e.tag in {NS+x for x in ("svg","title","desc","g","path")} for e in root.iter()))
            self.assertFalse(any(k.startswith("on") or "href" in k for e in root.iter() for k in e.attrib))
