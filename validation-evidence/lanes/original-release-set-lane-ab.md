# CC-MIG-11 Lane A/B independent numerical and parity ledger

Audit completed: 2026-07-30T12:43:47Z
Audit lane: A (numerical/scientific) and B (frozen/cross-app parity)
Reviewer work root: `/private/tmp/cc-mig-11-ab-FWonz1`
Controlling ticket: `conf_curve_migration_codex_tickets/tickets/11_independent_portfolio_validation.md` from the user-supplied ZIP
Production/GitHub mutations: none

## Lane verdict

**Public release set: NO-GO / not validated.** The independently resolved public tags contain two
demonstrated numerical blockers in `wald-inference` v0.4.0 and one additional public transform
finite-range blocker:

1. the inverse precision solver can skip a finite feasible band and return false infeasibility;
2. `support_comparison` can contradict the canonical pairwise support kernel, including reporting
   equality and the wrong ordering for finite inputs; and
3. `from_working_scale` silently maps sufficiently negative finite log-ratio values to natural
   ratio `0.0`, contrary to the documented invalid/unrepresentable-value contract and strict
   positivity of ratio measures.

The first two findings are repaired at Core checkpoint
`3fd7f1472dbf25027e3381c18f031a55dff34170`; the third is repaired by its child
`56b7dbe72c22889dc5d2541ac7112276d3cadebe` (package version 0.4.1). Independent full-suite,
frozen-oracle, and adversarial reruns pass on the clean child commit. **Lane A/B GO for candidate
56b7dbe**: no numerical/parity release blocker remains in the reviewed candidate. This is not a
portfolio release verdict: the commit is not the independently resolved public release, and the
other CC-MIG-11 lanes plus a fresh-tag rerun remain required.

The released ordinary B01-B08 paths otherwise pass the frozen numerical contract. The patched
support delegation causes a small, expected single-rounding drift within that contract rather than
bitwise identity; details are below.

## Exact release inventory

Tags were independently resolved with `git ls-remote`; annotated tag objects were peeled and then
cloned into new directories in detached-HEAD state.

| Repository | selected public tag | tag object | peeled commit | release status |
|---|---:|---|---|---|
| `reblocke/wald-inference-core` | `v0.4.0` | `59132c818b24026122ebda9a6105d272f0580868` | `fd7b24740122bed7ae07769674732c5e56c91277` | prerelease |
| `reblocke/scientific-applet-template` | `v0.1.0` | `0c7fc277075da18a04903ced937313695c7a3678` | `a360bde95c192d8de4f9a3b531e73600ebf3d8b8` | prerelease |
| `reblocke/compatibility-curve` | `v0.1.0` | `cd3fb8cc8b5d249921a9ff9d7ec3abf803b59f84` | `8945cfce61ecce29bdb6a922778f84d35fc4fe7f` | prerelease |
| `reblocke/wald-likelihood-support` | `v0.1.0` | `9ec64072973e9d78486a3c5b1f5b344161b85101` | `b013abd2d512e1b041f089018649039b102a5c36` | prerelease |
| `reblocke/critical-effect-size` | `v0.1.0` | `b84a2e374542a46ed93fb7f0c30149b822720ffd` | `b4e201b3b23072c66302c243551388d6eaa0436f` | prerelease |
| `reblocke/type-s-m-calibrator` | `v0.1.0` | `70627b36c02fe9a2e8d84237031f34f2dbab11d4` | `2af70621c42b371d019ab360c17ade12c53e37c7` | prerelease |
| `reblocke/precision-guardrail-planner` | `v0.1.0` | `060689ff19c7a810a70295fefb80e386735f9f93` | `b142950b164ec99c8ac6477eeefef62d686bf268` | prerelease |
| `reblocke/wald-inference-tools` | `v0.1.0` | `4741919aef3c528e7e2d251e5b123a0743c30f71` | `bbb045044a531244516540e2bcffaeca44c5e9df` | prerelease |
| `reblocke/conf_curve_likelihood` | `v0.2.0` | `ea4f6c31d239bb44241164814012d3d4f2dfad66` | `5fbf609df072100905d2a86ecbd55b286b5fa090` | prerelease |

Frozen authority:

- release tag `pre-split-baseline-2026-07-29`
- annotated tag object `58855d85227864efb30b7e66a79c28cb13103608`
- peeled commit `5fd501dd947d9b951d736014cfc2b310efa5e7b0`
- fixture-declared approved behavior source `830756ecb11b4e8161f8dfe1fc75afc346ef4467`

The staggered exact Core pins are intentional and lock-resolved:

| consumer | locked Core |
|---|---:|
| compatibility app | 0.1.1 |
| likelihood app | 0.2.1 |
| critical-effect app | 0.3.0 |
| Type S/M app | 0.3.0 |
| precision app | 0.4.0 |
| integrated app | 0.4.0 |

The template and catalog contain no portfolio numerical formula surface, so they were inventoried
but not treated as Lane-A formula consumers. Their cold-start, browser, provenance, and
documentation checks belong to the other CC-MIG-11 lanes.

## Environment and method

- macOS 26.5.2 build 25F84, Darwin 25.5.0, arm64
- Git 2.50.1 (Apple Git-155)
- uv 0.11.11
- system Python 3.14.4
- Core and integrated locked environment: CPython 3.11.10
- focused-app locked environment: CPython 3.12.13
- released Core numerical dependencies: NumPy 2.2.6, SciPy 1.14.1
- released Core test tools: pytest 9.1.1, Hypothesis 6.163.0, Ruff 0.16.0

Method:

1. resolve public tags independently;
2. clone only into a new temporary parent;
3. run locked installs and each numerical test surface;
4. inspect the formula authority, implementation, and test owner;
5. recompute ordinary, boundary, and extreme values independently;
6. run B01-B08 frozen parity and focused-subset anchors;
7. run an independent grid over all six selection rules and inverse target types;
8. reproduce blockers through both Core and consuming-app APIs; and
9. adversarially rerun the separate repair checkpoint without editing it.

## Formula authority and independent review

The scientific definitions are stated in Core `docs/SCIENTIFIC_SCOPE.md`; the frozen provenance and
module ownership map are in `docs/MIGRATION_PROVENANCE.md`; API precision and undefined behavior are
in `docs/API.md`. The formula implementation/test map is:

| quantity | production owner | principal tests | independent result |
|---|---|---|---|
| effect registry; identity/log transforms | `src/wald_inference/effects.py` | `tests/unit/test_effects_reconstruction.py`, observed properties | ordinary identity/log values and B01/B02 exact; public-release negative log-scale underflow blocker repaired at candidate 56b7dbe |
| CI midpoint/SE reconstruction | `src/wald_inference/reconstruction.py` | effects/reconstruction unit tests; observed properties; B01/B02/B08 | safe half-sum/half-difference and `half_width/z975` verified; large opposite-signed B08 finite |
| standardized distance and compatibility | `src/wald_inference/compatibility.py` | observed unit/property/reference tests | `2*Normal.sf(abs(z))` independently reproduced; focused anchors bit-exact |
| relative/log likelihood | `src/wald_inference/likelihood.py` | observed and grid/support unit/property tests | `-z^2/2` and exponentiation reproduced; log value remains authoritative when display ratio over/underflows |
| S−2 and generic support intervals | `src/wald_inference/likelihood.py` | support unit/property/scientific-reference tests | S−2 is `theta_hat +/- 2*SE`; generic distance `sqrt(-2c)*SE`; ratio criterion `sqrt(2 log R)*SE`; endpoint representability fails closed |
| pairwise support ratios | canonical `log_support_ratio` in `likelihood.py` | support unit/property tests | exact binary64 factorization is correct; released `support_comparison` duplicates it incorrectly (blocker 2) |
| legacy critical benchmark | `src/wald_inference/detectability.py` | grid/support unit and critical-app reference tests | `(z_.975 + z_.80)*SE` preserved and labeled separately |
| exact one-/two-sided detectability | `src/wald_inference/detectability.py` | detectability API/property/reference tests | directed result meets conservative float contract and prior float fails; kept distinct from legacy marker |
| six selection rules | `src/wald_inference/selection.py` | `tests/unit/test_selection.py`; Type S/M reference tests | all interval boundaries independently recomputed from normal tails |
| selected-claim probability | interval authority in `selection.py`; stable detectability kernel in `detectability.py`; direct Type-S/M kernel in `selection.py`/`type_sm.py` | detectability and Type-S/M suites | scientific formula agrees; two numerical kernels are an explicit ownership exception, described below |
| Type S | `src/wald_inference/type_sm.py` using selection helpers | Type-S/M unit/property/reference tests | wrong-sign selected probability divided by selection probability independently reproduced |
| Type M | same | same | `E(abs(Z) | selected)/abs(delta)` independently reproduced; ratio measures correctly use log distance |
| observed exaggeration | same | same | `abs(estimate-null)/abs(true-null)` on working scale; undefined near null |
| information and CI-width scaling | `src/wald_inference/precision.py` | precision unit/property/reference tests | `SE_new=SE_current/sqrt(m)` and width `2*z975*SE` independently reproduced |
| per-target inverse precision | `src/wald_inference/precision.py` | precision unit/property/reference tests | released global-halving assumption is false for one threshold rule (blocker 1) |
| joint guardrail and binding constraints | same | joint precision unit/property tests | strictest finite target is minimum SE/maximum information; binding tolerance and mandatory infeasibility behavior verified |
| extreme finite protections | effects, compatibility, likelihood, reconstruction, selection, Type-S/M | strict-validation and B08 tests | subtraction/square/support endpoint protections are strong; release log-ratio back-transform underflow repaired at candidate 56b7dbe |

### Consuming-app scientific wording

Inspected README/UI contract text is substantively aligned:

- compatibility is a two-sided Wald compatibility value, not a posterior probability;
- likelihood is normalized approximate Wald support, not an exact fitted/profile likelihood, Bayes
  factor, or posterior probability;
- S−2 is correctly identified as `exp(2):1`, not 2:1;
- the critical app separates the legacy z-sum benchmark from exact selected-claim inversion;
- Type S/M are repeated-study operating characteristics and ratio Type M uses log scale;
- precision reports relative information, not sample size without an explicit additional design
  assumption.

At the released precision tag, the false infeasibility result also makes the generated explanation
scientifically false for the blocker-1 case. Checkpoint 3fd7f14 adds explicit nonmonotone-transition
wording and corrects the result.

## Blocking numerical findings

### A-01 — precision solver skips a finite feasible band

Affected release:

- `wald-inference` v0.4.0, `src/wald_inference/precision.py`
- `precision-guardrail-planner` v0.1.0 through its locked Core

Concrete positive-direction repro:

```text
true effect       = 0.4
null              = 0
threshold         = 1
claim direction   = positive
selection rule    = estimate_exceeds_mcid_and_p_lt_alpha
alpha             = 0.05
current SE        = 5
target probability= 0.10
```

The release returns `required_se=None` and “No finite required precision...”. The focused app
reports `infeasible/no_finite_joint_solution`.

Independent formula:

```text
P(selected | true=0.4, SE)
  = Normal.sf(max(z_.975, 1/SE) - 0.4/SE)
```

Representative values:

| SE | independently recomputed probability |
|---:|---:|
| 5 | 0.030056493266163119 |
| 0.625 | 0.093423521450726965 |
| 0.589 | 0.10012373457006546 |
| 0.55 | 0.10884548744751049 |
| transition `1/z_.975 = 0.51021345692465381` | 0.11980175566841811 |
| 0.5 | 0.11506967022170822 |
| 0.4 | 0.066807201268858057 |
| 0.3125 | 0.027428949703836795 |

The forward Core metric equals this independent formula. The defect is only the inverse search:
halving jumps from failing 0.625 to failing 0.3125 across the finite qualifying band.

Independent breadth scan:

- 8,001 log-spaced information multipliers from 1 to `1e12`
- adjacent multiplier factor 1.0034598491478393
- 9 rule/direction configurations covering all six rules
- 12 positive/negative assumed effects
- 6 current SE values
- 14 power/Type-S/Type-M targets
- 9,072 target paths total

Exactly eight release existence misses were predicted independently and confirmed through the
public Core API; all are power targets for this one rule:

| direction/effect/threshold | current SE | target | largest satisfying grid SE | grid maximum |
|---|---:|---:|---:|---:|
| positive 0.4 / 1 | 5 | 0.1 | 0.5894812616218927 | 0.11964925389912895 |
| positive 0.4 / 1 | 10 | 0.1 | 0.5888436553555890 | 0.11980072284115922 |
| positive 0.6 / 1 | 5 | 0.2 | 0.5360681494501970 | 0.21637495954156633 |
| positive 0.6 / 1 | 10 | 0.2 | 0.5364138714402965 | 0.21652327070535837 |
| negative -0.4 / -1 | 5 | 0.1 | 0.5894812616218927 | 0.11964925389912895 |
| negative -0.4 / -1 | 10 | 0.1 | 0.5888436553555890 | 0.11980072284115922 |
| negative -0.6 / -1 | 5 | 0.2 | 0.5360681494501970 | 0.21637495954156633 |
| negative -0.6 / -1 | 10 | 0.2 | 0.5364138714402965 | 0.21652327070535837 |

There were zero Type-S/Type-M existence misses, zero misses for the other five rules, and zero
within-piece direction changes after splitting this rule at its exact cutoff transition.

### A-02 — `support_comparison` contradicts the canonical pairwise kernel

Affected release: `wald-inference` v0.4.0.

`log_support_ratio` is the root-public canonical implementation and uses exact binary64
factorization before a single rounding. Released `support_comparison` instead subtracts two
separately squared log-relative-likelihood values.

Finite repros:

| A | B | center/SE | canonical log L(A)/L(B) | released `support_comparison` | error |
|---:|---:|---|---:|---:|---:|
| `1e100` | `-1e100` | 1 / 1 | `2e100` | `0.0` (ratio 1; false equality) | wrong order |
| `1e150` | next float above | 0 / 1 | `1.8170968107390175e284` | `2.2305253627166746e284` | 22.7521% relative |
| `1e154` | next float above | 0 / 1 | `1.4885657073574032e292` | `1.99584030953472e292` | 34.0781% relative |

Compound-object finite-range nuance: `support_comparison(1e155, -1e155, center=0, SE=1)` must still
raise `ValidationError("Log relative likelihood exceeds the finite floating-point range.")`
because its required individual candidate/reference-to-MLE fields are unrepresentable, even though
the standalone pairwise log ratio is finite zero. Returning `None` or clamping the compound object
would violate its current contract. The repair preserves this failure behavior.

### A-03 — finite log-ratio back-transform silently underflows to invalid zero

Affected release: v0.4.0.

`docs/API.md` states that public functions raise `ValidationError` for invalid or unrepresentable
values, and that ratio transformations require strictly positive natural-scale values. Positive
overflow is tested and raises. Negative underflow is neither rejected nor represented:

```text
from_working_scale("odds_ratio", -745.0)  -> 5e-324
from_working_scale("odds_ratio", -746.0)  -> 0.0
from_working_scale("odds_ratio", -1000.0) -> 0.0
```

The latter two outputs are not valid natural-scale ratios and cannot round-trip. The shared log
transform means this affects all five ratio effect types. This is a public extreme-finite contract
failure.

Candidate 56b7dbe adds a strict-public positive-result check after exponentiation and scalar/vector
tests for all five ratio types. Independent rerun confirms `-745 -> 5e-324`, `-746` raises the
documented `ValidationError`, and the explicitly frozen `wald_inference.legacy` surface retains
`-746 -> 0.0`.

## Nonblocking numerical ownership limitation

There are two production numerical kernels for the selected-claim probability:

- the detectability API’s deliberately conservative, directed-rounding/certification kernel; and
- the frozen direct interval-probability kernel used by Type S/M and inverse precision.

They share the single six-rule interval authority and agree scientifically, but they are not
bitwise identical:

- maximum observed absolute difference in the audit scan:
  `3.774758283725532e-15` at alpha 0.5, delta -1;
- maximum observed relative difference:
  `1.0533245453471949e-12` at alpha `1e-300`, delta -4;
- at alpha 0.05 and the null:
  detectability returns exactly `0.05`, while the direct design metric returns
  `0.04999999999999996`.

This split is documented and serves different binary64 contracts, so it is not classified here as
a scientific-value blocker. The selection event/formula has one interval authority; the two
rounding paths serve different derived contracts. Attempting to route the conditional Type-S/M
denominator through the conservative inversion-certificate kernel broke the existing tighter
direct tail/moment reference identities, so that proposed consolidation was reverted rather than
weakening scientific-reference tests. The final portfolio report should record this approved
numerical-contract exception explicitly.

## Released B01-B08 and cross-app parity

### Core frozen oracle

Command:

```text
uv run python scripts/verify_baseline_parity.py --json-output reports/baseline-parity.json
```

Released v0.4.0 result:

- 14 successful Core-value cases
- 6 matched Core error cases
- 2 explicit app-only exclusions
- 23,095 numeric/scalar values compared
- maximum absolute difference: `0.0`
- maximum relative difference: `0.0`
- declared comparison tolerances: rtol `1e-12`, atol `1e-14`

The corpus covers B01-B08, including additive/ratio reconstruction, grids, compatibility,
likelihood/support, design metrics, precision, validation, and extreme finite cases.

### Focused-subset recomputation

| focused contract | frozen anchors recomputed | maximum absolute difference | maximum relative difference | result |
|---|---:|---:|---:|---|
| compatibility B01/B02/B03/B08 | 33 | 0 | 0 | pass |
| likelihood/S−2 B01/B02/B03 | 21 | `1.4210854715202004e-14` (B01 MLE/null displayed ratio) | `4.4493725366481632e-16` (B02 threshold/null ratio) | pass |
| Type S/M B04/B05/B07 | 49 | `3.9968028886505635e-15` | `1.1027325787414086e-14` | pass |
| precision B06/B07 | 22 | 0 | 0 | pass for frozen cases; adversarial A-01 fails |
| critical legacy/exact reference anchors | 4 | `2.3314683517128287e-14` | `4.033844917580397e-14` | pass |

Largest Type-S/M discrepancy details:

- absolute: B04, true effect 0.3, selected probability
  `0.4748512734696006` versus `0.4748512734696046`;
- relative: B04, true effect 0.1, selected probability
  `0.0969037898944932` versus `0.09690378989449427`.

Largest critical discrepancy details:

- absolute: ratio/log-scale legacy precision, actual `0.5795737427348193` versus expected
  `0.5795737427348426`;
- relative: additive exact working result, actual `0.44311546580689903` versus expected
  `0.4431154658069169`.

The integrated app regenerated and compared all 22 golden cases successfully at rtol `1e-12`,
atol `1e-14`.

### Focused negative-scope contracts

Passing contract/ownership tests confirm:

- compatibility excludes likelihood, support, design, precision, and accepts no enabled-design
  branch;
- likelihood excludes compatibility/p-values as a primary result, critical/design, selection,
  Type S/M, and precision;
- critical excludes observed compatibility/likelihood, Type S/M, and inverse precision;
- Type S/M contains forward design/scenario results but no inverse precision or observed-evidence
  result;
- precision contains guardrails/sensitivity but no observed compatibility/likelihood/S−2 or full
  Type-S/M calibration curve.

No cross-app formula copy was found in the focused adapters. The Core exceptions are the released
`support_comparison` duplication and the documented dual probability kernels described above.

## Candidate 56b7dbe adversarial rerun

Candidate:

```text
commit  56b7dbe72c22889dc5d2541ac7112276d3cadebe
parent  3fd7f1472dbf25027e3381c18f031a55dff34170
version 0.4.1
status  clean
```

### A-01 repair result

The repair evaluates
`abs(threshold-null)/z_(1-alpha/2)` when the estimate-exceeds rule can change active cutoff, then
bisects only one monotone segment.

- rerunning the complete 9,072-target scan: all 8 prior independent misses now return finite
  solutions; confirmed misses remaining = 0;
- all four negative mirrors are bitwise identical to positive cases;
- analytic maximal-SE roots and Core returns:

| effect/direction | current SE | target | independent largest root | Core required SE | conservative relative gap |
|---|---:|---:|---:|---:|---:|
| +/-0.4 mirror | 5 | 0.1 | 0.58961184789672971 | 0.58961184396002020 | `6.6767815605687823e-9` |
| +/-0.4 mirror | 10 | 0.1 | 0.58961184789672982 | 0.58961184649745291 | `2.3732170945170036e-9` |
| +/-0.6 mirror | 5 | 0.2 | 0.53650814965369187 | 0.53650814691436910 | `5.1058362680738081e-9` |
| +/-0.6 mirror | 10 | 0.2 | 0.53650814965369187 | 0.53650814771411182 | `3.6151921520218698e-9` |

For every case, 0.0001% less information (SE multiplied by `1+1e-6`) fails, while 0.0001% more
information passes. At the exact kink maximum, positive and negative directions return the same SE,
one ULP from the analytic transition; the probability plateau extends only one further binary64
SE, far below solver tolerance. The next representable target probability above the kink maximum
is correctly infeasible.

### A-02 repair result

`support_comparison` now delegates only its pairwise field to canonical `log_support_ratio`;
required individual fields are still computed and validated.

Independent exact-Fraction checks match bitwise for:

- ordinary B01-like inputs;
- `(1e100, -1e100, center=1, SE=1)` -> `2e100`;
- adjacent `1e150` candidates -> `1.8170968107390175e284`;
- adjacent `1e154` candidates -> `1.4885657073574032e292`; and
- display-ratio overflow (`None`) with a retained finite log result.

The compound-object `1e155/-1e155` case still raises the required individual-field finite-range
error, while standalone `log_support_ratio` remains finite zero.

### A-03 repair result

- all five strict public ratio back-transforms retain minimum-subnormal `-745 -> 5e-324`;
- all five reject scalar `-746` and mixed vector `[0, -746]` with a strictly-positive
  representability error;
- the legacy compatibility module intentionally retains zero-underflow behavior.

### Candidate regression gates

- full Core pytest: pass
- Ruff `src tests`: pass
- `git diff --check`: pass
- frozen oracle: pass, 14 success + 6 Core errors + 2 exclusions, 23,095 values
- patched frozen maximum absolute difference:
  `5.3290705182007514e-15`
- patched frozen maximum relative difference:
  `4.4493725366481632e-16`

The patched nonzero differences occur in B01, B02, B03, B04, and B07k threshold pairwise support
fields. They are the expected single-rounding result of delegating to the canonical exact
factorization, are below atol `1e-14`/rtol `1e-12`, and are therefore within the frozen parity
contract. They are not bitwise identical to the v0.4.0/baseline values.

Machine-readable final candidate parity evidence:
`/private/tmp/cc-mig-11-evidence/patched-core-final-baseline-parity.json`.

Boundary evidence:
`/private/tmp/cc-mig-11-evidence/patched-precision-boundaries.txt`.

## Locked test matrix

| checkout | install | numerical verification | result |
|---|---|---|---|
| Core v0.4.0 | `uv sync --locked --all-groups` | `uv run pytest -q`; baseline parity script | pass except independently added adversarial A-01/A-02/A-03 |
| compatibility v0.1.0 | `uv sync --locked` | `make test` | pass |
| likelihood v0.1.0 | `uv sync --locked` | `make test` | pass |
| critical v0.1.0 | `uv sync --locked` | `make test` | pass |
| Type S/M v0.1.0 | `uv sync --locked` | `make test` | pass |
| precision v0.1.0 | `uv sync --locked` | `make test` | pass frozen suite; adversarial A-01 fails |
| integrated v0.2.0 | `uv sync --locked` | `make test` including stage and golden comparison | pass |
| Core candidate 56b7dbe | clean locked worktree | full pytest, Ruff, diff check, frozen oracle, independent adversarial scripts | A-01/A-02/A-03 pass |

## Exact command ledger

Release/tag resolution and cloning:

```text
git ls-remote --tags https://github.com/reblocke/<repo>.git
git clone --depth 1 --branch <resolved-tag> https://github.com/reblocke/<repo>.git <fresh-dir>
git rev-parse HEAD
git status --short
```

Core:

```text
uv sync --locked --all-groups
uv tree --depth 1
uv run pytest -q
uv run python scripts/verify_baseline_parity.py --json-output reports/baseline-parity.json
```

Each focused/integrated app:

```text
uv sync --locked
make test
git status --short
```

Candidate:

```text
git rev-parse HEAD
git status --short
git diff --check
uv run ruff check src tests
uv run pytest -q
uv run python scripts/verify_baseline_parity.py \
  --json-output /private/tmp/cc-mig-11-evidence/patched-core-final-baseline-parity.json
PYTHONPATH=src .venv/bin/python \
  /private/tmp/cc-mig-11-ab-FWonz1/audit_precision_all_rules.py
PYTHONPATH=src .venv/bin/python \
  /private/tmp/cc-mig-11-ab-FWonz1/audit_patched_precision_boundaries.py
PYTHONPATH=src .venv/bin/python \
  /private/tmp/cc-mig-11-ab-FWonz1/audit_patched_support_comparison.py
```

## Required disposition

1. Do not validate the existing public release set.
2. Preserve A-01/A-02/A-03 repairs through review and a new exact Core release; the independent
   candidate evidence supports all three.
3. Record the dual selected-probability rounding paths as an approved numerical-contract exception.
4. After a new exact release tag exists, rerun Lane A/B from a fresh clone and repeat the other
   CC-MIG-11 lanes before changing the portfolio verdict.
