# Catalog validation record

## Independent validation gates

The stable catalog does not infer validation from release success. Version 0.2.0 carries an
independently produced report and machine-readable status that are checked against the manifest,
project-standard rubric, exact released commits, and preserved evidence. The following gates are
required:

- strict JSON parsing with duplicate-key rejection;
- complete schema, unique slugs, valid adjacency, and exact six-tool coverage;
- semantic conditioning and no-input-bearing-link checks;
- local HTML asset/link checks;
- public annotated GitHub release, exact tag-ref-to-tag-object-to-commit identity, approved tagger,
  hosted app/Core manifest, public README portfolio block, and deployed app footer agreement;
- file-by-file download and checksum verification for every staged live package, recomputed package
  and bundle digests, exact Core-wheel artifact identity, and identical staged Core bytes across all
  six scientific apps;
- deterministic Pages and release artifacts;
- Chromium and WebKit rendering, filter, keyboard, mobile, and privacy checks;
- formatting, lint, tests, and clean-diff checks;
- exact report/status inventory equality and report SHA-256 binding;
- complete, sorted, checksum-addressed evidence with all six review lanes represented, including
  strict semantic validation of the retained browser raw records and their driver hashes;
- a fail-closed scoring verdict with every original blocker explicitly closed.

Run:

```bash
uv sync --locked
uv run playwright install chromium webkit
make verify
make live-check
```

The completed cross-repository audit is recorded in
[`PORTFOLIO_VALIDATION_REPORT.md`](PORTFOLIO_VALIDATION_REPORT.md),
[`../data/validation_status.json`](../data/validation_status.json), and
[`../validation-evidence/index.json`](../validation-evidence/index.json). The status validator
rejects missing repositories, release drift, status/verdict disagreement, report digest drift,
incomplete evidence, placeholder text, rubric mismatch, or an unclosed original blocker.

The live check is a required CI and Pages build gate. A stale release, deployed source commit,
staged package, Core version, README or deployed-footer cross-link, or pinned Core release
therefore blocks deployment rather than first failing after the site is already public.
