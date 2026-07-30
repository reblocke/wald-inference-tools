# CC-MIG-11 independent validation — Lane E/F evidence ledger

**Lane:** Browser/privacy/accessibility; documentation/rights/citation/maintenance; provisional A–H scoring
**Audited:** 2026-07-30T06:51:52-06:00 (America/Denver)
**Reviewer posture:** read-only against production repositories and deployed sites; all local work was under `/private/tmp/cc-mig-11-ef-*`
**Ticket authority:** `conf_curve_migration_codex_tickets/tickets/11_independent_portfolio_validation.md` from the provided `conf_curve_migration_codex_tickets.zip`

## Executive verdict

**Not validated; release blockers remain.**

Two independently reproduced Lane E/F blockers prevent a release verdict:

1. **EF-01 — Five focused Pages deployments are not traceable to their released/tagged commit.** Compatibility, likelihood, critical-effect, Type S/M, and precision Pages manifests identify untagged commits ahead of their only `v0.1.0` release. Their staged Python bundle hashes still reproduce from the tag, but the complete hosted sites do not equal the released source state.
2. **EF-02 — Five deployed sites fail the required 390 px mobile viewport.** The template and four focused apps have document-level horizontal overflow of 750–890 px in a 390 px viewport. Precision, the integrated workbench, and the catalog pass.

The positive findings are substantial: all eight deployed sites loaded and ran in Chromium; all rendered in WebKit smoke tests; scientific app workflows, error recovery, CSV/PNG/caption/reviewer exports, basic keyboard operation, labels, live error announcements, text alternatives, privacy boundaries, and related links passed the checks described below. Documentation, authorship, MIT licensing, source-rights posture, clinical limitations, and no-research-data posture are strong. Those strengths do not waive the two release blockers.

No issue, PR, repository edit, manifest status change, tag, release, or deployment was created in this lane.

## Assumptions and decision rules

- The exact versions under review are the newest GitHub release objects visible on 2026-07-30. All nine are currently marked GitHub **prerelease**.
- For an app to satisfy the ticket’s “Pages deployment is traceable to release commit” requirement, the hosted `assets/py/manifest.json` `source_commit` (or catalog Pages workflow head) must equal the peeled release-tag commit. A hosted app version string or unchanged Python bundle alone is insufficient because HTML, JavaScript, CSS, and public documentation are part of the deployed artifact.
- Mobile passes only when both `document.documentElement.scrollWidth` and `document.body.scrollWidth` are no greater than the 390 px client width after a completed keyboard workflow.
- “Numerical inputs are not transmitted” means a conspicuous per-site sentinel was absent from every captured request URL/body and WebSocket frame, with no non-GET requests or WebSockets, while the workflow completed.
- Browser accessibility checks are focused runtime checks, not a WCAG conformance certification. No screen-reader or automated axe audit was performed.
- The ticket names A–H domains but supplies no weights or score thresholds. The provisional scoring rubric below is explicit and reproducible; the final synthesizer may replace it if an authoritative portfolio rubric is found.

## Environment and evidence artifacts

| Item | Value |
|---|---|
| Host | macOS 26.5.2 (25F84), Apple arm64 |
| Time zone | America/Denver |
| `uv` | 0.11.11 |
| Python | 3.11.10 for core/integrated; 3.12.13 for template/focused/catalog lock environments |
| Playwright | 1.61.0 |
| Chromium | 149.0.7827.55 |
| WebKit | 26.5 |
| Tag clones | `/private/tmp/cc-mig-11-ef-clones.1sNp1k/` |
| Browser driver | `/private/tmp/cc-mig-11-ef-live-audit.py` |
| Browser JSON | `/private/tmp/cc-mig-11-ef-browser-results.json` |
| Required-field error JSON | `/private/tmp/cc-mig-11-ef-error-links.json` |
| Mobile geometry JSON | `/private/tmp/cc-mig-11-ef-mobile-overflow.json` |
| Browser artifacts | `/private/tmp/cc-mig-11-ef-browser-artifacts/` |

Artifact SHA-256:

```text
040eef11e909e8ab7a08bd55fea042c0fbcdc64f2d6c8fe627e14e112499a15b  cc-mig-11-ef-live-audit.py
402ca92f63ac079d4f822d0bf5eaf98d467bb282604bfb7f8af78465681707b9  cc-mig-11-ef-browser-results.json
29d3a652cbd68b873fc5d1da3fab46174ed17f722a58a27f0963c11404f31628  cc-mig-11-ef-error-links.json
9e3ebcba759a74a3a8f3d59378c4d13697ba08f6bb2843ec50f3c51ca428ea69  cc-mig-11-ef-mobile-overflow.json
```

## Portfolio inventory and tested versions

Tag commits below are peeled commits, not annotated-tag object IDs.

| Repository | Release | Release commit | Hosted site / deployed source | Core in hosted manifest |
|---|---:|---|---|---:|
| [`wald-inference-core`](https://github.com/reblocke/wald-inference-core/releases/tag/v0.4.0) | `v0.4.0` | `fd7b24740122bed7ae07769674732c5e56c91277` | no Pages app | — |
| [`scientific-applet-template`](https://github.com/reblocke/scientific-applet-template/releases/tag/v0.1.0) | `v0.1.0` | `a360bde95c192d8de4f9a3b531e73600ebf3d8b8` | [Pages](https://reblocke.github.io/scientific-applet-template/) at same commit | none by design |
| [`compatibility-curve`](https://github.com/reblocke/compatibility-curve/releases/tag/v0.1.0) | `v0.1.0` | `8945cfce61ecce29bdb6a922778f84d35fc4fe7f` | [Pages](https://reblocke.github.io/compatibility-curve/) at `3cfc31b7e76bf857a6f640fefd4d77398c0bf192` | `0.1.1` |
| [`wald-likelihood-support`](https://github.com/reblocke/wald-likelihood-support/releases/tag/v0.1.0) | `v0.1.0` | `b013abd2d512e1b041f089018649039b102a5c36` | [Pages](https://reblocke.github.io/wald-likelihood-support/) at `20a9046462f649f6fccc222a1d29aacd49c24ab9` | `0.2.1` |
| [`critical-effect-size`](https://github.com/reblocke/critical-effect-size/releases/tag/v0.1.0) | `v0.1.0` | `b4e201b3b23072c66302c243551388d6eaa0436f` | [Pages](https://reblocke.github.io/critical-effect-size/) at `cad4eaa6caa63dac550ddbde34b62e6faa032eb7` | `0.3.0` |
| [`type-s-m-calibrator`](https://github.com/reblocke/type-s-m-calibrator/releases/tag/v0.1.0) | `v0.1.0` | `2af70621c42b371d019ab360c17ade12c53e37c7` | [Pages](https://reblocke.github.io/type-s-m-calibrator/) at `5b23961d32bd0e94a6abf80c786a76f3fc3531e3` | `0.3.0` |
| [`precision-guardrail-planner`](https://github.com/reblocke/precision-guardrail-planner/releases/tag/v0.1.0) | `v0.1.0` | `b142950b164ec99c8ac6477eeefef62d686bf268` | [Pages](https://reblocke.github.io/precision-guardrail-planner/) at `cb38276dff79d1ce5085b90457c980a519d7ab31` | `0.4.0` |
| [`wald-inference-tools`](https://github.com/reblocke/wald-inference-tools/releases/tag/v0.1.0) | `v0.1.0` | `bbb045044a531244516540e2bcffaeca44c5e9df` | [Pages](https://reblocke.github.io/wald-inference-tools/) at same commit | catalog records per-tool versions |
| [`conf_curve_likelihood`](https://github.com/reblocke/conf_curve_likelihood/releases/tag/v0.2.0) | `v0.2.0` | `5fbf609df072100905d2a86ecbd55b286b5fa090` | [Pages](https://reblocke.github.io/conf_curve_likelihood/) at same commit | `0.4.0` |

All repository API records were public, default branch `main`, and GitHub-detected MIT. Hosted homepage metadata was populated for the five focused apps, catalog, and integrated workbench. The template has an active Pages deployment but a blank GitHub repository `homepage` field; core has no Pages site and a blank homepage appropriately.

### Hosted bundle reproducibility

Running the release-tag staging command reproduced every hosted Python bundle SHA exactly:

| Site | Hosted bundle SHA-256 |
|---|---|
| Template | `29916f446b6f2dcef63ab3c1924b6ca8c3f6c1866934a6fe3f81557e7a5b833b` |
| Compatibility | `d217e8533dbf021b83f84deefe9f3f35529e90b9a6f8f66fc8e17e2e236df96b` |
| Likelihood | `8e46298486307fd19f42061383feb5bf97381a5a956a6bce49a66122acd2575a` |
| Critical effect | `277a5aa0a2440184071bdd00a3e3dbe8d777cac660d15ca4b3f5822980bf7aee` |
| Type S/M | `aba0bfb223b5e8530942c2e2a5385b89798f292d84fb3d17325e85933615b1c1` |
| Precision | `ac60f36ffe000ec8846c06cfc214a869effab38a49c9d031c253c54ed9e3de15` |
| Integrated | `13af1bef8091181753ad1c018283435c10d8b9801b3ecb049db1014c38678df5` |

This narrows EF-01: no discrepant scientific Python file was detected, but the hosted HTML/JS/public-copy source state is still not the release state.

## EF-01 — Deployed versus released traceability

| Site | Release → live | Commits ahead | Changed paths between release and live | Latest live Pages evidence |
|---|---|---:|---|---|
| Compatibility | `8945cfce…` → `3cfc31b7…` | 2 | `README.md`, `tests/integration/test_browser_policy.py`, `web/index.html` | [run 30533359139](https://github.com/reblocke/compatibility-curve/actions/runs/30533359139) |
| Likelihood | `b013abd2…` → `20a90464…` | 2 | `README.md`, `tests/integration/test_browser_policy.py`, `web/index.html` | [run 30533365312](https://github.com/reblocke/wald-likelihood-support/actions/runs/30533365312) |
| Critical effect | `b4e201b3…` → `cad4eaa6…` | 2 | `README.md`, `tests/integration/test_repository_policy.py`, `web/index.html` | [run 30533767648](https://github.com/reblocke/critical-effect-size/actions/runs/30533767648) |
| Type S/M | `2af70621…` → `5b23961d…` | 2 | `README.md`, `tests/integration/test_repository_policy.py`, `web/index.html` | [run 30533767116](https://github.com/reblocke/type-s-m-calibrator/actions/runs/30533767116) |
| Precision | `b142950b…` → `cb38276d…` | 6 | `README.md`, E2E/integration tests, `web/index.html`, `web/app.js` | [run 30536349743](https://github.com/reblocke/precision-guardrail-planner/actions/runs/30536349743) |

The first four deltas are portfolio navigation/footer and corresponding policy-test updates. Precision also changes the visible Core marker in `web/app.js`. They are small, reviewed-looking changes, and current CI is green; nevertheless, the ticket requires a released-commit deployment, not merely a scientifically unchanged staged package.

The tag-matched release/CI/Pages evidence is green:

- Core: [release](https://github.com/reblocke/wald-inference-core/actions/runs/30530738993), [CI](https://github.com/reblocke/wald-inference-core/actions/runs/30530725902).
- Template: [release](https://github.com/reblocke/scientific-applet-template/actions/runs/30515197294), [Pages](https://github.com/reblocke/scientific-applet-template/actions/runs/30515046977), [CI](https://github.com/reblocke/scientific-applet-template/actions/runs/30515046834), [self-test](https://github.com/reblocke/scientific-applet-template/actions/runs/30515046825).
- Focused releases: compatibility [release](https://github.com/reblocke/compatibility-curve/actions/runs/30519571553); likelihood [release](https://github.com/reblocke/wald-likelihood-support/actions/runs/30525897686); critical [release](https://github.com/reblocke/critical-effect-size/actions/runs/30531844467); Type S/M [release](https://github.com/reblocke/type-s-m-calibrator/actions/runs/30530303228); precision [release](https://github.com/reblocke/precision-guardrail-planner/actions/runs/30534339183).
- Catalog: [release](https://github.com/reblocke/wald-inference-tools/actions/runs/30541256383), [Pages](https://github.com/reblocke/wald-inference-tools/actions/runs/30541243239), [CI](https://github.com/reblocke/wald-inference-tools/actions/runs/30541243178).
- Integrated: [release](https://github.com/reblocke/conf_curve_likelihood/actions/runs/30540418333), [Pages](https://github.com/reblocke/conf_curve_likelihood/actions/runs/30540400728), [CI](https://github.com/reblocke/conf_curve_likelihood/actions/runs/30540400771).

## Lane E — Browser, privacy, and accessibility

### Browser matrix

“Pass*” in the mobile workflow column means the calculation/interaction completed, but layout separately failed.

| Deployed site | Chromium desktop workflow | WebKit smoke | 390×844 keyboard workflow | Document width at 390 | Layout verdict |
|---|---|---|---|---:|---|
| Template | pass | pass | pass* | 750 px | **fail** |
| Compatibility | pass | pass | pass* | 750 px | **fail** |
| Likelihood | pass | pass | pass* | 890 px initial; 880 px repeat | **fail** |
| Critical effect | pass | pass | pass* | 750 px | **fail** |
| Type S/M | pass | pass | pass* | 890 px initial; 825 px repeat | **fail** |
| Precision | pass | pass | pass | 390 px | pass |
| Integrated | pass | pass | pass (keyboard edit + auto-update) | 390 px | pass |
| Catalog | pass | pass | pass (skip link + radio filter) | 390 px | pass |

There were zero captured Chromium desktop or WebKit console/page errors.

### EF-02 mobile overflow reproduction

The five failing full-page screenshots are:

```text
/private/tmp/cc-mig-11-ef-browser-artifacts/scientific-applet-template-mobile-full.png       750×2430
/private/tmp/cc-mig-11-ef-browser-artifacts/compatibility-curve-mobile-full.png             750×4855
/private/tmp/cc-mig-11-ef-browser-artifacts/wald-likelihood-support-mobile-full.png         880×6157
/private/tmp/cc-mig-11-ef-browser-artifacts/critical-effect-size-mobile-full.png            750×6283
/private/tmp/cc-mig-11-ef-browser-artifacts/type-s-m-calibrator-mobile-full.png             825×6454
```

DOM geometry in `/private/tmp/cc-mig-11-ef-mobile-overflow.json` shows:

- Template/compatibility/critical `.controls` and `.results`: approximately 734 px wide.
- Likelihood `.controls` and `.results`: approximately 864 px wide.
- Type S/M `.controls` and `.results`: approximately 809 px wide.
- The parent `.app-shell` is only 358 px wide, but its grid children have computed `min-width: auto` and extend the grid’s scroll width.
- The shared CSS switches the small-screen grid to `grid-template-columns: 1fr`, but does not zero the intrinsic minimum on the affected grid items. For example, release-tag compatibility CSS defines `.app-shell` at [`web/styles.css#L151-L156`](https://github.com/reblocke/compatibility-curve/blob/8945cfce61ecce29bdb6a922778f84d35fc4fe7f/web/styles.css#L151-L156) and the mobile rule at [`web/styles.css#L375-L389`](https://github.com/reblocke/compatibility-curve/blob/8945cfce61ecce29bdb6a922778f84d35fc4fe7f/web/styles.css#L375-L389).

The failure is not inferred from a screenshot alone: it is reproduced by viewport metrics, computed element rectangles, and full-page image pixel width. Existing “controls/results visible” checks do not catch document-level horizontal overflow.

### Keyboard and accessible error behavior

- Template and all five focused apps were traversed from an edited field to the submit button with Tab and activated with Enter.
- Integrated completed its auto-update after a keyboard-only edit and Tab.
- Catalog’s skip link focused `#main-content`; a radio-group arrow-key change selected “Design” and filtered visible cards.
- Every visible enabled form control inventoried by the audit had a nonempty accessible name. No visible `<img>` lacked `alt`.
- Every calculation app had a visible text result alternative (result summary and one or more tables/caption/reviewer blocks).
- Runtime status used status/live regions; invalid-input summaries used `role="alert"`.
- Domain-invalid inputs produced a safe user-facing message without traceback or local filesystem path and recovered after correction.
- A separate missing-required-value test confirmed all six form apps set `aria-invalid="true"` and rendered a keyboard-activatable summary link that focused the invalid control:

| App | Error link |
|---|---|
| Template | `#first-value` |
| Compatibility | `#ci-lower` |
| Likelihood | `#ci-lower` |
| Critical effect | `#target-probability` |
| Type S/M | `#null-value` |
| Precision | `#target-true-effect` |

The template’s error-link activation adds `#first-value` to the URL, and the catalog skip link adds `#main-content`. Neither contains a user value. No numerical app placed a numerical input in its query or fragment.

### Export and clipboard matrix

Every requested download completed; every PNG began with the PNG signature; every requested clipboard item was nonempty.

| App | CSV bytes | PNG bytes | Clipboard bytes |
|---|---:|---:|---:|
| Template | 67 | 57,481; 66,592 | caption 125 |
| Compatibility | 59,899 | 292,377; 158,260 | caption 522 |
| Likelihood | 74,308 | 284,192; 175,724 | caption 775 |
| Critical effect | 24,251 | 150,809; 175,269 | caption 681 |
| Type S/M | 56,992 | 191,217; 211,710 | caption 562; reviewer 476 |
| Precision | scenario 1,758; sensitivity 4,095 | 98,964; 140,527 | caption 338; reviewer 728 |
| Integrated | 95,146 | 385,967; 583,629 | caption 907; reviewer 500 |
| Catalog | not applicable | not applicable | not applicable |

The browser artifacts directory contains 27 files: 22 exported files and the five failing mobile screenshots.

### Network and storage appendix

For every scientific app:

- Initial HTTP(S) traffic was static GET traffic to the same-origin Pages site, pinned Plotly `3.1.0` at `cdn.plot.ly`, and pinned Pyodide `0.29.3` plus its stdlib/WASM/NumPy/SciPy/OpenBLAS assets at `cdn.jsdelivr.net`.
- After sentinel entry/calculation, the mobile run produced **zero** network requests.
- The desktop run produced exactly two post-input `blob:` image loads while testing local PNG exports. There were no post-input HTTP(S) requests.
- The sentinel appeared in no request URL/body or WebSocket frame.
- There were no non-GET requests, WebSockets, or telemetry/analytics URL matches.
- `localStorage`, `sessionStorage`, IndexedDB databases, document/context cookies, service-worker registrations/controllers, and CacheStorage keys were all empty.

The catalog made exactly four same-origin static GETs and loaded no Pyodide or scientific calculation package. Its inspected script list was local, and no tracking/storage was observed.

The privacy docs accurately disclose that CDN operators can see ordinary network metadata but not entered form values; compatibility provides a representative statement at [`docs/PRIVACY.md#L10-L34`](https://github.com/reblocke/compatibility-curve/blob/8945cfce61ecce29bdb6a922778f84d35fc4fe7f/docs/PRIVACY.md#L10-L34).

### Related tools and catalog

Tag-clone catalog live validation passed:

```text
Validated 7 references in index.html.
Validated 38 public release, repository, README, citation, and Pages targets.
```

Integrated live link validation passed:

```text
Validated 20 checked-in portfolio link requirements.
Validated 10 public portfolio targets.
```

The live catalog `data/tools.json` lists six tools with app/core versions that match the hosted manifests:

```text
compatibility-curve          0.1.0 / core 0.1.1
wald-likelihood-support      0.1.0 / core 0.2.1
critical-effect-size         0.1.0 / core 0.3.0
type-s-m-calibrator          0.1.0 / core 0.3.0
precision-guardrail-planner  0.1.0 / core 0.4.0
conf_curve_likelihood        0.2.0 / core 0.4.0
```

All remain correctly labeled `release-candidate`. The catalog states that it is static and calculation-free and must not claim portfolio validation before the report is complete at [`README.md#L11-L30`](https://github.com/reblocke/wald-inference-tools/blob/bbb045044a531244516540e2bcffaeca44c5e9df/README.md#L11-L30). `docs/PORTFOLIO_VALIDATION_REPORT.md` and `data/validation_status.json` are absent at the audited tag, which is appropriate before this review but prevents a completed-validation claim.

## Lane F — Documentation, rights, citation, and maintenance

### Required-file inventory

All nine release tags contain all of:

```text
README.md
LICENSE
CITATION.cff
AGENTS.md
llms.txt
CHANGELOG.md
docs/DECISIONS.md
docs/MAINTENANCE.md
docs/PRIVACY.md
```

Core, template, and focused apps also provide a dedicated scientific-scope/provenance/validation set. Catalog and integrated scope are documented in their README, decisions, principles, privacy, and maintenance materials. Repositories without a numbered ADR still have dated decision logs; lack of a numbered ADR was not treated as a blocker.

### Documentation and scope findings by repository

| Repository | Evidence-backed finding |
|---|---|
| Core | README states supported and unsupported uses, API/scientific scope, verification, version/citation/license ([scope/non-goals](https://github.com/reblocke/wald-inference-core/blob/fd7b24740122bed7ae07769674732c5e56c91277/README.md#L52-L62), [verification](https://github.com/reblocke/wald-inference-core/blob/fd7b24740122bed7ae07769674732c5e56c91277/README.md#L241-L283)). Migration provenance records source/tag/fixture hashes, MIT source, responsibility mapping, and deletion of the temporary duplicate implementation ([provenance](https://github.com/reblocke/wald-inference-core/blob/fd7b24740122bed7ae07769674732c5e56c91277/docs/MIGRATION_PROVENANCE.md#L3-L64)). |
| Template | README provides literal initialization and verification commands, privacy, architecture, export behavior, and an author checklist ([commands/checklist](https://github.com/reblocke/scientific-applet-template/blob/a360bde95c192d8de4f9a3b531e73600ebf3d8b8/README.md#L107-L150)). `AUTHOR ACTION REQUIRED` prompts are intentional template controls and were removed by a disposable initializer test. |
| Compatibility | README clearly distinguishes a Wald compatibility curve from exact profile likelihood/posterior probability and documents core authority, setup, validation, privacy, related tools, and citation ([authority through privacy](https://github.com/reblocke/compatibility-curve/blob/8945cfce61ecce29bdb6a922778f84d35fc4fe7f/README.md#L105-L177)). |
| Likelihood | README clearly separates relative likelihood/support from compatibility/power/posterior claims and records core/provenance/privacy/development ([non-goals and authority](https://github.com/reblocke/wald-likelihood-support/blob/b013abd2d512e1b041f089018649039b102a5c36/README.md#L63-L174)). |
| Critical effect | README distinguishes exact detectability from the preserved legacy benchmark and states privacy/clinical limits and source context ([exact/legacy through source](https://github.com/reblocke/critical-effect-size/blob/b4e201b3b23072c66302c243551388d6eaa0436f/README.md#L62-L139)). |
| Type S/M | README separates assumed-truth/selection-rule calibration from observed-data and precision tools and supplies validation/provenance/method reference ([non-goals through method](https://github.com/reblocke/type-s-m-calibrator/blob/2af70621c42b371d019ab360c17ade12c53e37c7/README.md#L44-L151)). |
| Precision | README distinguishes information multiplier from sample size, documents per-target/joint semantics, binding constraints, exports, verification, privacy, and citation ([scope and semantics](https://github.com/reblocke/precision-guardrail-planner/blob/b142950b164ec99c8ac6477eeefef62d686bf268/README.md#L18-L125), [exports through privacy](https://github.com/reblocke/precision-guardrail-planner/blob/b142950b164ec99c8ac6477eeefef62d686bf268/README.md#L138-L186)). |
| Catalog | README states release-candidate status, calculation-free architecture, static/no-tracking posture, live validation commands, metadata update rules, and privacy ([README](https://github.com/reblocke/wald-inference-tools/blob/bbb045044a531244516540e2bcffaeca44c5e9df/README.md#L11-L80)). |
| Integrated | README distinguishes focused tools, explicit non-goals, released core/staging, verification, source citations, maintenance, no-clinical-data posture, and related tools ([non-goals](https://github.com/reblocke/conf_curve_likelihood/blob/5fbf609df072100905d2a86ecbd55b286b5fa090/README.md#L46-L64), [core and verification](https://github.com/reblocke/conf_curve_likelihood/blob/5fbf609df072100905d2a86ecbd55b286b5fa090/README.md#L120-L200), [documentation/data/license](https://github.com/reblocke/conf_curve_likelihood/blob/5fbf609df072100905d2a86ecbd55b286b5fa090/README.md#L200-L236)). |

### Data, privacy, and clinical posture

- The portfolio uses no research or patient-level dataset. Fixtures/examples are described as aggregate or synthetic.
- Apps state that PHI, direct identifiers, patient records, clinical free text, and uploads are not intended inputs.
- Every scientific app says it is not clinically validated and is not clinical decision support; user thresholds/MCIDs are not claimed as validated clinical cutoffs.
- Core supplies statistical software primitives, not clinical validation.
- Catalog has no numerical inputs.
- Integrated README states “No clinical data expected.”

These statements are appropriately scoped. This review does **not** certify clinical validity, clinical utility, regulatory suitability, or a clinical workflow.

### Authorship, license, citation, and source rights

- Current `pyproject.toml`, `CITATION.cff`, README/maintenance surfaces, and every MIT `LICENSE` consistently use **Brian Locke**; every license line is `Copyright (c) 2026 Brian Locke`.
- Historical `Reed Blocke` / `Brian W. Locke` strings occur only in integrated migration/decision provenance or a core forbidden-identity test. Current integrated authority explicitly resolves the metadata to Brian Locke at [`docs/DECISIONS.md#L288-L309`](https://github.com/reblocke/conf_curve_likelihood/blob/5fbf609df072100905d2a86ecbd55b286b5fa090/docs/DECISIONS.md#L288-L309). No identity was inferred by this reviewer.
- CITATION versions match all nine release versions. Release dates are present in eight. Compatibility’s complete 12-line `CITATION.cff` has no `date-released` ([file](https://github.com/reblocke/compatibility-curve/blob/8945cfce61ecce29bdb6a922778f84d35fc4fe7f/CITATION.cff)); this is a cross-portfolio completeness gap, not the basis of a release block.
- Core provenance records the MIT source, imported blob/hash checkpoint, responsibility mapping, and no external artifacts for later extensions ([migration provenance](https://github.com/reblocke/wald-inference-core/blob/fd7b24740122bed7ae07769674732c5e56c91277/docs/MIGRATION_PROVENANCE.md#L3-L64)).
- Template provenance says patterns were inspected but no app formula, prose, scientific name, fixture, figure, or visual content was copied ([template provenance](https://github.com/reblocke/scientific-applet-template/blob/a360bde95c192d8de4f9a3b531e73600ebf3d8b8/docs/TEMPLATE_PROVENANCE.md#L1-L12)).
- Likelihood documents Zampieri et al., DOI/retrieval date, CC BY-NC-ND 4.0, and that no figure/table/code/substantial text was copied ([runtime dependencies](https://github.com/reblocke/wald-likelihood-support/blob/b013abd2d512e1b041f089018649039b102a5c36/docs/RUNTIME_DEPENDENCIES.md#L65-L102)).
- Critical documents the Perugini source as contextual and states no external figure/table/dataset/code/substantial text was copied ([provenance](https://github.com/reblocke/critical-effect-size/blob/b4e201b3b23072c66302c243551388d6eaa0436f/docs/PROVENANCE.md#L47-L62)).
- Type S/M cites Gelman & Carlin with DOI/retrieval date and states no external figure/table/dataset/substantial text was copied ([scope](https://github.com/reblocke/type-s-m-calibrator/blob/2af70621c42b371d019ab360c17ade12c53e37c7/docs/SCIENTIFIC_SCOPE.md#L286-L297)).
- Precision records frozen source/tag/manifest/fixture hashes, no patient/external scientific artifact, and Core formula ownership ([migration provenance](https://github.com/reblocke/precision-guardrail-planner/blob/b142950b164ec99c8ac6477eeefef62d686bf268/docs/MIGRATION_PROVENANCE.md#L3-L32)).
- Catalog identifies original text/code as MIT and contains no calculation code.
- Integrated names the three methodology sources and states that third-party/publisher materials retain their original terms ([README](https://github.com/reblocke/conf_curve_likelihood/blob/5fbf609df072100905d2a86ecbd55b286b5fa090/README.md#L200-L232)).
- A tag-checkout file scan found no committed PNG/JPEG/GIF/SVG/PDF/font/CSV/XLSX artifact outside ignored generated browser packages in any repository.

The three methodology URLs resolved to the expected publisher domains, but direct automated retrieval returned HTTP 403 from the publishers. Rights findings therefore rely on repository provenance statements, absence of committed external assets, and inspected source/copy—not a full-text forensic comparison against publisher content.

### Maintenance and traceability gaps

- Maintenance/change/rollback guidance is present across all repositories.
- The catalog correctly remains `release-candidate` and has not yet added the final report/status.
- Most app docs tell users to cite a tag or exact commit and the hosted manifest records `source_commit`, but most do not state an explicit **last independently verified app release commit** in README/maintenance. Integrated does record exact Core release provenance. This is a bounded documentation gap.
- The five focused release-tag READMEs predate the navigation/footer copy now live on Pages/main. This is part of EF-01’s release/public-document divergence.
- All current portfolio release objects are prereleases. That is consistent with the validation gate but must not be presented as a completed validated release.

## Literal command and clean-check evidence from this lane

This lane checked the tag READMEs’ command blocks and executed the documentation/browser-relevant subset below. Lane C and the numerical lanes must supply the final all-command/full-`make verify` matrix; this ledger does not relabel unrun commands as passed.

Passed across all tag checkouts:

```text
uv sync --locked                         # core used --all-groups
make fmt-check
make lint
git status --short                       # clean after verification
git diff --check                         # clean
git rev-parse HEAD
uv tree --depth 1
```

Additional passed evidence:

| Repository | Commands/results in this lane |
|---|---|
| Core | `make metadata-check`; locked sync; format/lint; clean status |
| Template | `make stage-web`; integration tests: 11 passed; disposable initializer using the README compatibility example; post-initialization `uv sync --locked`; no unresolved required values |
| Compatibility | `make stage-web`; repository/browser policy tests: 5 passed; README legacy regression command: 11 passed |
| Likelihood | `make stage-web`; repository/browser policy tests: 6 passed |
| Critical effect | `make stage-web`; repository/browser policy tests: 5 passed |
| Type S/M | `make stage-web`; repository/browser policy tests: 4 passed; `uv run pytest -q tests/scientific_reference tests/regression`: 8 passed |
| Precision | `make stage-web`; repository/browser policy tests: 4 passed; `uv run pytest -q tests/scientific_reference/ tests/regression/`: 5 passed |
| Catalog | `make validate`; `make live-check`; live Chromium/WebKit/mobile audit |
| Integrated | `make stage-web`; workflow/related-tools integration tests: 8 passed; `uv run python scripts/check_portfolio_links.py --live` |

All release-tag staging runs were standalone; no sibling repository was required. Generated browser Python remained ignored, and every checkout ended clean.

## Claim–evidence ledger

| ID | Material claim | Best evidence | Status | Release consequence |
|---|---|---|---|---|
| C1 | Every Pages app is traceable to its release commit | Hosted manifests, release tag commits, Pages workflow heads | **Contradicted for five focused apps** | EF-01 blocker |
| C2 | Every deployed site is usable at the required 390 px mobile viewport | Chromium metrics, computed element rectangles, full-page PNG dimensions | **Contradicted for five sites** | EF-02 blocker |
| C3 | Numerical inputs remain client-side | Sentinel request/body/WebSocket inspection; zero mobile post-input requests; only local desktop blob exports | Supported for audited workflows | Positive |
| C4 | No application persistence or tracking | Storage/cookie/worker/cache inventory; network URL review | Supported for audited sessions | Positive |
| C5 | Advertised exports work | 22 downloaded artifacts, sizes/SHA/signatures, clipboard checks | Supported | Positive |
| C6 | Basic keyboard/error/text-alternative accessibility exists | Keyboard flows, label inventory, `role=alert`, `aria-invalid`, error links, text summaries/tables | Supported within defined scope | Positive; not WCAG certification |
| C7 | Catalog versions and links match deployed apps | Live `tools.json`, hosted manifests, `make live-check`, integrated live link check | Supported | Positive |
| C8 | Documentation, author, license, no-data/privacy, and source-rights posture are coherent | Tag docs/CITATION/LICENSE/metadata scan; no committed external binary assets | Supported with bounded gaps | Nonblocking except where release docs diverge under EF-01 |
| C9 | Portfolio may be marked validated | Catalog currently says release-candidate; final report/status absent; EF-01 and EF-02 | **Contradicted** | Verdict must remain blocked |
| C10 | Portfolio is clinically validated | Explicitly disclaimed and out of ticket scope | Not claimed / not tested | Must not certify |

## Provisional Scientific Coding Project Standard scores

### Rubric

Domain score:

- `3`: complete, independently evidenced for the reviewed release.
- `2`: substantial and usable, with a bounded gap.
- `1`: material incomplete state or systemic release risk.
- `0`: absent or contradicted at the project’s core.

Weights (ticket-local because no authoritative weighting was supplied):

| Domain | Weight |
|---|---:|
| A. Scientific design/statistical validity | 20% |
| B. Data provenance/rights/security | 10% |
| C. Computational reproducibility | 15% |
| D. Verification/testing/independent review | 20% |
| E. Readability/maintainability | 10% |
| F. Documentation/replicator usability | 10% |
| G. Version control/change management | 7.5% |
| H. Output traceability/dissemination/preservation | 7.5% |

Weighted total is `sum((domain score / 3) × domain weight)`.

Release thresholds:

- **Validated for release:** total ≥85, every domain ≥2, A/D/H ≥2, and no release blocker.
- **Validated with nonblocking limitations:** total 75–84.9, every domain ≥2, and no release blocker.
- **Not validated:** total <75, any domain 0–1, or any release blocker.

### Repository and portfolio matrix

A/D values are provisional synthesis inputs based on released-source documentation, green CI, targeted tests, and live behavior. They must be reconciled with the independent numerical/baseline/artifact lanes; this lane did not independently recompute every formula or B01–B08.

| Repository | A | B | C | D | E | F | G | H | Weighted total | Key score gap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `wald-inference-core` | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 100.0 | A/D require numerical-lane confirmation |
| `scientific-applet-template`* | 2 | 3 | 3 | 3 | 2 | 2 | 3 | 3 | 86.7 | Generic scientific authority is intentionally unresolved downstream; inherited mobile overflow |
| `compatibility-curve` | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 1 | 79.2 | Mobile overflow; live commit is untagged; missing CFF release date |
| `wald-likelihood-support` | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 1 | Mobile overflow; live commit is untagged |
| `critical-effect-size` | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 1 | Mobile overflow; live commit is untagged |
| `type-s-m-calibrator` | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 1 | Mobile overflow; live commit is untagged |
| `precision-guardrail-planner` | 3 | 3 | 3 | 2 | 3 | 3 | 2 | 1 | Mobile passes, but live commit is six commits beyond release |
| `wald-inference-tools`* | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | Calculation-free support repo; final validation report/status intentionally absent |
| `conf_curve_likelihood` | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | A/D require numerical-lane confirmation |
| **Portfolio** | **3** | **3** | **3** | **2** | **2** | **2** | **1** | **1** | **76.7** | Systemic release/live and mobile failures |

\* Template and catalog are support repositories rather than independent scientific calculation packages. They are scored for their portfolio role instead of being silently omitted.

The portfolio score is systemic, not a simple mean of repository totals: a release cannot be more traceable than the five untagged deployed sites, and mobile usability is materially incomplete across most template-derived sites.

## Release blockers and closure criteria

### EF-01 — Five hosted sites are not release-identical

**Closure evidence required:**

1. Tag/release the intended complete site source or redeploy the exact existing release commit.
2. Demonstrate `manifest.source_commit == peeled release-tag commit`.
3. Demonstrate Pages workflow head equals that commit.
4. Re-stage in a clean release-tag clone and compare complete artifact inventory/hashes, not only the Python bundle.
5. Rerun live links, browser, privacy, and export checks.

### EF-02 — Five hosted sites overflow at 390 px

**Closure evidence required:**

1. Fix the shared responsive grid/intrinsic minimum issue without obscuring plot/table content.
2. Add an assertion after calculation that document/body scroll width is no greater than viewport/client width at 390×844.
3. Cover template, compatibility, likelihood, critical, and Type S/M in Chromium; include WebKit mobile smoke.
4. Recheck keyboard focus, text alternatives, table/plot visibility, and PNG/CSV exports after the layout change.
5. Release/tag/deploy the fixes so EF-01 is not recreated.

## Nonblocking limitations and residual risks

- No screen-reader session, zoom/reflow audit, contrast measurement, automated axe suite, or formal WCAG conformance review was performed.
- WebKit was a load/calculate/render smoke, not the full Chromium export/error suite.
- Live sites are mutable; the recorded commit and JSON hashes are necessary evidence anchors.
- CDN privacy evidence is observational for the audited workflows. Ordinary request metadata (including IP and requested static asset) remains visible to CDN operators as documented.
- Publisher pages returned HTTP 403 to automated retrieval after DOI resolution; no full-text copyright comparison was possible.
- Compatibility `CITATION.cff` omits `date-released`; template repository homepage metadata is blank despite active Pages; most repos lack an explicit last independently verified app-release commit in public docs.
- Numerical formula correctness, B01–B08 max differences, clean-wheel/sdist validation, and complete literal README-command execution are synthesis dependencies from the other lanes.
- No clinical validation was attempted or inferred.

## Exact command families

Representative commands used; per-repository repeats used the exact release tags/paths in the inventory:

```bash
git clone --branch <tag> --single-branch https://github.com/reblocke/<repo>.git <temp-path>
uv sync --locked
uv sync --locked --all-groups                 # core
make stage-web                                # browser package apps
make fmt-check
make lint
make metadata-check                           # core
make validate                                 # catalog
make live-check                               # catalog
uv run python scripts/check_portfolio_links.py --live
uv run pytest -q tests/integration
uv run pytest -q tests/regression/test_legacy_compatibility.py
uv run pytest -q tests/scientific_reference tests/regression
uv run pytest -q tests/scientific_reference/ tests/regression/
git status --short
git diff --check
git rev-parse HEAD
uv tree --depth 1
gh run list -R reblocke/<repo> --json databaseId,name,headSha,event,status,conclusion,url,createdAt
curl -fsSL https://reblocke.github.io/<repo>/assets/py/manifest.json
python /private/tmp/cc-mig-11-ef-live-audit.py
```

## Lane handoff

- **Verdict:** Not validated; release blockers remain.
- **Lane evidence file:** `/private/tmp/cc-mig-11-evidence/lane_ef.md`
- **Blocking findings:** EF-01 release/live commit drift; EF-02 five-site mobile overflow.
- **Issues/PRs opened:** none (report-only lane).
- **Required synthesis caution:** Do not mark the catalog `validation_status` passed until both blockers are fixed, released, deployed, and independently rerun, and until numerical/cold-start/artifact lanes are reconciled.
