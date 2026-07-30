# CC-MIG-11 corrected-set Lane A/B independent rerun

Validated through: 2026-07-30T13:56:09Z
Fresh audit root: `/private/tmp/cc-mig-11-corrected-ab.uJMMgi`
Lanes: A — numerical/scientific; B — B01-B08 and cross-app parity
Production/GitHub mutations by reviewer: none

## Verdict

**GO for the corrected scientific set in Lane A/B.**

No numerical, scientific-formula-ownership, frozen-parity, focused-scope, dependency-pin, or
browser-staging blocker remains in the independently rerun corrected refs:

- `wald-inference` v0.4.1;
- all five focused v0.1.1 releases; and
- integrated `conf_curve_likelihood` v0.2.1.

The three release-blocking defects found in the initial set are independently closed:

1. all eight finite nonmonotone precision bands are found in both directions;
2. compound pairwise support delegates to the canonical exact-binary64 ratio while preserving its
   required individual-field finite-range error; and
3. strict public ratio back-transforms reject natural-zero underflow while the frozen legacy
   surface retains its prior behavior.

This is a Lane A/B verdict, not by itself the final portfolio release verdict. The only genuinely
pending publication checks observed at handoff are listed at the end.

## Exact corrected refs

Each annotated tag was independently resolved with `git ls-remote`, peeled, and cloned into a new
directory. Every tag checkout was detached, at the exact target, and clean.

| repository | tag | annotated tag object | peeled commit | GitHub Release |
|---|---|---|---|---|
| `reblocke/wald-inference-core` | v0.4.1 | `838c4aaab08570a17156bd59b1ff65dcabf56bfc` | `f4613177b6dc81d194aa70762152de2bfa86663b` | published prerelease |
| `reblocke/compatibility-curve` | v0.1.1 | `abed9da076fbc47b5e410df204bdf8c1de16e278` | `12a13e78953258c2d3ad09d0846de49e86151636` | published prerelease |
| `reblocke/wald-likelihood-support` | v0.1.1 | `4a7f510d146930ca35d4a8ddd858c007919749c3` | `c2fc494d600e0d0af5b70897f69de19fa81f38f4` | published prerelease |
| `reblocke/critical-effect-size` | v0.1.1 | `291e219567f6067ec45495e590b96710685ea271` | `00014f5c3995f5296dd372d97852ae8c202c1e6a` | published prerelease |
| `reblocke/type-s-m-calibrator` | v0.1.1 | `83d28108b6d12090379864f05bb2c49597eaf0f9` | `1b3f22fe7f86b9e52754ad81ed7800b6e313c6fb` | published prerelease |
| `reblocke/precision-guardrail-planner` | v0.1.1 | `5eaac5cfd616a94b90b2110a54ec3197cd797dff` | `bfc54c5d4d79e497fb145e931f9f562b31938616` | published prerelease |
| `reblocke/conf_curve_likelihood` | v0.2.1 | `044a2b89f00ad9678750cec3322f2c8d2feb7fa0` | `daae30681d1ac8c7c13a7afc085b13e0b56d23d2` | tag published; Release object absent at audit time |

The integrated commit was first tested from a fresh `main` clone while the tag was pending. After
the tag appeared, the reviewer independently peeled it, made a second fresh tag clone, and reran
the locked install, staging, 22-case comparator, and complete non-E2E suite. The tag clone produced
the same results and bundle hashes.

## Environment

- macOS 26.5.2 build 25F84
- Darwin 25.5.0, arm64
- Git 2.50.1 (Apple Git-155)
- uv 0.11.11
- system Python 3.14.4
- Core/integrated locked interpreter: CPython 3.11.10
- focused locked interpreter: CPython 3.12.13
- Core numerical dependencies: NumPy 2.2.6, SciPy 1.14.1

## Core v0.4.1 release gate

From the fresh v0.4.1 tag checkout:

```text
uv sync --locked --all-groups
make verify
```

Exit status: 0.

`make verify` passed:

- Ruff format check;
- Ruff lint;
- release metadata consistency;
- complete pytest suite;
- frozen baseline parity;
- wheel and sdist build/content inspection;
- cold-wheel environment install and public API smoke; and
- `git diff --check`.

The released wheel used by all consumers is:

```text
URL:
https://github.com/reblocke/wald-inference-core/releases/download/v0.4.1/
wald_inference-0.4.1-py3-none-any.whl

SHA-256:
d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b
```

The GitHub Release API reports the same digest. A direct recursive comparison between the installed
release wheel package and the v0.4.1 tagged `src/wald_inference` directory, excluding bytecode,
returned no differences.

## Independent adversarial repair rerun

### Nonmonotone precision search

Independent vectorized scan:

- 8,001 log-spaced information multipliers from 1 to `1e12`;
- adjacent multiplier factor `1.0034598491478393`;
- 9 rule/direction configurations covering all six selection rules;
- 12 positive/negative assumed effects;
- 6 current SE values;
- 14 probability/Type-S/Type-M targets;
- 9,072 target paths.

Result:

```text
independently predicted skipped-band cases = 8
public Core false-infeasibility results    = 0
within-piece metric direction changes     = 0
```

All eight former repros now return the analytically expected finite band:

| effect/direction | current SE | target | independent largest root | Core required SE | conservative relative gap |
|---|---:|---:|---:|---:|---:|
| +0.4 / positive | 5 | 0.1 | 0.58961184789672971 | 0.58961184396002020 | `6.6767815605687823e-9` |
| +0.4 / positive | 10 | 0.1 | 0.58961184789672982 | 0.58961184649745291 | `2.3732170945170036e-9` |
| +0.6 / positive | 5 | 0.2 | 0.53650814965369187 | 0.53650814691436910 | `5.1058362680738081e-9` |
| +0.6 / positive | 10 | 0.2 | 0.53650814965369187 | 0.53650814771411182 | `3.6151921520218698e-9` |
| -0.4 / negative | 5 | 0.1 | 0.58961184789672971 | 0.58961184396002020 | `6.6767815605687823e-9` |
| -0.4 / negative | 10 | 0.1 | 0.58961184789672982 | 0.58961184649745291 | `2.3732170945170036e-9` |
| -0.6 / negative | 5 | 0.2 | 0.53650814965369187 | 0.53650814691436910 | `5.1058362680738081e-9` |
| -0.6 / negative | 10 | 0.2 | 0.53650814965369187 | 0.53650814771411182 | `3.6151921520218698e-9` |

Positive/negative required SEs are bitwise mirror-equal. In every case, multiplying the returned SE
by `1+1e-6` fails and multiplying it by `1-1e-6` passes. At the exact cutoff transition:

- returned SE is one ULP from `1/z_.975`;
- the rounded satisfying plateau extends only one additional SE float;
- the next representable target probability above the maximum is infeasible.

The focused precision v0.1.1 contract was separately invoked for all eight cases. Every row and
joint result is feasible, and every app required SE is exactly equal to the installed Core result.

### Pairwise support

Independent exact-Fraction recomputation and compound-object checks passed:

| A/B/center/SE | expected and observed log L(A)/L(B) |
|---|---:|
| ordinary B01-like input | `3.2378581110949436` |
| `1e100`, `-1e100`, center 1, SE 1 | `2e100` |
| adjacent floats at `1e150`, center 0, SE 1 | `1.8170968107390175e284` |
| adjacent floats at `1e154`, center 0, SE 1 | `1.4885657073574032e292` |
| 0, `1e100`, center 0, SE 1 | `5e199`; exponentiated display ratio `None` |

`support_comparison(1e155, -1e155, center=0, SE=1)` still raises
`Log relative likelihood exceeds the finite floating-point range.` because required individual
candidate/reference-to-MLE fields are unrepresentable. Standalone canonical `log_support_ratio`
remains finite zero. The repair therefore fixes only the pairwise field and preserves the compound
object’s finite-range contract.

### Ratio back-transform underflow

Fresh v0.4.1 results:

```text
strict from_working_scale("odds_ratio", -745)  -> 5e-324
strict from_working_scale("odds_ratio", -746)  -> ValidationError
legacy from_working_scale("odds_ratio", -746)  -> 0.0
```

The complete Core suite covers all five ratio measures and mixed vectors. The strict public domain
is positive; the explicitly frozen legacy adapter remains backward compatible.

## Formula ownership

Lane-A source review remains GO.

- Effect registry and identity/log transforms: `effects.py`
- CI reconstruction: `reconstruction.py`
- standardized distance and compatibility: `compatibility.py`
- normalized/log support, S−2/generic intervals, pairwise ratios: `likelihood.py`
- legacy and exact detectability: `detectability.py`
- six selection-rule definitions: `selection.py`
- Type S, Type M, observed exaggeration: `type_sm.py`
- information scaling and per-target/joint precision: `precision.py`

Focused-source scans found only imports/delegation from root-public `wald_inference`; no focused
source imports SciPy or contains a local Wald, normal-tail, support, detectability, Type-S/M, or
precision formula. Focused scientific-ownership and exact-contract tests pass.

The integrated repository retains compatibility-shaped dataclasses and aliases but delegates
numerical work to the released Core/root-public or documented legacy surface. Its two preserved
`z975` signature defaults are passed to Core and do not implement a formula.

One documented internal numerical-contract distinction remains:

- detectability’s public probability/inversion/achieved-probability path uses a conservative
  certified binary64 kernel; and
- frozen conditional Type-S/M moments use direct selection-interval probability in their
  conditioning denominator.

Both use the sole six-rule event definition in `selection.py`. This is a rounding/certification
distinction within the one Core owner, not a second rule/formula implementation or a cross-repo
fork. An attempted consolidation would weaken the existing direct tail/moment reference identities
and was correctly not adopted.

## B01-B08 frozen parity

### Core projection

Fresh v0.4.1 Core oracle:

```text
successful Core-value cases = 14
matched Core-error cases    = 6
explicit app-only errors    = 2
values compared             = 23,095
max absolute difference     = 5.3290705182007514e-15
max relative difference     = 4.4493725366481632e-16
rtol / atol                 = 1e-12 / 1e-14
```

### Integrated v0.2.1 full responses

The native 22-case generator check and comparator pass. A separate recursive audit compared 27,268
stored/actual float leaves:

| case | maximum absolute difference | maximum relative difference |
|---|---:|---:|
| B01 | `5.3290705182007514e-15` | `4.1266019082733676e-16` |
| B02 | `5.3290705182007514e-15` | `4.4493725366481632e-16` |
| B03 | `5.3290705182007514e-15` | `4.4493725366481632e-16` |
| B04 | `5.3290705182007514e-15` | `4.1266019082733676e-16` |
| B05 | 0 | 0 |
| B06 | 0 | 0 |
| B07a/B07b/B07c | 0 | 0 |
| B07d-B07j | exact expected errors; no float leaves | exact |
| B07k | `5.3290705182007514e-15` | `4.1266019082733676e-16` |
| B08a-B08d | 0 | 0 |
| B08e | exact expected error; no float leaves | exact |

The nonzero path is the corrected canonical
`threshold_support_summaries[0].likelihood_ratio_threshold_to_null`. It is the intended
single-rounding repair and remains inside the frozen tolerance contract.

Overall integrated maxima:

```text
max absolute = 5.3290705182007514e-15
path         = B01/B02/B03/B04/B07k threshold-to-null support ratio

max relative = 4.4493725366481632e-16
path         = B02/B03 threshold-to-null support ratio
```

### Focused-subset differences

| app contract | recomputed numeric anchors | max absolute difference | max relative difference | result |
|---|---:|---:|---:|---|
| compatibility | 35 | 0 | 0 | pass |
| likelihood/S−2 | 21 | `1.4210854715202004e-14` | `4.4493725366481632e-16` | pass |
| critical exact/legacy | 4 | `2.3314683517128287e-14` | `4.0338449175803973e-14` | pass |
| Type S/M | 49 | `3.9968028886505635e-15` | `1.1027325787414086e-14` | pass |
| precision B06 | 22 | 0 | 0 | pass |

Focused maxima locators:

- likelihood absolute: B01 displayed MLE/null ratio,
  `33.97645283375536` versus `33.976452833755374`;
- likelihood relative: B02 threshold/null ratio,
  `11.977128177752659` versus `11.977128177752654`;
- critical absolute: log-scale exact positive effect,
  `0.5795737427348193` versus `0.5795737427348426`;
- critical relative: additive exact positive effect,
  `0.44311546580689903` versus `0.4431154658069169`;
- Type S/M absolute: B04 true effect 0.3 selected probability,
  `0.4748512734696006` versus `0.4748512734696046`;
- Type S/M relative: B04 true effect 0.1 selected probability,
  `0.0969037898944932` versus `0.09690378989449427`.

B07 precision null and threshold-infeasibility messages match exactly.

## Cross-app scope separation

Complete app suites and explicit targeted scope tests pass:

- compatibility response is exact, ordered, compatibility-only; `design_enabled` is rejected;
- likelihood response has only the focused reconstruction/support/grid/pairwise families and its
  contract delegates every scientific operation to root-public Core APIs;
- critical response exposes exact detectability as primary and legacy benchmark as separately
  labeled optional context;
- Type S/M response has exact focused top-level/grid keys and contains no inverse-precision or
  observed-evidence families;
- precision response contains guardrail/sensitivity output but no compatibility, likelihood,
  S−2, or full Type-S/M calibration panels.

Targeted command exit statuses were all 0:

```text
compatibility: 3 explicit ownership/scope tests
likelihood:    2 explicit delegation/scope tests
critical:      1 exact-contract test
Type S/M:      2 exact/out-of-scope contract tests
precision:     2 exact/prohibited-family contract tests
```

## Core pin and staged-package identity

Every corrected consumer lock contains:

```text
wald-inference 0.4.1
wheel URL .../releases/download/v0.4.1/wald_inference-0.4.1-py3-none-any.whl
wheel SHA-256 d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b
```

Every staged manifest contains 14 Core files. The staged Core package digest is identical across the
five focused apps:

```text
44c52ba0189155e0d976e283d383f17f3db0679563ec6dc6d45b9829c4a43b4d
```

After recursively sorting manifest keys, the `{version, files}` Core projections from all six
consumers, including integrated v0.2.1, have identical SHA-256:

```text
8dc3ff5dbeddaa4c9e01a48ea688684bc18c44bb2d57ea4a4dbf4a8d31d3bc00
```

Staging details:

| consumer | staged source commit | bundle SHA-256 | generated manifest SHA-256 | released manifest match |
|---|---|---|---|---|
| compatibility v0.1.1 | `12a13e78953258c2d3ad09d0846de49e86151636` | `95e6600f5788462f0e5ce8def8f42131e21298f08bbcc341ac84aec2c41101da` | `4deda63fc239611f27a45f5d56dddd9ce9927744dcdaa8579130f00d3359d8d6` | exact |
| likelihood v0.1.1 | `c2fc494d600e0d0af5b70897f69de19fa81f38f4` | `bdad1a100e2116612b179bda42ba5afc0edb050a9b180760ebd4fe84d5d55ef3` | `0445134f8b646b065e3daec9b137b0a08a608cd60cc0dcec9788a4f848c4faf5` | exact |
| critical v0.1.1 | `00014f5c3995f5296dd372d97852ae8c202c1e6a` | `976673533e7349454f4d4089eab3df8cdc190fde01784ad36188457ca4f874c0` | `1cd38c1bd852338c86ec57abb5970350b86edd14aa00259bfb8b5b5a86a05baf` | exact |
| Type S/M v0.1.1 | `1b3f22fe7f86b9e52754ad81ed7800b6e313c6fb` | `55f5293e76a836977048ea929f56eb31d8d27826746546c42e05355fc28b0cbc` | `365dce54bc7011d40357edd9e832fb989ad007ab9b9190cf9de409b1f596be0e` | exact |
| precision v0.1.1 | `bfc54c5d4d79e497fb145e931f9f562b31938616` | `bee9d58f4e5d695716b925f899e7c9a779dc13560f827847f0afcddb6abb5a47` | `9701e2e397e7e7f70476003451f0ec5f54e98c3b35b49ceff58cf4836f5dcc89` | exact |
| integrated v0.2.1 | `daae30681d1ac8c7c13a7afc085b13e0b56d23d2` | `51d8a75483e261244c71073c73bf05a9eb5faa26ab8ec2330ce741e396781460` | `d4d8bd51eb857d40d0e582dc7e6f40534d2c58a30d5a8970e3cd44f9b2970a0e` | release asset pending |

The focused manifest hashes exactly match the corresponding GitHub Release manifest-asset digests.
The integrated manifest is locally deterministic across both fresh clones; its GitHub Release
asset cannot yet be checked because the Release object is absent.

## Locked test matrix

| ref | install command | numerical/parity command | exit |
|---|---|---|---:|
| Core v0.4.1 | `uv sync --locked --all-groups` | `make verify` | 0 |
| compatibility v0.1.1 | `uv sync --locked` | `make test` | 0 |
| likelihood v0.1.1 | `uv sync --locked` | `make test` | 0 |
| critical v0.1.1 | `uv sync --locked` | `make test` | 0 |
| Type S/M v0.1.1 | `uv sync --locked` | `make test` | 0 |
| precision v0.1.1 | `uv sync --locked` | `make test` | 0 |
| integrated v0.2.1 fresh tag clone | `uv sync --locked` | `make test` | 0 |

All seven checkouts remain clean after ignored/generated verification output; `git diff --check`
passes in every checkout.

## Exact command ledger

Ref resolution and clean clones:

```text
git ls-remote --tags --heads https://github.com/reblocke/<repo>.git \
  refs/tags/<tag> refs/tags/<tag>^{} refs/heads/main
git clone --depth 1 --branch <tag> https://github.com/reblocke/<repo>.git <fresh-dir>
git rev-parse HEAD
git describe --tags --exact-match
git status --short
```

Core:

```text
uv sync --locked --all-groups
make verify
PYTHONPATH=src .venv/bin/python audit_precision_all_rules.py
PYTHONPATH=src .venv/bin/python audit_patched_precision_boundaries.py
PYTHONPATH=src .venv/bin/python audit_patched_support_comparison.py
uv run python -c '<strict and legacy underflow boundary check>'
diff -qr --exclude='__pycache__' \
  core/src/wald_inference \
  compatibility/.venv/lib/python3.12/site-packages/wald_inference
```

Consumers:

```text
uv sync --locked
make test
.venv/bin/python audit_focused_diffs.py <app>
.venv/bin/python audit_precision_app_repairs.py
.venv/bin/python audit_integrated_diff.py
uv run pytest -q <explicit focused scope/ownership tests>
jq -Sc '.packages[] | select(.distribution == "wald-inference") | {version,files}' \
  web/assets/py/manifest.json | shasum -a 256
git status --short
git diff --check
```

Current release-object check:

```text
curl -fsSL \
  https://api.github.com/repos/reblocke/<repo>/releases/tags/<tag>
```

## Truly pending tag/release checks

1. **Integrated v0.2.1 GitHub Release object and assets.** The annotated tag exists and is fully
   Lane-A/B tested, but the GitHub Release API returned 404 at this audit timestamp. The locally
   deterministic browser-stage manifest therefore cannot yet be matched to a release asset.
2. **Catalog v0.1.1 live gate, outside Lane A/B.** `wald-inference-tools` still had no v0.1.1 tag
   or Release object; `main` remained at `bbb045044a531244516540e2bcffaeca44c5e9df`.

No Core, focused-app, or integrated-tag Lane A/B rerun remains pending.
