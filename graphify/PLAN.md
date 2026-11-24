# v0.0.4 — Graphify ecosystem mapping

Status: implementation verified at ef1e2321de6771819835c70749f1e8eca0662171; see [verification receipt](VERIFICATION.md). Combined candidate revalidation pending. [Issue #3](https://github.com/vixttha/Converium-HQ/issues/3). Accepted baseline: [dc77ba9abe1e18fb9d27a12814213ce9acded31a](https://github.com/vixttha/Converium-HQ/tree/dc77ba9abe1e18fb9d27a12814213ce9acded31a).

## Scope and acceptance

1. Read the constitution, six-product registry, decision ledger and 23-case historical evidence register. Preserve exact source paths and revisions. Resolve all sources before asserting graph edges.
2. Separate six product nodes and the HQ knowledge node from laws, decisions, evidence cases, and the external BART adopter. Distinguish 14 directed operational relationships from self-use, feedback and external adoption; derive relationships from the actual case register, never from assumed dependencies. HQ references do not confer authority or imply runtime dependencies.
3. Evaluate the existing [pinned Graphify producer](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/tree/6af3c2025be3f51e02dca4e4502088c526aae6d1/versions/v0.0.8) and its locked requirements. Verify scope and provenance before execution. The Graphify distribution is intentionally named graphifyy; the Python import namespace is graphify. Verified run 45379972068 uses its locked 0.9.109 wheel. Do not treat the distinct spelling as a typo. Do not claim a Graphify run until actual output and receipt exist.
4. Generate a durable graph and readable navigation with exact HQ source revision and input hashes. Verify graph node/edge identity, citation paths, receipt binding, and reproducibility on standard GitHub public runners; include negative controls for stale or changed inputs, missing records, and fabricated edges. Preserve logs/receipt with exact run attempt. No product installations or remote writes by validation.
5. Audit and return the candidate for owner acceptance. No v0.0.5 work, release, commercial launch, or mandatory service.

Inputs: [constitution](../CONSTITUTION.md), [registry](../products/registry.json), [decisions](../history/DECISIONS.md), [historical evidence register](../evidence/imported/2026-11-24/dogfooding-evidence.json), [evidence manifest](../evidence/manifest.json). The existing historical compatibility results are not graph-verification results.
