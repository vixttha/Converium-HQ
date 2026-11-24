"""Qualify two historical real defects; no coding-agent comparison."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROVENISTEM="e36fcd6d12633395e9b573228c0797ade9e775b0"
LYDITE="a19c58a5b005bfab3e60b0b16aae13bf01023118"
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def cmd(root,*argv,env=None):
    p=subprocess.run(argv,cwd=root,env=env,text=True,capture_output=True,timeout=120)
    print("$",*argv,"\n",p.stdout,p.stderr,flush=True)
    require(p.returncode==0,"command failed: "+argv[0])
    return p.stdout
def checkout(root,name,sha):
    dst=root/name
    dst.mkdir()
    cmd(dst,"git","init","-q")
    cmd(dst,"git","fetch","--no-tags","--depth=1","https://github.com/vixttha/"+name+".git",sha)
    cmd(dst,"git","checkout","--detach","FETCH_HEAD")
    require(cmd(dst,"git","rev-parse","HEAD").strip()==sha,"wrong source")
    return dst
def commit(root,message):
    cmd(root,"git","add",".")
    cmd(root,"git","-c","user.name=Benchmark fixture","-c","user.email=fixture@users.noreply.github.com","commit","-qm",message)
    return cmd(root,"git","rev-parse","HEAD").strip()
def provenistem(root):
    src=checkout(root,"Provenistem",PROVENISTEM)
    starter=root/"provenistem-fixture"
    shutil.copytree(src/"packages/provenistem",starter)
    record=starter/"ideas/records/IDEA-000001.json"
    original=(starter/"templates/idea.example.json").read_text(encoding="utf-8")
    record.write_text(original,encoding="utf-8")
    cmd(starter,sys.executable,"-B","tools/library.py","build")
    cmd(starter,sys.executable,"-B","tools/library.py","check")
    changed=original.replace('"lifecycle_status": "captured",','"lifecycle_status": "adopted",\n  "lifecycle_status": "captured",',1)
    require(changed!=original,"fixture anchor missing")
    record.write_text(changed,encoding="utf-8")
    cmd(starter,sys.executable,"-B","tools/library.py","check")
    print("QUALIFIED Provenistem #4: valid unique control and conflicting duplicate false PASS at",PROVENISTEM)
def lydite(root):
    src=checkout(root,"Lydite-Test-Vault-Template",LYDITE)
    adopter=root/"lydite-fixture";adopter.mkdir()
    shutil.copytree(src/"starter/test-vault",adopter/"test-vault")
    cases=adopter/"test-vault/cases.md"
    with cases.open("a",encoding="utf-8") as file:
        file.write("| CLI-001 | CLI | P0 | Node and Python | Quote observation and receipt. |\n")
    cmd(adopter,"git","init","-q")
    control=commit(adopter,"Valid shared-evidence control")
    rel="test-vault/examples/shared-evidence/"
    test=adopter/rel/"app.test.mjs"
    def shared(label,expected,sha):
        with TemporaryDirectory(dir=root) as d:
            receipts=Path(d)/"receipts";receipts.mkdir()
            evidence=Path(d)/"observation.json"
            env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","VAULT_EXAMPLE_PYTHON":sys.executable,
                 "VAULT_EXAMPLE_RECEIPTS":str(receipts),"VAULT_EXAMPLE_EVIDENCE":str(evidence)}
            out=cmd(adopter,"node",rel+"run-node.mjs",env=env)
            require(re.search(r"(?m)^# pass "+str(expected)+r"\s*$",out),"unexpected native test count")
            cmd(adopter,sys.executable,rel+"check.py",env=env)
            result=cmd(adopter,sys.executable,"test-vault/verify_receipts.py","--case",rel+"case.json","--receipts",str(receipts),"--evidence",str(evidence),env=env)
            receipt=json.loads((receipts/"node.json").read_text())
            require("Overall: PASS" in result and receipt["status"]=="pass" and receipt["checkout_sha"]==sha,"expected observed PASS missing")
            print("FIXTURE",label,"commit",sha,"native passes",expected,"receipt PASS")
    shared("positive",2,control)
    test.write_text("""import test, { before } from 'node:test';
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
before(() => {
  const app=fileURLToPath(new URL('./app.mjs', import.meta.url));
  writeFileSync(process.env.VAULT_EXAMPLE_EVIDENCE,execFileSync(process.execPath,[app,'125','3']));
});
test('skipped test', {skip:true}, () => {});
""",encoding="utf-8")
    skipped=commit(adopter,"Skip-only native suite")
    shared("skip-only",0,skipped)
    print("QUALIFIED Lydite #117: zero native passes still credited PASS at source",LYDITE)
if __name__=="__main__":
    with TemporaryDirectory(prefix="converium-qualification-") as tmp:
        root=Path(tmp)
        print("Python",sys.version)
        cmd(root,"node","--version")
        provenistem(root)
        lydite(root)
    print("QUALIFICATION PASS: two reproduced historical defects; no agent comparison or product fix")
