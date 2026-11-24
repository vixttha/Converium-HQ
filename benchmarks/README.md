# Ongoing real-development benchmark

[Issue #10](https://github.com/vixttha/Converium-HQ/issues/10). Preserve the existing [pilot](../evidence/imported/2026-11-24/benchmark-pilot-1.md): 7/8 both arms, 9 versus 15 tool calls, no measured benefit. Historical dogfooding is descriptive, not causal.

## Prospective first batch (protocol before execution)
Use two real defects: [Provenistem #4](https://github.com/vixttha/Provenistem/issues/4) at the original confirmed defect revision e36fcd6d12633395e9b573228c0797ade9e775b0 and [Lydite #117](https://github.com/vixttha/Lydite-Test-Vault-Template/issues/117) at the original confirmed draft revision a19c58a5b005bfab3e60b0b16aae13bf01023118. Verify both reproduce at the chosen SHA before trial and replace a nonreproducing task only with a documented pretrial reason. Freeze hidden tests and the task instructions before either arm runs.

Control: ordinary GitHub docs/issues/Actions, no ecosystem branch capability. Intervention: same product snapshot and ordinary access plus the appropriate independent tools installed at separately recorded exact pins. No mandatory all-six installation. Same agent harness/model/effort, tool permissions and budgets in both arms; verify model ceiling, do not run a higher model or paid hosted execution. Randomize order and keep sessions independent; single active Worker; separate disposable branches and no product main changes. Freeze source and acceptance tests; no sharing solutions between arms. Human owner acts as solo reviewer and retains integration authority.

Score: correct fix / hidden acceptance pass, existing regression suite pass, introduced regressions, owner interventions, rework attempts, evidence fidelity and elapsed/tool/token/cost only with actual measurement. Record failures and unknowns. Primary outcome: accepted fixes without regressions, not test counts. Start with paired trials on these two tasks, then expand only if useful; n=2 is exploratory. No percentage productivity claims from this protocol. No new coding trials executed by this audit because fresh isolated matched-budget agent execution and hidden-test freeze are not yet available. Continue through real product development rather than an endless HQ feature pipeline.

## Task qualification

The public-runner qualification workflow reproduces both actual defects against their known historical revisions and a passing control, using disposable local Git checkouts inside the hosted runner. This is pretrial task qualification, not an agent comparison, product fix, or current main defect claim. It runs only for the qualification files on the review branch/PR, or manual dispatch. No product repository receives a write. Inspect the run logs before claiming reproduction.
