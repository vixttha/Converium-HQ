# Fresh-agent recovery retest — receipt navigation

Date: 2026-11-24. New Notion custom-agent session; targeted read-only retest from [snapshot c62d3741](https://github.com/vixttha/Converium-HQ/tree/c62d37413a4be7c539538bba4e6371281447c5f1). Agent reported no file modifications or execution. Visible response and event summaries reviewed. Different session does not prove a different model; model identity and isolation beyond requested instructions remain unverified.

| Retest target | Result |
| --- | --- |
| Foundation PR, merge SHA, scope | Correct; independently fetched PR #2 |
| Main CI run metadata | Correct recorded run 45376454437, but not independently retrieved by the agent |
| Graphify original implementation and CI receipt | Correct exact implementation SHA ef1e2321de6771819835c70749f1e8eca0662171, run 45379972068 attempt 1, job 138396156966 |
| Graph identities | Correct 41 nodes, 99 edges, 14 operational relationships, 23 evidence cases |
| Package provenance | Correct graphifyy distribution 0.9.109, graphify import namespace, producer commit and lock blob; prior false package concern no longer reproduced |
| Source revision and digests | Correct source dc77ba9abe1e18fb9d27a12814213ce9acded31a, graph SHA-256 13380851515de57f7e3d4cc6dad3dbf40d2b1512dca052c49735a1cc4076c7ae, semantic digest a876c5d236e835157b111021e8ff22ed15a7c4d8697c734d31261d0059127404 |
| Historical versus current | Correctly distinguished original verified receipt from later candidate and did not claim fresh combined CI from the snapshot |
| Authority | Correctly limited next work to exact candidate validation and owner review |

Targeted retest supports durable receipt recovery and correction of the prior false package concern; it is not a full repeated eight-criterion trial or a productivity benchmark. The agent could not independently retrieve historical Actions metadata. The supervising connector independently verified [main run 45376454437](https://github.com/vixttha/Converium-HQ/actions/runs/45376454437/attempts/1) at exact accepted SHA (completed/success), and original Graphify run 45379972068. Do not attribute that direct readback to the test agent.

At subsequent [candidate be981d85](https://github.com/vixttha/Converium-HQ/tree/be981d85c1ea8dad752e78038f1d6abfc4e3c1c3), four combined workflows passed and archived graph/semantic files matched deterministic output (see [validation log](../history/VALIDATION-LOG.md)). A genuinely fresh ChatGPT trial remains outstanding, as does full milestone acceptance. Private session references are not published.
