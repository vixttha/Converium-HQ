"""Read-only verification for Converium knowledge records, not a product runtime."""
import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
IDS = {"vib", "provenistem", "lydite", "veraphify", "readme-hq", "brand-identity"}
LAW_BLOB = "8f1956821ee179334c20e3f4a3d49dae2f5cbaf2"
LAW_START = b"<!-- engineering-laws:start -->"
LAW_END = b"<!-- engineering-laws:end -->"
COUNTS = {"cases": 23, "source_pins": 22, "distinct_runs": 21,
          "internal_cross_product_operational_edges": 14, "external_adopter_cases": 1}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def no_duplicates(items):
    out = {}
    for k, v in items:
        require(k not in out, "duplicate JSON key: " + k)
        out[k] = v
    return out

def load(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)

def laws(raw):
    require(raw.count(LAW_START) == raw.count(LAW_END) == 1, "invalid law delimiters")
    return raw.split(LAW_START, 1)[1].split(LAW_END, 1)[0]

def safe_path(path):
    require(isinstance(path, str) and all(x not in ("", ".", "..") for x in path.split("/"))
            and "\\" not in path, "unsafe path")
    return path

def sha(value):
    require(isinstance(value, str) and re.fullmatch("[0-9a-f]{40}", value), "invalid SHA")
    return value

def repo(value):
    require(isinstance(value, str) and re.fullmatch(r"vixttha/[A-Za-z0-9_.-]+", value), "invalid repo")
    return value

def read_public(repository, revision, path):
    url = "https://raw.githubusercontent.com/" + repo(repository) + "/" + sha(revision) + "/" + quote(safe_path(path), safe="/")
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent":"converium-hq-readback"}), timeout=20) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            if attempt == 2 or isinstance(exc, HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                raise
            time.sleep(attempt + 1)

def validate(root=ROOT, remote=False):
    required = ["README.md", "CONSTITUTION.md", "AGENTS.md", "STATE.md", "history/DECISIONS.md",
                "history/TIMELINE.md", "handoffs/LATEST.md", "roadmap/README.md", "products/README.md", "evidence/README.md"]
    for name in required:
        require((root / name).is_file(), "missing " + name)
    constitution = (root / "CONSTITUTION.md").read_bytes()
    law = laws(constitution)
    require(len(re.findall(rb"(?m)^[1-6]\. \*\*", law)) == 6, "six laws required")
    # Constitution embeds the entire exact source document, with HQ-specific text appended.
    source = constitution.split(b"\n## Converium HQ boundary\n", 1)[0]
    require(blob(source) == LAW_BLOB, "constitution source law blob changed")
    registry = load(root / "products/registry.json")
    products = registry["products"]
    require(len(products) == 6 and {p["id"] for p in products} == IDS, "six unique products required")
    require(len({p["repo"] for p in products}) == 6, "duplicate product repo")
    for p in products:
        repo(p["repo"]); sha(p["sha"]); sha(p["policy"]); sha(p["entry_blob"]); safe_path(p["entry"])
        require((root / "products" / (p["id"] + ".md")).is_file(), "missing product profile")
        profile = (root / "products" / (p["id"] + ".md")).read_text(encoding="utf-8")
        require(p["sha"] in profile and p["repo"] in profile, "profile pin mismatch")
    manifest = load(root / "evidence/manifest.json")
    require(manifest["counts"] == COUNTS, "historical counts changed")
    origin = manifest["origin"]
    repo(origin["repository"]); sha(origin["commit"])
    files = manifest["files"]
    require(len(files) == 9 and len({f["path"] for f in files}) == 9, "nine unique archive files required")
    for f in files:
        path = safe_path(f["path"]); safe_path(f["source_path"]); sha(f["blob"])
        require(path.startswith("evidence/imported/2026-11-24/"), "wrong archive directory")
        require(path.rsplit("/",1)[-1] == f["source_path"].rsplit("/",1)[-1], "archive name mismatch")
        require(blob((root / path).read_bytes()) == f["blob"], "archive blob mismatch: " + path)
        if remote:
            require(blob(read_public(origin["repository"], origin["commit"], f["source_path"])) == f["blob"], "origin blob mismatch")
    evidence = load(root / "evidence/imported/2026-11-24/dogfooding-evidence.json")
    cases = evidence["cases"]
    require(evidence["counts"] == COUNTS and len(cases) == 23 and len({c["id"] for c in cases}) == 23, "evidence register mismatch")
    require(len({(c["source"]["repository"],c["source"]["commit"],c["source"]["path"]) for c in cases}) == 22, "source count")
    require(len({(c["run"]["repository"],c["run"]["id"]) for c in cases if c["run"]}) == 21, "run count")
    edges = {(c["provider"], c["beneficiary"]) for c in cases if c["provider"] != c["beneficiary"] and c["classification"] not in ("feedback", "external-adopter")}
    require(len(edges) == 14, "relationship count")
    v = manifest["verification"]
    require((v["configuration_count"],v["nonempty_count"],v["native_smokes"],v["negative_controls"]) == (64,63,192,2), "compatibility totals")
    for path in required + ["products/" + p["id"] + ".md" for p in products]:
        text = (root / path).read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#",1)[0]
            dest = ((root / path).parent / local).resolve()
            require(dest.is_relative_to(root.resolve()) and dest.exists(), "broken local link: " + path + " -> " + target)
    if remote:
        for p in products:
            require(blob(read_public(p["repo"], p["sha"], p["entry"])) == p["entry_blob"], "entry blob mismatch: "+p["id"])
            require(blob(read_public(p["repo"], p["policy"], "ENGINEERING-LAWS.md")) == LAW_BLOB, "law parity mismatch: "+p["id"])
            print("Verified product source and historical law:", p["id"])
    print("PASS: six laws; six independent product profiles; nine archive blobs; 23 cases; 22 source pins; 21 historical runs; 14 edges; local navigation.")
    if remote:
        print("PASS: 9 origin archive blobs + 6 product entry blobs + 6 law documents independently read from exact public Git revisions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote", action="store_true")
    validate(remote=parser.parse_args().remote)
