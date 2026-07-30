# Catalog validation record

## Release-candidate gates

The initial catalog is not the portfolio's independent scientific validation report. Before the
catalog release, the following mechanical gates are required:

- strict JSON parsing with duplicate-key rejection;
- complete schema, unique slugs, valid adjacency, and exact six-tool coverage;
- semantic conditioning and no-input-bearing-link checks;
- local HTML asset/link checks;
- public GitHub release, hosted URL, and hosted app/Core manifest agreement;
- deterministic Pages and release artifacts;
- Chromium and WebKit rendering, filter, keyboard, mobile, and privacy checks;
- formatting, lint, tests, and clean-diff checks.

Run:

```bash
uv sync --locked
uv run playwright install chromium webkit
make verify
make live-check
```

The independent cross-repository audit will write `docs/PORTFOLIO_VALIDATION_REPORT.md` and
`data/validation_status.json`. Until that audit is complete, a `release-candidate` label means only
that the implementation is awaiting the portfolio-wide verdict.
