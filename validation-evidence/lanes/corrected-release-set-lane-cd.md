# CC-MIG-11 lanes C/D corrected-release recheck

Audit started: 2026-07-30T13:40:59Z
External release state last checked: 2026-07-30T14:27:19Z
Evidence set: core `v0.4.1`; template and five focused apps `v0.1.1`;
integrated workbench `v0.2.1`
Explicitly deferred: catalog `wald-inference-tools@v0.1.1`
Production/repository mutation: none

## Current decision

**Lane C passes for all eight audited tags. Lane D passes for the seven
published releases and is narrowly blocked for integrated `v0.2.1`: its
release workflow failed before artifact construction or publication.**

The original five-app Pages provenance blocker is cleared in the corrected
release set. For the template, all five focused apps, and the integrated
workbench, the following now agree exactly:

1. peeled annotated-tag commit;
2. current `main`;
3. successful Pages Actions `head_sha`;
4. successful Pages deployment SHA;
5. live browser manifest `source_commit`;
6. clean-clone generated browser manifest; and
7. for already published releases, released browser-manifest bytes.

The live `index.html` and principal application JavaScript also match the
corresponding tag files byte-for-byte.

The integrated tag, clean-clone verification, corrected Pages deployment, live
identity, and core provenance remain passing. They do not substitute for the
failed release gate: run `30548681294` ended `failure` after 13 of 48 Chromium
tests timed out while the app status remained at the Pyodide-loading phase.
No release artifacts were built or published.

The portfolio-wide Lane C/D verdict remains incomplete until the integrated
release workflow succeeds, its assets are published and checked, and the
separately pending catalog `v0.1.1` is supplied for the same bounded recheck.

## Scope and success criteria

This is a fresh recheck, not an inference from the original `v0.1.0`/`v0.4.0`
audit. Every repository was cloned again under a new temporary parent. A tag
passes only when:

- its annotated tag object independently peels to the expected commit;
- `uv sync --locked` succeeds with project `.python-version` discovery enabled
  and an empty per-tag dependency/browser cache;
- the documented repo-level verification and local serve smoke pass;
- browser staging records the exact released core wheel and clean tag;
- release assets pass `SHA256SUMS` and GitHub REST digest verification;
- release source archives match the tag tree;
- live Pages identity and content match the tag/release; and
- the final tracked worktree is clean.

The core additionally must pass its release distribution inspection,
deterministic release-bundle build, clean-wheel installed-package scientific/API
smoke, and package-tree comparison.

## Isolation and exact command surface

Each clone had its own initially empty `UV_CACHE_DIR`,
`UV_PYTHON_INSTALL_DIR`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`,
`PLAYWRIGHT_BROWSERS_PATH`, and npm cache. `PYTHONPATH`, `VIRTUAL_ENV`,
`CONDA_PREFIX`, `UV_PYTHON`, and `UV_PROJECT_ENVIRONMENT` were unset.
`PIP_CONFIG_FILE=/dev/null` and `PYTHONNOUSERSITE=1` were set. Project
configuration and `.python-version` discovery remained enabled.

The principal commands were:

```bash
git clone --branch <tag> https://github.com/reblocke/<repo>.git <new-path>
cd <new-path>
uv sync --locked
uv run playwright install chromium webkit  # browser repositories
make verify
make serve                                 # bounded HTTP 200 smoke
git status --short
git diff --check
```

Core additionally ran:

```bash
uv sync --locked --all-groups
make verify
uv build
uv run python scripts/check_distribution.py --dist-dir <downloaded-release>
uv run python scripts/smoke_installed_package.py --dist-dir <downloaded-release>
uv run python scripts/build_release_artifacts.py \
  --ref f4613177b6dc81d194aa70762152de2bfa86663b \
  --tag v0.4.1 \
  --parity-report reports/baseline-parity.json \
  --out-dir <empty-directory>
```

Released assets were checked with:

```bash
gh release download <tag> --repo reblocke/<repo> --dir <empty-directory>
shasum -a 256 -c SHA256SUMS
```

Every downloaded file was also hashed independently and compared with the
corresponding GitHub REST `assets[].digest`.

## Environment

| Item | Observed value |
|---|---|
| OS | macOS 26.5.2, build 25F84 |
| Kernel/architecture | Darwin 25.5.0, arm64, Apple M2 |
| Git | 2.50.1 (Apple Git-155) |
| uv | 0.11.11, Homebrew aarch64 build |
| Core/integrated Python | CPython 3.11.15 from `.python-version` 3.11 |
| Template/focused Python | uv-managed CPython 3.12.13 from `.python-version` 3.12 |
| Core dependencies | NumPy 2.2.6; SciPy 1.14.1; pytest 9.1.1; Ruff 0.16.0 |
| Integrated dependencies | NumPy 2.2.6; SciPy 1.14.1; pytest 9.0.2; pytest-playwright 0.7.2; Ruff 0.15.1; Playwright 1.58.0 |
| Template/focused dependencies | pytest 8.4.2; pytest-playwright 0.8.0; Ruff 0.16.0; Playwright 1.61.0; focused apps also use NumPy 2.2.6 and SciPy 1.14.1 |
| Integrated browser binaries | Chrome for Testing 145.0.7632.6 / revision 1208; WebKit 26.0 / revision 2248 |
| Template/focused browser binaries | Chrome for Testing 149.0.7827.55 / revision 1228; WebKit 26.5 / revision 2311 |

Complete dependency lists and trees are preserved in each corrected cold
parent's `logs/uv-pip-list.log` and `logs/uv-tree.log`.

## Exact annotated tags and releases

Every tag ref below has GitHub object type `tag`; none is a lightweight tag.
All supplied peeled commits were independently confirmed. GitHub reports each
tag as unsigned (`verified=false`, `reason=unsigned`), a retained nonblocking
provenance limitation. Published releases are `draft=false`,
`prerelease=true`.

| Repository/tag | Annotated tag object | Peeled commit | Release assets |
|---|---|---|---:|
| `wald-inference-core@v0.4.1` | `838c4aaab08570a17156bd59b1ff65dcabf56bfc` | `f4613177b6dc81d194aa70762152de2bfa86663b` | 4 |
| `scientific-applet-template@v0.1.1` | `f4c76b6c91eac602834f84cb3edab9d8ab9f6865` | `c13d27de9fa456075cb9e52d897a5e9f866d8f32` | 3 |
| `compatibility-curve@v0.1.1` | `abed9da076fbc47b5e410df204bdf8c1de16e278` | `12a13e78953258c2d3ad09d0846de49e86151636` | 3 |
| `wald-likelihood-support@v0.1.1` | `4a7f510d146930ca35d4a8ddd858c007919749c3` | `c2fc494d600e0d0af5b70897f69de19fa81f38f4` | 3 |
| `critical-effect-size@v0.1.1` | `291e219567f6067ec45495e590b96710685ea271` | `00014f5c3995f5296dd372d97852ae8c202c1e6a` | 3 |
| `type-s-m-calibrator@v0.1.1` | `83d28108b6d12090379864f05bb2c49597eaf0f9` | `1b3f22fe7f86b9e52754ad81ed7800b6e313c6fb` | 3 |
| `precision-guardrail-planner@v0.1.1` | `5eaac5cfd616a94b90b2110a54ec3197cd797dff` | `bfc54c5d4d79e497fb145e931f9f562b31938616` | 3 |
| `conf_curve_likelihood@v0.2.1` | `044a2b89f00ad9678750cec3322f2c8d2feb7fa0` | `daae30681d1ac8c7c13a7afc085b13e0b56d23d2` | 0; release workflow failed |

## Lane C cold-start matrix

All completed commands below exited 0. Clone time was 1 second per repository.
Runtimes are machine observations, not benchmark guarantees.

| Repository/tag | Python | Locked sync | Browser install | `make verify` | Corrected serve smoke | Final tracked state |
|---|---:|---:|---:|---:|---:|---|
| `wald-inference-core@v0.4.1` | 3.11.15 | 15 s | n/a | 245 s | n/a | clean |
| `scientific-applet-template@v0.1.1` | 3.12.13 | 14 s | 59 s | 97 s | 1 s | clean |
| `compatibility-curve@v0.1.1` | 3.12.13 | 19 s | 70 s | 405 s | 3 s | clean |
| `wald-likelihood-support@v0.1.1` | 3.12.13 | 16 s | 77 s | 476 s | 1 s | clean |
| `critical-effect-size@v0.1.1` | 3.12.13 | 19 s | 78 s | 459 s | 2 s | clean |
| `type-s-m-calibrator@v0.1.1` | 3.12.13 | 22 s | 75 s | 558 s | 3 s | clean |
| `precision-guardrail-planner@v0.1.1` | 3.12.13 | 22 s | 78 s | 376 s | 2 s | clean |
| `conf_curve_likelihood@v0.2.1` | 3.11.15 | 10 s | 62 s | 540 s | 4 s | clean |

Integrated `make verify` passed 205 non-E2E tests, the complete 48-test
Chromium suite, frozen 22-case B01–B08 checks, strict staging, Ruff, and
portfolio-link checks. Because integrated `make verify` intentionally leaves
WebKit to a separate CI job, the exact WebKit initial-render smoke was also run
locally and passed in 25 seconds.

Additional standalone documented checks passed:

| Repository | Check | Runtime |
|---|---|---:|
| template | `make template-self-test` | 25 s |
| compatibility | legacy compatibility regression | 4 s |
| type S/M | `make scientific-test` | 3 s |
| precision | scientific-reference and regression suites | 5 s |
| integrated | live portfolio-link checker | 4 s |

Generated `.venv`, caches, test artifacts, staged `web/assets/py`, core
`dist`/reports, and similar outputs are ignored. `git status --short` was empty
and `git diff --check` exited 0 after final verification in all eight clones.

### Discarded serve-probe attempt

An initial smoke helper tried to pass arbitrary ports while the repository
Makefiles intentionally hard-code port 8000. Running three such probes in
parallel therefore polled the wrong ports and caused a port collision. This
was a harness defect, not a repository failure. Those probes were discarded.
Every browser repository was then rerun sequentially against the documented
fixed port 8000, returned HTTP 200, terminated cleanly, and left no listener.
Only the corrected serve results appear in the matrix.

## Lane D published artifact evidence

For the seven currently published releases:

- `SHA256SUMS`: **7/7 passed**;
- downloaded files versus GitHub REST digests: **22/22 exact**;
- app release archive versus annotated-tag tree: **6/6 exact**;
- clean-clone generated versus released browser manifest: **6/6 byte-exact**;
- live versus released browser manifest: **6/6 byte-exact**;
- focused staged core versus released core wheel tree: **5/5 exact**.

### Published asset checksums

| Repository/tag | Asset | SHA-256 |
|---|---|---|
| core `v0.4.1` | wheel | `d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b` |
| core `v0.4.1` | sdist | `5b30fbc22c416cc724b75d9920157f42886ba185d34b628b4ad4c66691376bbf` |
| core `v0.4.1` | baseline parity report | `18d020e6a00746646ffed913eb88f1e4b148aa2725872db647823019f1e65dba` |
| template `v0.1.1` | browser manifest | `167a73eff0e5be32e676ddd7165ca47e8e69104741c855aa88a372e8f6d75f35` |
| template `v0.1.1` | source archive | `853391b580530ea8aee3388a2244a84de3c9ff90ab0d79c593762e2818945477` |
| compatibility `v0.1.1` | browser manifest | `4deda63fc239611f27a45f5d56dddd9ce9927744dcdaa8579130f00d3359d8d6` |
| compatibility `v0.1.1` | source archive | `5b78ed862442bc5cf92cbf491f2f47dbfc5a6d744476b7b44bb06b103fa8592b` |
| likelihood `v0.1.1` | browser manifest | `0445134f8b646b065e3daec9b137b0a08a608cd60cc0dcec9788a4f848c4faf5` |
| likelihood `v0.1.1` | source archive | `82688799af455e7ebe722e514439dc20493c3e0e2e51e81c129d9a9ed46425ea` |
| critical effect `v0.1.1` | browser manifest | `1cd38c1bd852338c86ec57abb5970350b86edd14aa00259bfb8b5b5a86a05baf` |
| critical effect `v0.1.1` | source archive | `40b94555b891732ae85e332176eb68946d48e7a35eeac6793c84f4cb0fc6ea0d` |
| type S/M `v0.1.1` | browser manifest | `365dce54bc7011d40357edd9e832fb989ad007ab9b9190cf9de409b1f596be0e` |
| type S/M `v0.1.1` | source archive | `5b0b287c1beb28e7b9fa4ce89e3755befa8462effd9735a20e51ffd9c5e211d2` |
| precision `v0.1.1` | browser manifest | `9701e2e397e7e7f70476003451f0ec5f54e98c3b35b49ceff58cf4836f5dcc89` |
| precision `v0.1.1` | source archive | `fb642b0178ed2651ff0d4a5068455fff139bde4b5fb8f9723c69030c0f89752d` |

Each release also publishes the corresponding `SHA256SUMS`, whose own REST
digest was included in the 22/22 independent comparison.

### Core release and staged-package provenance

Core `v0.4.1` passed:

- released wheel/sdist distribution inspection;
- clean external wheel installation with NumPy 2.2.6 and SciPy 1.14.1;
- `uv pip check`;
- installed public API and scientific smoke;
- exact extracted released-wheel/released-sdist file-tree comparison against
  the clean tag build; and
- tracked-clean verification.

The clean wheel smoke took 46 seconds. The release-specific deterministic
bundle builder recreated the released wheel and sdist **byte-for-byte**:

| Artifact | Local deterministic build | Released | Result |
|---|---|---|---|
| wheel | `d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b` | same | exact |
| sdist | `5b30fbc22c416cc724b75d9920157f42886ba185d34b628b4ad4c66691376bbf` | same | exact |

Every focused app's `uv.lock`, installed environment, generated manifest, and
staged core records `wald-inference==0.4.1` and wheel SHA-256
`d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b`.
All five 14-file staged `wald_inference` trees are exact to the downloaded
released wheel. The template intentionally has no numerical core.

The integrated lock and clean environment also resolve core `0.4.1` at this
exact URL/hash, and its 14-file staged core tree is exact to the released
wheel. Its live and local manifests are already byte-exact at SHA-256
`d4d8bd51eb857d40d0e582dc7e6f40534d2c58a30d5a8970e3cd44f9b2970a0e`;
comparison with an integrated release asset remains impossible because the
release workflow failed before building or publishing it.

### Cross-platform parity-report observation

The released core parity report passed its published checksum and records all
14 successful B01–B08 cases, 6 matched core-error cases, 2 explicit app
exclusions, and 23,095 compared values. The fresh macOS arm64 report has the
same cases, statuses, counts, and declared tolerances but is not byte-identical
because its floating-point maximum-difference summaries are smaller:

| Report | Maximum absolute difference | Maximum relative difference |
|---|---:|---:|
| released Linux artifact | `2.842170943040401e-14` | `1.3881501524486269e-15` |
| fresh macOS arm64 run | `5.329070518200751e-15` | `4.449372536648163e-16` |

Both pass `rtol=1e-12`, `atol=1e-14`. This is a nonblocking
platform-floating-point observation, not a parity failure. It explains why a
locally rebuilt parity JSON and aggregate `SHA256SUMS` differ even though the
deterministic wheel and sdist are byte-exact.

## Pages release traceability

All seven current Pages deployments are successful and identify the corrected
tag commit. Core has no Pages site, as expected.

| Repository | Tag / `main` / Pages commit | Pages run | Deployment | Live manifest SHA-256 | Result |
|---|---|---:|---:|---|---|
| template | `c13d27de9fa456075cb9e52d897a5e9f866d8f32` | `30547437227` | `5675675967` | `167a73eff0e5be32e676ddd7165ca47e8e69104741c855aa88a372e8f6d75f35` | exact |
| compatibility | `12a13e78953258c2d3ad09d0846de49e86151636` | `30547135738` | `5675615559` | `4deda63fc239611f27a45f5d56dddd9ce9927744dcdaa8579130f00d3359d8d6` | exact |
| likelihood | `c2fc494d600e0d0af5b70897f69de19fa81f38f4` | `30547135668` | `5675612131` | `0445134f8b646b065e3daec9b137b0a08a608cd60cc0dcec9788a4f848c4faf5` | exact |
| critical effect | `00014f5c3995f5296dd372d97852ae8c202c1e6a` | `30547432765` | `5675677474` | `1cd38c1bd852338c86ec57abb5970350b86edd14aa00259bfb8b5b5a86a05baf` | exact |
| type S/M | `1b3f22fe7f86b9e52754ad81ed7800b6e313c6fb` | `30547432997` | `5675680391` | `365dce54bc7011d40357edd9e832fb989ad007ab9b9190cf9de409b1f596be0e` | exact |
| precision | `bfc54c5d4d79e497fb145e931f9f562b31938616` | `30546716725` | `5675528031` | `9701e2e397e7e7f70476003451f0ec5f54e98c3b35b49ceff58cf4836f5dcc89` | exact |
| integrated | `daae30681d1ac8c7c13a7afc085b13e0b56d23d2` | `30547846891` | `5675763923` | `d4d8bd51eb857d40d0e582dc7e6f40534d2c58a30d5a8970e3cd44f9b2970a0e` | exact |

Each deployment's latest deployment status is `success`. Live `index.html`
and the principal app JavaScript are byte-exact to the corresponding clean tag
for all seven sites. The prior focused-app post-tag divergence no longer
exists in this corrected set.

## Limitations and pending items

1. Integrated `v0.2.1` release run `30548681294` completed with `failure` at
   2026-07-30T14:25:22Z. The Chromium progress line records 35 passes and 13
   failures. Each failure hit the 120-second readiness timeout with the status
   stuck at `Loading Pyodide, NumPy, and SciPy in the browser.` The subsequent
   WebKit, tracked-clean, deterministic-build, bundle-upload, and release jobs
   were skipped. The Actions artifacts API reports zero artifacts and the
   release API returns HTTP 404. The common observed failure mode is recorded;
   this audit does not claim a cause. Local cold-clone verification and Pages
   identity still pass, but release-asset checksums/digests and archive-to-tag
   comparison are blocked.
2. Catalog `wald-inference-tools@v0.1.1` has not yet been supplied and is
   outside this evidence set. The portfolio Lane C/D result cannot be called
   complete until it receives the same recheck.
3. Tags are annotated but unsigned.
4. Releases are GitHub prereleases.
5. The audit proves empty-local-cache network cold start, not offline
   installation.
6. Lane E owns the full deployed interaction/accessibility/privacy/network
   audit. This lane checked Pages provenance and byte identity, not every
   manual interaction.

## Evidence locations

- GitHub metadata, annotated-tag objects, workflow/deployment JSON:
  `/private/tmp/cc-mig-11-cd-corrected-metadata.j1B9me`
- Corrected cold clones and command logs:
  `/private/tmp/cc-mig-11-cd-corrected-*`
- Downloaded release assets and comparisons:
  `/private/tmp/cc-mig-11-cd-corrected-artifacts.w58MSh`
- Live Pages manifests/static files and headers:
  `/private/tmp/cc-mig-11-cd-corrected-live.lyCoa3`

## Lane verdict

**Lane C: PASS for the eight audited corrected tags. Lane D: PASS for the
seven published corrected releases and their live sites; BLOCKED for integrated
`v0.2.1` release assets by failed workflow `30548681294`. The original
five-app Pages provenance blocker is cleared. Portfolio completion still
awaits a successful integrated release and catalog `v0.1.1`.**
