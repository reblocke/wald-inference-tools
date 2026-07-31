# Runtime Dependencies and Provenance

## Browser runtime

The published catalog has no third-party browser runtime. It loads only checked-in same-origin
HTML, CSS, JavaScript, and `data/tools.json`. It does not load Pyodide, scientific Python, a CDN
script, analytics, telemetry, storage, or an app runtime. Following an app or repository link is
an explicit user navigation, not a background request.

## Development dependencies

`uv.lock` controls local and CI resolution. Ruff formats and lints; pytest supplies the test
runner; Playwright and pytest-playwright drive Chromium and WebKit. These dependencies are
development-only and are absent from the built static site and catalog release metadata.

## Repository automation

Every third-party GitHub Action is pinned in `.github/workflows/` to a reviewed full commit SHA
with its exact version in a comment. The established action major families are retained: checkout
7, setup-python 7, setup-uv 9, upload-artifact 7, configure-pages 6, upload-pages-artifact 5, and
deploy-pages 5. The split release handoff adds download-artifact 8. Their upstream repositories
report MIT licensing; source repository and content-addressed revision are machine-readable in the
workflow files.

Credentialed release steps install GitHub CLI 2.93.0 from:

```text
https://github.com/cli/cli/releases/download/v2.93.0/gh_2.93.0_linux_amd64.tar.gz
```

The required SHA-256 is
`02d1290eba130e0b896f3709ffff22e1c75a51475ddb70476a85abc6b5807af0`.
GitHub CLI is MIT licensed. The version, upstream checksum manifest, action tags/commits, and
upstream repository licenses were reviewed on 2026-07-30.

Dependabot applies a seven-day eligibility cooldown and proposes grouped weekly `uv` and Actions
updates for review without automatic merging. Workflow static analysis for this governance change
uses MIT-licensed zizmor 1.28.0 in online, pedantic, strict mode. Neither tool is part of the
published site or scientific evidence chain.

## Licensing boundary

Repository-authored code, documentation, tests, and synthetic fixtures are MIT licensed.
Dependencies and publications retain their own licenses. No external code, publisher figure,
table, dataset, or substantial publication text is copied into the repository.
