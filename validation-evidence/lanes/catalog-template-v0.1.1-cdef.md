# CC-MIG-11 catalog/template v0.1.1 final Lane C/D/E/F audit

Audit completed: 2026-07-30T16:11:05Z
Catalog repository: `reblocke/wald-inference-tools`
Template repository: `reblocke/scientific-applet-template`
Audited release in each repository: `v0.1.1` (published GitHub prerelease)
Catalog isolated root: `/private/tmp/cc-catalog-v011-isolated.SQxGmS`
Template isolated root: `/private/tmp/cc-template-v011-isolated.G3zFzG`
Artifact/Pages root: `/private/tmp/cc-portfolio-v011-audit.pQ1HQ0`
Production or GitHub mutations by auditor: none

## Decision

**GO for `wald-inference-tools` v0.1.1 and `scientific-applet-template` v0.1.1 in
portfolio Lanes C, D, E, and F. No release blocker was found.**

The verdict is deliberately scoped:

- Catalog v0.1.1 is a mechanically verified `release-candidate`, not a claim that the whole
  portfolio has already been promoted to independently validated/stable status.
- Template v0.1.1 is a verified engineering scaffold with a replace-me arithmetic demonstration,
  not a scientifically validated calculation tool.
- No connected direct-live Browser session was available. Completed browser behavior comes from
  exact-tag Chromium/WebKit runs, while full Pages artifact and live-byte reconciliation proves
  those tested bytes are deployed. No direct-live interaction or screenshot is claimed.

## Exact release identities

| Item | Wald inference tools | Scientific applet template |
|---|---|---|
| annotated tag | `v0.1.1` | `v0.1.1` |
| tag object | `65d859bad697f22e8ffe05b0307661782c8fafd3` | `f4c76b6c91eac602834f84cb3edab9d8ab9f6865` |
| peeled commit | `6fffdd51dbf5c53beeb6146f9deb10daeb194760` | `c13d27de9fa456075cb9e52d897a5e9f866d8f32` |
| `main` at final drift check | same peeled commit | same peeled commit |
| tagger | Brian Locke `<reblocke@gmail.com>` | Brian Locke `<reblocke@gmail.com>` |
| tag date | `2026-07-30T15:52:14Z` | `2026-07-30T13:35:55Z` |
| release publication | `2026-07-30T15:53:29Z` | `2026-07-30T13:37:35Z` |
| main CI | `30558657348`, success, exact commit | `30547439776`, success, exact commit |
| release workflow | `30558804206`, success, exact commit | `30547647201`, success, exact commit |
| Pages workflow | `30558657321`, success, exact commit | `30547437227`, success, exact commit |
| Pages deployment | `5677922622`, success | `5675675967`, success |
| live URL | `https://reblocke.github.io/wald-inference-tools/` | `https://reblocke.github.io/scientific-applet-template/` |

Local Git, `git ls-remote`, and GitHub's Git-data API independently agreed that both refs are
annotated tag objects peeling directly to the commits above. Both releases are public, non-draft,
and intentionally prerelease.

Catalog CI completed its test, live-metadata, Chromium, and WebKit jobs. Template CI completed its
test, Chromium, and WebKit-smoke jobs. Template self-test run `30547437064` also succeeded at the
exact template commit by initializing and testing a disposable downstream app.

Both Pages configurations were public, workflow-built, and HTTPS-enforced. Their successful
deployment records named the exact audited commits and live URLs above.

## Isolation and exact README workflows

Both repositories were cloned into new parents with:

```text
git clone --branch v0.1.1 --single-branch <repository-url> repository
```

For each repository, verification unset `CONDA_PREFIX`, `VIRTUAL_ENV`, `PYTHONPATH`, `UV_PYTHON`,
and `UV_PROJECT_ENVIRONMENT`; set `PIP_CONFIG_FILE=/dev/null` and `PYTHONNOUSERSITE=1`; and used
initially absent, repository-specific paths for:

```text
UV_CACHE_DIR
UV_PYTHON_INSTALL_DIR
XDG_CACHE_HOME
XDG_CONFIG_HOME
PLAYWRIGHT_BROWSERS_PATH
npm_config_cache
```

Each run independently downloaded CPython 3.12.13, its locked environment, Chrome for Testing
149.0.7827.55 (Playwright build 1228), FFmpeg build 1011, and WebKit 26.5 (build 2311). The runs
therefore did not depend on global Python packages, sibling repositories, or pre-existing uv/npm/
browser caches.

Host/tool context:

- macOS 26.5.2 build 25F84, Darwin 25.5.0, Apple arm64;
- Git 2.50.1 (Apple Git-155);
- uv 0.11.11;
- CPython 3.12.13;
- Playwright 1.61.0;
- pytest 8.4.2;
- pytest-playwright 0.8.0;
- Ruff 0.16.0.

### Catalog README/release commands

| Command | Exit | Result |
|---|---:|---|
| `uv sync --locked` | 0 | 21 locked packages resolved in an isolated environment |
| `uv run playwright install chromium webkit` | 0 | fresh Chromium/WebKit/FFmpeg downloaded |
| `make verify` | 0 | 18 files format-clean; lint clean; six-tool manifest and seven local references valid; 29 non-E2E, 4 Chromium, and 4 WebKit tests passed; exact site built; `git diff --check` passed |
| `make live-check` | 0 | 38 public release/repository/README/citation/Pages/manifest targets validated |
| `uv run python scripts/check_release_metadata.py --tag v0.1.1` | 0 | tag, project, catalog, citation, and changelog metadata agreed |
| `uv run python scripts/build_release_artifacts.py --version 0.1.1 --output release` | 0 | all four published release assets reproduced byte-for-byte |
| `make serve` | 1 after intentional Ctrl-C | local site started; `/`, `data/tools.json`, and `docs/PRIVACY.md` returned HTTP 200 |
| final Git checks | 0 | detached exact tag; no tracked/untracked source changes, whitespace errors, or staged differences |

### Template README/release commands

| Command | Exit | Result |
|---|---:|---|
| `uv sync --locked` | 0 | 23 locked packages and template package 0.1.1 installed |
| `uv run playwright install chromium webkit` | 0 | fresh Chromium/WebKit/FFmpeg downloaded |
| `make verify` | 0 | 31 files format-clean; lint clean; deterministic stage generated; 30 non-E2E, 5 Chromium, and 1 WebKit test passed |
| `make template-self-test` | 0 | disposable `example-applet` initialized with zero unresolved identity values; 22 downstream non-E2E and 1 Chromium test passed |
| `make serve` | 1 after intentional Ctrl-C | local site started; `/`, stage manifest, and worker returned HTTP 200 |
| final Git checks | 0 | detached exact tag; no tracked/untracked source changes, whitespace errors, or staged differences; generated stage untracked and ignored |

The disposable initializer self-test changed the expected identity-bearing files, renamed
`src/template_applet` to `src/example_applet`, removed the four template-maintainer-only paths,
created a new Git repository, regenerated its lock/stage, and returned no unresolved template
identity values. It does not claim to complete the downstream scientific-author prompts; those
remain an intentional author responsibility.

## Catalog release, Pages, and live provenance

### Release assets

The downloaded GitHub release assets, GitHub-recorded digests, `SHA256SUMS`, and independent local
hashes agreed:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 288 | `9c103ea6920881beaaa44296a47908a1a81fc90c6b1f4a32da683bde4b929a49` |
| `tools-v0.1.1.json` | 10,248 | `cc0222943b8dcd6e97273211e6622db7f33bd0a7b954aebe33585eb18a4b3f94` |
| `wald-inference-tools-site-v0.1.1.zip` | 12,513 | `afe04ffc7606a0f8dc0c0cadd18f0728999188c33ea7553598ae7fb4d9c8a295` |
| `wald-inference-tools-v0.1.1.tar.gz` | 45,706 | `f5cc9d9702770f7ee4a7c965e739470a5d9d171c849aa9656979af5386ab9c72` |

`shasum -a 256 -c SHA256SUMS` and ZIP integrity passed.

The catalog intentionally uses its own normalized PAX/gzip builder instead of delegating source
archive formatting to platform Git/tar defaults. A fresh exact-tag run reproduced every published
compressed asset byte-for-byte, including `SHA256SUMS`. The source archive contained exactly the
33 tracked regular files, no links/devices/traversal, and extracted to a file tree byte-equal to the
tag. Its normalized uncompressed tar SHA-256 was:

```text
307376026b3064da50ac23652ae82f4bbf186c9f4d865894f9dd7cb713a7171a
```

The site ZIP contained the exact allowlisted nine-file Pages build, including `.nojekyll`, with
fixed ZIP timestamps. The released `tools-v0.1.1.json`, tagged `data/tools.json`, generated site
copy, Pages artifact copy, and live copy were byte-identical.

### Pages and live bytes

Pages artifact `8765884573` had GitHub outer digest:

```text
ef0961febfd1a6a584067b725fa5cb531e1035234b35e0b02c1bc843645ba936
```

Its downloaded `artifact.tar` was 51,200 bytes with SHA-256:

```text
5376e05bb1464fd8d61bf00dba42ab39d1c04c4034b76cb058ff589e7ca7b023
```

It contained eight regular files and three directories, no unsafe/non-regular member, and matched
the exact generated site except `.nojekyll`. The live site matched all eight served files:

| Live/tagged file | Bytes | SHA-256 |
|---|---:|---|
| `index.html` | 5,727 | `d9314038221723fb9e755700f945e36c34a72a92feb23e0972aa5057afcdddba` |
| `styles.css` | 6,985 | `c3e6c72066cc4c4982c6f2fa92aa08effea7f547dc9545b2d3923fdd613a7ecd` |
| `app.js` | 4,074 | `f538d49e3cf1800e6b88c661f38d32758210ef34ac2cd9e97bd69954a24bfc5c` |
| `data/tools.json` | 10,248 | `cc0222943b8dcd6e97273211e6622db7f33bd0a7b954aebe33585eb18a4b3f94` |
| `docs/DECISIONS.md` | 2,626 | `eda24373b74180b72c4e53599e192f765f4b9aec353a407d003a27b689377550` |
| `docs/MAINTENANCE.md` | 2,557 | `cccd4a338dc3c72a5c1e63db03470150ae6f0b1864d0471349626f909375209e` |
| `docs/PRIVACY.md` | 917 | `6c3a51ee53134993e565e160969b367b01e5914bd860603ec35ec5ac03a4bee1` |
| `docs/VALIDATION.md` | 1,417 | `9f6187ee072a5afdea16ab1ab44aa4b7f0b4d004bde1e19710629671d8c1` |

The Pages upload action explicitly excludes dotfiles, explaining why `.nojekyll` is absent from
the deployment artifact and returns HTTP 404. The deployment uses the Pages artifact API, not a
Jekyll source build; every served byte is otherwise exact. This is nonblocking.

## Catalog exact deployed app/tag manifest gate

`make live-check` and an independent GitHub/live-manifest pass verified every catalog row. For each
tool, the cataloged app version resolved to an annotated tag, the live manifest `source_commit`
equaled the tag's peeled commit, and the live app/Core versions equaled the catalog.

| Tool | App | Annotated tag object | Peeled = deployed commit | Live manifest SHA-256 |
|---|---|---|---|---|
| compatibility-curve | 0.1.2 | `1639c9342fbadfe33d3227e05348406ac85854b4` | `64c6264b9ac93d6665d12c30fa5f4290dd571421` | `90d920b9719424e4042d2ea24d477645407000cf731eb4350f32e8c12e8ac666` |
| wald-likelihood-support | 0.1.2 | `5285b792379cb538bfa93859ecc9d18f07ec2dbb` | `7f5557d2a93235e25215261ef5890868b3fb07bb` | `21be10dd5197300594401f69605288b95d95a533d448c0284cea2870bfd023b0` |
| critical-effect-size | 0.1.2 | `fee04866ddb0b8d39575e8d0e958a219dbe7cb52` | `73bc391adff6cf2f08fba28baa67014c043b9cb0` | `233e42b64c7b98e0bf2446040bd5ba8c13475ef766fb84d7e07af319a426e734` |
| type-s-m-calibrator | 0.1.2 | `919ec07dd62fe726b7a71ad01ac5c48642c68064` | `fd6d384e56626c513ca5b83c92a62cbc29ecdd14` | `2d21e0f3d48ea71421c9a6ad34f54690fa4ef18d9862dcde421be9dfb3b5beae` |
| precision-guardrail-planner | 0.1.1 | `5eaac5cfd616a94b90b2110a54ec3197cd797dff` | `bfc54c5d4d79e497fb145e931f9f562b31938616` | `9701e2e397e7e7f70476003451f0ec5f54e98c3b35b49ceff58cf4836f5dcc89` |
| conf_curve_likelihood | 0.2.2 | `045a23f58ebfe444cb40355ebbb317d731812612` | `78d189ac03ec223a69778843497d27c70a8720c2` | `b81f7b5781d77ae0ed1f95b513d6f7f3f27ac853ae2b552d2ea5aebb4210e073` |

Every live row reported Core 0.4.1. Core's annotated v0.4.1 tag object
`838c4aaab08570a17156bd59b1ff65dcabf56bfc` peeled to
`f4613177b6dc81d194aa70762152de2bfa86663b`.

The live bundle hashes were:

```text
compatibility-curve        3215dfe4f24d30eac18591aad95873c1ec9084cc1da4636fb30b721dbca6ae17
wald-likelihood-support    b9c5247cba1dc13a004959e8354f1c96c00381aca5e31cda84a121b260316db0
critical-effect-size       bd5eb3d202962b4a2f31d50eb32d6214687dc94cfd6b72fc38a9cf7fa81580c5
type-s-m-calibrator        28eed989a661d757b081212f407d0773ea8ac357d03497bede2f5625d5968b40
precision-guardrail        bee9d58f4e5d695716b925f899e7c9a779dc13560f827847f0afcddb6abb5a47
integrated workbench       b6e487540a5f5fa349ce22aa631916ab8d4d5a6b83145ad3acd2714fad22f592
```

The same live check verified the six public repositories, public non-draft releases, hosted apps,
citations, current public README `Related Wald tools` blocks, deployed footers, adjacent-tool
links, integrated-workbench links, and Core release markers. It validated 38 targets without
failure.

All six tool rows, the catalog portfolio, and Core remain labeled `release-candidate`. That label
is accurate at this predecessor tag: stable promotion is explicitly gated on the consolidated
independent portfolio report/status update and must not be inferred from this mechanical
reconciliation alone.

## Template release, stage, Pages, and live provenance

### Release assets and source

The downloaded GitHub assets, GitHub-recorded digests, `SHA256SUMS`, and independent hashes agreed:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 208 | `537b6125ad4a92831a4a58d8fcca85fc6e90ebedc73f74f70ad783b6933af191` |
| `browser-stage-manifest-v0.1.1.json` | 1,310 | `167a73eff0e5be32e676ddd7165ca47e8e69104741c855aa88a372e8f6d75f35` |
| `scientific-applet-template-v0.1.1.tar.gz` | 63,632 | `853391b580530ea8aee3388a2244a84de3c9ff90ab0d79c593762e2818945477` |

`shasum -a 256 -c SHA256SUMS` passed. The source archive contained 56 regular files and 21
directories with one safe prefix and no links/devices/traversal. Its extracted file tree matched
all 56 tagged files. Its uncompressed tar stream was byte-identical to a fresh exact-tag
`git archive`:

```text
c5ba4fcacf0c0646365b228bc833fa0a41ab49fab186039d1d8aefb3a7275bd2
```

Local macOS `gzip -n` produced compressed SHA-256
`ad1cce08d0a66d7dbc26fa22c556fe071f18f8eaf125c95ac6d4edf5e24f47b0`, different from the Linux
release asset while decompressing to the exact same tar stream. The published compressed asset
is independently checksum-addressed; this compressor/platform variance is nonblocking.

### Stage and Pages

The release asset, isolated stage, Pages artifact, and live manifest were byte-identical. Manifest
identity:

```text
manifest SHA-256:
  167a73eff0e5be32e676ddd7165ca47e8e69104741c855aa88a372e8f6d75f35
source commit:
  c13d27de9fa456075cb9e52d897a5e9f866d8f32
scientific-applet-template-package 0.1.1, 4 files:
  baefb7c517e053b8ba52105ced20d2ea28a800dcb22e33aa45c20dfbce73405d
bundle:
  baefb7c517e053b8ba52105ced20d2ea28a800dcb22e33aa45c20dfbce73405d
Pyodide:
  0.29.3
```

All four live staged files returned HTTP 200 with their declared byte counts and SHA-256 hashes.
The default scaffold contains no external scientific Core package.

Pages artifact `8761309280` had GitHub outer digest:

```text
757bba1e28c6120e821bf6186f19f3c007e54500386f34a6872d16623c2ea5bf
```

Its downloaded `artifact.tar` was 61,440 bytes with SHA-256:

```text
6c5f49f84ae9a4afde0d9dcec9fac52f2819d8e1442b74e1e86a447de123b8a6
```

It contained 15 regular files and five directories, no unsafe/non-regular member, and matched the
generated `web/` tree exactly except `.nojekyll`. The upload action log explicitly records the
dotfile exclusion. The live marker returns HTTP 404, while all 10 served tracked static files and
all five generated stage files (manifest plus four Python files) were byte-equal to the tag.

Selected live/tagged hashes:

| File | Bytes | SHA-256 |
|---|---:|---|
| `index.html` | 5,582 | `7bab0a725d11a5c37fcc9317beaa9606c2e0ee043c4f5ce35de9a24c993f2b83` |
| `app.js` | 4,345 | `d531d8a77d2cbd917f99caafa42e64bd742b262a28d1a20b3b851bc58be0314c` |
| `styles.css` | 4,206 | `a973e42fd3098c37b028e07e98d04a4ecc436779b46a80bd16765a62fa1400db` |
| `pyodide_worker.js` | 11,390 | `69c576f4a170525411343e1a3b193d6121e6829b6219ba9ec1ffeb9895bd409c` |
| `assets/py/manifest.json` | 1,310 | `167a73eff0e5be32e676ddd7165ca47e8e69104741c855aa88a372e8f6d75f35` |

## Lane E browser, privacy, accessibility, and links

### Catalog

The same exact-tag catalog suite completed in both Chromium and WebKit:

- six question cards and six comparison rows rendered from `data/tools.json`;
- catalog/Core versions and links came from the manifest rather than duplicated card markup;
- observed-data/design/all filters returned the expected 3/4/6 cards;
- 390 x 844 skip-link focus, Enter navigation, radio-keyboard operation, visible focus, and no
  horizontal overflow;
- initial browser traffic consisted only of same-origin GET requests for `/`, `app.js`,
  `styles.css`, and `data/tools.json`, with no request bodies;
- local storage, session storage, and cookies remained empty;
- no controlling service worker was present.

Static review confirmed no form, calculation runtime, Pyodide, remote script, telemetry, analytics,
state-writing call, input-bearing URL, or scientific formula. The catalog accepts no user values.
The live site is byte-identical to this tested candidate.

### Template

The exact-tag Chromium suite completed:

- worker/Pyodide load and exact replace-me result `2 + 3 = 5`;
- finite-value error, sanitized linked input error, worker recovery, and textual/table result;
- exact three-row CSV, PNG figure/dashboard hooks, and caption copy;
- runtime version 0.1.1;
- 390 x 844 keyboard flow, controls/results visibility, and no horizontal overflow;
- sentinel `12345.67891` absent from request URLs and request bodies;
- unchanged URL plus empty local storage, session storage, and cookies.

Static review also found no IndexedDB use, service worker, backend, telemetry, analytics, upload,
cookie write, input-bearing query/fragment, WebSocket, EventSource, or input logging. Inputs stay in
page/worker memory. Fixed external runtime links returned HTTP 200:

- Plotly.js 3.1.0 from `cdn.plot.ly`;
- Pyodide 0.29.3 from versioned jsDelivr.

The separate WebKit worker/calculation smoke passed. The live site, worker, static modules, and all
stage bytes were independently matched to the candidate.

Template live/repository/privacy/scientific-scope/owner/CI links and both runtime CDN URLs returned
HTTP 200. Catalog `make live-check` provided the broader 38-target portfolio link check described
above.

Accessibility evidence covered semantic headings/cards/table, text alternatives, labeled controls,
skip navigation, visible focus, keyboard operation, `aria-live`, alert/error linkage, details/
summary controls, textual results in addition to plots, and 390 px containment. This is automated
DOM/keyboard/rendered-layout evidence, not an exhaustive manual screen-reader or WCAG conformance
audit.

### Direct-live evidence boundary

No connected direct-live Browser session was available to this audit or the parent reviewer.
Consequently, no direct live interaction, computed screenshot, or manual assistive-technology
session is claimed. This is a nonblocking evidence limitation because:

1. local Chromium/WebKit tests completed against clean exact-tag clones;
2. Pages artifacts matched the generated candidates;
3. all served catalog bytes and all served template static/staged bytes matched those candidates;
4. live links and catalog release/tag/manifest relationships were independently queried after
   deployment.

## Lane F authorship, license, scope, and provenance

Both repositories consistently use the user-approved identity and license:

- author/maintainer: Brian Locke;
- repository-authored code/text: MIT;
- `LICENSE`: `Copyright (c) 2026 Brian Locke`;
- `CITATION.cff`: version 0.1.1, release date 2026-07-30, exact repository/live URL;
- no exact-word `Reed` or `Blocke` identity remained.

No committed PNG, JPEG, GIF, SVG, PDF, Office, ZIP, TAR, or GZIP external artifact was found in
either source tag.

Catalog provenance is machine-readable and source-backed:

- `data/tools.json` is the sole tool-metadata authority;
- released, Pages, and live copies are checksum-identical;
- every cataloged app/Core version is tied to a public annotated tag and deployed manifest commit;
- the catalog contains no calculation or shared runtime dependency;
- conditioning, question, input, output, non-goal, and limitation text remain distinct for
  observed-data, assumed-truth design, and mixed views;
- all entries remain conservatively `release-candidate`.

Template provenance is intentionally scaffold-specific:

- `docs/TEMPLATE_PROVENANCE.md` identifies the repositories whose structural patterns were
  inspected and states that no app-specific formula, prose, scientific name, fixture, figure, or
  visual content was copied;
- the audit independently found no committed external binary/document artifact and no external
  scientific package in the default stage;
- the repository clearly separates its MIT-authored template from Pyodide, Plotly, Python
  packages, papers, data, figures, and publisher assets that retain their own licenses;
- the arithmetic example is repeatedly and visibly labeled replaceable and non-scientific.

`AUTHOR ACTION REQUIRED` text is expected and correct in the **uninitialized template**. It marks
scientific scope, validation, dependency, maintenance, citation, decision, and downstream
ownership questions that the template cannot safely invent. The initializer removes template-only
provenance/self-test material and exhausts repository identity values, but downstream authors must
resolve those scientific prompts before claiming a completed app. Their presence is not an
unresolved template-release identity conflict.

## Blockers and retained nonblockers

Blockers:

- none for the v0.1.1 Lane C/D/E/F predecessor audit.

Retained nonblocking boundaries:

1. Neither release is promoted as stable: catalog/app statuses remain `release-candidate`, and the
   template remains a prerelease engineering scaffold. Consolidated portfolio validation/status is
   a separate downstream gate.
2. No connected direct-live Browser session was available; exact-tag Chromium/WebKit plus complete
   live-byte identity provide the completed browser evidence.
3. GitHub Pages upload actions omit `.nojekyll`; both artifact-API deployments match every served
   file and are not Jekyll source builds.
4. Template source gzip bytes vary by compressor/platform while the published checksum and
   uncompressed tag archive match exactly.
5. Accessibility evidence is automated; no exhaustive manual screen-reader/WCAG audit is claimed.

## Final disposition

`reblocke/wald-inference-tools` v0.1.1 and `reblocke/scientific-applet-template` v0.1.1 are
annotated-tag exact, cold-clone reproducible, CI/Pages-head reconciled, checksum-addressed,
release/Pages/live-byte traceable, privacy/accessibility tested, and consistently attributed to
Brian Locke under MIT. They pass the requested predecessor Lane C/D/E/F audit within the explicit
candidate/scaffold and direct-live evidence boundaries above.
