# CC-MIG-11 compatibility-curve v0.1.2 final Lane C/D/E/F audit

Audit completed: 2026-07-30T15:29:43Z
Repository: `reblocke/compatibility-curve`
Release: `v0.1.2` (published GitHub prerelease)
Fresh isolated audit root: `/private/tmp/cc-compat-v012-isolated.XBtDyE`
Artifact/Pages audit root: `/private/tmp/cc-compat-v012-audit.7IVMCU`
Production or GitHub mutations by auditor: none

## Decision

**GO for compatibility-curve v0.1.2 in Lanes C, D, and F. Lane E's exact-tag
Chromium/WebKit, mobile, accessibility, privacy, storage, and network gates pass; the only
remaining Lane E qualification is a nonblocking limitation in direct live-browser evidence.**

No compatibility-curve release blocker was found.

The live site is byte-traceable to the same commit, source, JavaScript, CSS, worker, focused
package, Core package, and released stage manifest that passed the isolated test suite. A second
reviewer opened the live site at 390 x 844 and observed runtime identity
`compatibility-curve 0.1.2` / `wald-inference 0.4.1`. That in-app browser runtime did not complete
the subsequent Plotly render and its screenshot operation failed, so this ledger does **not**
claim a completed direct-live visual render. The exact-tag isolated Chromium test did complete
the full workflow for all nine effect measures and required every rendered Plotly title bounding
box to remain within both the plot and the 390 px viewport. Because the complete hosted file set
was independently matched to that test candidate, the live-tool limitation is evidence coverage,
not evidence of an application defect.

## Exact identity

| Item | Value |
|---|---|
| annotated tag | `v0.1.2` |
| tag object | `1639c9342fbadfe33d3227e05348406ac85854b4` |
| peeled commit | `64c6264b9ac93d6665d12c30fa5f4290dd571421` |
| current `main` | `64c6264b9ac93d6665d12c30fa5f4290dd571421` |
| tagger | Brian Locke `<reblocke@gmail.com>` |
| tag date | `2026-07-30T15:03:26Z` |
| release workflow | run `30554788707`, success |
| release workflow head | `64c6264b9ac93d6665d12c30fa5f4290dd571421` |
| release publication | `2026-07-30T15:09:02Z` |
| Pages workflow | run `30554486218`, success |
| Pages deployment | `5677091093`, success |
| Pages deployment SHA | `64c6264b9ac93d6665d12c30fa5f4290dd571421` |
| live URL | `https://reblocke.github.io/compatibility-curve/` |
| live manifest source commit | `64c6264b9ac93d6665d12c30fa5f4290dd571421` |

`git cat-file -t refs/tags/v0.1.2` returned `tag`; both local Git and the GitHub Git-data API
resolved the annotated tag object to the expected commit. `git ls-remote` showed the same commit
for `main` and the peeled tag.

## Environment and isolation

- Host: macOS 26.5.2 build 25F84, Darwin 25.5.0, Apple arm64.
- Git: 2.50.1 (Apple Git-155).
- uv: 0.11.11.
- Project interpreter: independently downloaded CPython 3.12.13.
- compatibility-curve: 0.1.2.
- wald-inference: 0.4.1.
- NumPy: 2.2.6.
- SciPy: 1.14.1.
- pytest: 8.4.2.
- pytest-playwright: 0.8.0.
- Playwright Python package: 1.61.0.
- Chromium: Chrome for Testing 149.0.7827.55, Playwright build 1228.
- WebKit: 26.5, Playwright build 2311.
- Ruff: 0.16.0.

The canonical clone used:

```text
git clone --branch v0.1.2 --single-branch \
  https://github.com/reblocke/compatibility-curve.git repository
```

It was run in a new parent. The verification commands unset `CONDA_PREFIX`, `VIRTUAL_ENV`,
`PYTHONPATH`, `UV_PYTHON`, and `UV_PROJECT_ENVIRONMENT`; used `/dev/null` for
`PIP_CONFIG_FILE`; set `PYTHONNOUSERSITE=1`; and assigned initially absent, audit-local paths for
`UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`,
`PLAYWRIGHT_BROWSERS_PATH`, and the npm cache. The run downloaded its own Python, Python
dependencies, Chromium, FFmpeg, and WebKit. It therefore did not depend on a sibling checkout,
global Python package, or pre-existing dependency/browser cache.

## Lane C — cold-start reproducibility

Results from the isolated tag clone:

| Command | Exit | Result |
|---|---:|---|
| `uv sync --locked` | 0 | 26 packages resolved; app 0.1.2 and released Core 0.4.1 installed |
| `uv run playwright install chromium webkit` | 0 | fresh Chromium 149.0.7827.55 and WebKit 26.5 downloads |
| `make verify` | 0 | Ruff format/lint, 56 non-E2E, 7 Chromium, and 1 WebKit test passed |
| `uv run pytest -q tests/regression/test_legacy_compatibility.py` | 0 | 11 focused B01-B03/B08 regressions passed |
| `make serve` | 1 after intentional Ctrl-C | server started; `/`, manifest, and worker each returned HTTP 200 before shutdown |
| `git diff --check` | 0 | no whitespace errors |
| `git status --short` | 0 | no tracked or untracked source changes |
| `git diff --exit-code` / cached equivalent | 0 | no tracked differences |
| `uv tree` | 0 | exact dependency tree resolved without sibling sources |

The served index, manifest, and worker matched the tag-generated files exactly:

```text
17b66960b68730644bc3058e5930abdcbda76eab4f44d027558f3d223f3a7ee5  index.html
90d920b9719424e4042d2ea24d477645407000cf731eb4350f32e8c12e8ac666  manifest.json
69c576f4a170525411343e1a3b193d6121e6829b6219ba9ec1ffeb9895bd409c  pyodide_worker.js
```

The checkout remained detached at `v0.1.2` / `64c6264b...`; generated `.venv`, cache, test-result,
egg-info, and `web/assets/py` paths were ignored and no generated Python was tracked.

## Lane D — release and deployment provenance

### Published assets

GitHub's release API and independent local hashing agreed:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 201 | `8903fa2c958d2214376e7fb83329756ac49d7b500c11f6aef528c7fc8121b737` |
| `browser-stage-manifest-v0.1.2.json` | 4,547 | `90d920b9719424e4042d2ea24d477645407000cf731eb4350f32e8c12e8ac666` |
| `compatibility-curve-v0.1.2.tar.gz` | 88,269 | `51883a0877ff8ee0a694916e25787824a6ad5310095b469a310ce08b8c2f6beb` |

`shasum -a 256 -c SHA256SUMS` passed for the manifest and source archive. GitHub's recorded
per-asset digests matched the downloaded bytes.

The uploaded source archive contained 54 regular files and 21 directories, with one safe
`compatibility-curve-v0.1.2/` prefix, no links/devices, no traversal path, and no generated
environment or staged-browser files. Its uncompressed tar stream was byte-identical to a fresh
`git archive` of `v0.1.2`:

```text
06a0434b614db308769cd389194af98c37a2809fdad68fab4dd334af5170d0d2
```

The extracted file tree matched the tagged tree. GitHub's automatic source tarball also extracted
to the same file tree.

Cross-platform recompression with local macOS `gzip -n` produced different compressed bytes while
decompressing to the identical tar stream. This is a compressor/platform portability observation,
not an integrity failure: the authoritative published compressed asset is checksum-addressed and
verified.

### Core and browser stage

The exact Core artifact downloaded from the manifest URL passed ZIP integrity and hashed to:

```text
d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b
```

The same URL, version, and digest appear in `pyproject.toml`, `uv.lock`,
`browser-stage.toml`, `docs/RUNTIME_DEPENDENCIES.md`, and the released/live manifest. The Core
v0.4.1 annotated tag peeled to documented commit
`f4613177b6dc81d194aa70762152de2bfa86663b`.

The release, isolated clone, Pages artifact, and live site produced identical manifest bytes.
All 19 staged files passed declared byte count and SHA-256 checks. The independently recomputed
package and aggregate hashes were:

```text
compatibility-curve 0.1.2, 5 files:
  fd689298e085903a4382a04c7eb9dec6548f8f12be66b65fd581ea36e3de9667
wald-inference 0.4.1, 14 files:
  44c52ba0189155e0d976e283d383f17f3db0679563ec6dc6d45b9829c4a43b4d
bundle:
  3215dfe4f24d30eac18591aad95873c1ec9084cc1da4636fb30b721dbca6ae17
```

The staging verifier also checked the lock, installed direct URL, Core wheel `RECORD`, and every
copied external file before construction.

### Pages traceability

Pages run `30554486218` staged and tested commit `64c6264b...`, uploaded Actions artifact
`8764176359`, and successfully deployed the same SHA. The GitHub artifact digest was:

```text
4e175e98a4121b47d8bf0946ef6aac076e91aaa35e4846827a5ed6c9b0df80f0
```

The downloaded inner `artifact.tar` SHA-256 was
`814bfd2855e4043e4afe09c1a777d21b6628bf40309442f397034ae2ed35dd63`.
It contained 30 regular files and six directories with no unsafe or non-regular member, and
matched the generated `web/` tree exactly except for `.nojekyll`.

That exception is expected for `actions/upload-pages-artifact@v4`: the official action explicitly
excludes `.[^/]*`, so the tracked source marker is neither in the deployment artifact nor directly
served (`/.nojekyll` returns 404). This deployment uses the Pages artifact API, not a Jekyll
source build. The omission does not alter the served site and is nonblocking.

Independent HTTP comparisons found:

- all 10 served tracked non-dot web files byte-equal to the tag;
- all 19 live staged Python files HTTP 200 with exact declared size/hash;
- live `index.html`, `js/renderers.js`, and manifest hashes equal the tag/release;
- live manifest source commit `64c6264b...`, app 0.1.2, and Core 0.4.1;
- GitHub Pages configured public, workflow-built, and HTTPS-enforced.

## Lane E — browser, accessibility, privacy, and links

The isolated Chromium suite completed these release gates:

- initial worker/Pyodide load and end-to-end calculation;
- additive and ratio workflows;
- linked, focusable validation error plus worker recovery;
- presentation-only display-range invariance;
- exact CSV, dashboard PNG, manuscript PNG, and caption-copy exports;
- textual/table alternatives and plot-description/accessibility hooks;
- 390 x 844 keyboard workflow and document containment;
- all nine effect measures selected and calculated at 390 px;
- a nonempty rendered `.gtitle` for each measure;
- every title bounding box inside the plot and viewport;
- URL unchanged after a distinctive numeric input;
- local storage, session storage, IndexedDB, and cookie state all empty;
- distinctive input absent from every captured request URL/body.

The WebKit worker/calculation smoke passed separately.

Static production-code review found no backend, persistence, telemetry, analytics, cookies,
input-bearing URL state, upload, WebSocket, EventSource, or application input logging. The only
production `fetch` calls retrieve the same-origin manifest and checksum-addressed staged Python
files. Inputs pass to the same-origin worker through `postMessage` and do not form request URLs or
bodies. External runtime requests are fixed versioned assets:

- Plotly `https://cdn.plot.ly/plotly-3.1.0.min.js` — HTTP 200;
- Pyodide `https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js` — HTTP 200.

All six exact related-tool links in the live/tagged HTML and README returned HTTP 200:

1. Wald inference tools catalog;
2. Wald likelihood support;
3. integrated workbench;
4. compatibility source repository;
5. Core v0.4.1 release;
6. compatibility privacy note.

### Direct-live qualification

The auditing child had no available connected Browser runtime after required discovery and
bootstrap troubleshooting. A second reviewer connected to the live site and confirmed the exact
runtime versions at 390 x 844, but its in-app browser remained in an intermediate
`Calculating...` frame after the update action and its screenshot call failed. No completed live
render or live all-nine-effect bounding-box result is claimed from that tool.

This is retained as a **nonblocking validation limitation** because the completed isolated
Chromium/WebKit checks ran against the exact source and stage bytes independently proven to be
deployed. It should not be rewritten as a live-render pass, and the intermediate tool frame
should not be treated as an application failure.

## Lane F — documentation, rights, citation, and maintenance

All required repository documents were present:

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
llms.txt
```

Findings:

- README setup, verification, focused baseline, staging, and serve commands were exercised.
- README, CFF, package metadata, HTML/footer, source package, stage config, lock, and changelog
  consistently identify app version 0.1.2.
- README, runtime provenance, lock, stage config, tests, UI, and manifest consistently identify
  Core 0.4.1 and its release checksum.
- Author/maintainer/copyright identity is consistently Brian Locke.
- `CITATION.cff` records Brian Locke, MIT, version 0.1.2, release date 2026-07-30, repository, and
  hosted URL.
- GitHub detects MIT; the tagged `LICENSE` is the MIT text with Brian Locke's copyright.
- Scientific scope and UI explicitly limit the app to reconstructed Wald compatibility and
  exclude profile likelihood, power, critical effects, Type S/M, precision, binary significance,
  threshold validation, posterior interpretation, and clinical decision support.
- Privacy, dependency provenance, decisions, validation, maintenance, changelog, and release
  process are documented.
- Core, template, and frozen-baseline tag/commit references independently resolve to the
  documented commits.
- No committed PNG/JPEG/GIF/SVG/PDF/Office/data artifact or copied third-party figure was found.
  External Plotly/Pyodide/Core licensing and provenance routes are documented; the app's own code
  is MIT.

No rights, citation, author, maintenance, public-copy, clinical-scope, or command-documentation
blocker was found.

## Exact principal commands

The canonical isolated environment prefix described above was applied to every `uv`, Playwright,
and `make` command:

```text
git clone --branch v0.1.2 --single-branch \
  https://github.com/reblocke/compatibility-curve.git repository
git cat-file -t refs/tags/v0.1.2
git rev-parse refs/tags/v0.1.2^{}
uv sync --locked
uv run playwright install chromium webkit
make verify
uv run pytest -q tests/regression/test_legacy_compatibility.py
make serve
curl -fsS http://127.0.0.1:8000/
curl -fsS http://127.0.0.1:8000/assets/py/manifest.json
curl -fsS http://127.0.0.1:8000/pyodide_worker.js
git diff --check
git status --short
git diff --exit-code
uv tree

gh run view 30554788707 --repo reblocke/compatibility-curve
gh release view v0.1.2 --repo reblocke/compatibility-curve
gh release download v0.1.2 --repo reblocke/compatibility-curve
shasum -a 256 -c SHA256SUMS
git archive --format=tar --prefix=compatibility-curve-v0.1.2/ v0.1.2
gh run view 30554486218 --repo reblocke/compatibility-curve
gh run download 30554486218 --repo reblocke/compatibility-curve \
  --name github-pages
gh api repos/reblocke/compatibility-curve/pages
gh api repos/reblocke/compatibility-curve/deployments
curl -fsSL https://reblocke.github.io/compatibility-curve/
curl -fsSL https://reblocke.github.io/compatibility-curve/assets/py/manifest.json
```

All principal read-only verification commands exited 0 except the bounded `make serve`, which was
intentionally interrupted after three HTTP 200 responses, and the explicit `/.nojekyll` probe,
which returned its documented HTTP 404 observation.

## Residual nonblocking limitations

1. No completed direct-live all-nine-effect plot render was obtained from the available in-app
   browser runtime; exact-tag tests plus byte-exact deployment provenance are the completed
   evidence.
2. `gzip -n` source-archive compressed bytes vary across the Linux release runner and macOS audit
   host, while the decompressed tar stream and extracted tree are identical.
3. `actions/upload-pages-artifact@v4` excludes the tracked `.nojekyll` marker; the artifact-based
   deployment does not invoke a Jekyll source build, and the served site is unaffected.
