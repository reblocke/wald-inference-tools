# Contributing

## Repository scope

This repository owns the calculation-free portfolio catalog, its static presentation, the
`data/tools.json` metadata contract, local and live validators, and the preserved portfolio
validation evidence. It does not own any Wald formula or scientific app behavior. Numerical
changes belong in [`wald-inference-core`](https://github.com/reblocke/wald-inference-core);
app-specific orchestration and presentation changes belong in the affected app repository.

Keep observed-estimate compatibility and likelihood questions distinct from assumed-truth design
calibration. Do not mark a tool validated, change a pinned release or deployed source commit, or
edit the report/status/evidence hash chain without a completed independent review that supports
the exact change. Successful CI, Pages, or release automation is engineering evidence, not new
scientific validation.

Use public issue forms only for nonsensitive catalog engineering, metadata, and accessibility
reports. Report vulnerabilities through the private process in [SECURITY.md](SECURITY.md). Never
place credentials, protected health information, patient-level data, unpublished restricted data,
or other sensitive values in an issue, pull request, fixture, screenshot, URL, or workflow log.
The catalog has no user inputs, so reproductions should use public metadata and synthetic examples
only.

## Change process

1. Start from the current protected `main` branch and make one reviewable change.
2. State assumptions, success criteria, silent-failure risks, and verification before editing.
3. Treat `data/tools.json` as the public metadata source of truth; do not duplicate its values in
   rendered card markup.
4. Preserve the calculation-free, input-free, same-origin site and the distinction between
   observed-data and assumed-truth conditioning.
5. Keep live metadata validation fail closed in CI, Pages, and release workflows.
6. Preserve validation evidence verbatim unless an independently reviewed evidence update is the
   explicit task.
7. Keep every third-party GitHub Action pinned to a reviewed full commit SHA with a version
   comment.
8. Open a pull request and let all required checks complete before merging.

Do not add statistical formulas, Pyodide, a backend, telemetry, persistence, cookies, storage,
uploads, third-party browser requests, or input-bearing links as conveniences.

## Verification

Restore the locked environment and run the complete documented suite:

```bash
uv sync --locked
uv run playwright install chromium webkit
make verify
make live-check
git diff --check
git status --short
```

Metadata or validation-status changes require exact public annotated-tag, peeled-commit, deployed
source, hosted manifest, README/footer, report/status, evidence-index, and checksum review.
Document every skipped check, warning, or unavailable public source.

## Release changes

A new release requires a reviewed pull request and a signed, annotated version tag pointing to the
exact reviewed merge commit. The tag must equal `v` plus the authoritative catalog version, and
that version needs exactly one nonempty changelog section. The tag workflow:

1. installs an exact checksummed GitHub CLI;
2. cryptographically verifies the remote GitHub tag object and binds it to the event commit;
3. requires the verified tag target to be contained in protected `main` history before reading
   project metadata or executing repository code;
4. runs the status validator in release-only mode and rejects a verdict that still reports release
   blockers;
5. runs the complete local browser suite and repeats the live metadata gate with read-only
   contents permission and release caching disabled;
6. builds the exact source, site, manifest, report, status, evidence archive, evidence index, and
   checksum assets;
7. transfers and rechecks the complete eight-file asset bundle in a narrowly write-enabled job;
8. requires repository release immutability through an administration-read token;
9. creates a draft stable release using only the matching version's changelog section;
10. downloads and compares the exact release body, asset names, bytes, and checksums; and
11. publishes the verified draft once as stable and confirms immutable provenance.

Before creating a new tag, enable immutable releases and configure a fine-grained
repository-administration read token as the `RELEASE_SETTINGS_READ_TOKEN` Actions secret. The
publishing job uses that secret only for the fail-closed settings query; release creation uses the
job-scoped GitHub token.

The existing v0.2.0 stable release predates this hardened workflow. Preserve its tag, body, and
assets as historical records; do not rebuild, replace, or retroactively relabel them. New releases
use a draft as the candidate and publish once into their intended stable lifecycle state. If a new
release job fails after draft creation, leave the release as a draft for inspection.
