# Wald inference tools

This repository is the question-based catalog for a portfolio of client-side Wald inference
applets. It helps readers choose a focused tool without turning the catalog into another
calculation runtime.

The catalog begins with one question: **What question are you trying to answer?** It distinguishes
tools that condition on an observed estimate and confidence interval from design-calibration tools
that condition on assumed true effects and repeated-study selection behavior.

## Current status

Version `0.1.1` records the corrective Core and app release set. Entries marked
`release-candidate` in [`data/tools.json`](data/tools.json) must not be described as
portfolio-validated until the independent validation report is complete.

Maintenance owner: Brian Locke. See [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md) for the release and
metadata-update policy.

## Architecture

- `data/tools.json` is the single source for tool questions, scope, versions, and links.
- `index.html`, `styles.css`, and `app.js` render a static, calculation-free site.
- `scripts/validate_tools_manifest.py` enforces the local schema and semantic invariants.
- `scripts/check_links.py` validates local references and can verify public annotated releases,
  exact deployed source commits, hosted manifests, and URLs with `--live`.
- `scripts/build_site.py` creates the exact Pages artifact.

The catalog has no Pyodide, scientific Python, telemetry, cookies, storage, saved state, or shared
runtime dependency for the apps.

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
7. Update the validation report/status file when independent review changes the portfolio verdict.

To add a tool, supply every schema field, a unique slug, repository and hosted URLs, a manifest
probe, accurate non-goals, and an adjacent-tool slug. The site renders directly from the manifest;
do not duplicate card copy in HTML.

## Scope and privacy

The catalog performs no statistical calculation and receives no user inputs. All app links are
plain, input-free URLs. See [`docs/DECISIONS.md`](docs/DECISIONS.md),
[`docs/PRIVACY.md`](docs/PRIVACY.md), and [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md).

## Citation and license

Use each app's citation guidance for scientific use. Cite this catalog only when the portfolio
navigation/manifest itself is relevant. Catalog code and original text are MIT licensed; see
[`LICENSE`](LICENSE) and [`CITATION.cff`](CITATION.cff).
