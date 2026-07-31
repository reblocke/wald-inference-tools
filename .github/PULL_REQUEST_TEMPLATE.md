## Scope

Describe the catalog engineering, metadata, validation-evidence, documentation, governance, or
maintenance problem addressed. Identify the authoritative Core or app repository when this catalog
does not own the requested behavior.

## Risk and release impact

Describe silent-failure risks, conditioning or validation-status implications, privacy and
accessibility effects, public metadata/deployment impact, and whether the change requires a new
release or independent validation review.

## Verification

List the exact commands run and their outcomes. Include skipped checks, warnings, unavailable
public sources, and the exact commit reviewed.

## Checklist

- [ ] No Wald formula, scientific calculation, Pyodide runtime, or app-specific behavior was
      copied into this catalog.
- [ ] `data/tools.json` remains the source of truth; card markup does not duplicate manifest
      versions, URLs, or validation status.
- [ ] Observed-estimate reconstruction remains distinct from assumed-truth design calibration.
- [ ] Validation labels, report/status data, evidence hashes, and release metadata are supported by
      the exact preserved evidence and were not inferred from successful automation.
- [ ] App/Core versions, annotated tags, peeled commits, deployed source commits, hosted manifests,
      public README blocks, and deployed footers agree where metadata changed.
- [ ] Public copy stays within validated functionality and does not imply clinical or regulatory
      readiness.
- [ ] Examples and fixtures are public or synthetic and contain no credentials, sensitive data, or
      protected health information.
- [ ] No backend, telemetry, persistence, cookies, storage, service worker, upload, third-party
      browser request, or input-bearing URL was added.
- [ ] Every third-party GitHub Action remains pinned to a reviewed full commit SHA with a version
      comment.
- [ ] `uv sync --locked`, `make verify`, and `make live-check` pass.
- [ ] README, validation, privacy, maintenance, runtime dependencies, decisions, citation, and
      changelog were reviewed for synchronization.
