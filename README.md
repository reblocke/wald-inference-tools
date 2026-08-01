# Wald inference tools

This repository is the question-based catalog for a portfolio of client-side Wald inference
applets. It helps readers choose a focused tool without turning the catalog into another
calculation runtime.

The catalog begins with one question: **What question are you trying to answer?** It distinguishes
tools that condition on an observed estimate and confidence interval from design-calibration tools
that condition on assumed true effects and repeated-study selection behavior.

## Why the portfolio is split

- One released [`wald-inference` Core](https://github.com/reblocke/wald-inference-core) owns the
  numerical definitions, so applications do not fork formulas.
- Five focused apps each answer one question and remain independently deployable, citable, and
  reviewable.
- The formula-free
  [`scientific-applet-template`](https://github.com/reblocke/scientific-applet-template) provides
  reusable engineering infrastructure without becoming a shared runtime dependency.
- The integrated workbench preserves backward-compatible APIs and supports intentional
  cross-paradigm comparison.
- This catalog provides calculation-free navigation and release evidence, so changing its copy
  cannot change a scientific result.

## Intended use and audience

Researchers, methods collaborators, reviewers, and educators can use this README or the
[hosted catalog](https://reblocke.github.io/wald-inference-tools/) to select the narrowest app that
answers their question. Maintainers can use it to resolve repository ownership, releases,
citations, and validation evidence. The catalog is not itself a statistical tool, does not accept
analysis inputs, and does not transfer values between apps.

## Complete portfolio map

| Repository | Independent role | Public entry and documented release |
|---|---|---|
| [`wald-inference-core`](https://github.com/reblocke/wald-inference-core) | Sole numerical and formula authority; Python package, not a web app | [v0.4.2](https://github.com/reblocke/wald-inference-core/releases/tag/v0.4.2) |
| [`scientific-applet-template`](https://github.com/reblocke/scientific-applet-template) | Formula-free applet scaffold; its arithmetic demo is not a scientific method | [template demonstration](https://reblocke.github.io/scientific-applet-template/) · [v0.1.3](https://github.com/reblocke/scientific-applet-template/releases/tag/v0.1.3) |
| [`compatibility-curve`](https://github.com/reblocke/compatibility-curve) | Focused observed-data compatibility display | [app](https://reblocke.github.io/compatibility-curve/) · [v0.1.5](https://github.com/reblocke/compatibility-curve/releases/tag/v0.1.5) |
| [`wald-likelihood-support`](https://github.com/reblocke/wald-likelihood-support) | Focused normalized Wald relative-support display | [app](https://reblocke.github.io/wald-likelihood-support/) · [v0.1.4](https://github.com/reblocke/wald-likelihood-support/releases/tag/v0.1.4) |
| [`critical-effect-size`](https://github.com/reblocke/critical-effect-size) | Focused fixed-precision detectability app | [app](https://reblocke.github.io/critical-effect-size/) · [v0.1.5](https://github.com/reblocke/critical-effect-size/releases/tag/v0.1.5) |
| [`type-s-m-calibrator`](https://github.com/reblocke/type-s-m-calibrator) | Focused repeated-study Type S/M app | [app](https://reblocke.github.io/type-s-m-calibrator/) · [v0.1.5](https://github.com/reblocke/type-s-m-calibrator/releases/tag/v0.1.5) |
| [`precision-guardrail-planner`](https://github.com/reblocke/precision-guardrail-planner) | Focused inverse-precision and joint-guardrail app | [app](https://reblocke.github.io/precision-guardrail-planner/) · [v0.1.4](https://github.com/reblocke/precision-guardrail-planner/releases/tag/v0.1.4) |
| [`conf_curve_likelihood`](https://github.com/reblocke/conf_curve_likelihood) | Backward-compatible integrated workbench for advanced cross-paradigm comparison | [app](https://reblocke.github.io/conf_curve_likelihood/) · [v0.2.7](https://github.com/reblocke/conf_curve_likelihood/releases/tag/v0.2.7) |
| [`wald-inference-tools`](https://github.com/reblocke/wald-inference-tools) | This calculation-free catalog and portfolio-validation evidence carrier | [catalog](https://reblocke.github.io/wald-inference-tools/) · [v0.2.2](https://github.com/reblocke/wald-inference-tools/releases/tag/v0.2.2) |

## Choose the narrowest scientific app

| If your question is… | Conditioning and principal inputs | Use and principal outputs | Do not use it as… |
|---|---|---|---|
| Which candidate effects are compatible with a reported estimate and 95% CI? | Observed-data; effect measure, estimate/CI, null, display range | [Compatibility curve](https://reblocke.github.io/compatibility-curve/); curve, candidate summaries, CSV/PNG/caption | a probability that an effect is true |
| How much relative support does that Wald reconstruction provide? | Observed-data; estimate/CI, support ratio, candidate values | [Wald likelihood support](https://reblocke.github.io/wald-likelihood-support/); normalized relative likelihood, pairwise and S−2 support | an exact fitted-model likelihood or posterior probability |
| How large must an assumed true effect be for a claim rule to select it with a target probability? | Design; SE or CI, null, alpha, rule, direction, target probability | [Critical effect size](https://reblocke.github.io/critical-effect-size/); exact fixed-SE critical effect and selection curve | an MCID, observed evidence, or study-specific sample-size calculation |
| If an effect were true, how often would selected claims have the wrong sign or exaggerate magnitude? | Design; SE or CI, assumed truths, alpha, selection rule | [Type S/M calibrator](https://reblocke.github.io/type-s-m-calibrator/); selected-claim probability, Type S, Type M | a probability that an observed estimate is wrong |
| What precision would meet one or more selection, Type S, or Type M guardrails? | Design; current SE or CI, assumed truth, claim rule, guardrails | [Precision guardrail planner](https://reblocke.github.io/precision-guardrail-planner/); required SE, information, binding target, sensitivity | an exact sample-size calculator or automatic target selector |
| Do you intentionally need observed-data and design paradigms together? | Mixed; observed reconstruction plus explicit design scenarios | [Integrated workbench](https://reblocke.github.io/conf_curve_likelihood/); combined displays and backward-compatible exports | the default interface for one focused question |

## Current status

Version `0.2.2` is the validation-bearing catalog release. The portfolio verdict is
**Validated for release.** The exact audited tags, commits, commands, numerical differences,
browser observations, release checksums, limitations, and project-standard scores are recorded in
[`docs/PORTFOLIO_VALIDATION_REPORT.md`](docs/PORTFOLIO_VALIDATION_REPORT.md),
[`data/validation_status.json`](data/validation_status.json), and the checksum-addressed
[`validation-evidence/index.json`](validation-evidence/index.json).

The catalog's own audited predecessor is v0.2.1. Version 0.2.2 carries the maintenance-refreshed
report for the Core v0.4.2 release set and does not treat its own publication as evidence for the
verdict. Its tag, release assets, and Pages bytes are reconciled externally after publication.

Maintenance owner: Brian Locke. See [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md) for the release and
metadata-update policy.

## Architecture

- `data/tools.json` is the single source for tool questions, scope, versions, and links.
- `index.html`, `styles.css`, and `app.js` render a static, calculation-free site.
- `scripts/validate_tools_manifest.py` enforces the local schema and semantic invariants.
- `scripts/check_links.py` validates local references and can verify public annotated releases,
  exact deployed source commits, hosted manifests, and URLs with `--live`.
- `data/validation_status.json` binds the independent verdict to the exact report digest and
  release inventory.
- `validation-evidence/index.json` hashes every preserved audit ledger and machine-readable result.
- `scripts/build_site.py` creates the exact Pages artifact.

The catalog has no Pyodide, scientific Python, telemetry, cookies, storage, saved state, or shared
runtime dependency for the apps.

## Scientific authority and interpretation boundary

All six scientific apps consume the exact released Core version recorded in their dependency and
staging metadata. The five focused apps record browser-stage manifests; the integrated workbench
stages its locked installed dependency through `scripts/stage_web_python.py`. Core governs
numerical behavior; each app governs request validation, presentation, warnings, accessibility,
and exports. The template supplies copied scaffolding only, and the catalog does not import Core or
execute any formula.

The portfolio's validation verdict applies to the exact releases and evidence identified below.
It does not establish that a one-parameter Wald approximation is suitable for a new study, validate
user-entered effects or thresholds, or confer clinical, diagnostic, treatment, regulatory, or
patient-specific suitability.

## Setup and verification

```bash
uv sync --locked
uv run playwright install chromium webkit
make verify
```

To run the catalog:

```bash
make serve
```

Then open <http://127.0.0.1:8000/>.

To validate public annotated releases, deployed release-commit identity, hosted manifests, and the
compact portfolio block in every public README after all sites and cross-link PRs are live:

```bash
make live-check
```

## Updating tool metadata

1. Update the relevant object in `data/tools.json`.
2. Use the app release tag, not an unreleased branch version.
3. Confirm `app_version`, `core_version`, and `source_commit` against the hosted staged-package
   manifest and annotated release tag.
4. Set `validation_status` only from recorded evidence.
5. Run `make verify` and `make live-check`.
6. Confirm the catalog CI and Pages workflows both passed their live-metadata gate before merging
   or deploying.
7. Update the validation report, status, and evidence index only from a completed independent
   review; never infer validation from a successful release workflow.

To add a tool, supply every schema field, a unique slug, repository and hosted URLs, a manifest
probe, accurate non-goals, and an adjacent-tool slug. The site renders directly from the manifest;
do not duplicate card copy in HTML.

## Scope and privacy

The catalog performs no statistical calculation and receives no user inputs. All app links are
plain, input-free URLs. See [`docs/DECISIONS.md`](docs/DECISIONS.md),
[`docs/PRIVACY.md`](docs/PRIVACY.md), and [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md).

## Citation map and source roles

Cite the exact tagged software release or commit actually used. Each repository's
`CITATION.cff` is the software-citation authority; a method paper does not replace that citation,
and no paper governs executable behavior.

| Repository or capability | Software citation | Applicable method source |
|---|---|---|
| Core | [Core `CITATION.cff`](https://github.com/reblocke/wald-inference-core/blob/main/CITATION.cff) | Cite the source for the concept being discussed; Core APIs and tests remain implementation authority |
| Template | [Template `CITATION.cff`](https://github.com/reblocke/scientific-applet-template/blob/main/CITATION.cff) | No scientific method citation; initialized apps must replace author-action metadata and add their own sources |
| Compatibility curve | [App `CITATION.cff`](https://github.com/reblocke/compatibility-curve/blob/main/CITATION.cff) | Rafi and Greenland for compatibility terminology and interpretation |
| Wald likelihood support | [App `CITATION.cff`](https://github.com/reblocke/wald-likelihood-support/blob/main/CITATION.cff) | Zampieri et al. for evidential likelihood, support, and S−2 terminology |
| Critical effect size | [App `CITATION.cff`](https://github.com/reblocke/critical-effect-size/blob/main/CITATION.cff) | Perugini et al. for critical-effect-size design rationale |
| Type S/M calibrator | [App `CITATION.cff`](https://github.com/reblocke/type-s-m-calibrator/blob/main/CITATION.cff) | Gelman and Carlin for Type S and Type M concepts |
| Precision guardrail planner | [App `CITATION.cff`](https://github.com/reblocke/precision-guardrail-planner/blob/main/CITATION.cff) | Gelman and Carlin plus Perugini et al. provide conceptual context; Core owns the exact joint inverse solver |
| Integrated workbench | [Workbench `CITATION.cff`](https://github.com/reblocke/conf_curve_likelihood/blob/main/CITATION.cff) | Cite whichever of the four method sources applies to the panels used |
| Catalog | [Catalog `CITATION.cff`](CITATION.cff) | Cite only when the navigation, manifest, or validation-evidence carrier is itself relevant |

Method references:

- Rafi Z, Greenland S. Semantic and cognitive tools to aid statistical science: replace confidence
  and significance by compatibility and surprise. *BMC Medical Research Methodology*.
  2020;20:244. <https://doi.org/10.1186/s12874-020-01105-9>. Compatibility terminology and
  interpretation; open access under CC BY 4.0; retrieved 2026-08-01.
- Zampieri FG, Cahusac PMB, Maia IS, et al. Trial Analysis and Interpretation in Critical Care
  Using the Evidential (Likelihood) Approach: Rationale and Practical Considerations. *American
  Journal of Respiratory and Critical Care Medicine*. 2025;211(9):1610–1621.
  <https://doi.org/10.1164/rccm.202504-0809TR>. Likelihood/support terminology; retrieved
  2026-04-23; CC BY-NC-ND 4.0.
- Perugini A, Gambarota F, Toffalini E, et al. The Benefits of Reporting Critical-Effect-Size
  Values. *Advances in Methods and Practices in Psychological Science*.
  2025;8(2):25152459251335298.
  <https://doi.org/10.1177/25152459251335298>. Critical-effect-size and design rationale; retrieved
  2026-04-23; CC BY-NC 4.0.
- Gelman A, Carlin J. Beyond Power Calculations: Assessing Type S (Sign) and Type M (Magnitude)
  Errors. *Perspectives on Psychological Science*. 2014;9(6):641–651.
  <https://doi.org/10.1177/1745691614551642>. Type S/M terminology and interpretation; retrieved
  2026-06-14; publisher page © the authors 2014, reuse by permission.

These citations are contextual. No publication figure, table, dataset, code, or substantial text
is copied into the catalog, and publisher access and reuse terms continue to apply. Catalog code
and original text are MIT licensed; see [`LICENSE`](LICENSE).
