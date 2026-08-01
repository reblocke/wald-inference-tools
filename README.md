# Wald inference tools

This repository is the question-based catalog for a portfolio of client-side Wald inference
applets. It helps readers choose a focused tool without turning the catalog into another
calculation runtime.

The catalog begins with one question: **What question are you trying to answer?** It distinguishes
tools that condition on an observed estimate and confidence interval from design-calibration tools
that condition on assumed true effects and repeated-study selection behavior.

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

## Citation and license

Use each app's citation guidance for scientific use. Cite this catalog only when the portfolio
navigation/manifest itself is relevant. Catalog code and original text are MIT licensed; see
[`LICENSE`](LICENSE) and [`CITATION.cff`](CITATION.cff).
