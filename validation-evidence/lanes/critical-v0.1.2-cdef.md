# CC-MIG-11 critical-effect-size v0.1.2 final Lane C/D/E/F audit

Audit completed: 2026-07-30T15:52:41Z
Repository: `reblocke/critical-effect-size`
Release: `v0.1.2` (published GitHub prerelease)
Fresh isolated audit root: `/private/tmp/cc-critical-v012-isolated.j8Q3jA`
Artifact/Pages audit root: `/private/tmp/cc-critical-v012-audit.zlS5S0`
Production or GitHub mutations by auditor: none

## Decision

**GO for critical-effect-size v0.1.2 in Lanes C, D, and F. Lane E's exact-tag
Chromium/WebKit, responsive-label, export, accessibility, privacy, storage, network, and link gates
pass; the only remaining Lane E qualification is a nonblocking limitation in completed
direct-live Plotly evidence.**

No critical-effect-size release blocker was found.

The live site is byte-traceable to the same commit, JavaScript, CSS, worker, focused app package,
released Core package, and stage manifest that passed the isolated suite. A second reviewer opened
the live site at 390 x 844, confirmed runtime identity `critical-effect-size 0.1.2` /
`wald-inference 0.4.1`, completed the default calculation, and observed the exact numeric/text/table
results. The in-app browser then remained in Plotly's intermediate `Calculating…` frame with a
default 700 px SVG, leaving exports disabled; completed live geometry and a screenshot therefore
are not claimed. The exact-tag isolated Chromium suite completed the responsive geometry,
breakpoint, and mobile-origin high-resolution export checks against bytes independently proven to
be deployed. The in-app browser limitation is evidence coverage, not evidence of an application
defect.

## Exact identity

| Item | Value |
|---|---|
| annotated tag | `v0.1.2` |
| tag object | `fee04866ddb0b8d39575e8d0e958a219dbe7cb52` |
| peeled commit | `73bc391adff6cf2f08fba28baa67014c043b9cb0` |
| current `main` | `73bc391adff6cf2f08fba28baa67014c043b9cb0` |
| tagger | Brian Locke `<reblocke@gmail.com>` |
| tag date | `2026-07-30T15:35:17Z` |
| main CI | run `30556974365`, success |
| release workflow | run `30557419967`, success |
| release workflow head | `73bc391adff6cf2f08fba28baa67014c043b9cb0` |
| release publication | `2026-07-30T15:38:50Z` |
| Pages workflow | run `30556974295`, success |
| Pages deployment | `5677585824`, success |
| Pages deployment SHA | `73bc391adff6cf2f08fba28baa67014c043b9cb0` |
| live URL | `https://reblocke.github.io/critical-effect-size/` |
| live manifest source commit | `73bc391adff6cf2f08fba28baa67014c043b9cb0` |

`git cat-file -t refs/tags/v0.1.2` returned `tag`; `git ls-remote` independently showed the
annotated object, peeled tag, and `main` at the values above. GitHub reported the release as
published, non-draft, and intentionally prerelease.

Main CI run `30556974365` completed its non-browser test, Chromium E2E, and WebKit smoke jobs
successfully at the exact commit. Pages run `30556974295` built and tested that commit before
deploying it. Release run `30557419967` reran the complete verification gate, built the artifacts,
and published them from the same commit.

## Environment and isolation

- Host: macOS 26.5.2 build 25F84, Darwin 25.5.0, Apple arm64.
- Git: 2.50.1 (Apple Git-155).
- uv: 0.11.11.
- Project interpreter: independently downloaded CPython 3.12.13.
- critical-effect-size: 0.1.2.
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
  https://github.com/reblocke/critical-effect-size.git repository
```

It was run in a new parent. Verification unset `CONDA_PREFIX`, `VIRTUAL_ENV`, `PYTHONPATH`,
`UV_PYTHON`, and `UV_PROJECT_ENVIRONMENT`; used `/dev/null` for `PIP_CONFIG_FILE`; set
`PYTHONNOUSERSITE=1`; and assigned initially absent, audit-local paths for `UV_CACHE_DIR`,
`UV_PYTHON_INSTALL_DIR`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, `PLAYWRIGHT_BROWSERS_PATH`, and
the npm cache. The run downloaded its own Python, Python dependencies, Chromium, FFmpeg, and
WebKit. It did not depend on a sibling checkout, global Python package, or pre-existing
dependency/browser cache.

`uv tree` resolved the app directly to released `wald-inference` 0.4.1, NumPy 2.2.6, and SciPy
1.14.1. The installed Core distribution's `direct_url.json` identified the exact release URL and
checksum, not a sibling or editable source.

## Lane C — cold-start reproducibility

Results from the isolated tag clone:

| Command | Exit | Result |
|---|---:|---|
| `uv sync --locked` | 0 | 26 packages resolved; app 0.1.2 and released Core 0.4.1 installed |
| `uv run playwright install chromium webkit` | 0 | fresh Chromium 149.0.7827.55 and WebKit 26.5 downloads |
| `make verify` | 0 | Ruff format/lint, 59 non-E2E, 12 Chromium, and 1 WebKit test passed |
| `uv run pytest -q tests/regression/ tests/scientific_reference/` | 0 | 13 focused regression/scientific-reference tests passed |
| `uv run python scripts/stage_browser_packages.py` | 0 | deterministic app/Core bundle regenerated |
| `make serve` | 1 after intentional Ctrl-C | server started; `/`, manifest, and worker each returned HTTP 200 before shutdown |
| `git diff --check` | 0 | no whitespace errors |
| `git status --short` | 0 | no tracked or untracked source changes |
| `git diff --exit-code` / cached equivalent | 0 | no tracked differences |
| `uv tree` | 0 | exact dependency tree resolved without sibling sources |

The served index, manifest, and worker matched the tag-generated files exactly:

```text
5f5c4b8d4a8431f7aec056046710e0fcfe2be19f5f4d5b02a7f7463ac3fe9ccf  index.html
233e42b64c7b98e0bf2446040bd5ba8c13475ef766fb84d7e07af319a426e734  manifest.json
69c576f4a170525411343e1a3b193d6121e6829b6219ba9ec1ffeb9895bd409c  pyodide_worker.js
```

The checkout remained detached at `v0.1.2` / `73bc391a...`; generated `.venv`, cache,
test-result, egg-info, and `web/assets/py` paths were ignored. No generated browser Python was
tracked.

## Lane D — release and deployment provenance

### Published assets

GitHub's release API, the downloaded `SHA256SUMS`, and independent local hashing agreed:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 202 | `a6ae4b3dc726493745290ec8ccd6955e67150cf5f883db50e11c70d8fe6c12bf` |
| `browser-stage-manifest-v0.1.2.json` | 4,554 | `233e42b64c7b98e0bf2446040bd5ba8c13475ef766fb84d7e07af319a426e734` |
| `critical-effect-size-v0.1.2.tar.gz` | 92,818 | `d43585d79cac8c631478d5a0261f41368ff965f066bf6cbf4e2e57e5e17f2b1c` |

`shasum -a 256 -c SHA256SUMS` passed for the manifest and source archive. GitHub's recorded
per-asset digests matched the downloaded bytes.

The uploaded source archive contained 57 regular files and 24 directories, with one safe
`critical-effect-size-v0.1.2/` prefix, no links/devices, no traversal path, and no generated
environment or staged-browser files. Its uncompressed tar stream was byte-identical to a fresh
`git archive` of `v0.1.2`:

```text
8f711ac46f459891392644ee7357de79d3f60529df4488b898547214814c70ce
```

The extracted file tree matched the tagged tree. GitHub's automatic source archive also extracted
to the same file tree.

Cross-platform recompression with local macOS `gzip -n` produced compressed SHA-256
`72e497465ab1a21c8a3b5171aade2ddd2702304c1695b15df40e85ab3039bd29`, different from the Linux
release asset while decompressing to the identical tar stream. This is a compressor/platform
portability observation, not an integrity failure: the authoritative published compressed asset
is checksum-addressed and verified.

### Core and browser stage

The exact Core artifact downloaded afresh from the manifest URL passed ZIP integrity and hashed
to:

```text
d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b
```

The same URL, version, and digest appear in `pyproject.toml`, `uv.lock`,
`browser-stage.toml`, `docs/RUNTIME_DEPENDENCIES.md`, and the released/live manifest. Core
v0.4.1's annotated tag object `838c4aaab08570a17156bd59b1ff65dcabf56bfc` independently peeled
to documented commit `f4613177b6dc81d194aa70762152de2bfa86663b`. Core release run
`30545293704` and main CI run `30545147370` were successful at that commit.

The release, isolated clone, Pages artifact, and live site have identical manifest bytes. All 19
staged files passed declared byte-count and SHA-256 checks. Independently recomputed package and
aggregate hashes were:

```text
critical-effect-size 0.1.2, 5 files:
  8abaaf5d66e57b7f8249d3d779714e6c170a6622704fa56893f7e56fce96c40a
wald-inference 0.4.1, 14 files:
  44c52ba0189155e0d976e283d383f17f3db0679563ec6dc6d45b9829c4a43b4d
bundle:
  bd5eb3d202962b4a2f31d50eb32d6214687dc94cfd6b72fc38a9cf7fa81580c5
```

The staging verifier also checked the lock, installed direct URL, Core wheel `RECORD`, and every
copied external file before construction.

### Pages traceability

Pages run `30556974295` staged and tested commit `73bc391a...`, uploaded Actions artifact
`8765203893`, and successfully deployed the same SHA. GitHub recorded this outer artifact digest:

```text
318a51ebbe085d05fbfa48179270add5c50ccaa7128703850adfa38fc4258d0c
```

The downloaded inner `artifact.tar` SHA-256 was:

```text
bab2c0ac173778c5e7d0703158773258548f41bba324cb2344f65816277fb8d2
```

It contained 30 regular files and six directories with no unsafe or non-regular member, and
matched the generated `web/` tree exactly except for `.nojekyll`.

That exception is expected for `actions/upload-pages-artifact@v4`: the action log shows its
dotfile exclusion, so the tracked source marker is neither in the deployment artifact nor directly
served. This deployment uses the Pages artifact API rather than a Jekyll source build. The omission
does not alter the served site and is nonblocking.

Independent live HTTP comparisons found:

- all 10 served tracked non-dot web files byte-equal to the tag (70,254 bytes total);
- all 19 live staged Python files HTTP 200 with exact declared size/hash;
- live manifest SHA-256
  `233e42b64c7b98e0bf2446040bd5ba8c13475ef766fb84d7e07af319a426e734`;
- live `index.html` SHA-256
  `5f5c4b8d4a8431f7aec056046710e0fcfe2be19f5f4d5b02a7f7463ac3fe9ccf`;
- live `js/renderers.js` SHA-256
  `0d9c155137a0710592c68ced378bc1d4c04106690333c8550ca8c3f9417876ae`;
- live `js/exports.js` SHA-256
  `b6fc056d5ad458aa17ae5e4020fc16ac475275e5f4bf966a22a750ae292e5556`;
- live manifest source commit `73bc391a...`, app 0.1.2, and Core 0.4.1;
- GitHub Pages configured public, workflow-built, and HTTPS-enforced.

## Lane E — browser, responsive rendering, exports, accessibility, privacy, and links

### Exact-tag Chromium and WebKit

The isolated full Chromium suite completed these release gates:

- initial worker/Pyodide load, exact default calculation, and runtime version assertions;
- reported-CI and direct-SE inputs, additive and ratio effects, information scenarios, and
  directional one-sided behavior;
- sanitized validation failures, linked/focusable input errors, stale-result clearing, and worker
  recovery;
- display-range omission warnings without changing scientific results;
- exact four-column CSV with more than 300 data rows;
- 1600 x 1200 figure PNG, 1400 x 1200 dashboard PNG, and caption export;
- a 390 x 844 keyboard workflow and document containment;
- 390 px Plotly title, legend, annotation, axis-label, and tick-label containment/non-overlap;
- compact live rendering with zero direct `.textpoint` labels and readable legend/annotations;
- post-render width-category behavior: 850 px compact, 870 px stable without a redundant rebuild,
  1200 px noncompact with direct point labels, 1250 px stable, and 850 px compact again;
- mobile-origin high-resolution exports rendered through temporary noncompact plot state with
  direct marker labels and the unwrapped selected-claim-probability title;
- cleanup of temporary export nodes while the live mobile plot remained compact.

The mobile-origin export assertions observed figure output at 1600 x 1200 and dashboard output at
1400 x 1200, with a temporary 1200 x 820 noncompact plot for the dashboard composition. Export
snapshots required marker-plus-text traces, `Reported 95% CI` and `Observed estimate` annotations,
and export—not live—render mode.

The separate WebKit worker/calculation smoke passed.

### Privacy, network, storage, and accessibility

The mobile privacy test used distinctive input `1.234567891` and confirmed:

- the URL did not change after calculation/recalculation;
- local storage, session storage, cookies, and IndexedDB were empty;
- the sentinel was absent from every captured request URL and request body;
- inputs and outputs remained contained within the document/worker workflow.

Static production-code review found no backend, persistence, telemetry, analytics, cookies,
input-bearing URL state, upload, WebSocket, EventSource, or application input logging. The only
production `fetch` calls retrieve the same-origin manifest and checksum-addressed staged Python
files. Inputs pass to the same-origin worker with `postMessage` and do not form request URLs or
bodies. External runtime requests are fixed versioned assets:

- Plotly `https://cdn.plot.ly/plotly-3.1.0.min.js` — HTTP 200;
- Pyodide `https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js` — HTTP 200.

Accessibility contracts passed for labeled controls, `aria-live`, alert semantics, linked and
focusable errors, skip navigation, visible focus, keyboard flow, details/summary disclosure,
reference-table and figure-caption text alternatives, stale-state handling, and responsive
containment. This is automated keyboard/DOM/rendered-geometry evidence, not a claim of an
exhaustive manual screen-reader or WCAG conformance audit.

All first-party navigation and documentation links checked returned HTTP 200:

1. live critical-effect-size app;
2. Wald inference tools catalog;
3. Precision guardrail planner;
4. Integrated workbench;
5. critical-effect-size repository;
6. Core v0.4.1 release;
7. critical-effect-size privacy note;
8. critical-effect-size scientific-scope note.

The external methodology link is safely marked `target="_blank"` with
`rel="noopener noreferrer"`. SAGE's DOI page returned HTTP 403 to automated `curl` retrieval.
Crossref nevertheless resolved DOI `10.1177/25152459251335298` with status `ok`, exact title
*The Benefits of Reporting Critical-Effect-Size Values*, publisher SAGE Publications, and 2025
publication metadata. The automated publisher-page restriction is retained as a nonblocking link
audit limitation, not silently reported as HTTP 200.

### Direct-live qualification

A second reviewer used the connected in-app browser against the live deployment at 390 x 844.
Observed evidence:

- runtime identity `critical-effect-size 0.1.2 · wald-inference 0.4.1`;
- initial document and viewport widths 390 / 390;
- one unambiguous Calculate action produced completed numeric/text/table results;
- default target-80% critical odds ratios were `0.6408734` and `1.560371`;
- the plot carried `data-compact="true"` with zero `.textpoint` nodes;
- the URL contained only the audit cache-buster and no input value.

The in-app browser then remained indefinitely in Plotly's intermediate `Calculating…` frame with a
default 700 px SVG. Exports stayed disabled, and completed live label geometry or a live screenshot
could not be claimed. This is a **nonblocking validation limitation** because the complete hosted
file set is byte-identical to the candidate that passed the exact-tag locked Chromium 12-test
responsive/export suite and WebKit smoke. It must not be rewritten as either a completed
direct-live render pass or an observed application failure.

## Lane F — documentation, rights, citation, and maintenance

All required public and repository documents were present and nonempty:

```text
README.md
LICENSE
CITATION.cff
AGENTS.md
CHANGELOG.md
llms.txt
docs/SCIENTIFIC_SCOPE.md
docs/VALIDATION.md
docs/PRIVACY.md
docs/PROVENANCE.md
docs/RUNTIME_DEPENDENCIES.md
docs/DECISIONS.md
docs/MAINTENANCE.md
```

The public documentation is internally consistent about:

- app version 0.1.2 and release date 2026-07-30;
- Brian Locke as author and maintainer;
- MIT for repository-authored code and artifacts;
- exact Core 0.4.1 release URL, checksum, and peeled commit;
- Core as the sole numerical authority, with no copied local Wald formula;
- the primary exact critical effect versus the distinctly labeled fixed-default legacy benchmark;
- the distinction from observed power/evidence, confidence bounds, MCID validation, sample-size
  planning, clinical guidance, and regulatory use;
- browser-only local/worker processing and the absence of backend, storage, telemetry, and uploads;
- compact live plotting and temporary noncompact high-resolution export behavior;
- active experimental maintenance status and exact release workflow.

An exact-word search found no unresolved `Reed` or `Blocke` identity. `pyproject.toml`,
`CITATION.cff`, `LICENSE`, README, provenance, and maintenance text all use the user-approved
Brian Locke / MIT identity.

Provenance checks also reconciled:

- `scientific-applet-template` annotated v0.1.0 peels to
  `a360bde95c192d8de4f9a3b531e73600ebf3d8b8`;
- that template commit's tree is
  `6a6c8c33cbef24b5dcbd35706d2292d9d3e5e359`;
- critical-effect-size initial commit
  `5ff3a10bfc610fbfe915f438aa8f11cdee6c3361` has the identical tree;
- the frozen integrated-behavior source commit
  `830756ecb11b4e8161f8dfe1fc75afc346ef4467` exists in the integrated source repository;
- the carried fixture contains only two named synthetic numerical scenarios and no patient/study
  records;
- no committed PNG, JPEG, GIF, SVG, PDF, Office, ZIP, TAR, or GZIP external artifact was found;
- no external code, publisher figure/table/dataset, or substantial publication text is claimed or
  present.

## Blockers and nonblockers

Blockers:

- none.

Retained nonblocking observations:

1. Direct live 390 px calculation and compact-state evidence completed, but the connected in-app
   browser did not complete Plotly's final frame or exports. Exact-tag Chromium/WebKit plus full
   live byte identity provide the completed responsive/export evidence.
2. SAGE returned HTTP 403 to automated retrieval; Crossref resolved the exact DOI/title/metadata.
3. GitHub's Pages upload action omits `.nojekyll`; the artifact-API deployment remains byte-exact
   for every served file and does not use a Jekyll source build.
4. Cross-platform gzip recompression differs at the compressed-byte layer while the release
   checksum, decompressed tar stream, and tagged tree all match exactly.

## Final disposition

`reblocke/critical-effect-size` v0.1.2 is an exact-commit, checksum-addressed, cold-clone
reproducible, independently tested, source/Core/stage/Pages-byte-reconciled release. It meets the
ticketed Lane C/D/E/F gates with the explicitly bounded direct-live tooling qualification above.
