# All-ticket acceptance record: CC-MIG-00 through CC-MIG-11

Recorded: 2026-07-31
Evidence-carrier target: reblocke/wald-inference-tools v0.2.1
Mode: independent prepublication synthesis with terminal external carrier reconciliation

## Decision and evidence boundary

**The implementation portfolio is validated for release at the v0.2.1 carrier
source boundary.** The evidence covers all 145 bullet acceptance criteria in
CC-MIG-00 through CC-MIG-11. No scientific, functional, privacy, accessibility,
documentation, metadata, artifact, or reproducibility blocker remains in the
eight published final identities or the catalog v0.2.1 source candidate.

The checked-in catalog row audits released predecessor v0.2.0. Version v0.2.1
cannot contain its own tag-object, release-asset, or deployed-byte identity.
Those are verified after publication in a checksum-addressed external closeout.
Publishing another carrier solely to describe v0.2.1 would move rather than
solve this self-reference.

This record is valid only while the carrier commit passes all of these gates:

- data/tools.json contains the exact release set and validated status;
- docs/PORTFOLIO_VALIDATION_REPORT.md contains the explicit verdict and A-H scores;
- data/validation_status.json binds the report digest and exact repository inventory;
- validation-evidence/inventory/release-inventory.json validates exact tags, releases,
  assets, deployments, and hosted manifests;
- validation-evidence/index.json hashes every preserved evidence file;
- make verify, make live-check, and clean-tree verification pass.

## Exact audited portfolio

| Repository | Audited release | Peeled commit | Publication state |
|---|---|---|---|
| reblocke/wald-inference-core | v0.4.2 | 8afd0a463cc1d2586b8ce5cf92f40900647c3190 | stable, immutable |
| reblocke/scientific-applet-template | v0.1.2 | 04353d7bb07ee74ae0585107431563db89387f05 | stable, immutable |
| reblocke/compatibility-curve | v0.1.4 | eeaff9a374bc022c2d5ca16fdb3c59fbdfcd90f4 | stable, immutable |
| reblocke/wald-likelihood-support | v0.1.3 | beb18d87939f3ba9738b97e1c2e10724e31c5945 | stable, immutable |
| reblocke/critical-effect-size | v0.1.4 | 1c451fe9ed7d7d21fe732ec5da178248053fe912 | stable, immutable |
| reblocke/type-s-m-calibrator | v0.1.4 | bb4372c55a2e839b9f57d8424f797c944f5b4eb0 | stable, immutable |
| reblocke/precision-guardrail-planner | v0.1.3 | a88926b966766a94b00a61799539351cce44581a | stable, immutable |
| reblocke/conf_curve_likelihood | v0.2.6 | 60ca0e3f5d6f05bb943cb4b7b7d02ed5a1d5714a | stable, immutable |
| reblocke/wald-inference-tools predecessor | v0.2.0 | ae76d86f731239e7fe2e902d6813093b35e4e69b | stable; predates immutable setting |
| reblocke/wald-inference-tools carrier | v0.2.1 | resolved by reviewed carrier commit | external reconciliation required |

All nine repositories are public, MIT licensed, attributed to Brian Locke, use
main as the default branch, have Issues enabled, and are not archived. The
template alone is configured as a GitHub template. Static sites use
workflow-based GitHub Pages with HTTPS.

All six Core consumers pin the official Core v0.4.2 wheel at its exact release
URL and SHA-256
225331d7b9d7b70e2508eecb92851a92a8c4e245baf412a1eb0f464d85da1349.

## Preserved evidence used

- Lane A/B: lanes/final-release-set-v0.4.2-lane-ab.md,
  results/core-v0.4.2-baseline-parity.json, and
  results/core-v0.4.2-independent-recomputation.json.
- Lane C/D: lanes/final-release-set-v0.4.2-lane-cd.md,
  results/final-release-set-v0.4.2-cold-start.json, and the release inventory.
- Lane E/F: lanes/final-release-set-v0.4.2-lane-ef.md, browser/browser-summary.json,
  and the three refreshed raw browser records.
- Command and identity binding: commands/README_COMMANDS.md,
  inventory/release-inventory.json, and index.json.

## Ticket-by-ticket acceptance

The counts correspond one-for-one to the bullet acceptance criteria at the
ticket locators.

| Ticket | Acceptance locator | Criteria | Disposition | Direct evidence summary |
|---|---|---:|---|---|
| CC-MIG-00 | tickets/00_freeze_integrated_baseline.md:394-407 | 14 | PASS | Frozen source/environment, 22 B01-B08 cases, deterministic corpus, strict JSON/export schemas, negative controls, baseline release, metadata, and clean verification. |
| CC-MIG-01 | tickets/01_extract_wald_inference_core.md:460-473 | 14 | PASS | Public typed MIT Core; sole formula owner; nine effects/six rules; finite, undefined, property, and reference tests; 23,095-value parity; byte-reproducible wheel/sdist; cold-wheel smoke; exact checksums; stable v0.4.2. |
| CC-MIG-02 | tickets/02_rewire_integrated_workbench.md:326-337 | 12 | PASS | Exact released Core pin; no formula fork; legacy API and 22 goldens; strict JSON; browser; deterministic staging; one local/Pages path; documented ownership; preserved URL; release notes; clean checkout. |
| CC-MIG-03 | tickets/03_create_scientific_applet_template.md:328-338 | 11 | PASS | Public MIT GitHub template; disposable initializer/self-test; no domain formulas; deterministic staging; strict browser contract; accessibility/privacy; CI/Pages; complete metadata; stable v0.1.2. |
| CC-MIG-04 | tickets/04_build_compatibility_curve.md:314-326 | 13 | PASS | Nine-effect compatibility scope; B01-B03/B08 parity; negative scope; CSV/PNG/caption/error contracts; strict JSON; two-engine browser; privacy/accessibility; docs; exact Core pin and links. |
| CC-MIG-05 | tickets/05_build_wald_likelihood_support.md:327-337 | 11 | PASS | Core support primitives; focused scope; likelihood/S-minus-2 parity; generic intervals and log-safe pairwise support; negative scope; strict JSON; exports; two-engine browser; wording and Core pin. |
| CC-MIG-06 | tickets/06_build_critical_effect_size.md:342-352 | 11 | PASS | Released detectability API; exact critical-effect primary; separate legacy benchmark; one/two-sided and CI/direct-SE references; ratio behavior; negative scope; exports; browser/privacy/accessibility; limitations. |
| CC-MIG-07 | tickets/07_build_type_s_m_calibrator.md:320-331 | 12 | PASS | Six rules; B04/B05/B07 parity; conditioning/nonposterior wording; direct-SE/CI modes; ratio Type M; strict undefined/null JSON; uncapped exports; browser/privacy/accessibility; Core pin. |
| CC-MIG-08 | tickets/08_build_precision_guardrail_planner.md:342-352 | 11 | PASS | Released joint/sensitivity API; B06/B07 parity; per-target/joint semantics; binding/infeasibility; sufficient-current multiplier; caveated sample-size option; negative scope; exports; browser/privacy/accessibility. |
| CC-MIG-09 | tickets/09_build_catalog_and_crosslinks.md:267-277 | 11 | PASS at carrier-source boundary | Public calculation-free MIT catalog; question cards/conditioning table; strict final-version manifest; live links; cross-links; accessibility/privacy; workflows; maintenance docs. v0.2.1 publication is the external gate. |
| CC-MIG-10 | tickets/10_finalize_integrated_workbench.md:249-259 | 11 | PASS | v0.2.6 preserves URLs/imports and 22 cases; no formula fork; exact catalog/focused links; paradigm distinction; maintenance/templates; synchronized metadata; exact Pages/release assets; clean verification. |
| CC-MIG-11 | tickets/11_independent_portfolio_validation.md:345-358 | 14 | PASS under carrier invariants | Exact releases/commands; B01-B08 and ownership; scope separation; cold installs/builds/two-engine browser; checksums; privacy/accessibility; identity/MIT; complete A-H scores; fail-closed status; hash binding; independent reruns. |

Coverage arithmetic:
14 + 14 + 12 + 11 + 13 + 11 + 11 + 12 + 11 + 11 + 11 + 14 = 145.

## Additional constraints and limitations

- Core v0.4.2 is stable and preserves the frozen baseline. Its later version is
  the documented outcome of corrective prereleases; the ticket's suggested
  first-stable v0.1.0 version was nonbinding.
- Catalog v0.2.1 records the exact final set. Its stable immutable publication
  is the remaining external carrier gate.
- Annotated tags are intentionally unsigned at the repository owner's
  direction. Control rests on tag-object identity, exact commit/main
  containment, immutable releases, checksummed deterministic assets, draft-first
  publication, workflow identity, and post-publication byte verification.
- Other bounded gaps are no PyPI distribution, automated rather than manual
  assistive-technology testing, smoke-level WebKit depth, external CDN/GitHub
  availability, and one documented dual-binary64 selected-claim probability
  compatibility path. None changes the scientific contract or validation score.

## Required external v0.2.1 reconciliation

After merge and publication, an independent external audit must verify:

1. the annotated v0.2.1 tag object peels to the reviewed main commit and names Brian Locke;
2. the GitHub release is non-draft, non-prerelease, latest, and immutable;
3. Release, CI, and Pages workflows succeed at that exact commit;
4. Pages and live tools/report/status/index bytes equal the carrier commit;
5. all eight assets match GitHub digests and SHA256SUMS;
6. source, site, report, status, manifest, index, and evidence archive reproduce twice;
7. make verify, make live-check, build/serve, and clean-tree checks pass detached;
8. a checksum-addressed external closeout records the actual tag, release, assets,
   Pages identity, settings, and nine-repository clean-state reconciliation.

Only that external reconciliation closes the migration goal. It is not used as
evidence inside v0.2.1.
