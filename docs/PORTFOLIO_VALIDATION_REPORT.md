# Wald inference portfolio validation report

<!-- validation-evidence-index-sha256:e27565387d560209834eb55455bf7eb2540182a2126811cc9b85ccd1cbe08f25 -->

Validation timestamp: 2026-07-31T13:45:28Z
Catalog evidence carrier: wald-inference-tools v0.2.1

## Executive verdict

**Validated for release.**

Independent fresh-context reviews resolved the eight final published targets to
annotated tag objects and exact main commits, reproduced locked cold starts,
rechecked numerical contracts and B01-B08 parity, inspected live sites in
Chromium and WebKit, and verified release assets, documentation, privacy,
accessibility automation, licensing, and provenance. All prior blockers are
closed.

The catalog carrier audits its already-published v0.2.0 predecessor. Version
v0.2.1's own immutable release, eight assets, Pages bytes, and exact tag identity
are terminal external reconciliation gates because a release cannot contain its
own publication identity. They are not used as scientific evidence inside the
carrier.

This is software and scientific-implementation validation, not clinical
validation, causal validation, or evidence of patient-level suitability. The
checksum-addressed record is validation-evidence/index.json; literal commands
are preserved in validation-evidence/commands/README_COMMANDS.md.

<!-- validation-inventory:start -->
{
  "validated_at": "2026-07-31T13:45:28Z",
  "verdict": "Validated for release.",
  "core_version": "0.4.2",
  "repositories": [
    {
      "name": "reblocke/wald-inference-core",
      "commit": "8afd0a463cc1d2586b8ce5cf92f40900647c3190",
      "release": "v0.4.2",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/scientific-applet-template",
      "commit": "04353d7bb07ee74ae0585107431563db89387f05",
      "release": "v0.1.2",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/compatibility-curve",
      "commit": "eeaff9a374bc022c2d5ca16fdb3c59fbdfcd90f4",
      "release": "v0.1.4",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/wald-likelihood-support",
      "commit": "beb18d87939f3ba9738b97e1c2e10724e31c5945",
      "release": "v0.1.3",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/critical-effect-size",
      "commit": "1c451fe9ed7d7d21fe732ec5da178248053fe912",
      "release": "v0.1.4",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/type-s-m-calibrator",
      "commit": "bb4372c55a2e839b9f57d8424f797c944f5b4eb0",
      "release": "v0.1.4",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/precision-guardrail-planner",
      "commit": "a88926b966766a94b00a61799539351cce44581a",
      "release": "v0.1.3",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/wald-inference-tools",
      "commit": "ae76d86f731239e7fe2e902d6813093b35e4e69b",
      "release": "v0.2.0",
      "status": "validated",
      "blocking_findings": []
    },
    {
      "name": "reblocke/conf_curve_likelihood",
      "commit": "60ca0e3f5d6f05bb943cb4b7b7d02ed5a1d5714a",
      "release": "v0.2.6",
      "status": "validated",
      "blocking_findings": []
    }
  ]
}
<!-- validation-inventory:end -->

## Portfolio inventory and tested versions

| Repository | Release | Exact commit | Role |
|---|---|---|---|
| wald-inference-core | v0.4.2 | 8afd0a463cc1d2586b8ce5cf92f40900647c3190 | numerical authority |
| scientific-applet-template | v0.1.2 | 04353d7bb07ee74ae0585107431563db89387f05 | formula-free scaffold |
| compatibility-curve | v0.1.4 | eeaff9a374bc022c2d5ca16fdb3c59fbdfcd90f4 | focused app |
| wald-likelihood-support | v0.1.3 | beb18d87939f3ba9738b97e1c2e10724e31c5945 | focused app |
| critical-effect-size | v0.1.4 | 1c451fe9ed7d7d21fe732ec5da178248053fe912 | focused app |
| type-s-m-calibrator | v0.1.4 | bb4372c55a2e839b9f57d8424f797c944f5b4eb0 | focused app |
| precision-guardrail-planner | v0.1.3 | a88926b966766a94b00a61799539351cce44581a | focused app |
| wald-inference-tools predecessor | v0.2.0 | ae76d86f731239e7fe2e902d6813093b35e4e69b | calculation-free catalog |
| conf_curve_likelihood | v0.2.6 | 60ca0e3f5d6f05bb943cb4b7b7d02ed5a1d5714a | backward-compatible workbench |

All six scientific consumers use Core 0.4.2. The official wheel URL and SHA-256
are exact; all six staged copies of the 14-file Core package were byte-identical.
The full machine inventory is
validation-evidence/inventory/release-inventory.json.

## Methods/environment

The three independent lanes began from supplied exact release identities, used
fresh clones or release snapshots, and did not modify production state.

- Lane A/B: macOS 26.5.2 arm64; uv 0.11.11; Python 3.11.10 or
  3.12.13; SciPy 1.14.1.
- Lane C/D: macOS 26.5.2 arm64; Git 2.50.1; GitHub CLI 2.92.0;
  isolated clone parents, uv caches, and browser caches.
- Lane E/F: Python 3.12.13; Playwright 1.61.0; Chromium
  149.0.7827.55; WebKit 26.5.

Implementation changes and review evidence were separated. Fresh checks were
performed only after the final release set was live. Generated browser Python
was reproduced and remained ignored. Restricted or patient data were neither
required nor used.

## Numerical findings

Core remained the sole owner of effect transforms, CI reconstruction,
compatibility, likelihood/support, detectability, selection, Type S/M, and
precision calculations. Production-source and AST scans found no protected
formula copy in consumers.

Core frozen parity passed 14 numeric cases, six matched errors, and two declared
app-owned exclusions across 23,095 values at rtol 1e-12 and atol 1e-14.
Maximum absolute and relative differences were 5.329070518200751e-15 and
4.449372536648163e-16.

Independent normal/SciPy identities passed 40 scalar comparisons, all six
selection rules, strict JSON checks, and extreme finite guards. The largest
independent absolute and relative differences were 7.993605777301127e-15 and
1.5399215851702873e-14.

## Baseline/cross-app parity

The integrated B01-B08 comparison passed 22 cases and 27,268 floating-point
comparisons with maximum absolute and relative differences
5.329070518200751e-15 and 4.449372536648163e-16.

Focused comparisons passed: compatibility 35 values exactly; likelihood 33
values; critical effect 4 values; Type S/M 49 values; and precision 22 values
exactly. No protected formula drift was observed.

Core retains two documented binary64 paths for selected-claim probability: the
conservative detectability/inversion kernel and the frozen direct interval
probability used by Type S/M and inverse precision. They share the six-rule
interval authority; adapters fail closed on material drift. This is a
backward-compatibility exception, not observed disagreement.

## Cold-start results

| Target | Non-browser tests | Chromium | WebKit | Result |
|---|---:|---:|---:|---|
| Core | 396 | not applicable | not applicable | pass |
| Template | 38 | 5 | 1 | pass |
| Compatibility | 64 | 7 | 1 | pass |
| Likelihood | 80 | 11 | 1 | pass |
| Critical effect | 67 | 12 | 1 | pass |
| Type S/M | 84 | 21 | 1 | pass |
| Precision | 60 | 6 | 1 | pass |
| Integrated | 219 | 50 | independent smoke supplied in Lane E | pass |

Core's wheel and sdist rebuilt byte-for-byte and the official wheel passed a
cold installed-public-API smoke. All app archives reproduced byte-identical
decompressed tar streams. The compressed gzip bytes differed between macOS and
Ubuntu DEFLATE implementations; no content difference was observed.

## Release artifact provenance

All eight published final releases were stable, non-draft, non-prerelease, and
immutable. Every annotated tag object peeled to the recorded commit, each
commit equaled main, and every hosted asset passed its SHA256SUMS file.

Core wheel SHA-256:
225331d7b9d7b70e2508eecb92851a92a8c4e245baf412a1eb0f464d85da1349.
Core sdist SHA-256:
86808922f5ab9164523380e0838b324e24bed6a7228deb37ce2ca4cc19f06fe3.
SLSA attestations verified both against the v0.4.2 release workflow, exact tag
and commit, and run 30629025349.

Each regenerated browser manifest was byte-identical to both the release asset
and live Pages manifest. Catalog predecessor v0.2.0 is stable but predates the
immutable-release setting; it is historical evidence, not the new carrier.

## Browser/privacy/accessibility

All seven scientific/template sites passed Chromium desktop, exact 390-pixel
containment and keyboard flow, and WebKit initial-load/default-calculation
smoke. Every advertised export/copy path produced nonempty output with the
expected schema, dimensions, and signature.

No console/page errors, non-GET requests, WebSockets, telemetry matches, user
sentinels in requests, cookies, local/session storage, IndexedDB, Cache Storage,
or service workers were observed. The only post-input observations were local
blob-image GETs. Invalid inputs produced bounded assistive-technology-visible
messages and valid input recovered.

The catalog predecessor passed skip-link/filter keyboard behavior, 390-pixel
containment, WebKit smoke, and 18 of 18 rendered links at HTTP 200.

## Documentation/license/citation

All exact release snapshots had the required README, limitations, privacy,
security, maintenance, release, and citation materials for their roles.
Package/CFF/changelog versions agreed. All repositories use MIT licensing and
Brian Locke authorship; historical identity is retained only as explicit
provenance.

Public copy is educational/research-facing and one-parameter Wald-specific. It
does not claim clinical, causal, regulatory, posterior, or patient-level
validity. User-supplied thresholds and assumed truths are labeled accordingly.
No tracked publisher-style image, PDF, font, dataset, table, or substantial
copied text was found.

## Project-standard scores

Weights are A 20%, B 10%, C 15%, D 20%, E 10%, F 10%, G 7.5%, and
H 7.5%. A validated result requires a weighted numerator of at least 2550,
every domain at least 2, and no blocker. Score 2 identifies a bounded gap.

Template and catalog receive A=2 because they route rather than own formulas.
Critical effect and Type S/M receive D=2 because no external empirical
benchmark was evaluated. Every record receives G=2 because the owner-approved
annotated tags are unsigned.

<!-- validation-scores:start -->
{
  "schema_version": 1,
  "domain_definitions": {
    "A": "Scientific design/statistical validity",
    "B": "Data provenance/rights/security",
    "C": "Computational reproducibility",
    "D": "Verification/testing/independent review",
    "E": "Readability/maintainability",
    "F": "Documentation/replicator usability",
    "G": "Version control/change management",
    "H": "Output traceability/dissemination/preservation"
  },
  "weights_tenths": {
    "A": 200,
    "B": 100,
    "C": 150,
    "D": 200,
    "E": 100,
    "F": 100,
    "G": 75,
    "H": 75
  },
  "validated_min_numerator": 2550,
  "conditional_min_numerator": 2250,
  "scores": [
    {
      "name": "reblocke/wald-inference-core",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ab.md", "validation-evidence/results/core-v0.4.2-baseline-parity.json", "validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md"],
      "gaps": ["The annotated release tag is not cryptographically signed."]
    },
    {
      "name": "reblocke/scientific-applet-template",
      "domains": {"A": 2, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md", "validation-evidence/lanes/final-release-set-v0.4.2-lane-ef.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The scaffold routes rather than owns formulas.", "The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/compatibility-curve",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ab.md", "validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/wald-likelihood-support",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ab.md", "validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/critical-effect-size",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 2, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ab.md", "validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["No external empirical benchmark was evaluated.", "The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/type-s-m-calibrator",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 2, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ab.md", "validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["No external empirical benchmark was evaluated.", "The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/precision-guardrail-planner",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ab.md", "validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/wald-inference-tools",
      "domains": {"A": 2, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ef.md", "validation-evidence/browser/browser-summary.json", "validation-evidence/inventory/release-inventory.json"],
      "gaps": ["The catalog routes rather than owns formulas.", "The annotated predecessor tag is unsigned."]
    },
    {
      "name": "reblocke/conf_curve_likelihood",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/final-release-set-v0.4.2-lane-ab.md", "validation-evidence/lanes/final-release-set-v0.4.2-lane-cd.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The annotated tag is unsigned."]
    },
    {
      "name": "portfolio",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/all-ticket-acceptance-final.md", "validation-evidence/inventory/release-inventory.json", "validation-evidence/commands/README_COMMANDS.md"],
      "gaps": ["The release chain uses unsigned annotated tags."]
    }
  ]
}
<!-- validation-scores:end -->

## Release blockers

| Finding | Original evidence | Closure evidence | Status |
|---|---|---|---|
| A-01: inverse-precision solver skipped finite feasible bands | adversarial solver scan | repaired Core plus zero-miss rerun and released precision adoption | closed |
| A-02: support comparison contradicted canonical pairwise support | exact-fraction and adjacent-float reproducers | canonical Core delegation and independent rerun | closed |
| A-03: finite log-ratio silently underflowed | five ratio families | representability guard and scalar/vector/wheel reruns | closed |
| EF-01: focused Pages exceeded released source | tag/Pages/manifest comparison | exact immutable releases and matching deployments/manifests | closed |
| EF-02: five sites overflowed at 390 pixels | DOM geometry | responsive repair and zero-offender seven-site rerun | closed |
| F-03: integrated lifecycle copy was stale | detached documentation audit | exact release facts and regression coverage | closed |
| F-04: focused README/citation versions lagged | final-tag documentation audits | synchronized stable patch releases and rerun | closed |
| F-05: integrated copy mislabeled stable Core | lifecycle audit | v0.2.6 wording/metadata and exact-tag rerun | closed |

No release blocker remains.

## Nonblocking limitations

- Tags are annotated and content-addressed but intentionally unsigned; signer
  identity is not cryptographically proven.
- The catalog predecessor predates immutable release enforcement. Every newly
  published final target is immutable; carrier v0.2.1 must be immutable at the
  terminal external gate.
- App tar contents reproduced exactly, but gzip compressed bytes can differ
  across macOS and Ubuntu DEFLATE implementations.
- GitHub release assets and Pages, rather than PyPI, distribute the packages.
- Automated accessibility checks do not replace manual screen-reader, contrast,
  or broader zoom/reflow studies.
- WebKit coverage is smoke-level; Chromium covers complete workflows.
- Focused/template Plotly lacks SRI; versions are pinned and no input egress was
  observed. Integrated Plotly uses SRI.
- Live checks depend on GitHub, Pages, and pinned CDNs remaining reachable.

## Issues/PRs opened

The final governance/adoption sequence was isolated by repository:

| Repository | Pull requests |
|---|---|
| Core | wald-inference-core 16 |
| Template | scientific-applet-template 10 |
| Compatibility | compatibility-curve 12 and 13 |
| Likelihood | wald-likelihood-support 10 and 11 |
| Critical effect | critical-effect-size 11 and 12 |
| Type S/M | type-s-m-calibrator 11 and 12 |
| Precision | precision-guardrail-planner 12 and 13 |
| Integrated | conf_curve_likelihood 34 and 35 |
| Catalog | [wald-inference-tools #6](https://github.com/reblocke/wald-inference-tools/pull/6) |

Earlier numerical, responsive, lifecycle, and documentation corrections remain
preserved in each repository's history and earlier evidence records.

## Exact commands

The literal executable ledger is
validation-evidence/commands/README_COMMANDS.md. It records fresh clone/tag
resolution, locked environment restoration, tests, browser installation,
release downloads, SHA256SUMS, SLSA checks, live-manifest byte comparison,
evidence-index generation, deterministic carrier builds, make verify, and
make live-check.

Release identity was established from Git tag-object, release, workflow,
deployment, and asset APIs rather than a branch name or notification. The
repository-owner-approved unsigned control model is explicitly recorded.

## Appendix: numerical difference table

| Target | Values/cases | Maximum absolute difference | Maximum relative difference | Result |
|---|---:|---:|---:|---|
| Core frozen parity | 23,095 | 5.329070518200751e-15 | 4.449372536648163e-16 | pass |
| Independent scalar recomputation | 40 | 7.993605777301127e-15 | 1.5399215851702873e-14 | pass |
| Integrated B01-B08 | 27,268 / 22 | 5.329070518200751e-15 | 4.449372536648163e-16 | pass |
| Compatibility | 35 | 0 | 0 | pass |
| Likelihood | 33 | 5.329070518200751e-15 | 4.449372536648163e-16 | pass |
| Critical effect | 4 | 2.3314683517128287e-14 | 4.0338449175803973e-14 | pass |
| Type S/M | 49 | 3.9968028886505635e-15 | 1.1027325787414086e-14 | pass |
| Precision | 22 | 0 | 0 | pass |

Acceptance used the combined absolute-plus-relative tolerance, not either
displayed maximum in isolation.

## Appendix: network/storage observations

| Site class | Post-input requests | User-input transmission | Storage | Result |
|---|---|---|---|---|
| Template and six calculation sites | two local blob-image GET observations per site | none; sentinel absent from HTTP and WebSocket traffic | empty cookies, local/session storage, IndexedDB, Cache Storage, service workers | pass |
| Catalog predecessor | four same-origin static GETs | no calculation input | empty | pass |

Startup requests were GET-only and limited to same-origin assets and pinned
Plotly, Pyodide, NumPy, SciPy, and OpenBLAS resources. No POST, WebSocket,
analytics, or telemetry endpoint was observed.
