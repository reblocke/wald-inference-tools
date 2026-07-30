# Wald inference portfolio validation report

<!-- validation-evidence-index-sha256:07dfb86fccc3ffdb8782fafd6b51b604add61c979dbd8bfca90dcb87decac9eb -->

Validation date: 2026-07-30 UTC
Catalog evidence carrier: `wald-inference-tools` v0.2.0

## Executive verdict

**Validated for release.**

Independent review resolved every repository to a content-addressed annotated-tag
object and peeled commit, reproduced the locked builds from cold clones, independently
checked the numerical contracts and B01-B08 baseline, inspected released Pages
sites in Chromium and WebKit, and verified release assets, documentation,
privacy, accessibility automation, licensing, and citation metadata. All five
original release blockers and the later lifecycle-documentation findings are
closed. There are no unresolved release-blocking findings.

This is a software and scientific-implementation validation decision, not
clinical validation or evidence that any result is appropriate for a particular
patient or decision. The checksum-addressed source record is
`validation-evidence/index.json`; exact commands are preserved in
`validation-evidence/commands/README_COMMANDS.md`.

<!-- validation-inventory:start -->
{
  "core_version": "0.4.1",
  "repositories": [
    {
      "blocking_findings": [],
      "commit": "f4613177b6dc81d194aa70762152de2bfa86663b",
      "name": "reblocke/wald-inference-core",
      "release": "v0.4.1",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "c13d27de9fa456075cb9e52d897a5e9f866d8f32",
      "name": "reblocke/scientific-applet-template",
      "release": "v0.1.1",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "0abf653cb455885b07765d4b9fe1af4cc38cf3b2",
      "name": "reblocke/compatibility-curve",
      "release": "v0.1.3",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "7f5557d2a93235e25215261ef5890868b3fb07bb",
      "name": "reblocke/wald-likelihood-support",
      "release": "v0.1.2",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "a10482c73cdb89d37814bf1b8c955166957ecd6b",
      "name": "reblocke/critical-effect-size",
      "release": "v0.1.3",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "ed8881d13eea8ecffa77304555d251296d63f058",
      "name": "reblocke/type-s-m-calibrator",
      "release": "v0.1.3",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "ec47753aa1119b802e12856c4bc18feefa1ad6d5",
      "name": "reblocke/precision-guardrail-planner",
      "release": "v0.1.2",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "6fffdd51dbf5c53beeb6146f9deb10daeb194760",
      "name": "reblocke/wald-inference-tools",
      "release": "v0.1.1",
      "status": "validated"
    },
    {
      "blocking_findings": [],
      "commit": "1c283a5e1774b371b658469156fa24b9a397b8e6",
      "name": "reblocke/conf_curve_likelihood",
      "release": "v0.2.5",
      "status": "validated"
    }
  ],
  "validated_at": "2026-07-30T18:58:05Z",
  "verdict": "Validated for release."
}
<!-- validation-inventory:end -->

## Portfolio inventory and tested versions

The catalog v0.2.0 is the evidence carrier. To avoid circular validation, its
own row below is the independently audited v0.1.1 predecessor; publication of
v0.2.0 is checked afterward as a release-reconciliation step.

| Repository | Release | Peeled commit | Role |
|---|---|---|---|
| `wald-inference-core` | v0.4.1 | `f4613177b6dc81d194aa70762152de2bfa86663b` | sole shared formula owner |
| `scientific-applet-template` | v0.1.1 | `c13d27de9fa456075cb9e52d897a5e9f866d8f32` | reusable non-formula scaffold |
| `compatibility-curve` | v0.1.3 | `0abf653cb455885b07765d4b9fe1af4cc38cf3b2` | observed compatibility |
| `wald-likelihood-support` | v0.1.2 | `7f5557d2a93235e25215261ef5890868b3fb07bb` | observed likelihood/support |
| `critical-effect-size` | v0.1.3 | `a10482c73cdb89d37814bf1b8c955166957ecd6b` | detectability/critical effects |
| `type-s-m-calibrator` | v0.1.3 | `ed8881d13eea8ecffa77304555d251296d63f058` | selection-conditioned Type S/M |
| `precision-guardrail-planner` | v0.1.2 | `ec47753aa1119b802e12856c4bc18feefa1ad6d5` | inverse precision planning |
| `wald-inference-tools` | v0.1.1 | `6fffdd51dbf5c53beeb6146f9deb10daeb194760` | audited catalog predecessor |
| `conf_curve_likelihood` | v0.2.5 | `1c283a5e1774b371b658469156fa24b9a397b8e6` | backward-compatible integrated workbench |

The machine-collected GitHub, tag, release, workflow, Pages deployment, live
manifest, license, and asset inventory is
`validation-evidence/inventory/release-inventory.json`.

## Methods/environment

Review was split across independent numerical/parity, cold-start/provenance,
browser/privacy/accessibility, and documentation/rights lanes. Candidate fixes
were never accepted as evidence: every closure was rerun against a fresh
detached checkout of the final annotated tag.

The principal cold environment was macOS 26.5.2 (build 25F84), arm64, Python
3.12.13, uv 0.11.11, and Node 25.9.0. The detached integrated v0.2.5 lane used
Playwright 1.58.0, Chromium 145.0.7632.6, and WebKit 26.0. The final retained
post-release cross-site browser run used Playwright 1.61.0, Chromium
149.0.7827.55, and WebKit 26.5. GitHub Actions repeated applicable gates on
Ubuntu. Dependencies were restored from each repository's checked-in
`uv.lock`; no sibling checkout, editable cross-repository install, or manual
source substitution was used.

Comparison rules remained frozen: exact equality for schemas, strings,
booleans, nulls, ordering, and required warnings; `rtol=1e-12`,
`atol=1e-14` for same-stack migration; and `rtol=1e-10`, `atol=1e-12` for
browser-engine comparisons. Browser payloads were serialized with strict JSON;
no tolerance was widened during review.

## Numerical findings

Core v0.4.1 owns effect transforms, CI/SE reconstruction, compatibility,
relative likelihood/log support, S-2 and generic support intervals, pairwise
support, legacy and exact detectability, six selection rules, selected-claim
probability, Type S, Type M, observed exaggeration, information scaling, and
per-target/joint precision solvers. Source and staged-package diff audits found
no second production formula implementation in any app.

Independent scalar, vector, property, frozen-reference, exact-fraction, and
extreme-finite checks passed. The corrected Core baseline compared 23,095
published values with maximum absolute difference `2.842e-14` and maximum
relative difference `1.388e-15`; the fresh macOS recomputation had maxima
`5.329e-15` and `4.449e-16`. These are below the applicable combined
absolute/relative tolerances.

The post-repair precision scan traversed 9,072 solver paths with zero missed
finite feasible bands. It retained eight explicit regression cases discovered
by the independent audit. Pairwise support delegates to the canonical
log-support implementation, and finite-but-unrepresentable ratio results now
fail explicitly instead of silently becoming invalid zero.

## Baseline/cross-app parity

All 22 frozen B01-B08 cases passed. Recursive comparison of 27,268 integrated
response values had maximum absolute difference `5.329e-15` and maximum
relative difference `4.449e-16`.

| Case | Contract covered | Result |
|---|---|---|
| B01 | additive reconstruction, compatibility, likelihood, support, strict JSON | pass |
| B02 | ratio/log reconstruction, natural display, S-2 | pass |
| B03 | presentation-only display window and marker warnings | pass |
| B04 | two-sided forward calibration, null undefined values, symmetry | pass |
| B05 | directional ratio threshold and fourfold-information scaling | pass |
| B06 | ordered inverse-precision targets, solutions, information, CI width | pass |
| B07 | undefined, invalid, disabled-design, and infeasible cases | pass |
| B08 | extreme finite values, clipping, warnings, strict JSON | pass |

Focused-contract audits found exact exclusion of out-of-scope fields.
Compatibility reproduced the legacy compatibility subset; likelihood reproduced
likelihood, S-2, generic support, and pairwise support; critical effect
preserved the legacy benchmark while labeling exact detectability separately;
Type S/M reproduced the design subset; and precision reproduced per-target
legacy outputs while documenting joint/binding extensions.

## Cold-start results

Every release was cloned into a new temporary parent, checked out by exact tag,
restored with `uv sync --locked`, and run through its documented commands.
Build/stage commands left no unexplained tracked diff.

| Repository | Non-E2E tests | Chromium | WebKit | Result |
|---|---:|---:|---:|---|
| Core v0.4.1 | 380 | not applicable | not applicable | pass |
| Template v0.1.1 | 30 plus 22 scaffold self-tests | 5 plus 1 self-test | 1 | pass |
| Compatibility v0.1.3 | 57 | 7 | 1 | pass |
| Likelihood v0.1.2 | 73 | 11 | 1 | pass |
| Critical effect v0.1.3 | 60 | 12 | 1 | pass |
| Type S/M v0.1.3 | 74 | 21 | 1 | pass |
| Precision v0.1.2 | 51 | 6 | 1 | pass |
| Catalog predecessor v0.1.1 | 29 | 4 | 4 | pass |
| Integrated v0.2.5 | 208 | 49 | 1 | pass |

Core built wheel and sdist artifacts. Each scientific calculation app staged
its exact locked Core wheel into the Pages artifact, served locally, and passed
browser smoke and contract checks. The template instead staged and tested its
formula-free demonstration package through the disposable-app self-test. Exact
environment and command detail is retained in `validation-evidence/lanes/` and
the command ledger.

## Release artifact provenance

All nine audited tags are annotated, peel to one commit, and have a non-draft
GitHub release. Every applicable Release workflow completed successfully at
that peeled commit. Each staged-package Pages application has a successful
deployment for the same commit, and its live manifest's `source_commit` equals
that commit. The catalog predecessor's manifest intentionally has no
`source_commit`; it is instead bound to the audited release by the successful
Pages deployment SHA, exact `catalog_version`, and byte comparison of the live
static files.

The independently downloaded Core wheel
`wald_inference-0.4.1-py3-none-any.whl` is 37,939 bytes with SHA-256
`d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b`.
Its release checksum, downloaded bytes, installed package version, file set,
and scientific smoke results agree. Focused and integrated source archives,
site/package manifests, and `SHA256SUMS` files likewise passed local checks and
the GitHub asset-digest comparison.

The exact tag objects, peeled commits, Release/CI/Pages workflow URLs,
deployment identifiers, asset sizes/digests, and live-manifest hashes are in
`validation-evidence/inventory/release-inventory.json`. No staged Python file
was accepted when it differed from the source package or lockfile.

## Browser/privacy/accessibility

The six calculation sites plus the scientific-applet template scaffold passed
full Chromium desktop, Chromium 390-pixel, and WebKit smoke checks. At 390
pixels, every document and body matched the viewport and no visible descendant
escaped containment. Keyboard focus order, labels, result text, applicable
CSV/PNG/caption/reviewer exports, invalid-input announcement, and recovery were
exercised. The five focused apps plus the template scaffold additionally passed
explicit error-link-to-invalid-control focus tests; the integrated app
announces its recoverable error through an `aria-live="polite"` status.

Network inspection observed only GET requests. Startup fetched same-origin
static files plus versioned Plotly/Pyodide/package resources. After numerical
input, the only two observations per calculation site were local `blob:`
image GETs; no HTTP request, WebSocket, beacon, telemetry match, or sentinel
input transmission occurred. User values did not enter the URL. Cookies,
local/session storage, IndexedDB, Cache Storage, service workers, and service
worker controllers were all empty. The catalog made four same-origin static
GETs and contains no calculation or tracking code.

Raw results and their consolidated counts are preserved under
`validation-evidence/browser/`.

## Documentation/license/citation

Every repository contains the required README, MIT `LICENSE`, `CITATION.cff`,
`AGENTS.md`, changelog, scientific scope, validation, privacy, decision,
maintenance, and `llms.txt` surfaces appropriate to its role. README setup and
verification commands were executed literally. Public task questions,
non-goals, formula assumptions, observed-versus-design boundaries, hosted and
repository links, pinned Core version, limitations, privacy posture, and
related-tool navigation agree with code and catalog metadata.

Authorship and maintenance metadata consistently use the user-approved
identity **Brian Locke**. License metadata consistently identifies MIT.
Tracked repository assets, source, and public copy contained no copied
publisher figure, table, dataset, or substantial third-party prose. Direct
automated retrieval of the publisher full texts returned HTTP 403, so a
forensic full-text comparison was not possible; the bounded rights finding
therefore rests on the inspected repository content and recorded provenance.
Application references support the formulas they describe. No repository
claims clinical validation.

The independent rerun identified and then closed traceability-only release
gaps: focused-app README/citation version drift was corrected in final patch
releases, integrated v0.2.3's prospective lifecycle text was reconciled in
v0.2.4, and stale stable-Core wording was corrected in v0.2.5. The repairs did
not alter formulas, defaults, browser contracts, exports, or golden outputs.

## Project-standard scores

Weights were frozen as A 20%, B 10%, C 15%, D 20%, E 10%, F 10%, G 7.5%,
and H 7.5%. A validated result requires a weighted numerator of at least 2550
(85/100), every domain at least 2, and no blocker. A score of 2 indicates a
documented nonblocking limitation, not a failed gate.

| Domain | Definition |
|---|---|
| A | Scientific design/statistical validity |
| B | Data provenance, rights, and security |
| C | Computational reproducibility |
| D | Verification, testing, and independent review |
| E | Readability and maintainability |
| F | Documentation and replicator usability |
| G | Version control and change management |
| H | Output traceability, dissemination, and preservation |

| Repository | A | B | C | D | E | F | G | H | Weighted /100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Core | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 97.5 |
| Template | 2 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 90.8 |
| Compatibility | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 97.5 |
| Likelihood | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 97.5 |
| Critical effect | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 90.8 |
| Type S/M | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 3 | 90.8 |
| Precision | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 97.5 |
| Catalog | 2 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 90.8 |
| Integrated | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 97.5 |
| Portfolio | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 97.5 |

| Repository | Evidence basis | Bounded gap represented by score 2 |
|---|---|---|
| Core | Core A/B and C/D ledgers; frozen parity JSON; clean wheel/asset checks | unsigned annotated tag |
| Template | template C/D/E/F ledger; disposable-app self-test; live browser evidence | formula-free routing scope (A); unsigned tag (G) |
| Compatibility | focused A/B anchors; final-tag supplement; browser/network records | unsigned tag (G) |
| Likelihood | final A/B ledger; generic/pairwise support tests; C/D/E/F audit | unsigned tag (G) |
| Critical effect | exact/legacy anchor tests; final-tag supplement; browser audit | no external empirical benchmark (D); unsigned tag (G) |
| Type S/M | six-rule anchors; final-tag supplement; browser audit | no external empirical benchmark (D); unsigned tag (G) |
| Precision | boundary scan and app-repair driver; final-tag supplement; browser audit | unsigned tag (G) |
| Catalog | predecessor C/D/E/F audit; strict manifest/link/browser tests | routing rather than formula ownership (A); unsigned tag (G) |
| Integrated | B01-B08 recursive parity; v0.2.5 C/D/E/F audit; live browser evidence | unsigned tag (G) |
| Portfolio | all-ticket acceptance matrix; release inventory; evidence index | unsigned release chain (G) |

Template and catalog receive A=2 because they route rather than own scientific
formula behavior. Critical-effect and Type S/M receive D=2 because their
detectability and selection-conditioned model outputs were independently
validated numerically but not against an external empirical benchmark. Every
repository and the portfolio receive G=2 because annotated tags are not
cryptographically signed. The evidence for every score is spread across the six
lane records indexed by the evidence manifest; the corresponding gaps are
listed under nonblocking limitations.

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
      "evidence": ["validation-evidence/lanes/core-likelihood-final-ab.md", "validation-evidence/results/core-v0.4.1-baseline-parity.json", "validation-evidence/lanes/corrected-release-set-lane-cd.md"],
      "gaps": ["The annotated release tag is not cryptographically signed."]
    },
    {
      "name": "reblocke/scientific-applet-template",
      "domains": {"A": 2, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/catalog-template-v0.1.1-cdef.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The scaffold routes rather than owns formulas.", "The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/compatibility-curve",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/corrected-release-set-lane-ab.md", "validation-evidence/lanes/focused-docs-only-final-release-supplement.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/wald-likelihood-support",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/lanes/core-likelihood-final-ab.md", "validation-evidence/lanes/likelihood-v0.1.2-cdef.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/critical-effect-size",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 2, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/critical-v0.1.2-cdef.md", "validation-evidence/lanes/focused-docs-only-final-release-supplement.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["No external empirical benchmark was evaluated.", "The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/type-s-m-calibrator",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 2, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/type-s-m-v0.1.2-cdef.md", "validation-evidence/lanes/focused-docs-only-final-release-supplement.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["No external empirical benchmark was evaluated.", "The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/precision-guardrail-planner",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/results/core-precision-boundary-audit.txt", "validation-evidence/drivers/audit_precision_app_repairs.py", "validation-evidence/lanes/focused-docs-only-final-release-supplement.md", "validation-evidence/browser/browser-summary.json"],
      "gaps": ["The annotated tag is unsigned."]
    },
    {
      "name": "reblocke/wald-inference-tools",
      "domains": {"A": 2, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2725,
      "evidence": ["validation-evidence/lanes/catalog-template-v0.1.1-cdef.md", "validation-evidence/browser/browser-summary.json", "validation-evidence/inventory/release-inventory.json"],
      "gaps": ["The catalog routes rather than owns formulas.", "The annotated predecessor tag is unsigned."]
    },
    {
      "name": "reblocke/conf_curve_likelihood",
      "domains": {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G": 2, "H": 3},
      "weighted_numerator": 2925,
      "evidence": ["validation-evidence/drivers/audit_integrated_diff.py", "validation-evidence/lanes/integrated-v0.2.5-cdef.md", "validation-evidence/browser/browser-summary.json"],
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
| A-01: inverse-precision solver skipped finite feasible bands | 9,072-path adversarial scan found 8 misses | Core v0.4.1 solver repair, eight regressions, 9,072-path zero-miss rerun, precision v0.1.2 | closed |
| A-02: `support_comparison` contradicted canonical pairwise support | exact-fraction and adjacent-float reproducers | Core v0.4.1 canonical delegation and independent exact-fraction/frozen rerun | closed |
| A-03: finite log-ratio silently underflowed to zero | all five ratio families reproduced the defect | Core v0.4.1 representability guard with scalar/vector/wheel reruns | closed |
| EF-01: five focused Pages sites were ahead of releases | tag, Pages, manifest, and source-archive comparison | exact final patch tags, matching deployments/live manifests, release assets, independent detached-tag audits | closed |
| EF-02: five sites overflowed at 390 pixels | DOM width and visible-descendant measurements | responsive repair plus all-seven-site 390-pixel rerun with zero uncontained elements | closed |
| F-03: integrated lifecycle text remained prospective after v0.2.3 | independent detached-tag documentation audit | v0.2.4 exact release facts plus stale-lifecycle regression and independent tag rerun | closed |
| F-04: focused README/citation versions lagged final releases | independent final-tag documentation audits | docs-only patch releases and detached-tag documentation/provenance rerun | closed |
| F-05: integrated v0.2.4 described stable Core v0.4.1 as a prerelease | independent post-release lifecycle audit | v0.2.5 metadata-only correction, stable-Core wording regression, and independent exact-tag rerun | closed |

No release blocker remains.

## Nonblocking limitations

- Annotated-tag objects and peeled commits are content-addressed and were
  independently resolved, but every tag is unsigned. Tag refs and GitHub
  release records are mutable administrative objects that a privileged
  maintainer can move, edit, or delete.
- The five focused apps and integrated workbench retain explicit experimental
  pre-1.0/GitHub-prerelease labeling; stable Core, template, and catalog
  releases provide the supported foundation and navigation.
- Packages are distributed as GitHub release assets and staged Pages content,
  not through PyPI.
- Versioned CDN URLs are static and the staged Python wheels are hashed, but
  browser responses for upstream CDN JavaScript are not independently
  content-addressed by this portfolio.
- Archive contents and declared checksums reproduced exactly; compression bytes
  can vary across external platform tooling when an archive is regenerated
  outside the deterministic project builders.
- Accessibility evidence is automated keyboard, labeling, live-region,
  focus, text-alternative, and two-engine browser testing; no manual
  screen-reader or other assistive-technology study was performed.
- The review establishes numerical/software conformance to declared formulas,
  not clinical validity, empirical transportability, causal validity, or
  suitability for patient-level decisions.
- Live verification depends on GitHub, GitHub Pages, and the versioned CDNs
  being reachable.

## Issues/PRs opened

Each corrective change was isolated from the review evidence and merged only
after exact-head tests, then independently rerun from its resolved annotated-tag
object and peeled commit:

| Repository/work | Pull request |
|---|---|
| Core numerical repairs and v0.4.1 | [wald-inference-core#7](https://github.com/reblocke/wald-inference-core/pull/7) |
| Template responsive/release reconciliation | [scientific-applet-template#2](https://github.com/reblocke/scientific-applet-template/pull/2) |
| Compatibility Core/release traceability | [compatibility-curve#3](https://github.com/reblocke/compatibility-curve/pull/3) |
| Compatibility mobile plot readability | [compatibility-curve#4](https://github.com/reblocke/compatibility-curve/pull/4) |
| Compatibility final reconciliation | [compatibility-curve#5](https://github.com/reblocke/compatibility-curve/pull/5) |
| Likelihood Core/release traceability | [wald-likelihood-support#3](https://github.com/reblocke/wald-likelihood-support/pull/3) |
| Likelihood final release | [wald-likelihood-support#4](https://github.com/reblocke/wald-likelihood-support/pull/4) |
| Critical-effect Core/release traceability | [critical-effect-size#3](https://github.com/reblocke/critical-effect-size/pull/3) |
| Critical-effect mobile plot readability | [critical-effect-size#4](https://github.com/reblocke/critical-effect-size/pull/4) |
| Critical-effect final reconciliation | [critical-effect-size#5](https://github.com/reblocke/critical-effect-size/pull/5) |
| Type S/M Core/release traceability | [type-s-m-calibrator#3](https://github.com/reblocke/type-s-m-calibrator/pull/3) |
| Type S/M mobile plot readability | [type-s-m-calibrator#4](https://github.com/reblocke/type-s-m-calibrator/pull/4) |
| Type S/M final reconciliation | [type-s-m-calibrator#5](https://github.com/reblocke/type-s-m-calibrator/pull/5) |
| Precision Core/release traceability | [precision-guardrail-planner#5](https://github.com/reblocke/precision-guardrail-planner/pull/5) |
| Precision final reconciliation | [precision-guardrail-planner#6](https://github.com/reblocke/precision-guardrail-planner/pull/6) |
| Catalog/cross-links predecessor | [wald-inference-tools#3](https://github.com/reblocke/wald-inference-tools/pull/3) |
| Integrated Core/release traceability | [conf_curve_likelihood#21](https://github.com/reblocke/conf_curve_likelihood/pull/21) |
| Integrated mobile plot readability | [conf_curve_likelihood#22](https://github.com/reblocke/conf_curve_likelihood/pull/22) |
| Integrated scientific/release closeout | [conf_curve_likelihood#23](https://github.com/reblocke/conf_curve_likelihood/pull/23) |
| Integrated lifecycle-evidence reconciliation | [conf_curve_likelihood#24](https://github.com/reblocke/conf_curve_likelihood/pull/24) |
| Integrated stable-Core lifecycle correction | [conf_curve_likelihood#25](https://github.com/reblocke/conf_curve_likelihood/pull/25) |

## Exact commands

The literal executable ledger is
`validation-evidence/commands/README_COMMANDS.md`. Core commands included
`make verify` and `uv build`; app commands included `uv sync --locked`,
`make verify`, browser installation, local serve, and exact-tag
stage/manifest comparison; catalog commands included `make verify` and
`make live-check`.

Release identity used GitHub's tag-object, release, workflow, deployment, and
asset APIs rather than branch names. Asset verification used downloaded
`SHA256SUMS` files and local SHA-256. Evidence creation used the preserved
Python and Node drivers named in the command ledger. Each command's resolved
repository/tag/commit and result appears in the indexed lane or machine result.

## Appendix: numerical difference table

| Target | Values/cases | Maximum absolute difference | Maximum relative difference | Result |
|---|---:|---:|---:|---|
| Core published baseline | 23,095 values | `2.842e-14` | `1.388e-15` | pass |
| Core fresh macOS recomputation | 23,095 values | `5.329e-15` | `4.449e-16` | pass |
| Integrated B01-B08 recursive parity | 27,268 values / 22 cases | `5.329e-15` | `4.449e-16` | pass |
| Compatibility anchors | 35 | `0` | `0` | pass |
| Likelihood/support anchors | 21 | `1.421e-14` | `4.449e-16` | pass |
| Critical-effect anchors | 4 | `2.331e-14` | `4.034e-14` | pass |
| Type S/M anchors | 49 | `3.997e-15` | `1.103e-14` | pass |
| Precision anchors | 22 | `0` | `0` | pass |
| Precision adversarial solver scan | 9,072 paths | zero missed feasible bands | not applicable | pass |

Absolute and relative maxima can occur at different values. Acceptance used
the frozen combined `atol + rtol * |expected|` rule, not either displayed
maximum in isolation.

## Appendix: network/storage observations

| Site class | Requests after numerical input | User-input transmission | Persistent/browser storage | Result |
|---|---|---|---|---|
| Six calculation sites plus template scaffold | two local `blob:` image GET observations per site; no HTTP request | none; sentinel absent from requests and WebSockets | no cookies, local/session storage, IndexedDB, Cache Storage, or service worker | pass |
| Catalog | four same-origin static GETs | no calculation inputs exist | no cookies or browser storage; no tracking code | pass |

Startup requests were GET-only and limited to same-origin application assets
and versioned Plotly, Pyodide, NumPy, SciPy, and OpenBLAS resources. There were
no POST requests, WebSockets, analytics endpoints, or telemetry matches.
