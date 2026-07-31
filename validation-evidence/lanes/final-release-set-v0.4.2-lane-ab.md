# Final Core v0.4.2 release-set Lane A/B audit

Audit window: 2026-07-31T13:02:31Z through the final source inspection after
2026-07-31T13:17:56Z. Mode: independent, read-only, fresh-context numerical and
formula-ownership review.

## Verdict

**PASS with one documented nonblocking numerical-contract exception.** No blocker,
high-severity, or medium-severity scientific finding was identified.

## Exact release identities

| Repository | Tag | Peeled commit |
|---|---|---|
| `reblocke/wald-inference-core` | v0.4.2 | `8afd0a463cc1d2586b8ce5cf92f40900647c3190` |
| `reblocke/scientific-applet-template` | v0.1.2 | `04353d7bb07ee74ae0585107431563db89387f05` |
| `reblocke/compatibility-curve` | v0.1.4 | `eeaff9a374bc022c2d5ca16fdb3c59fbdfcd90f4` |
| `reblocke/wald-likelihood-support` | v0.1.3 | `beb18d87939f3ba9738b97e1c2e10724e31c5945` |
| `reblocke/critical-effect-size` | v0.1.4 | `1c451fe9ed7d7d21fe732ec5da178248053fe912` |
| `reblocke/type-s-m-calibrator` | v0.1.4 | `bb4372c55a2e839b9f57d8424f797c944f5b4eb0` |
| `reblocke/precision-guardrail-planner` | v0.1.3 | `a88926b966766a94b00a61799539351cce44581a` |
| `reblocke/conf_curve_likelihood` | v0.2.6 | `60ca0e3f5d6f05bb943cb4b7b7d02ed5a1d5714a` |

Every remote annotated tag peeled to the supplied commit. Detached test worktrees
remained clean.

## Environment and commands

- macOS 26.5.2 build 25F84, arm64
- uv 0.11.11
- Core and integrated: Python 3.11.10, SciPy 1.14.1
- Focused apps: Python 3.12.13, SciPy 1.14.1
- Template: Python 3.12.13, with SciPy intentionally absent
- Fresh clone root: `/tmp/ticket11-science.Fr3e93`

Each target ran:

~~~sh
uv sync --locked
make test
git status --porcelain
git ls-remote origin "refs/tags/$tag" "refs/tags/$tag^{}"
~~~

Core additionally ran `uv sync --locked --all-groups` and `make parity`.

## Results

| Target | Non-browser tests |
|---|---:|
| Core | 396 |
| Template | 38 |
| Compatibility | 64 |
| Likelihood | 80 |
| Critical effect | 67 |
| Type S/M | 84 |
| Precision | 60 |
| Integrated | 219 |

Core frozen parity passed 14 numeric cases, six matched-error cases, and two
declared app-owned exclusions across 23,095 values. Maximum absolute and relative
differences were `5.329070518200751e-15` and `4.449372536648163e-16`, below
`rtol=1e-12`, `atol=1e-14`.

The integrated B01-B08 differential comparison passed all 22 cases and 27,268
floating-point comparisons with the same maxima. Focused comparisons passed:
compatibility 35 exact values; likelihood 33 values; critical effect four values;
Type S/M 49 values; and precision 22 exact values. An independent SciPy/normal
identity recomputation passed 40 scalar comparisons, all six selection rules,
strict JSON, and extreme-finite guards. Machine results are preserved in
`validation-evidence/results/core-v0.4.2-baseline-parity.json` and
`validation-evidence/results/core-v0.4.2-independent-recomputation.json`.

## Formula ownership and adoption

Core remains the sole owner of Wald effect transforms, CI reconstruction,
compatibility, likelihood/support, detectability, selection, Type S/M, and
precision calculations. Source and AST scans found no protected scientific
implementation in focused-app production packages. Focused apps import the
root-public Core API; integrated compatibility imports are confined to the
explicitly frozen `wald_inference.legacy` surface. The template remains
formula-free apart from disposable demonstration arithmetic, and the catalog is
calculation-free.

Every consumer pins the official Core v0.4.2 wheel and SHA-256
`225331d7b9d7b70e2508eecb92851a92a8c4e245baf412a1eb0f464d85da1349`.
The 14-file staged Core package was byte-identical across all six consumers.

## Nonblocking limitation

Core intentionally retains two binary64 evaluation paths for selected-claim
probability: the conservative detectability/inversion kernel and the frozen
direct interval-probability path used by Type S/M and inverse precision. They
share one six-rule interval authority but are not bitwise identical. The Type S/M
adapter emits the canonical probability and fails closed on material cross-API
drift. This is a documented backward-compatibility exception, not observed
scientific drift.

Public wording remained within scope: none of the tools claim posterior,
profile-likelihood, clinical-validation, MCID, or exact sample-size meaning.
