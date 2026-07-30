# CC-MIG-11 final-tag Lane A/B supplement

Audit completed: 2026-07-30T16:25:22Z
Scope: `reblocke/wald-inference-core` v0.4.1 and
`reblocke/wald-likelihood-support` v0.1.2
Lane: A (scientific/numerical) and B (frozen/cross-repository parity)
Reviewer work root: `/private/tmp/cc-mig-11-ab-final.TKbZWk`
Production or GitHub mutation: none

## Verdict

**GO — no Lane A/B release blocker found in either exact final tag.**

- Core v0.4.1 is the sole production owner of Wald reconstruction, normalized relative
  likelihood, pairwise support, and support-interval formulas.
- Wald Likelihood Support v0.1.2 imports only root-public Core APIs for scientific calculations.
  Its local code owns validation, payload assembly, display decisions, warnings, and exports; the
  independent static scan found no copied likelihood/support formula token and no private Core
  import.
- The published Core frozen-parity asset passes all 22 B01-B08 case families, and an independent
  fresh-tag rerun also passes without changing the declared tolerances.
- All 21 focused B01-B03 numerical anchors pass. S-minus-2, candidate A:B ordering, exact
  binary64 pairwise delegation, antisymmetry, identity, strict JSON, and six representative
  fail-closed errors pass.
- The app's staged Core tree is byte-for-byte equal to the v0.4.1 release wheel package tree.

This supplement does not replace browser, accessibility, deployment, documentation, or complete
portfolio validation lanes.

## Controlling evidence

- User ticket archive:
  `conf_curve_migration_codex_tickets.zip`
- Ticket archive SHA-256:
  `726d8fc86a21141d4cb734eaf7a09375e396e1d9c284d6c734e8a0d1438249d5`
- Extracted `tickets/11_independent_portfolio_validation.md` SHA-256:
  `acd60a30f7d20d9a7eafecd5091f06861fcc1d427b64d16c246791703032fc30`

## Exact immutable releases

Fresh clones were made in a new temporary parent. Each checkout is detached at the peeled commit,
and both `git cat-file -t` checks returned `tag`.

| Repository | annotated tag | tag object | peeled commit / `HEAD` | release |
|---|---|---|---|---|
| `reblocke/wald-inference-core` | `v0.4.1` | `838c4aaab08570a17156bd59b1ff65dcabf56bfc` | `f4613177b6dc81d194aa70762152de2bfa86663b` | prerelease published 2026-07-30T13:05:44Z |
| `reblocke/wald-likelihood-support` | `v0.1.2` | `5285b792379cb538bfa93859ecc9d18f07ec2dbb` | `7f5557d2a93235e25215261ef5890868b3fb07bb` | prerelease published 2026-07-30T15:08:44Z |

Tag subjects and tagger timestamps:

- Core: `wald-inference-core v0.4.1`, Brian Locke,
  `2026-07-30T07:04:37-06:00`.
- Likelihood: `Wald Likelihood Support v0.1.2`, Brian Locke,
  `2026-07-30T09:05:15-06:00`.

Live tag resolution through `git ls-remote` returned the same tag objects and peeled commits.

## Environment

- macOS 26.5.2 build 25F84; Darwin 25.5.0; arm64
- Git 2.50.1 (Apple Git-155)
- uv 0.11.11
- Core environment: CPython 3.11.10, NumPy 2.2.6, SciPy 1.14.1
- Likelihood environment: CPython 3.12.13, NumPy 2.2.6, SciPy 1.14.1
- Core package in the app environment:
  `.venv/lib/python3.12/site-packages/wald_inference`, version 0.4.1
- App package: editable exact-tag source, version 0.1.2

The app lock resolved Core only from:

```text
https://github.com/reblocke/wald-inference-core/releases/download/v0.4.1/wald_inference-0.4.1-py3-none-any.whl
```

The wheel SHA-256 is bound in package metadata, `uv.lock`, `browser-stage.toml`, documentation,
and tests. The installed Core package tree matched the extracted release-wheel package tree with
`diff -qr --exclude=__pycache__`; the same wheel tree also matched
`wald-inference-core@v0.4.1/src/wald_inference`.

## One-formula ownership

### Core owner map

The reviewed production ownership remains:

| Quantity | sole Core owner |
|---|---|
| effect registry and identity/log transforms | `src/wald_inference/effects.py` |
| CI midpoint and SE reconstruction | `src/wald_inference/reconstruction.py` |
| standardized distance and compatibility | `src/wald_inference/compatibility.py` |
| normalized/log relative likelihood, pairwise support, S-minus-2 and generic support intervals | `src/wald_inference/likelihood.py` |
| selection-event definitions | `src/wald_inference/selection.py` |
| Type S/M and observed exaggeration | `src/wald_inference/type_sm.py` |
| information scaling and inverse precision | `src/wald_inference/precision.py` |

The exact-source inspection confirmed:

- one definition each of `_relative_likelihood_kernel`,
  `_log_relative_likelihood_kernel`, `_log_support_ratio_kernel`,
  `relative_likelihood`, `log_relative_likelihood`, `log_support_ratio`,
  `support_ratio`, `support_comparison`, `support_interval`, and
  `support_interval_for_ratio`;
- the frozen `legacy` wrappers delegate to the shared private relative/log-likelihood kernels;
- `support_ratio` and `support_comparison` delegate the A:B value to
  `log_support_ratio`; and
- `support_interval_for_ratio` delegates interval construction to `support_interval`.

The previously documented internal selected-claim rounding distinction remains inside the one
Core repository: certified detectability inversion and the frozen direct Type-S/M conditioning
path share the sole selection-event definition but serve different binary64 contracts. It is not
a second cross-repository rule or formula fork.

### Focused app boundary

The app contract imports the following scientific operations only from the root
`wald_inference` package:

```text
build_grid
from_working_scale
get_effect_spec
log_relative_likelihood
log_support_ratio
max_safe_grid_span
reconstruct_wald_from_95_ci
relative_likelihood
standardized_distance
support_interval
support_interval_for_ratio
support_ratio
to_working_scale
```

Static and test results:

- private Core imports: none;
- copied `exp`, `log`, square, square-root, or `-0.5*z^2` formula tokens in app source: none;
- `test_app_delegates_scientific_calculations_to_root_public_core_apis`: pass;
- formula-bearing Core files found in the app repository: none.

Local NumPy use converts Core arrays into payload lists; local `math.isfinite` and
`math.isclose` calls implement strict JSON checks and display classification, not Wald formulas.

## Core frozen B01-B08 parity

Frozen authority:

| Item | Value |
|---|---|
| baseline tag | `pre-split-baseline-2026-07-29` |
| baseline tag target | `5fd501dd947d9b951d736014cfc2b310efa5e7b0` |
| behavior source | `830756ecb11b4e8161f8dfe1fc75afc346ef4467` |
| manifest SHA-256 | `f54bb2d8311788c07adcf23fc9f038e35702449e4a77a474abea9411246cabcc` |
| fixture-set SHA-256 | `81c341b39e711caffc85a444f0c1e4bc1e2d00633474c82e720afeb60def3c4d` |
| tolerance | `rtol=1e-12`, `atol=1e-14` |

### Published v0.4.1 parity asset

The release `SHA256SUMS` verifies the attached `baseline-parity.json`. Its result is:

```text
verdict                       = pass
successful Core-value cases  = 14
matched Core-error cases     = 6
explicit app-only exclusions = 2
values compared              = 23,095
maximum absolute difference  = 2.842170943040401e-14
maximum relative difference  = 1.3881501524486269e-15
```

### Independent macOS fresh-tag rerun

`make parity` from the detached v0.4.1 checkout reports:

```text
verdict                       = pass
successful Core-value cases  = 14
matched Core-error cases     = 6
explicit app-only exclusions = 2
values compared              = 23,095
maximum absolute difference  = 5.3290705182007514e-15
maximum relative difference  = 4.4493725366481632e-16
```

The freshly generated JSON SHA-256 is
`4d8330ea3585a2f438f9db21776907dc73750b4c28627d0e697f115bc27d50a0`.
It is not byte-identical to the Linux release asset: a structured diff shows that only per-case
and global maximum-difference fields vary. Baseline identifiers, case statuses, counts, paths,
tolerances, and verdict are identical. This is ordinary platform-level numerical variation,
not a parity failure; both sets of maxima are far inside the unchanged comparison contract.

## Core release assets

All attached files pass the published `SHA256SUMS`:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `baseline-parity.json` | 7,540 | `18d020e6a00746646ffed913eb88f1e4b148aa2725872db647823019f1e65dba` |
| `wald_inference-0.4.1-py3-none-any.whl` | 37,939 | `d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b` |
| `wald_inference-0.4.1.tar.gz` | 353,910 | `5b30fbc22c416cc724b75d9920157f42886ba185d34b628b4ad4c66691376bbf` |
| `SHA256SUMS` | 285 | `57949779d61ac2a75b28710da12606bcbb56c8c13b1e17cd233544aa6c12fd5a` |

Core test result: all 380 collected tests pass. A focused 19-test corpus/parity/closed-form and
extreme-support/ratio-transform group passes. The positive and negative threshold-transition
regressions for the v0.4.1 inverse-precision repair both pass.

## Wald Likelihood Support B01-B03 anchors

The audit independently evaluated the 21 explicit release-test anchors using the exact v0.1.2
app and its installed v0.4.1 release wheel.

| Case | Anchor group | Result |
|---|---|---|
| B01 | estimate `0.42`; SE `0.15816617164664273`; S-minus-2 display endpoints `0.10366765670671452`, `0.7363323432932855`; null/threshold log and ordinary support | pass |
| B02 | estimate `1.8`; log estimate `0.5877866649021191`; log SE `0.20687375447019513`; S-minus-2 display endpoints `1.1901021645028553`, `2.722455345968936`; null/threshold support | pass |
| B03 | display endpoints `0.9`, `1.1`; first displayed relative likelihood `0.003649390717838349`; reconstruction, support interval, reference, and pairwise summaries unchanged from B02 | pass |

Focused-anchor maxima:

```text
anchor count                = 21
maximum absolute difference = 1.4210854715202004e-14
location                    = B01 null MLE-to-candidate ordinary ratio
actual / expected           = 33.97645283375536 / 33.976452833755374

maximum relative difference = 4.449372536648163e-16
location                    = B02 threshold-to-null ordinary ratio
actual / expected           = 11.97712817775266 / 11.977128177752654
```

Relative difference is defined only when the expected reference is nonzero. Every anchor passes
`rtol=1e-12`, `atol=1e-14`.

## S-minus-2 and pairwise support

S-minus-2 anchors:

| Quantity | Value |
|---|---:|
| log-relative-likelihood cutoff | `-2.0` |
| MLE-to-bound ratio | `7.38905609893065` |
| B01 working lower / upper | `0.10366765670671452` / `0.7363323432932855` |
| B02 working lower / upper | `0.1740391559617288` / `1.0015341738425092` |

Thus S-minus-2 remains the MLE plus or minus two standard errors on the working scale and
corresponds to `exp(2):1`, not 2:1.

For the B02 ratio reconstruction with candidate A `1.25` and candidate B `1.0`:

```text
app log L(A)/L(B)                         = 2.4829988458996426
independent exact-binary64 factorization  = 2.4829988458996426
absolute difference                      = 0
ordinary L(A)/L(B)                        = 11.97712817775266
direction                                 = candidate_a_more_supported
reverse log L(B)/L(A)                     = -2.4829988458996426
antisymmetry residual                     = 0
identity log ratio / ordinary ratio       = 0 / 1
```

The app value is also bitwise equal to the root-public Core `log_support_ratio` result. Core
extreme-finite regressions confirm that `support_comparison` preserves a nonzero symmetric or
adjacent-float A:B result rather than subtracting two separately rounded squared values.

## Strict errors and JSON

Each probe raised the public `ValidationError` with an authored message:

| Probe | Result |
|---|---|
| nonfinite JSON constant (`NaN`) | rejected |
| nonpositive ratio bound | rejected |
| custom support ratio equal to one | rejected |
| unpaired candidate A/B | rejected |
| unexpected request field | rejected |
| adjacent-float S-minus-2 endpoint near `1e308` | rejected because the requested boundary is not representable accurately |

B01, B02, and B03 responses serialize with `json.dumps(..., allow_nan=False)`. The tested strict
JSON byte lengths were 42,284; 41,844; and 45,710 respectively. Extreme overflow tests retain the
finite signed log result while representing an unavailable ordinary ratio with the documented
status rather than emitting nonstandard JSON.

## Likelihood release/staging evidence

The exact v0.1.2 checkout stages:

```text
source commit  = 7f5557d2a93235e25215261ef5890868b3fb07bb
app version    = 0.1.2
Core version   = 0.4.1
bundle SHA-256 = b9c5247cba1dc13a004959e8354f1c96c00381aca5e31cda84a121b260316db0
manifest hash  = 21be10dd5197300594401f69605288b95d95a533d448c0284cea2870bfd023b0
```

The generated manifest is byte-identical to the v0.1.2 release asset. All attached files pass the
published checksum list:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `browser-stage-manifest-v0.1.2.json` | 4,576 | `21be10dd5197300594401f69605288b95d95a533d448c0284cea2870bfd023b0` |
| `wald-likelihood-support-v0.1.2.tar.gz` | 100,839 | `f0a457dfc153a39f1b3183af142a443361e1e965bcd1d76c7f825371ee294bac` |
| `SHA256SUMS` | 205 | `4d6d4e8732dddfefbf71ac6f441c630df600da6dee314685e2adabfc4226ce81` |

`make test` stages the packages and passes all 73 non-E2E tests. A separate 55-test focused group
covering ownership, B01-B03/B08, S-minus-2/generic intervals, pairwise identities/properties, and
strict request/response behavior passes.

## Commands and clean-state evidence

Principal commands:

```text
git ls-remote <repo> refs/tags/<tag> refs/tags/<tag>^{}
git clone --filter=blob:none --branch <tag> --single-branch <repo> <fresh>
git cat-file -t refs/tags/<tag>
git rev-parse refs/tags/<tag> refs/tags/<tag>^{} HEAD

# Core
uv sync --locked --all-groups
uv run pytest -q
make parity
uv run pytest -q <targeted corpus/parity/closed-form/extreme tests>
gh release download v0.4.1 --repo reblocke/wald-inference-core
sha256sum -c SHA256SUMS
diff -qr --exclude=__pycache__ <wheel>/wald_inference <tag>/src/wald_inference

# Likelihood
uv sync --locked
make test
uv run pytest -q <ownership/scientific/property/contract tests>
uv run python <independent in-memory anchor/error audit>
gh release download v0.1.2 --repo reblocke/wald-likelihood-support
sha256sum -c SHA256SUMS
cmp web/assets/py/manifest.json browser-stage-manifest-v0.1.2.json

git diff --check
git status --short --untracked-files=all
```

Both final checkouts remained at their peeled commits with no tracked or untracked nonignored
changes. `git diff --check` passed.

One exploratory targeted-test invocation used a nonexistent test node name and exited 4 before
collection. The corrected existing parameterized node then passed both positive and negative
cases. This was an audit-command selector error, not a repository test failure.

## Remaining limitations

- The published Core parity JSON and the independent macOS parity JSON are not byte-identical
  because their platform-specific maximum-difference fields differ. Both are checksum-addressed,
  both preserve all identifiers/counts/statuses, and both pass the same unchanged tolerance.
- This supplement verifies the exact final numerical tags only. Browser/deployment and complete
  cross-repository release readiness remain governed by the other CC-MIG-11 lanes.
- No new external numerical data, figure, table, code, or substantial publication text was used.

No unresolved Lane A/B question or release blocker remains for Core v0.4.1 or Wald Likelihood
Support v0.1.2.
