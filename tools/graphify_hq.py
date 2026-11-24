"""Revision-bound semantic projection using Graphify, with no remote writes."""
import asyncio
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from importlib.metadata import version
from collections import Counter
from graphify.build import build_from_json
from graphify.export import to_json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
PIN = json.loads((ROOT / "graphify/pins.json").read_text())
def require(ok, msg):
    if not ok: raise ValueError(msg)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def git(*args): return subprocess.check_output(["git", *args], cwd=ROOT)
def source_inputs():
    data={}
    for p in PIN["inputs"]:
        raw=git("cat-file","blob",PIN["source_commit"]+":"+p["path"])
        require(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==p["blob"],"source pin mismatch")
        require(raw==(ROOT/p["path"]).read_bytes(),"stale or altered current input: "+p["path"])
        data[p["path"]]=raw
    return data

def project(data):
    registry=json.loads(data["products/registry.json"])
    casepath="evidence/imported/2026-11-24/dogfooding-evidence.json"
    cases=json.loads(data[casepath])["cases"]
    nodes=[]; edges=[]; names={}
    def node(id,label,kind,path):
        nodes.append(dict(id=id,label=label,file_type=kind,source_file=path,source_location=None))
    def edge(a,b,rel,path):
        edges.append(dict(source=a,target=b,relation=rel,source_file=path,source_location=None,confidence="EXTRACTED",confidence_score=1.0,weight=1.0))
    node("hq","Converium HQ (knowledge only)","concept","CONSTITUTION.md")
    for p in registry["products"]:
        key="product:"+p["id"]
        names[p["repo"].split("/")[-1]]=key
        node(key,p["name"],"concept","products/registry.json")
        edge("hq",key,"indexes_product","products/registry.json")
    require(len(names)==6,"six products")
    names["Blender-Agent-Refinement-Toolkit"]="external:bart"
    node("external:bart","BART (external adopter)","concept",casepath)
    import re
    laws=re.findall(r"(?m)^([1-6])\. \*\*([^:]+):\*\*",data["CONSTITUTION.md"].decode())
    require(len(laws)==6,"six laws")
    for i,label in laws:
        node("law:"+i,label,"concept","CONSTITUTION.md");edge("hq","law:"+i,"records_law","CONSTITUTION.md")
    decisions=[l.split("|")[1].strip() for l in data["history/DECISIONS.md"].decode().splitlines() if l.startswith("| HQ-") or l.startswith("| ENGINEERING-")]
    require(len(decisions)==4,"four decisions")
    for d in decisions:
        node("decision:"+d,d,"concept","history/DECISIONS.md");edge("hq","decision:"+d,"records_decision","history/DECISIONS.md")
    pairs={}; kinds=Counter(); ids=set()
    for c in cases:
        require(c["id"] not in ids,"duplicate case")
        ids.add(c["id"])
        a,b=names[c["provider"]],names[c["beneficiary"]]
        t=c["classification"]; k="case:"+c["id"]
        require(t in {"self-use","self-validation","adopter-use","verified-draft","integrated","feedback","external-adopter"},"unknown case type")
        node(k,c["id"]+" "+t,"concept",casepath)
        edge("hq",k,"indexes_case",casepath)
        edge(a,k,"provider_"+t,casepath);edge(k,b,"beneficiary_"+t,casepath)
        if a==b: kinds["self"]+=1
        elif t=="feedback": kinds["feedback"]+=1
        elif t=="external-adopter": kinds["external"]+=1
        else:
            pairs.setdefault((a,b),[]).append(c["id"])
    require(len(ids)==23 and len(pairs)==14 and kinds=={"self":6,"feedback":2,"external":1},"historical coverage mismatch")
    for (a,b),ids in sorted(pairs.items()):
        edge(a,b,"observed_operational",casepath)
    return {"nodes":nodes,"edges":edges,"operational_evidence":[{"source":a,"target":b,"cases":ids} for (a,b),ids in sorted(pairs.items())]}
def validate_projection(s, expected):
    require(s==expected,"projection differs from authoritative records")
    ids={n["id"] for n in s["nodes"]}
    require(len(ids)==len(s["nodes"]),"duplicate node")
    keys={(e["source"],e["target"],e["relation"]) for e in s["edges"]}
    require(len(keys)==len(s["edges"]) and all(a in ids and b in ids for a,b,_ in keys),"invalid edges")
    require(not any("depend" in rel for _,_,rel in keys),"dependency edge forbidden")
    return keys
async def verify_mcp(path,n,e,commit):
    params=StdioServerParameters(command=sys.executable,args=["-m","graphify.serve",str(path)])
    async with asyncio.timeout(30), stdio_client(params) as (reader,writer):
        async with ClientSession(reader,writer) as session:
            await session.initialize()
            result=await session.call_tool("graph_stats",{})
            require(not result.is_error,"MCP stats failed")
            stats="\n".join(x.text for x in result.content if x.type=="text")
            require({f"Nodes: {n}",f"Edges: {e}",f"Built at commit: {commit}"}<=set(stats.splitlines()),"MCP stats mismatch")
            for name in ("product:vib","product:provenistem","product:lydite","product:veraphify","product:readme-hq","product:brand-identity"):
                result=await session.call_tool("get_neighbors",{"node_id":name,"token_budget":8000})
                require(not result.is_error,"MCP neighbors failed "+name)
def build(out):
    data=source_inputs(); semantic=project(data)
    keys=validate_projection(semantic,project(data))
    graph=build_from_json({"nodes":semantic["nodes"],"edges":semantic["edges"]},directed=True,dedup=False)
    require(graph.is_directed() and graph.number_of_nodes()==len(semantic["nodes"]) and graph.number_of_edges()==len(keys),"Graphify lost graph structure")
    actual={(a,b,x["relation"]) for a,b,x in graph.edges(data=True)}
    require(actual==keys,"Graphify edge mismatch")
    out.mkdir(parents=True,exist_ok=True)
    path=out/"graph.json"
    to_json(graph,{0:list(graph)},str(path),built_at_commit=PIN["source_commit"])
    # Validate serialized node and edge identity (Graphify node-link export).
    exported=json.loads(path.read_text())
    links=exported.get("links",exported.get("edges"))
    require(isinstance(links,list),"missing exported edges")
    require({n["id"] for n in exported["nodes"]}==set(graph),"exported node mismatch")
    require({(x["source"],x["target"],x["relation"]) for x in links}==keys,"exported edge mismatch")
    asyncio.run(verify_mcp(path,len(graph),len(keys),PIN["source_commit"]))
    (out/"semantic.json").write_text(json.dumps(semantic,indent=2)+"\n")
    receipt={"source_commit":PIN["source_commit"],"input_sha256":{k:digest(v) for k,v in data.items()},"producer":PIN["producer"],"graphify_version":version("graphifyy"),"nodes":len(graph),"edges":len(keys),"operational_edges":len(semantic["operational_evidence"]),"graph_sha256":digest(path.read_bytes()),"semantic_sha256":digest((out/"semantic.json").read_bytes()),"mcp_verified":True}
    require(receipt["graphify_version"]==PIN["producer"]["graphify_version"],"wrong Graphify version")
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print("GRAPHIFY PASS",json.dumps(receipt))
if __name__=="__main__":
    out=Path(sys.argv[1])
    build(out)
    with tempfile.TemporaryDirectory() as d:
        other=Path(d);build(other)
        for p in ("graph.json","semantic.json","receipt.json"):
            require((out/p).read_bytes()==(other/p).read_bytes(),"nondeterministic "+p)
    print("Deterministic rebuild PASS")
