# Catalog v0.2.2 maintenance release-set supplement

Evidence refresh completed: 2026-08-01T03:06:11Z

## Verdict

**PASS. The Core v0.4.2 scientific-validation verdict remains applicable to the exact maintenance
release set below.** No numerical authority, protected scientific implementation module, pinned
Core artifact, or frozen integrated golden case changed. The later tags contain dependency,
GitHub Actions, repository-policy, release/version, test, and documentation changes only.

This supplement does not claim a new independent numerical audit. It binds the earlier independent
Core v0.4.2 review to the later maintenance tags through exact predecessor diffs, exact-tag CI,
immutable release provenance, live staged-package verification, and renewed browser checks.

## Exact release identities and workflows

| Repository | Prior audited tag | Current tag and peeled commit | Exact-tag CI | Pages | Release |
|---|---|---|---:|---:|---:|
| `wald-inference-core` | v0.4.2 | v0.4.2 `8afd0a463cc1d2586b8ce5cf92f40900647c3190` | 30628647428 | n/a | 30629025349 pass |
| `scientific-applet-template` | v0.1.2 | v0.1.3 `74bb297574641a24b00e3e30e9e5f5ebae51f7a6` | 30677858148 | 30677858145 | 30677931872 pass |
| `compatibility-curve` | v0.1.4 | v0.1.5 `bda025b36d7f528f287d6ed8586fc329cf592423` | 30672716842 | 30672716848 | 30672853190 post-publication race |
| `wald-likelihood-support` | v0.1.3 | v0.1.4 `a5d9f938cc9a34cf3aa4f66181e0989b3513a89b` | 30673696470 | 30673696429 | 30674245810 pass |
| `critical-effect-size` | v0.1.4 | v0.1.5 `9e8987a7022647eed8e5c1437e1541559200d87d` | 30675603861 | 30675603890 | 30675772344 pass |
| `type-s-m-calibrator` | v0.1.4 | v0.1.5 `48e829b2f6dd921bf0875e1ba52c39eca59f068d` | 30677065561 | 30677065562 | 30677268367 post-publication race |
| `precision-guardrail-planner` | v0.1.3 | v0.1.4 `369809a77365e49d093c43c794e10f2260197269` | 30678524106 | 30678524099 | 30678618747 pass |
| `wald-inference-tools` predecessor | v0.2.0 | v0.2.1 `1daea9d6f035e80f8c470432b6c29d1e7a513fc3` | 30637402713 | 30637403039 | 30637591770 pass |
| `conf_curve_likelihood` | v0.2.6 | v0.2.7 `81f4cf0909f16e02fbfe37edfb9cbd55120a6eda` | 30680357838 | 30680357849 | 30680786034 pass |

Every tag is annotated and peels to the listed commit. Every listed release is stable, non-draft,
and immutable. Current `gh release verify` attestation checks passed for all nine releases. The
machine inventory records exact tag objects, taggers, release asset names/digests, workflow runs,
Pages deployments, live manifest digests, staged file records, and current attestation results.

## Bounded predecessor-diff review

The exact compare ranges were `v0.1.2...v0.1.3` for the template,
`v0.1.4...v0.1.5` for Compatibility, Critical Effect, and Type S/M,
`v0.1.3...v0.1.4` for Likelihood and Precision, and `v0.2.6...v0.2.7` for the
integrated workbench.

- No focused-app scientific model, calculation worker, Plotly builder, export implementation,
  privacy/storage/network implementation, or input/default behavior changed.
- The template remained formula-free. Its changes were dependency, version, staging metadata,
  documentation, and version assertions.
- Focused-app changes were limited to dependency locks, pinned Actions, release/version surfaces,
  repository-policy tests, documentation, and version assertions.
- The integrated workbench changed development dependencies, current-version policy, release and
  staging metadata, documentation, and frozen-baseline provenance handling. The historical golden
  manifests remained unchanged; the frozen corpus aggregate SHA-256 remained
  `da168ab1bfdb6504ab1c59e2ca1d240f7e6e92f86b3b41e9ac9baf70d9a0e9d2`.
- Core remained exactly v0.4.2. All six scientific consumers still stage the official Core wheel
  and identical 14-file Core package recorded by the release inventory.

The 13 maintenance pull requests were merged only after exact-head checks: template #4;
Compatibility #8 and #9; Likelihood #7 and #8; Critical #8 and #9; Type S/M #8 and #9;
Precision #9 and #10; integrated #32; and catalog #7.

## Live release and browser evidence

The regenerated inventory failed closed unless each staged manifest named the tag's peeled commit,
each staged file matched its declared size and digest, package and bundle digests recomputed, the
released live-data asset matched the Pages bytes, and all six consumers staged identical Core
files. The catalog predecessor's live manifest reports catalog version 0.2.1 and is bound to its
successful Pages deployment.

The renewed live browser audit ran from 2026-08-01T02:55:49Z through
2026-08-01T02:59:12Z. All eight public sites passed Chromium desktop, Chromium at 390 pixels, and
WebKit smoke. The dedicated containment rerun completed at 2026-08-01T03:05:19Z with all seven
app/template documents exactly 390 pixels wide and zero uncontained visible elements. The six
focused/template error-link and recovery paths passed by 2026-08-01T03:06:11Z; integrated error
recovery passed in the full audit. No user-input transmission, telemetry, persistent storage,
cookie, WebSocket, service worker, or unexpected non-GET request was observed.

An initial dedicated mobile attempt timed out while waiting for Likelihood runtime readiness after
the first two sites had passed. The unchanged immediate rerun passed Likelihood and all remaining
sites. The full audit had also passed Likelihood immediately beforehand. This is retained as a
nonblocking transient runtime-readiness observation.

## Post-publication attestation races

Compatibility run 30672853190 and Type S/M run 30677268367 each created and published the exact
verified immutable release, then failed at the immediate final `gh release verify` call because
GitHub had not yet exposed the new attestation. Their current release and every asset now verify.
The inventory accepts these two failures only by exact repository, tag, run ID, failed conclusion,
immutable release state, and successful current attestation verification. All other releases still
require a successful Release workflow.

## Remaining limitation

Tags remain intentionally unsigned. This does not alter the exact tag-object, peeled-commit,
protected-main, immutable-release, attestation, checksum, Pages, or live-package evidence.
