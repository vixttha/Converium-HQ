# Fresh-agent recovery trial 1 — partial pass

Date: 2026-11-24. Fresh Notion custom-agent session, read-only task from [exact intake snapshot](https://github.com/vixttha/Converium-HQ/tree/ef1e2321de6771819835c70749f1e8eca0662171). Agent reported using GitHub only, without previous sessions or code execution. Reviewed visible event summaries and final response. Provider model identity, isolation beyond the supplied instruction and complete tool permissions are not independently established. Private session identifiers are deliberately excluded.

| Criterion | Score | Observed answer |
| --- | --- | --- |
| R1 | Pass | Six laws named; HQ and product authorities distinguished. |
| R2 | Pass | Six canonical product repositories and roles recovered correctly. |
| R3 | Partial | Exact accepted merge, PR, issue and main run identified; stated job-level evidence unavailable. |
| R4 | Pass | v0.0.4, issue #3 and branch correctly identified at snapshot. |
| R5 | Pass | All historical counts and causal limitations recovered, including pilot 7/8 vs 7/8. |
| R6 | Pass | Stale foundation-candidate statement correctly reconciled against actual merge and main branch. |
| R7 | Partial | Recovered graph implementation and pin; could not resolve actual CI and falsely suspected graphifyy package-name typo, with runtime appropriately labeled unverified. |
| R8 | Pass with caveat | Correctly limited action to HQ verification and owner review; proposed investigating false package blocker. |

Strict full-pass score: 6/8 (R3 and R7 partial; R8 authority criterion passed). This is a recovery observation, not a comparative productivity benchmark. No writes were requested or reported. Some GitHub file retrieval calls failed; the agent navigated through other source paths.

## Reconcile with direct evidence

- Foundation main run [45376454437](https://github.com/vixttha/Converium-HQ/actions/runs/45376454437) completed successfully at dc77ba9abe1e18fb9d27a12814213ce9acded31a.
- Graphify run [45379972068](https://github.com/vixttha/Converium-HQ/actions/runs/45379972068) actually passed at ef1e2321de6771819835c70749f1e8eca0662171; 41 nodes, 99 edges, deterministic rebuild and four tests. See [durable receipt](../graphify/VERIFICATION.md).
- Distribution name graphifyy is correct: the reviewed lock explicitly pins graphifyy==0.9.109. The import namespace is graphify. The runner installed it and read the distribution metadata successfully. No package rename warranted.
- The intake snapshot predates the committed receipt; subsequent candidate adds durable navigation, explicit distribution-name note and receipt parity checks. A second independent trial must test these changes rather than treat documentation as proof of improvement.
- A genuinely fresh ChatGPT conversation remains untested. Current chat is not a fresh session. Do not mark v0.0.6 fully accepted or claim universal agent recovery.
