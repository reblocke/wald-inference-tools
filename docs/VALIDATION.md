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
Its normal mode accepts any internally coherent CC-MIG-11 verdict so failed audits remain
recordable. The release workflow adds `--require-releasable`, which permits validated and
conditionally validated portfolios but rejects a verdict that still reports release blockers.

The live check is a required CI and Pages build gate. A stale release, deployed source commit,
staged package, Core version, README or deployed-footer cross-link, or pinned Core release
therefore blocks deployment rather than first failing after the site is already public.

## Repository-policy verification

Governance regression tests additionally require the exact branch-check names, full-SHA Action
pins and retained major families, least-privilege permissions, disabled checkout credential
persistence, release cache isolation, seven-day Dependabot cooldowns, private vulnerability
reporting, catalog-specific contribution boundaries, and the complete fail-closed release
sequence.

For workflow or release-policy changes, run:

```bash
uv sync --locked
uv run playwright install chromium webkit
make verify
make live-check
uvx --from zizmor==1.28.0 zizmor --pedantic --strict-collection .
git diff --check
git status --short
```

The release policy tests enforce annotated remote-tag binding, exact event binding,
protected-`main` containment before project code, current-version changelog extraction, the exact
eight-asset catalog/evidence inventory, a release-only releasable-verdict guard, checksummed GitHub
CLI installation, immutable draft-first stable publication, exact body and asset redownload, and
post-publication verification. These checks establish repository and release integrity; they do
not alter the validation verdict, expand any scientific claim, or replace independent evidence
review.
