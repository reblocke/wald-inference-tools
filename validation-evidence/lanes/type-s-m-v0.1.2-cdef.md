# Type S/M Calibrator v0.1.2 — exact-tag C/D/E/F audit

Audit date: 2026-07-30 (America/Denver)

## Verdict

- Blocking findings: **none**.
- The exact annotated tag, release, CI, Pages deployment, release assets, cold
  checkout, staged browser payload, pinned Core wheel, hosted app, responsive
  behavior, exports, privacy boundary, accessibility contract, documentation,
  and public links satisfy the audited C/D/E/F release criteria.
- The bounded nonblocking observations are recorded at the end of this ledger.

## Audited identity

- Repository: `reblocke/type-s-m-calibrator`
- Tag: `v0.1.2`
- Annotated tag object: `919ec07dd62fe726b7a71ad01ac5c48642c68064`
- Peeled commit: `fd6d384e56626c513ca5b83c92a62cbc29ecdd14`
- Tagger: Brian Locke `<reblocke@gmail.com>`, 2026-07-30T15:35:46Z
- Tag message: `Release v0.1.2`
- Tag verification: annotated and unsigned (`verified=false`,
  `reason=unsigned`)
- Exact detached audit checkout:
  `/private/tmp/cc-mig-11-typesm-final.prb1dL/repo`
- `HEAD`, `v0.1.2^{}`, all three workflow `head_sha` values, the Pages
  deployment SHA, stage-manifest `source_commit`, and release asset provenance
  all resolve to `fd6d384e56626c513ca5b83c92a62cbc29ecdd14`.
- `git status --short --untracked-files=all` was empty and `git diff --check`
  passed after all cold verification and serving checks. Generated stage files
  remained ignored.

## Cold-clone and documented-command verification

The audit used empty, audit-specific caches:

```text
UV_CACHE_DIR=/private/tmp/cc-mig-11-typesm-final.prb1dL/caches/uv
UV_PYTHON_INSTALL_DIR=/private/tmp/cc-mig-11-typesm-final.prb1dL/caches/uv-python
XDG_CACHE_HOME=/private/tmp/cc-mig-11-typesm-final.prb1dL/caches/xdg
XDG_CONFIG_HOME=/private/tmp/cc-mig-11-typesm-final.prb1dL/caches/config
PLAYWRIGHT_BROWSERS_PATH=/private/tmp/cc-mig-11-typesm-final.prb1dL/caches/playwright
npm_config_cache=/private/tmp/cc-mig-11-typesm-final.prb1dL/caches/npm
PIP_CONFIG_FILE=/dev/null
PYTHONNOUSERSITE=1
```

`PYTHONPATH`, `VIRTUAL_ENV`, `CONDA_PREFIX`, `UV_PYTHON`, and
`UV_PROJECT_ENVIRONMENT` were unset. No sibling repository or mutable local
Core checkout was available to dependency resolution.

Documented commands and results:

```text
uv sync --locked
  PASS; installed CPython 3.12.13 and 25 locked packages.
  type-s-m-calibrator 0.1.2
  wald-inference 0.4.1 from the official checksum-bound release URL
  NumPy 2.2.6; SciPy 1.14.1; Hypothesis 6.163.0
  Playwright 1.61.0; pytest 8.4.2; pytest-playwright 0.8.0; Ruff 0.16.0

uv run playwright install chromium webkit
  PASS from an initially empty browser cache.
  Chromium 149.0.7827.55; WebKit 26.5

make verify
  PASS
  Ruff format check: 31 files already formatted
  Ruff lint: pass
  Browser stage generated and validated
  Python unit/integration/property suite: 73 tests passed
  Chromium E2E: 21 passed
  WebKit smoke: 1 passed

make scientific-test
  PASS; 8 tests passed

make serve
  PASS; staged first, served on port 8000, returned HTTP 200 for `/`, and
  served the exact manifest hash below. The foreground server was then stopped.
  A final `lsof -nP -iTCP:8000 -sTCP:LISTEN` returned no listener.
```

Host/tool context: macOS 26.5.2 build 25F84, Darwin 25.5.0, arm64 Apple M2,
Git 2.50.1, uv 0.11.11, Node 25.9.0, npm 11.12.1.

## GitHub workflows, release, and deployment

Primary GitHub metadata and the connected GitHub app agreed:

- CI run `30557049466`: `completed/success`, attempt 1, push to `main`, exact
  head `fd6d384e...`; jobs `test`, `e2e-chromium`, and
  `e2e-webkit-smoke` all completed successfully, including every non-skipped
  verification step.
- Pages run `30557049604`: `completed/success`, attempt 1, exact head
  `fd6d384e...`; `build` and `deploy` both completed successfully.
- Release run `30557461421`: `completed/success`, attempt 1, tag branch
  `v0.1.2`, exact head `fd6d384e...`; `make verify`, deterministic asset
  construction, and prerelease publication all completed successfully.
- Pages deployment `5677598462`: environment `github-pages`, exact SHA
  `fd6d384e...`, final state `success`, environment URL
  `https://reblocke.github.io/type-s-m-calibrator/`.
- Pages workflow artifact `github-pages` id `8765227600`: exact head
  `fd6d384e...`, not expired at audit time, GitHub outer-artifact digest
  `sha256:b8f2f3d25a4401162e71bb5763d162c8b7ee9e3c3a721d6a8fa98df54c31df54`.
- Release: public, non-draft prerelease, published
  `2026-07-30T15:40:41Z` at
  `https://github.com/reblocke/type-s-m-calibrator/releases/tag/v0.1.2`.

## Release assets and source archive

Downloaded release assets matched GitHub `assets[].digest` and the published
checksum file:

```text
2f227e29c4a27fa27cfd897539a2dbdd2ea910cdd938e6d13f9c4066e722194f  SHA256SUMS
2d21e0f3d48ea71421c9a6ad34f54690fa4ef18d9862dcde421be9dfb3b5beae  browser-stage-manifest-v0.1.2.json
71031f28f578d43b4b88660c4de7e3baff13081de73a5df681648150870f98be  type-s-m-calibrator-v0.1.2.tar.gz
```

`shasum -a 256 -c SHA256SUMS` returned `OK` for both addressed assets.
The source archive contains exactly 57 files, equal to the 57 files from
`git ls-files`; all 57 are byte-exact, with no missing, extra, or mismatched
file. Its decompressed tar SHA-256 is:

```text
8a9de36728024d26a730eede5ddf35074370d4c4310aa4bd9977f2905f57d20a
```

## Browser stage, released Core, and Pages byte provenance

Cold-local, release-asset, and live Pages manifests are byte-identical:

```text
2d21e0f3d48ea71421c9a6ad34f54690fa4ef18d9862dcde421be9dfb3b5beae  web/assets/py/manifest.json
```

Manifest facts:

- schema: 1
- source commit: `fd6d384e56626c513ca5b83c92a62cbc29ecdd14`
- bundle SHA-256:
  `28eed989a661d757b081212f407d0773ea8ac357d03497bede2f5625d5968b40`
- app 0.1.2: 5 files; package SHA-256
  `b69098797e30caee2db822b6bb0ebcd10a7f1bee05a7349bbb89f961f9dc0549`
- Core 0.4.1: 14 files; package SHA-256
  `44c52ba0189155e0d976e283d383f17f3db0679563ec6dc6d45b9829c4a43b4d`

All five staged app files are byte-exact to `src/type_sm_calibrator`. All 14
staged `wald_inference` files are byte-exact to the official release wheel,
and every manifest file hash is exact.

The official Core wheel URL and version are pinned identically in
`pyproject.toml`, `uv.lock`, `browser-stage.toml`, documentation, and the
generated manifest. Downloaded wheel SHA-256:

```text
d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b
```

The app imports transformations, reconstruction, information scaling,
selection probability/rules, and Type S/M design metrics from
`wald_inference`; static inspection found no local SciPy distribution
formula, normal CDF/SF/PDF, `erf`, or copied Type S/M formula.

Downloaded Pages payload:

```text
832424a4d1c1bad1e61525b4b85552e8494792efa731a890ee9ff66eaab4d41c  github-pages/artifact.tar
```

Thirty deployed payload files are byte-exact to the cold local `web/` tree,
with zero content mismatches or deployed extras. The sole local-only file is
`web/.nojekyll`; this is discussed under nonblocking observations.

The live root and manifest return HTTP 200. Live byte identities:

```text
d125fd3d287d6d997042bdadba77d8344c31c742f19f763e7c7ae2ae9fa0be8b  index.html
2d21e0f3d48ea71421c9a6ad34f54690fa4ef18d9862dcde421be9dfb3b5beae  assets/py/manifest.json
```

Both are byte-exact to the cold local files; the live manifest is also
byte-exact to the release asset.

## Independent live Chromium and WebKit audit

URL: `https://reblocke.github.io/type-s-m-calibrator/`

Both engines:

- returned HTTP 200 and reached `Ready. Calculations stay in this browser.`;
- reported `type-s-m-calibrator 0.1.2 · wald-inference 0.4.1`;
- completed the four-scenario calculation with optional observed estimate;
- rendered panels A-D and the explicit “not Type M” warning;
- at 390×844 used `compact`, had no document/body horizontal overflow, and
  kept all title/panel/legend and four x-/four y-axis title boxes within the
  390-pixel viewport;
- rendered six title/panel/legend labels, four x-axis titles, and four y-axis
  titles with no peer overlap;
- preserved keyboard Tab order from effect measure to precision input;
- at viewport 850 the actual 345-pixel plot remained compact; 870 produced a
  364.8125-pixel plot and no rerender; 1200 produced a 694.8125-pixel plot and
  exactly one `noncompact` rerender; 1250 produced no redundant rerender;
  returning to 850 produced exactly one `compact` rerender;
- completed linked validation error handling for a blank null value, focused
  the alert, set `aria-invalid=true`, linked to `#null-value`, then recovered
  on corrected input and cleared `aria-invalid`;
- exported an exact eight-column CSV with 402 rows including the header and a
  populated observed-exaggeration column.

The CSV was byte-identical across engines:

```text
953f78d81eb442eb581a77481ce0a00422384ea98a96e9f1191d235441e32a82
```

Mobile-origin PNG export instrumentation in both engines established:

- the live plot remained compact;
- each export used a separate `data-plot-purpose=export` element;
- the export target was noncompact and was not the live element;
- exported plot data exactly matched live plot data;
- figure target was 1600×1200 and dashboard plot target was 1200×900;
- noncompact panel and axis annotations contained no compact `<br>` wrapping;
- title retained the disclosure that plot values above 10× are clipped but
  numeric values remain uncapped;
- temporary export elements were removed and live data/title/layout were
  unchanged after both exports.

Actual PNG files:

```text
Chromium figure:    1600x1200, 143972 bytes, sha256:b5d3571c88059b87a4dd597639ef56783f9b55e5e2e8e911341a716374b1cd3e
Chromium dashboard: 1400x1280, 183429 bytes, sha256:67c287c4ce042ddc47fa0b95d8a46ed123441780eaa405d9bc473f3663f44d6b
WebKit figure:      1600x1200, 126896 bytes, sha256:d76dd4d7ee20a43c815537fb9beb5730e7ba0e819b1c4e35290758c6c0c52049
WebKit dashboard:   1400x1280, 160830 bytes, sha256:da96059af4843829fa69b4d89d5bba73ff11aad8ce60c3a83dff404b754add3d
```

All four files had valid PNG signatures and IHDR dimensions. Chromium caption
and reviewer copy actions completed, and both copied texts contained
assumed-true-effect and nonposterior qualification.

## Privacy, accessibility, links, and public documentation

After runtime readiness, calculation, deliberate synthetic sentinel entry,
responsive resizing, validation/recovery, and all exports:

- Chromium and WebKit made zero network requests;
- the conspicuous synthetic sentinel appeared in no request URL or body;
- the page URL was unchanged;
- local storage, session storage, cookies, IndexedDB, Cache Storage, service
  workers, and WebSockets were all empty/absent;
- there were zero failed requests and zero console errors.

Chromium accessibility inspection found 22 visible enabled controls and no
unnamed control. The plot has `role=img` and a detailed text alternative;
runtime uses `role=status` and polite live updates; result summary is a polite
live region; validation summary uses `role=alert`; the skip link target
exists; the scenario table has a descriptive caption and eight scoped column
headers. The validation focus/recovery check passed in both engines.

All seven non-DOI footer destinations returned HTTP 200:

- Wald inference tools catalog
- Precision guardrail planner
- Integrated workbench
- repository
- Core v0.4.1 release
- Privacy document
- Scientific scope document

The DOI resolver returned HTTP 302 to the expected SAGE article URL. SAGE
returned HTTP 403 to command-line automation; the DOI itself is valid and
resolves.

README internal links all target existing files. The CI badge and Semantic
Versioning links returned HTTP 200.

Required public/release documents are present:

```text
README.md
LICENSE
CITATION.cff
AGENTS.md
CHANGELOG.md
docs/SCIENTIFIC_SCOPE.md
docs/VALIDATION.md
docs/PRIVACY.md
docs/DECISIONS.md
docs/MAINTENANCE.md
docs/RUNTIME_DEPENDENCIES.md
llms.txt
```

Version 0.1.2, MIT licensing, and Brian Locke authorship/maintenance are
consistent across package, citation, license, README, changelog, and tag
metadata. No `Reed` or `Brian W.` identity remained. Public copy consistently
describes forward repeated-study operating characteristics, not posterior
probabilities; disclaims exact sample-size planning, clinical validation, and
clinical guidance; and preserves the no-backend/no-storage/no-telemetry
boundary. Provenance documentation records the exact Core artifact, template
origin, runtime CDN versions/licenses, and the Gelman/Carlin method citation;
it states that no external figure, table, publisher asset, or dataset is
committed.

## Bounded nonblocking observations

1. The annotated tag is unsigned. GitHub reports `reason=unsigned`; signed
   tags are not a stated release criterion, and all immutable tag/commit,
   workflow, checksum, and byte-provenance checks pass.
2. Recompressing the byte-exact source tar with the host macOS `gzip -n`
   produces a different compressed hash because the platform compressor emits
   a different deflate stream. The published compressed asset matches both
   GitHub’s digest and `SHA256SUMS`, while the decompressed tar hash and all 57
   tracked file bytes are exact.
3. GitHub Pages upload omitted the one-byte tracked `web/.nojekyll`; live
   `/.nojekyll` returns 404. The Actions Pages pipeline deploys the already
   built static payload, and all 30 functional deployed files are byte-exact;
   root, modules, manifest, Python payload, and app behavior are unaffected.
4. WebKit reported one `ResizeObserver loop completed with undelivered
   notifications.` page diagnostic during deliberate rapid breakpoint
   changes. There were no console errors, request failures, state loss, or
   functional failures, and the entire WebKit mobile/breakpoint/export,
   validation, privacy, and storage audit passed.
