# CC-MIG-11 final documentation-only app patch release supplement

Audit completed: 2026-07-30T16:55:00Z

Audit root: `/private/tmp/cc-mig-11-docpatch-tags.zPyFxp`

Production/GitHub mutations by reviewer: none

## Verdict

**GO for the four exact final patch tags.**

The final metadata releases for Compatibility Curve, Critical Effect Size, Type S/M Calibrator,
and Precision Guardrail Planner pass the requested immutable-tag, release-artifact, checksum,
Pages, live-manifest, fresh detached-tag, predecessor-diff, documentation/metadata, and exact-Core
checks. No scientific, focused-contract, privacy, accessibility, plotting, or export behavior
changed relative to the immediately preceding audited releases.

These four repositories remain experimental GitHub prereleases. Their README wording does not
claim stable publication or portfolio validation: it states experimental maturity and delegates
the mutable GitHub publication state to the exact versioned release page.

## Immutable release identities

Every ref is an annotated, unsigned tag. In every row, the peeled tag commit, `main`, successful
CI/Pages/Release workflow `headSha`, successful Pages deployment SHA, live manifest
`source_commit`, and fresh detached checkout `HEAD` are identical.

| Repository | Tag | Annotated tag object | Peeled commit | Release ID | Publication |
|---|---|---|---|---:|---|
| `compatibility-curve` | `v0.1.3` | `ba55c6e90f377e2b783cfd3d1ee7c344fe88d667` | `0abf653cb455885b07765d4b9fe1af4cc38cf3b2` | `362580877` | published prerelease |
| `critical-effect-size` | `v0.1.3` | `5ad8c46820df787b1531cab9ac966a68e6188360` | `a10482c73cdb89d37814bf1b8c955166957ecd6b` | `362583459` | published prerelease |
| `type-s-m-calibrator` | `v0.1.3` | `438d41e5ea623c07c12935b1886c9f087ee1341e` | `ed8881d13eea8ecffa77304555d251296d63f058` | `362583371` | published prerelease |
| `precision-guardrail-planner` | `v0.1.2` | `02c52998b4a16023f51bd90f76755a35179db91c` | `ec47753aa1119b802e12856c4bc18feefa1ad6d5` | `362580665` | published prerelease |

Unsigned annotated tags are a retained nonblocking provenance limitation.

## Release artifacts and checksums

`gh release download` succeeded for all four releases. `shasum -a 256 -c SHA256SUMS` passed for
all eight listed payloads. All 12 locally computed asset digests, including each `SHA256SUMS`
file, exactly match GitHub REST `assets[].digest`.

| Repository | `SHA256SUMS` | Browser manifest | Source archive |
|---|---|---|---|
| Compatibility | `7e64d6816d7e22e4f9290bae79f647ae13fa546edb03cd6e3e366047546645ba` | `33f56fb9a686203770f8bfae7cf65f71f87add2c4f78760167badfbae79de82e` | `90d498ef63675d4779c027cb4941c8ba4a882d68fe54e10c0d26d9a44e6c206e` |
| Critical effect | `d37359ff7209b8022b35d0555650077b3ee85dc9900051eac6a5c50345179d42` | `bb752b090753b49b7f19c18b2f14778cbbe25fcd3d0e7c9c35415787107f8b87` | `246cbbe9e80c3790295391476e084d1d6cb5f6781b02a1eff128cfbfec77dd16` |
| Type S/M | `b7c72d9f7685b63924b2d535946405974609815fda644b14e726eec14194c6c6` | `4a99e9a724bc59fe52bfb0d8fb3db5d7f99f1368361556e64f8be56c5a3952d6` | `5c749e739a0d359540dbed6fd21c856fbceb73e3947d22b7781fd698ac0165b1` |
| Precision | `6be2475385fc533198eac7681bdd6db2f0d24195e8b4c850b34ce543f07c596f` | `5710b0310abea8a30b628ce8edb3dcc50cd4e66846857eb75983c6e687f4ace4` | `5f9063fba32e19c67b169113d86088e81efd1a221c56b7999c91fcc7d85a5ea0` |

After extraction, source-archive file lists and bytes exactly match every tracked tag file:

| Repository | Tracked files compared | Result |
|---|---:|---|
| Compatibility | 54 | exact |
| Critical effect | 57 | exact |
| Type S/M | 57 | exact |
| Precision | 56 | exact |

## Pages and browser-stage provenance

All four latest Pages deployments succeeded from the exact tag commit. Each fresh checkout
regenerated the manifest deterministically. Local generated, released, and live manifest bytes are
identical.

| Repository | Pages deployment | Manifest SHA-256 | App package / bundle SHA-256 |
|---|---:|---|---|
| Compatibility | `5678648585` | `33f56fb9a686203770f8bfae7cf65f71f87add2c4f78760167badfbae79de82e` | `1ae3112eb9649de04d6a78ba4832cd041d7ce2079993c20d28e170f3dbd09489` / `5ef8850f04895098b3a21c20df1e4bc74d934ba153a1c98463ddc996994e554b` |
| Critical effect | `5678676727` | `bb752b090753b49b7f19c18b2f14778cbbe25fcd3d0e7c9c35415787107f8b87` | `0106639c9bb196871245b941061bfafe0de71ecdc98503ef85e3ba68c0552c21` / `323e8e512b397cd52075cfd885cf9b7d917dbd7ed04791509889d42f188ef195` |
| Type S/M | `5678679459` | `4a99e9a724bc59fe52bfb0d8fb3db5d7f99f1368361556e64f8be56c5a3952d6` | `fe02c6830697873e21a6e5883adcd663645afdca9c4e9171c2ed89bdb335844a` / `047e3a0ebed5a57df1481702030fa189c0964b4efc0ace86aea1aa3f5c10b8a0` |
| Precision | `5678651657` | `5710b0310abea8a30b628ce8edb3dcc50cd4e66846857eb75983c6e687f4ace4` | `e3d477b52d9510c2431931dfe3ead3c78bd7a970c0a74424a056089fcc8d9a3a` / `0245c2be5e50cf4d36a07aa76b10b6aac952c157c21ed317180e6f6450e1c791` |

Every manifest pins the official Core `v0.4.1` wheel:

```text
https://github.com/reblocke/wald-inference-core/releases/download/v0.4.1/
wald_inference-0.4.1-py3-none-any.whl
SHA-256 d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b
```

The staged 14-file Core package digest is
`44c52ba0189155e0d976e283d383f17f3db0679563ec6dc6d45b9829c4a43b4d`
in every app. Each site retains `web/.nojekyll`, the worker path, local staged-package imports, and
the expected GitHub Pages-relative asset paths.

## Fresh detached-tag verification

Each repository was cloned into a new directory at the exact annotated tag, creating a detached
HEAD and a new `.venv`. CPython 3.12.13 was selected from the checked-in version contract.

Commands run in each clone:

```bash
uv sync --locked
uv run playwright install chromium webkit
make verify
uv run pytest -q tests/scientific_reference/ tests/regression/  # critical, Type S/M, precision
uv run pytest -q tests/regression/test_legacy_compatibility.py  # compatibility
uv run python scripts/stage_browser_packages.py
git diff --check
git status --short --untracked-files=no
```

Results:

| Repository | Non-E2E | Chromium | WebKit smoke | Extra scientific/regression | Final tracked state |
|---|---:|---:|---:|---:|---|
| Compatibility | 57 passed | 7 passed | 1 passed | 11 passed | clean |
| Critical effect | 60 passed | 12 passed | 1 passed | 13 passed | clean |
| Type S/M | 74 passed | 21 passed | 1 passed | 8 passed | clean |
| Precision | 51 passed | 6 passed | 1 passed | 5 passed | clean |

Ruff format and lint, strict JSON/contracts, deterministic staging, browser privacy/storage/network
checks, accessibility checks, and export paths are included in the repository verification
targets. No tests were skipped or xfailed in these commands.

Raw verification-log SHA-256 digests:

| Repository | Log SHA-256 |
|---|---|
| Compatibility | `fe5655a301786f6143dd95f026681533bad0eb80dda249c282c908be272645e2` |
| Critical effect | `5877a82eb2a3c4be39a6a1740e439fbae3a651648be29c91ef180626606f2915` |
| Type S/M | `690d60876f564d5eea616258d90f93b9d84d60aed0d7fee44a8cf8f34929349b` |
| Precision | `2f916d89625cc94d4c2b4b16beb39d225a92a6a5f87fc249c2ba0772c84eeeac` |

## Predecessor-diff review

Exact compare ranges:

| Repository | Predecessor -> final | Commits ahead/behind | Diff finding |
|---|---|---|---|
| Compatibility | `v0.1.2...v0.1.3` | 2 / 0 | documentation, version surfaces, version assertions only |
| Critical effect | `v0.1.2...v0.1.3` | 2 / 0 | documentation, version surfaces, version assertions only |
| Type S/M | `v0.1.2...v0.1.3` | 2 / 0 | documentation, version surfaces, version assertions only |
| Precision | `v0.1.1...v0.1.2` | 2 / 0 | documentation, version surfaces, version assertions only |

No contract/model/scientific module, calculation worker, Plotly builder, privacy/storage/network
implementation, export implementation, or user-input/default behavior changed. Production-code
changes are limited to package/browser version constants and visible version labels. Test changes
assert the new version and the README release/citation policy. The full exact-tag verification
above confirms the claimed behavior preservation.

## Metadata, licensing, and public-copy audit

All four final tags agree on:

- author and maintainer: Brian Locke;
- `CITATION.cff` given/family name: Brian / Locke;
- license and repository visibility: MIT / public;
- package, lock, staged app, browser display, changelog, and `CITATION.cff` version;
- exact versioned GitHub release URL;
- experimental software maturity;
- citation instruction to use the exact tagged release or commit; and
- exact Core `v0.4.1` URL and digest.

No final-tag README or release body claims that the software is stable, clinically validated, or
portfolio validated. GitHub reports all four release objects as `prerelease=true`, matching the
public wording.

## CI transient retained as evidence

Critical Effect Size main CI run `30562550969` attempt 1 had one WebKit readiness timeout: the
runtime remained `loading` for 120 seconds. The unchanged failed-job rerun, attempt 2, completed
successfully, as did exact-tag Release run `30563030057` and this independent local WebKit smoke.
The isolated first-attempt timeout is retained as a nonblocking browser-runtime flake; it is not
silently erased.

Successful exact-head workflow runs:

| Repository | CI | Pages | Release |
|---|---:|---:|---:|
| Compatibility | `30562402814` | `30562402825` | `30562751740` |
| Critical effect | `30562550969` attempt 2 | `30562550556` | `30563030057` |
| Type S/M | `30562550798` | `30562550837` | `30562943828` |
| Precision | `30562403106` | `30562404073` | `30562752493` |

## Remaining limitations

1. Tags are annotated but unsigned.
2. The audit proves clean network installation, not offline installation.
3. These four exact releases are ready inputs to the portfolio report; they do not by themselves
   complete CC-MIG-11, update the catalog manifest, create `data/validation_status.json`, or
   promote any GitHub prerelease to stable.
