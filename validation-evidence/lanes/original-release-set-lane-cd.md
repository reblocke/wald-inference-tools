# CC-MIG-11 independent audit evidence: lanes C and D

Audit snapshot: 2026-07-30T13:03:39Z
Auditor scope: lane C cold-start reproducibility and lane D release-artifact provenance only
Production/repository mutation: none

This ledger is intentionally frozen to the release set resolved at the audit
snapshot. Releases created afterward—including core `v0.4.1` and any focused
app patch releases—are outside this result and require the planned bounded
recheck before they can clear the blocker.

## Decision

**Lane C: APPROVE. Lane D: BLOCK. Combined lane C/D contribution to the
portfolio release decision: NOT VALIDATED; RELEASE BLOCKERS REMAIN.**

All 16 published tags across the nine repositories passed corrected,
per-tag, isolated cold-clone verification. All 52 assets from the 15 releases
that publish assets matched both their `SHA256SUMS` files and GitHub's REST
SHA-256 digests. Core wheels and sdists passed release checks, and all six core
wheels passed clean installed-package scientific/API smoke tests.

The blocking exception is deployed-release traceability. The current GitHub
Pages deployments for five focused apps are built from post-release commits,
not from their `v0.1.0` release commits:

- `compatibility-curve`: deployed commit is 2 commits after `v0.1.0`.
- `wald-likelihood-support`: deployed commit is 2 commits after `v0.1.0`.
- `critical-effect-size`: deployed commit is 2 commits after `v0.1.0`.
- `type-s-m-calibrator`: deployed commit is 2 commits after `v0.1.0`.
- `precision-guardrail-planner`: deployed commit is 6 commits after `v0.1.0`.

Those post-tag HTML, documentation, tests, and—in the precision app—display
JavaScript changes do not appear in the `v0.1.0` source archives or their
`SHA256SUMS`. The live package manifests show that the staged Python package
and released core contents are unchanged apart from `source_commit`, which
limits the scientific blast radius, but it does not satisfy the ticket's
requirement that each Pages deployment be traceable to its release commit.

This report is a lane C/D finding, not a substitute for lanes A, B, E, or F.

## Success criteria applied

Lane C was considered successful only if every published tag:

1. resolved to an exact peeled commit;
2. cloned into its own new temporary parent;
3. synchronized from `uv.lock` without a sibling checkout or pre-populated
   package/browser cache;
4. passed its documented verification;
5. for browser repositories, installed Chromium and WebKit and served an HTTP
   200 response;
6. for core, passed `make verify` and `uv build`;
7. left no tracked worktree change.

Lane D was considered successful only if:

1. every published release asset matched published checksums;
2. core distributions and clean wheel installs passed;
3. application source archives matched tag trees;
4. generated browser manifests matched the released app/core packages and
   exact lock pins;
5. the live Pages deployment was traceable to the corresponding release
   commit and artifact set.

The last criterion fails for the five focused apps above.

## Method and isolation

- GitHub REST metadata was retrieved independently for repository heads,
  releases, tag refs, annotated tag objects, Pages configuration, deployments,
  deployment statuses, Actions runs, and tag-to-Pages comparisons.
- Each tag was cloned with
  `git clone --branch <tag> https://github.com/reblocke/<repo>.git <new-path>`.
  No shared migration worktree was used as test evidence.
- Each tag had its own initially empty `UV_CACHE_DIR`,
  `UV_PYTHON_INSTALL_DIR`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`,
  `PLAYWRIGHT_BROWSERS_PATH`, and npm cache. `PYTHONPATH`, `VIRTUAL_ENV`,
  `CONDA_PREFIX`, `UV_PYTHON`, and `UV_PROJECT_ENVIRONMENT` were unset;
  `PIP_CONFIG_FILE=/dev/null` and `PYTHONNOUSERSITE=1` were set.
- Project configuration and `.python-version` discovery remained enabled.
  This is essential to reproduce the repository contract.
- `make serve` is intentionally long-running. It was exercised with a bounded
  harness that started the documented target, required an HTTP 200 response
  from `/`, terminated it, and confirmed that no listener remained.
- Command output, start/finish timestamps, elapsed whole seconds, and exit
  codes are retained under each cold-clone parent.
- All runtime numbers below are observations from this machine, not benchmark
  guarantees.

### Exact command protocol and result counts

The literal cold-start command surface was:

```bash
git clone --branch <tag> https://github.com/reblocke/<repo>.git <new-path>
cd <new-path>
uv sync --locked
uv run playwright install chromium webkit  # browser repositories
make verify
make serve                                 # bounded HTTP 200 smoke
uv sync --locked --all-groups              # core, additionally
uv build                                   # core
git status --short
git diff --check
```

Artifact/provenance command surfaces included:

```bash
gh release download <tag> --repo reblocke/<repo> --dir <empty-directory>
shasum -a 256 -c SHA256SUMS
uv run python scripts/check_distribution.py <wheel> <sdist>  # core
uv run python scripts/smoke_installed_package.py <wheel>     # clean core venv
git archive --format=tar.gz --output=<path> <peeled-commit>
diff -ruN <released-archive-tree> <git-archive-tree>
```

The installed-wheel smoke script creates/uses a clean environment and verifies
the installed distribution rather than importing the source checkout.
Repository-specific staging commands are invoked by `make verify`; staged
package trees and manifests were then compared independently.

Result counts for this frozen audit snapshot:

- tag refs resolved and peeled: **16/16**;
- new-parent clones: **16/16 passed**;
- locked syncs: **16/16 passed**;
- full `make verify`: **16/16 passed**;
- browser installs: **10/10 passed**;
- bounded serve HTTP smokes: **10/10 passed**;
- explicit core `uv build`: **6/6 passed**;
- tracked-clean final states: **16/16**;
- releases with assets whose `SHA256SUMS` passed: **15/15**;
- downloaded asset REST digests matched: **52/52**;
- app release archive/tag-tree comparisons: **9/9 exact**;
- core wheel/sdist distribution checks: **6/6 passed**;
- clean installed core-wheel scientific/API smokes: **6/6 passed**;
- numerical app staged-core/released-wheel comparisons: **7/7 exact**;
- current Pages deployments at exact release commits: **3/8** app/template/catalog/integrated sites, with **5/8 blocked** by post-tag deploys.

### Discarded harness run

An earlier exploratory harness set `UV_NO_CONFIG=1`. That setting suppressed
the repositories' `.python-version`, selected CPython 3.14, and caused NumPy
source-build failures. It was a harness defect, not a repository defect. That
entire run was discarded and contributes no result to any table or verdict
below. Every tag was recloned and rerun with project configuration discovery
enabled. The corrected run selected the pinned Python versions and all 16
locked syncs passed.

## Environment

| Item | Observed value |
|---|---|
| OS | macOS 26.5.2, build 25F84 |
| Kernel | Darwin 25.5.0 |
| Architecture | arm64, Apple M2 |
| Git | 2.50.1 (Apple Git-155) |
| uv | 0.11.11, Homebrew aarch64 build |
| Node / npm | 25.9.0 / 11.12.1 |
| Core and integrated tags | `.python-version` 3.11; selected CPython 3.11.15 |
| Template, focused apps, catalog | `.python-version` 3.12; downloaded/selected CPython 3.12.13 |
| Core dependency profile | NumPy 2.2.6; SciPy 1.14.1; pytest 9.1.1; Ruff 0.16.0 |
| Integrated dependency profile | NumPy 2.2.6; SciPy 1.14.1; pytest 9.0.2; pytest-playwright 0.7.2; Ruff 0.15.1; Playwright 1.58.0 |
| Template/focused/catalog profile | focused apps: NumPy 2.2.6 and SciPy 1.14.1; all: pytest 8.4.2, pytest-playwright 0.8.0, Ruff 0.16.0, Playwright 1.61.0 |
| Integrated browser binaries | Chrome for Testing 145.0.7632.6 / Playwright Chromium revision 1208; WebKit 26.0 / revision 2248 |
| Template/focused/catalog browser binaries | Chrome for Testing 149.0.7827.55 / revision 1228; WebKit 26.5 / revision 2311 |

Exact complete dependency lists are in each
`/private/tmp/cc-mig-11-cd-literal-*/logs/uv-pip-list.log`; dependency trees
are in the adjacent `uv-tree.log`.

## Release and annotated-tag inventory

All 16 refs are annotated tag objects (`ref.object.type == "tag"`), not
lightweight tags. GitHub reports every tag object's verification as
`verified=false`, `reason=unsigned`. Unsigned tags are recorded as a
nonblocking provenance limitation because Ticket 11 does not require signed
tags. All releases are `draft=false`. All releases except the historical
pre-split baseline are marked `prerelease=true`.

| Repository | Release tag | Annotated tag object | Peeled commit | Release status | Assets |
|---|---|---|---|---|---:|
| `wald-inference-core` | `v0.1.0` | `7b4d606740ac65c29b2eca46494461b51438d44f` | `40a401e38d1876242400b743d288f9895850bbbf` | prerelease | 4 |
| `wald-inference-core` | `v0.1.1` | `8985f6b3344ba3f8d0c83b504a57a31d997fba6b` | `d1ffb0baa46eb8ad27175d58c90e4febc0ac2809` | prerelease | 4 |
| `wald-inference-core` | `v0.2.0` | `21ca4ef7f99453fe968ea3ea0a198d4601c99bf4` | `7de706b80127ed708b9f53a5be042750a14acdad` | prerelease | 4 |
| `wald-inference-core` | `v0.2.1` | `0ae6288bd36c7ddb58134bac9f6d225154ab0e48` | `4628a9ce9a6e051ce4b66e18e1d33536346696ac` | prerelease | 4 |
| `wald-inference-core` | `v0.3.0` | `be5306f7844981f73703f4a773dcd806dd4f464a` | `9618abf3a632838794e9e40752af7823e77115cb` | prerelease | 4 |
| `wald-inference-core` | `v0.4.0` | `59132c818b24026122ebda9a6105d272f0580868` | `fd7b24740122bed7ae07769674732c5e56c91277` | prerelease | 4 |
| `scientific-applet-template` | `v0.1.0` | `0c7fc277075da18a04903ced937313695c7a3678` | `a360bde95c192d8de4f9a3b531e73600ebf3d8b8` | prerelease | 3 |
| `compatibility-curve` | `v0.1.0` | `cd3fb8cc8b5d249921a9ff9d7ec3abf803b59f84` | `8945cfce61ecce29bdb6a922778f84d35fc4fe7f` | prerelease | 3 |
| `wald-likelihood-support` | `v0.1.0` | `9ec64072973e9d78486a3c5b1f5b344161b85101` | `b013abd2d512e1b041f089018649039b102a5c36` | prerelease | 3 |
| `critical-effect-size` | `v0.1.0` | `b84a2e374542a46ed93fb7f0c30149b822720ffd` | `b4e201b3b23072c66302c243551388d6eaa0436f` | prerelease | 3 |
| `type-s-m-calibrator` | `v0.1.0` | `70627b36c02fe9a2e8d84237031f34f2dbab11d4` | `2af70621c42b371d019ab360c17ade12c53e37c7` | prerelease | 3 |
| `precision-guardrail-planner` | `v0.1.0` | `060689ff19c7a810a70295fefb80e386735f9f93` | `b142950b164ec99c8ac6477eeefef62d686bf268` | prerelease | 3 |
| `wald-inference-tools` | `v0.1.0` | `4741919aef3c528e7e2d251e5b123a0743c30f71` | `bbb045044a531244516540e2bcffaeca44c5e9df` | prerelease | 4 |
| `conf_curve_likelihood` | `pre-split-baseline-2026-07-29` | `58855d85227864efb30b7e66a79c28cb13103608` | `5fd501dd947d9b951d736014cfc2b310efa5e7b0` | stable historical baseline | 0 |
| `conf_curve_likelihood` | `v0.1.1` | `d46687b2c48b6721f748a3f07fe7f7746be82a4a` | `201f4a57b337ab7a82e85d08aa458c775a5825da` | prerelease | 3 |
| `conf_curve_likelihood` | `v0.2.0` | `ea4f6c31d239bb44241164814012d3d4f2dfad66` | `5fbf609df072100905d2a86ecbd55b286b5fa090` | prerelease | 3 |

The historical pre-split release deliberately publishes no assets. That is
recorded as a historical limitation; current integrated `v0.2.0` does publish
a source archive, browser manifest, and checksums.

## Lane C cold-start matrix

Every command in this matrix exited 0. Clone times were 0–2 seconds.
`uv build` also exited 0 for every core tag and took 3 seconds per tag.

| Repository | Tag | Python | `uv sync --locked` | Browser install | `make verify` | Serve HTTP smoke | Final tracked status |
|---|---|---:|---:|---:|---:|---:|---|
| `wald-inference-core` | `v0.1.0` | 3.11.15 | 4 s | n/a | 135 s | n/a | clean |
| `wald-inference-core` | `v0.1.1` | 3.11.15 | 5 s | n/a | 127 s | n/a | clean |
| `wald-inference-core` | `v0.2.0` | 3.11.15 | 4 s | n/a | 127 s | n/a | clean |
| `wald-inference-core` | `v0.2.1` | 3.11.15 | 4 s | n/a | 128 s | n/a | clean |
| `wald-inference-core` | `v0.3.0` | 3.11.15 | 9 s | n/a | 126 s | n/a | clean |
| `wald-inference-core` | `v0.4.0` | 3.11.15 | 9 s | n/a | 129 s | n/a | clean |
| `scientific-applet-template` | `v0.1.0` | 3.12.13 | 10 s | 36 s | 68 s | 1 s | clean |
| `compatibility-curve` | `v0.1.0` | 3.12.13 | 7 s | 37 s | 228 s | 2 s | clean |
| `wald-likelihood-support` | `v0.1.0` | 3.12.13 | 7 s | 19 s | 164 s | 2 s | clean |
| `critical-effect-size` | `v0.1.0` | 3.12.13 | 10 s | 40 s | 287 s | 1 s | clean |
| `type-s-m-calibrator` | `v0.1.0` | 3.12.13 | 13 s | 35 s | 281 s | 1 s | clean |
| `precision-guardrail-planner` | `v0.1.0` | 3.12.13 | 11 s | 32 s | 237 s | 1 s | clean |
| `wald-inference-tools` | `v0.1.0` | 3.12.13 | 5 s | 31 s | 73 s | 0 s | clean |
| `conf_curve_likelihood` | `pre-split-baseline-2026-07-29` | 3.11.15 | 12 s | 39 s | 574 s | 0 s | clean |
| `conf_curve_likelihood` | `v0.1.1` | 3.11.15 | 13 s | 34 s | 614 s | 5 s | clean |
| `conf_curve_likelihood` | `v0.2.0` | 3.11.15 | 9 s | 30 s | 598 s | 2 s | clean |

The integrated historical suites were slower primarily while starting and
exercising Pyodide workers. This is an observation, not a performance claim.

For all six core tags, `uv sync --locked --all-groups` also exited 0. Core
`make verify` invokes formatting/lint, metadata, unit/property/parity,
distribution build, and installed smoke targets. Browser `make verify` targets
invoke their documented staging, format-check/lint, Python tests, Chromium
E2E, and WebKit smoke contracts. Generated outputs were ignored (`.venv`,
caches, staged `web/assets/py`, core `dist`/reports, and catalog `site`);
`git status --short` remained empty and `git diff --check` exited 0.

### Standalone README/validation commands exercised

In addition to the complete `make verify` targets:

| Repository/tag | Standalone documented check | Exit | Runtime |
|---|---|---:|---:|
| `compatibility-curve@v0.1.0` | legacy compatibility regression test | 0 | 3 s |
| `type-s-m-calibrator@v0.1.0` | `make scientific-test` | 0 | 3 s |
| `precision-guardrail-planner@v0.1.0` | scientific-reference and regression suites | 0 | 3 s |
| `conf_curve_likelihood@v0.2.0` | live portfolio-link checker | 0 | 4 s |
| `wald-inference-tools@v0.1.0` | `make live-check` | 0 | 13 s |
| `scientific-applet-template@v0.1.0` | `make template-self-test` | 0 | 21 s |

The template README initializer was also run literally in a separate disposable
fresh clone with the documented compatibility-curve arguments. It exited 0 and
left no unresolved required template values. Its intentional generated edits
were confined to
`/private/tmp/cc-mig-11-cd-readme-template-init.MUADrn`.

## Lane D artifact results

### Released files and checksums

- 52 assets were downloaded from 15 releases; the pre-split baseline has no
  assets by release design.
- All 15 `SHA256SUMS` manifests passed `shasum -a 256 -c`.
- Each of the 52 local file hashes also matched the corresponding GitHub REST
  `assets[].digest` value exactly.
- All nine released app source archives—template, five focused apps, catalog,
  and integrated `v0.1.1`/`v0.2.0`—were tree-exact to a fresh `git archive`
  from their peeled tag commits. Each recursive diff exited 0.
- Freshly generated tag browser manifests matched the released manifest assets
  byte-for-byte for the template, all five focused apps, and integrated
  `v0.1.1`/`v0.2.0`.

### Core distributions and clean installs

Every released core wheel/sdist pair passed the corresponding tag's
`scripts/check_distribution.py`. Every released wheel was then installed into
a clean temporary environment and exercised with that tag's
`scripts/smoke_installed_package.py`; all public API/scientific smokes exited 0.

| Core tag | Released wheel SHA-256 | Distribution check | Clean wheel smoke |
|---|---|---:|---:|
| `v0.1.0` | `932b7f9203127ef955cfc1c0aa2165307a435506d24254a0de85ba7a0d1d24c2` | pass | pass, 68 s |
| `v0.1.1` | `95bc10d770836544d726362c401032e0640a5a9ec1573f043add7f6bd3a65457` | pass | pass, 68 s |
| `v0.2.0` | `3d1cd3f3c48478bcd898a60c7ac0c645e808b5f98bd6f843d0c75ef954cec2ab` | pass | pass, 68 s |
| `v0.2.1` | `dcede569ff923061313635f2f680de9e3f8d1ea9415ef1b9391a0756023212fc` | pass | pass, 90 s |
| `v0.3.0` | `630fdece13c2940f751d1f5d3a4d6477182dbb099131a9907ceef7067348f939` | pass | pass, 87 s |
| `v0.4.0` | `401a0cc2a182918764149eb03c79672217b647147c494215c83515fd609c7af6` | pass | pass, 87 s |

The latest `v0.4.0` clean install independently reported
`wald-inference==0.4.0`, NumPy 2.2.6, SciPy 1.14.1, a passing `uv pip check`,
and a passing cold-wheel public API smoke.

### App lock/core/manifest provenance

| App release | Locked/staged core | Released core wheel SHA-256 | Staged core vs released wheel |
|---|---|---|---|
| `compatibility-curve@v0.1.0` | `wald-inference==0.1.1` | `95bc10d770836544d726362c401032e0640a5a9ec1573f043add7f6bd3a65457` | exact file-tree match |
| `wald-likelihood-support@v0.1.0` | `wald-inference==0.2.1` | `dcede569ff923061313635f2f680de9e3f8d1ea9415ef1b9391a0756023212fc` | exact file-tree match |
| `critical-effect-size@v0.1.0` | `wald-inference==0.3.0` | `630fdece13c2940f751d1f5d3a4d6477182dbb099131a9907ceef7067348f939` | exact file-tree match |
| `type-s-m-calibrator@v0.1.0` | `wald-inference==0.3.0` | `630fdece13c2940f751d1f5d3a4d6477182dbb099131a9907ceef7067348f939` | exact file-tree match |
| `precision-guardrail-planner@v0.1.0` | `wald-inference==0.4.0` | `401a0cc2a182918764149eb03c79672217b647147c494215c83515fd609c7af6` | exact file-tree match |
| `conf_curve_likelihood@v0.1.1` | `wald-inference==0.1.1` | `95bc10d770836544d726362c401032e0640a5a9ec1573f043add7f6bd3a65457` | exact file-tree match |
| `conf_curve_likelihood@v0.2.0` | `wald-inference==0.4.0` | `401a0cc2a182918764149eb03c79672217b647147c494215c83515fd609c7af6` | exact file-tree match |

The pre-split baseline contains the historical monolith and has no external
core pin. The template and catalog intentionally contain no runtime numerical
core. The focused manifests directly record core wheel URL and artifact hash.
The integrated manifest records the complete per-file core hashes but not an
artifact URL/hash field; its `uv.lock` contains the exact released wheel URL
and hash, and the staged core file tree was independently exact to that wheel.
No app contained a hand-edited external core copy.

## Current Pages provenance matrix

All eight Pages repositories use the `main` branch at `/`. The latest `Deploy
Pages` Actions run for every repository was a completed, successful push run.
The catalog's live `data/tools.json` SHA-256 is
`b63b3c8ea5bf6f67ee150f24ec842535b868f1046f1ce5116eb650dae65a2308`,
byte-exact to the released `tools-v0.1.0.json`.

| Repository | Release tag commit | Current Pages commit | Delta from release | Latest Pages run | Result |
|---|---|---|---:|---:|---|
| `scientific-applet-template` | `a360bde95c192d8de4f9a3b531e73600ebf3d8b8` | `a360bde95c192d8de4f9a3b531e73600ebf3d8b8` | exact | `30515046977` | pass |
| `compatibility-curve` | `8945cfce61ecce29bdb6a922778f84d35fc4fe7f` | `3cfc31b7e76bf857a6f640fefd4d77398c0bf192` | +2 commits | `30533359139` | **block** |
| `wald-likelihood-support` | `b013abd2d512e1b041f089018649039b102a5c36` | `20a9046462f649f6fccc222a1d29aacd49c24ab9` | +2 commits | `30533365312` | **block** |
| `critical-effect-size` | `b4e201b3b23072c66302c243551388d6eaa0436f` | `cad4eaa6caa63dac550ddbde34b62e6faa032eb7` | +2 commits | `30533767648` | **block** |
| `type-s-m-calibrator` | `2af70621c42b371d019ab360c17ade12c53e37c7` | `5b23961d32bd0e94a6abf80c786a76f3fc3531e3` | +2 commits | `30533767116` | **block** |
| `precision-guardrail-planner` | `b142950b164ec99c8ac6477eeefef62d686bf268` | `cb38276dff79d1ce5085b90457c980a519d7ab31` | +6 commits | `30536349743` | **block** |
| `wald-inference-tools` | `bbb045044a531244516540e2bcffaeca44c5e9df` | `bbb045044a531244516540e2bcffaeca44c5e9df` | exact | `30541243239` | pass |
| `conf_curve_likelihood` | `5fbf609df072100905d2a86ecbd55b286b5fa090` | `5fbf609df072100905d2a86ecbd55b286b5fa090` | exact | `30540400728` | pass |

`wald-inference-core` has no Pages site, as expected; current `main` and
`v0.4.0` both resolve to
`fd7b24740122bed7ae07769674732c5e56c91277`.

### Exact post-tag changes

| Repository | Non-merge post-tag commit(s) | Files changed from release tag to deployed commit |
|---|---|---|
| `compatibility-curve` | `14146f63fb2f7dc0e35ad3ae41e236afa4da142e` (`docs: add portfolio navigation links`) | `README.md`, `tests/integration/test_browser_policy.py`, `web/index.html` |
| `wald-likelihood-support` | `53dea14ea1d0c3089266edb42d893580cabeb764` (`docs: add portfolio navigation links`) | `README.md`, `tests/integration/test_browser_policy.py`, `web/index.html` |
| `critical-effect-size` | `615f7fbae2ff35a0b94edff5a9b4aa9e9596979d` (`docs: link related Wald tools`) | `README.md`, `tests/integration/test_repository_policy.py`, `web/index.html` |
| `type-s-m-calibrator` | `41c1706c3fb4ce32bbf5d0a054d268f8cf778160` (`docs: link related Wald tools`) | `README.md`, `tests/integration/test_repository_policy.py`, `web/index.html` |
| `precision-guardrail-planner` | `fc4495c84005011ae7928ee1b8ba776572dffaac`, `7d4b9e6f35ad43d79887483b8c951293110cfad4`, `c5c0847e273a76a738a705e9addedb4e97178c85` plus their three merge commits | `README.md`, `tests/e2e/test_applet.py`, browser/repository policy tests, `web/app.js`, `web/index.html` |

The live template and integrated manifests are byte-exact to their release
manifest assets. For every focused app, the live manifest differs from its
release manifest only in `source_commit`: sorting the JSON and deleting that
field produces an exact hash match. This is affirmative evidence that the
deployed staged Python/app/core package set did not drift, but it also
affirmatively records that the containing Pages source commit did drift.

## Findings, limitations, and hidden assumptions

### Blocking

1. **Five focused Pages deployments are not release-commit deployments.**
   Their current deployed commits and web source bytes are absent from the
   only published app releases and checksums. Git history makes the pages
   commit-traceable, but not release-artifact-traceable. Lane D therefore
   cannot pass.

### Nonblocking

1. All current portfolio releases are GitHub prereleases; the historical
   pre-split baseline is the only non-prerelease.
2. All annotated tags are unsigned. Exact object and peeled commit resolution
   was independently verified, but cryptographic signer identity was not.
3. The historical pre-split baseline has no release assets or browser manifest.
   The current integrated release does.
4. The integrated browser manifest omits direct artifact URL/hash fields while
   retaining complete per-file hashes; the exact URL/hash is in `uv.lock` and
   the staged package was independently compared to the released wheel.
5. The test used real network access to GitHub, PyPI/uv sources, Playwright
   CDNs, and live Pages. It proved empty local-cache cold start, not an offline
   build.
6. The 3.11 repositories selected an already installed Homebrew CPython
   3.11.15; all Python packages were nevertheless created in fresh per-tag
   environments. The 3.12 repositories downloaded a fresh uv-managed
   CPython 3.12.13.
7. This lane did not duplicate the full manual deployed-site interaction,
   accessibility, network/privacy, scientific formula, cross-app parity, or
   documentation/rights audits assigned to other Ticket 11 lanes.

## Required remediation and rerun

Recommended smallest provenance-preserving remedy:

1. Create new releases for the five focused apps at the exact commits currently
   deployed (for example, a patch version rather than moving existing tags).
2. Regenerate and publish each source archive, browser-stage manifest, and
   `SHA256SUMS`; ensure the manifest `source_commit` is the new peeled release
   commit.
3. Update the catalog version/commit records if the focused versions change,
   release the catalog if its recorded artifact changes, and deploy only the
   exact released commit.
4. Independently rerun tag resolution, cold clone, locked sync, Playwright
   install, `make verify`, serve smoke, asset checksum, archive/tree
   comparison, staged-core/wheel comparison, and live Pages commit/manifest
   checks.

An alternative is to redeploy the exact existing `v0.1.0` commits, but that
would remove the later cross-tool navigation/display corrections. Either
remedy must end with equality among the peeled release commit, current Pages
run `head_sha`, live manifest `source_commit`, and checksum-addressed release
artifact contents.

Do not mark the portfolio validation passed until that remediation has been
released, deployed, and independently rerun.

## Evidence locations

- GitHub metadata and comparison JSON:
  `/private/tmp/cc-mig-11-cd-metadata.7P0yp9`
- Corrected per-tag cold clones, command logs, and command metadata:
  `/private/tmp/cc-mig-11-cd-literal-*`
- Downloaded release assets and checksum logs:
  `/private/tmp/cc-mig-11-cd-artifacts.4D6x4f`
- App source-archive versus `git archive` comparisons:
  `/private/tmp/cc-mig-11-cd-archive-compare-*`
- Staged core versus released-wheel comparisons:
  `/private/tmp/cc-mig-11-cd-core-stage-*`
- Live Pages manifests, response headers, and catalog data:
  `/private/tmp/cc-mig-11-cd-live-manifests.y6nq3C`
- Disposable literal template-initializer clone:
  `/private/tmp/cc-mig-11-cd-readme-template-init.MUADrn`

## Final lane verdict

**NOT VALIDATED; RELEASE BLOCKERS REMAIN.** Lane C is reproducible and passes.
Lane D remains blocked only because five focused production Pages deployments
do not correspond to their published release commits/artifact sets.
