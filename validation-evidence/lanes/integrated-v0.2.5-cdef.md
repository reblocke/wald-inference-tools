# Integrated workbench v0.2.5 CDEF final audit

Audit completed: `2026-07-30T18:40:01Z`

Verdict: **GO — validated for catalog acceptance within the integrated-workbench
scope, with nonblocking limitations.**

No blocking finding remains at the immutable v0.2.5 identity. This is a
software/release/contract audit, not a claim of clinical validation, exact
profile-likelihood recovery, or scientific revalidation beyond the documented
frozen tests and independent review.

## Scope and supersession

This ledger independently resolves the integrated-workbench CDEF supplement:
repository and release identity, source and dependency provenance, frozen
B01-B08 parity, browser/runtime behavior, Pages deployment, public wording,
maintenance boundaries, and release-asset reproducibility.

- v0.2.3 is retained as historical evidence but was superseded because its
  migration documents still contained prospective lifecycle wording after the
  release completed.
- v0.2.4 closed that lifecycle gap but was superseded after Core v0.4.1 became
  a stable GitHub release while the app documents still described Core as a
  prerelease.
- v0.2.5 is the final audited identity. It distinguishes stable Core from the
  intentionally experimental integrated-app prerelease.
- The portfolio-level verdict remains authoritative in the
  `reblocke/wald-inference-tools` catalog. This ledger does not let the
  integrated repository self-certify the portfolio.

## Immutable identity

| Field | Audited value |
|---|---|
| Repository | `reblocke/conf_curve_likelihood` |
| Repository status | public, unarchived, default branch `main`, MIT detected, Issues and Pages enabled |
| Pull request | [#25](https://github.com/reblocke/conf_curve_likelihood/pull/25) |
| PR head | `1ef821b6cbe8a0e5fbbe17ea59709b57df5084aa` |
| PR base | `609488ce431be5419b5bcf7c7b4bbbc9ccd7b65c` |
| Merge/release commit | `1c283a5e1774b371b658469156fa24b9a397b8e6` |
| Merge parents | `609488ce431be5419b5bcf7c7b4bbbc9ccd7b65c`, `1ef821b6cbe8a0e5fbbe17ea59709b57df5084aa` |
| Merged | `2026-07-30T18:05:42Z` |
| Annotated tag | `v0.2.5` |
| Tag object | `a0dbb71eba4288469894f10154149b54a340d5cf` |
| Tag target | `1c283a5e1774b371b658469156fa24b9a397b8e6` |
| Tagger | Brian Locke |
| Tag timestamp | `2026-07-30T18:15:24Z` |
| Tag message | `Integrated Wald Inference Workbench v0.2.5` |
| Tag signature | unsigned; `git verify-tag` reports `no signature found` |
| GitHub release | [v0.2.5](https://github.com/reblocke/conf_curve_likelihood/releases/tag/v0.2.5), ID `362633006` |
| Release state | non-draft, prerelease |
| Published | `2026-07-30T18:26:55Z` |

The cold clone warned that the annotated tag itself “is not a commit” and then
correctly detached at the peeled commit. `git status --short --branch` reported
`## HEAD (no branch)`, with no tracked or untracked non-ignored changes.

## GitHub workflows and Pages

All workflow runs are complete, successful, and bound to
`1c283a5e1774b371b658469156fa24b9a397b8e6`.

| Gate | Run | Result | Timing |
|---|---:|---|---|
| Main CI #102 | [30568906462](https://github.com/reblocke/conf_curve_likelihood/actions/runs/30568906462) | success | `2026-07-30T18:05:45Z` to `2026-07-30T18:14:51Z` |
| Deploy Pages #41 | [30568906401](https://github.com/reblocke/conf_curve_likelihood/actions/runs/30568906401) | success | `2026-07-30T18:05:45Z` to `2026-07-30T18:06:20Z` |
| Release #7 | [30569610989](https://github.com/reblocke/conf_curve_likelihood/actions/runs/30569610989) | success | `2026-07-30T18:15:28Z` to `2026-07-30T18:26:57Z` |

Release job `90962685131` passed checkout, locked setup, annotated-tag/version
validation, Ruff format/lint, deterministic staging, frozen baseline, live
portfolio links, all non-browser tests, full Chromium, WebKit smoke, clean-tree
validation, deterministic bundle construction, and artifact upload. Job
`90965471471` then passed bundle download, checksum validation, and prerelease
creation.

Pages deployment `5679868187` has successful deployment status
`16151116489` at
<https://reblocke.github.io/conf_curve_likelihood/>. The deployment is bound to
the exact release commit. The live site returned HTTP 200 and a
`Last-Modified` timestamp of `2026-07-30T18:06:13Z`.

## Release assets and source reproduction

Downloaded bytes match both the GitHub asset digests and the published
`SHA256SUMS`.

| Asset | Asset ID | Bytes | SHA-256 |
|---|---:|---:|---|
| `browser-stage-manifest.json` | `495711308` | 4,308 | `d0739f5f81adc37452095ca25fafdc45a9ca61d6f7755ff9005c844e5e128c4f` |
| `conf_curve_likelihood-0.2.5.tar.gz` | `495711306` | 474,047 | `d598295b48a719bc94b26312b4c8e34b715c219aca76c5ed6f2356a1f1bc0cf6` |
| `SHA256SUMS` | `495711305` | 195 | `9491f5a48e0265670c1adf878bd3b186009cfdba7f3d832863d619f38601da5f` |

The archive contains 180 entries. The decompressed release tar stream and a
fresh `git archive --format=tar --prefix=conf_curve_likelihood-0.2.5/` of the
peeled tag are byte-identical, both with SHA-256
`5c3c2abb36b7f7c6808c8286b337c4583795212ccd18947b758313e5f4891927`.

The macOS `gzip -n` implementation produced a different compressed-byte digest
(`03bc7b42e51c8241c4fd824fad34dfa505ffb9f4d0285d1bea2fe68c23095dc3`)
than the GNU-gzip-produced release asset. This is a compressor-implementation
difference, not a source-tree difference: the decompressed tar bytes match
exactly, the release workflow compared two same-runner builds, and the
published compressed asset passes its own downloaded and GitHub checksums.

## Browser stage and Core provenance

The freshly staged cold-clone manifest, downloaded release manifest, and live
Pages manifest are byte-identical:

| Manifest field | Value |
|---|---|
| Manifest SHA-256 | `d0739f5f81adc37452095ca25fafdc45a9ca61d6f7755ff9005c844e5e128c4f` |
| Schema | `1` |
| Source commit | `1c283a5e1774b371b658469156fa24b9a397b8e6` |
| Bundle SHA-256 | `21a45855e857cdf1a368ffaa7bae94611c9c8b1dc35cc5e3681d946d12e2baec` |
| App package | `confcurve` 0.2.5, 7 files |
| Core package | `wald-inference` 0.4.1, 14 files |
| Pyodide | 0.29.3 |
| Plotly | 3.1.0 |

Core v0.4.1 is an official stable, non-draft GitHub release at commit
`f4613177b6dc81d194aa70762152de2bfa86663b`. The exact wheel URL and digest
are bound in `README.md`, `pyproject.toml`, `uv.lock`, staging, and tests.
A fresh download independently matched SHA-256
`d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b`
and 37,939 bytes. Wheel metadata reports `wald-inference` 0.4.1,
`License-Expression: MIT`, and Python `>=3.11`.

## Cold detached-tag verification

Checkout: `/private/tmp/cc-mig11-v025.qiBFhF/repo`

Host/runtime:

- macOS 26.5.2 build 25F84, arm64
- Git 2.50.1 (Apple Git-155)
- uv 0.11.11
- locked CPython 3.11.10
- NumPy 2.2.6
- SciPy 1.14.1
- Playwright 1.58.0
- Chromium 145.0.7632.6
- WebKit 26.0

| Gate | Audited result |
|---|---|
| `uv sync --locked` | PASS; 36 resolved, 35 installed, no sibling Core checkout |
| Test collection | 257 total: 208 non-E2E and 49 E2E |
| `make verify` | PASS |
| Ruff format | PASS, 34 files |
| Ruff lint | PASS |
| Checked-in portfolio navigation | PASS, 20 requirements |
| Deterministic Python stage | PASS |
| Frozen B01-B08 baseline | PASS, 22 cases |
| Non-E2E suite | PASS, 208 |
| Chromium E2E suite | PASS, 49 |
| WebKit initial-render smoke | PASS, 1 |
| Live portfolio targets | PASS, 10 |
| `git diff --check` | PASS |
| `git status --porcelain --untracked-files=all` | empty |

The WebKit release gate used the documented initial-render test with tracing,
video, and screenshots retained only on failure.

## Independent frozen-parity traversal

The stored fixture manifest SHA-256 is
`f54bb2d8311788c07adcf23fc9f038e35702449e4a77a474abea9411246cabcc`;
the fixture-set SHA-256 is
`81c341b39e711caffc85a444f0c1e4bc1e2d00633474c82e720afeb60def3c4d`.
The declared tolerance is `rtol=1e-12`, `atol=1e-14`, with declared identity
fields exact.

An independent recursive comparison traversed 27,268 stored/current float
pairs across all 22 cases. The overall maximum absolute difference was
`5.329070518200751e-15` at
`B01.response.meta.threshold_support_summaries[0].likelihood_ratio_threshold_to_null`.
The overall maximum relative difference, measured against the stored expected
value, was `4.449372536648163e-16` at the corresponding B02 path. Both are
comfortably inside the frozen tolerance.

| Matrix | Cases | Float pairs | Maximum absolute difference | Maximum relative difference |
|---|---:|---:|---:|---:|
| B01 | 1 | 2,445 | `5.329070518200751e-15` | `4.1266019082733676e-16` |
| B02 | 1 | 2,445 | `5.329070518200751e-15` | `4.449372536648163e-16` |
| B03 | 1 | 2,449 | `5.329070518200751e-15` | `4.449372536648163e-16` |
| B04 | 1 | 5,695 | `5.329070518200751e-15` | `4.1266019082733676e-16` |
| B05 | 1 | 5,687 | `0` | `0` |
| B06 | 1 | 5,691 | `0` | `0` |
| B07 | 11 | 2,694 | `5.329070518200751e-15` | `4.1266019082733676e-16` |
| B08 | 5 | 162 | `0` | `0` |

This traversal supplements, rather than replaces, the repository comparator,
which also verifies canonical JSON, hashes, key ordering, schemas, errors, and
declared exact fields.

## Diff containment

The complete v0.2.2-to-v0.2.5 reconciliation changes 20 files with 604
insertions and 66 deletions. It adds the required
`docs/SCIENTIFIC_SCOPE.md` and `docs/VALIDATION.md`; otherwise it changes
documentation, version/policy markers, exact Core provenance, staging/runtime
version markers, portfolio-link validation, and regression assertions.

The final v0.2.4-to-v0.2.5 patch changes 17 files with 87 insertions and 31
deletions. It is confined to lifecycle documentation, versions, manifest/user
agent markers, link/policy checks, and regression tests.

There is no diff across either final corrective patch in the formula/contract
authorities:

- `src/confcurve/core.py`
- `src/confcurve/design.py`
- `src/confcurve/models.py`
- `src/confcurve/web_contract.py`
- `tests/golden/`
- `web/assets/app.js`
- `web/assets/config.js`
- `web/assets/formatters.js`
- `web/assets/plot.js`
- `web/assets/plot-helpers.js`
- `web/assets/renderers.js`
- `web/index.html`

No formula, frozen fixture, tolerance, request/response schema, default input,
view, warning/error, privacy, accessibility, UI, or CSV/PNG/caption/reviewer
export change was accepted.

## Documentation and public-copy assertions

| Assertion | Audited source |
|---|---|
| Integrated purpose and one-sentence task question | `README.md:1-24` |
| Focused catalog and five focused apps | `README.md:3-6`, `README.md:32-43` |
| Observed-data versus design conditioning | `README.md:45-47`, `docs/SCIENTIFIC_SCOPE.md:13-26` |
| Stable released Core and exact pin | `README.md:28-30`, `README.md:123-136`, `pyproject.toml:14` |
| Frozen B01-B08 authority and tolerances | `README.md:151-162`, `docs/VALIDATION.md:18-43` |
| Exact verification commands | `README.md:93-121`, `docs/VALIDATION.md:94-115` |
| Maintenance and feature-freeze boundary | `README.md:203-217`, `README.md:224-231`, `docs/MAINTENANCE.md:3-22` |
| Backward-compatibility policy | `docs/MAINTENANCE.md:36-45`, `CHANGELOG.md:7-29` |
| No clinical/scientific overclaim | `README.md:60-68`, `docs/SCIENTIFIC_SCOPE.md:9-11`, `docs/SCIENTIFIC_SCOPE.md:103-121`, `docs/VALIDATION.md:3-8`, `docs/VALIDATION.md:136-141` |
| Canonical author | `CITATION.cff:5-8`, `pyproject.toml:8-10`, `README.md:241-243` |
| MIT consistency | `CITATION.cff:10`, `LICENSE:1-3`, `README.md:237-239` |
| External portfolio-verdict authority | `docs/VALIDATION.md:131-134`, `docs/migration/METADATA_AUDIT.md:79-83` |

Historical “pending” and “planned” terms in the migration log are scoped to
their named pre-tag or earlier milestone records. The current correction says
Core v0.4.1 is stable, the integrated app remains an experimental prerelease,
and stable Core does not promote or clinically validate the app. A regression
test binds this distinction.

## Deployed-browser observation

Independent live smoke loaded the Pages URL in both engines:

| Browser | HTTP | Visible version | Plot traces | Requests | Origins | Failures/errors | Storage/cookies |
|---|---:|---|---:|---:|---|---|---|
| Chromium 145.0.7632.6 | 200 | `confcurve app 0.2.5 · wald-inference core 0.4.1` | 2 | 40 GET | GitHub Pages, jsDelivr, Plotly CDN | none | empty |
| WebKit 26.0 | 200 | `confcurve app 0.2.5 · wald-inference core 0.4.1` | 2 | 40 GET | GitHub Pages, jsDelivr, Plotly CDN | none | empty |

Both reached `Curves updated.` without changing the input-free URL. The full
local Chromium suite separately exercises inputs, errors and recovery,
responsive/accessibility behavior, display alternatives, and exports.

## Findings and limitations

Blocking findings: **none**.

Nonblocking limitations:

1. The annotated v0.2.5 tag is unsigned, so provenance is resolved by Git and
   GitHub identity plus exact hashes rather than a cryptographic tag signature.
2. The integrated app is intentionally a GitHub prerelease and described as
   experimental; this GO verdict does not promote it to a stable app release.
3. Cross-implementation gzip bytes differ, although decompressed archive bytes
   reproduce exactly and all published asset/checksum gates pass.
4. The audit validates implementation, frozen parity, release traceability,
   documented privacy/accessibility contracts, and scoped public wording. It
   does not validate a source study, user threshold, Wald suitability, clinical
   decision, or patient-specific use.
5. Portfolio validation remains external to this repository and must be
   integrated into the catalog's authoritative report.

## Final disposition

**GO.** Accept immutable integrated-workbench v0.2.5 at annotated tag object
`a0dbb71eba4288469894f10154149b54a340d5cf`, peeled commit
`1c283a5e1774b371b658469156fa24b9a397b8e6`, release-asset set headed by
source archive SHA-256
`d598295b48a719bc94b26312b4c8e34b715c219aca76c5ed6f2356a1f1bc0cf6`,
and live/release manifest SHA-256
`d0739f5f81adc37452095ca25fafdc45a9ca61d6f7755ff9005c844e5e128c4f`.
