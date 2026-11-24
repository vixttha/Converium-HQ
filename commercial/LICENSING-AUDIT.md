# Licensing and release audit — 2026-11-24

[Machine-readable observations](audit-2026-11-24.json). All six live canonical working-branch refs matched the dated registry pins when queried; no product repositories changed. Read all six recursive source trees, checked notices at exact revisions, rechecked release refs, release metadata and release CI for the two published packages. Not a legal opinion, ownership audit of every contribution, exhaustive dependency SBOM, or legal permission to distribute.

| Product | Observed notice and scope | Next action |
| --- | --- | --- |
| VIB | No LICENSE/COPYING found at pinned candidate | Owner confirms rights and chooses terms; do not market as open source or redistribute absent grant. |
| Provenistem | MIT root and package notices, identical blobs | Preserve both as applicable, check imported records and original authorship; fix #2–4 before commercial pilot. |
| Lydite | MIT root and starter notices; reviewed published tag also contains same notice | Standalone starter scope only; Graphify dependency lock separate; known test-result defects need repair. |
| Veraphify | MIT root, distinct imported Brand and Lydite notices | Preserve all applicable notices; Go/TypeScript manifests in imported Vault; do not imply whole combined archive is first-party. |
| README HQ | No product grant; four BART historical notices | Historical licenses do not authorize unrelated HQ source. Separate archived materials, technique catalog and Graphify dependencies. |
| Brand Identity | MIT kit notice, imported Vault has own MIT notice; published kit same notice | Confirm exact kit scope, no unapproved artwork or fonts; browser dependencies separate. |
| Converium HQ | No root license in accepted tree | Owner chooses documentation/code terms only for material they own; copied evidence and upstream materials retain original rights. |

[GitHub licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository): public visibility is not a general redistribution grant. [OSI MIT terms](https://opensource.org/license/mit): preserve required copyright and permission notices; no warranty. A license notice is evidence, not proof that its publisher owns every file. Do not replace valid notices with a blanket ecosystem license.

## Release verification

- [Lydite v0.0.4](https://github.com/vixttha/Lydite-Test-Vault-Template/releases/tag/v0.0.4): tag resolves to 87d25d80d3154d295052412b64b29a0f0f152c27, source starter has 15 files and matching MIT blob, [release CI](https://github.com/vixttha/Lydite-Test-Vault-Template/actions/runs/44506598515) success at that SHA.
- [Brand Identity v0.0.2](https://github.com/vixttha/Brand-Identity-Template/releases/tag/v0.0.2): tag resolves to 87d0f9aedbe69ca4b16815d6b3329efcf5889da9, kit has 18 files and matching MIT blob, [release CI](https://github.com/vixttha/Brand-Identity-Template/actions/runs/44499438408) success at that SHA.
- Neither release has a separately uploaded asset; both expose GitHub-generated source archives. Actual archive ZIP contents were not downloaded or compared here. Neither kit subtree contained a package/requirements manifest or PNG/SVG/font/ZIP matching the inventory filter. This is not a proof of no external material.
- The other four had no GitHub release listed at observation. Preview/version branch is not a published release.

## Remaining rights gates

Before distribution: verify contributor and asset origin, full dependency license/notice obligations for the exact distribution contents, archive rights/privacy, owner-approved license for each unlicensed scope, and name clearance. No source license edited, no new grant or public launch. Recommend separate product grants rather than a shared license; owner decision required. 
