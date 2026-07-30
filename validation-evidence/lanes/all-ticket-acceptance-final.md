# All-ticket acceptance record: CC-MIG-00 through CC-MIG-11

Recorded: `2026-07-30T18:52:46Z`
Evidence-carrier target: `reblocke/wald-inference-tools` v0.2.0
Mode: independent prepublication synthesis

## Decision and evidence boundary

**The implementation portfolio is validated for release at the prepublication candidate
boundary.** The evidence below covers all 145 bullet acceptance criteria in CC-MIG-00 through
CC-MIG-11. No scientific, functional, privacy, accessibility, documentation, metadata, release
artifact, or reproducibility blocker remains in the eight already published final identities or
the catalog v0.2.0 source candidate.

This record is valid inside the catalog evidence carrier only when that carrier's checked-in
validators confirm all of the following in the same commit:

- `data/tools.json` contains the exact release set below and portfolio status `validated`;
- `docs/PORTFOLIO_VALIDATION_REPORT.md` has an allowed explicit verdict and complete A-H scores;
- `data/validation_status.json` contains the exact report SHA-256 and repository inventory;
- `validation-evidence/inventory/release-inventory.json` validates against the report, status,
  release objects, assets, deployments, and live manifests;
- `validation-evidence/index.json` enumerates and hashes every preserved evidence file, including
  this record;
- `make verify`, `make live-check`, the report/status/evidence validators, and clean-tree checks
  pass.

The catalog's own v0.2.0 tag, stable GitHub release, release assets, and Pages deployment cannot be
evidence inside their own tag. Their postpublication reconciliation is therefore the single
remaining **external** gate. This is a non-circular evidence boundary, not an unreported
acceptance failure. Actual goal closure requires the external audit described at the end of this
record.

## Exact audited portfolio

| Repository | Audited release | Peeled commit | GitHub publication state |
|---|---|---|---|
| `reblocke/wald-inference-core` | v0.4.1 | `f4613177b6dc81d194aa70762152de2bfa86663b` | stable, non-draft |
| `reblocke/scientific-applet-template` | v0.1.1 | `c13d27de9fa456075cb9e52d897a5e9f866d8f32` | stable, non-draft |
| `reblocke/compatibility-curve` | v0.1.3 | `0abf653cb455885b07765d4b9fe1af4cc38cf3b2` | prerelease, non-draft |
| `reblocke/wald-likelihood-support` | v0.1.2 | `7f5557d2a93235e25215261ef5890868b3fb07bb` | prerelease, non-draft |
| `reblocke/critical-effect-size` | v0.1.3 | `a10482c73cdb89d37814bf1b8c955166957ecd6b` | prerelease, non-draft |
| `reblocke/type-s-m-calibrator` | v0.1.3 | `ed8881d13eea8ecffa77304555d251296d63f058` | prerelease, non-draft |
| `reblocke/precision-guardrail-planner` | v0.1.2 | `ec47753aa1119b802e12856c4bc18feefa1ad6d5` | prerelease, non-draft |
| `reblocke/conf_curve_likelihood` | v0.2.5 | `1c283a5e1774b371b658469156fa24b9a397b8e6` | prerelease, non-draft |
| `reblocke/wald-inference-tools` | audited predecessor v0.1.1 | `6fffdd51dbf5c53beeb6146f9deb10daeb194760` | prerelease, non-draft |
| `reblocke/wald-inference-tools` | evidence carrier target v0.2.0 | resolved by carrier commit | intended stable release; external reconciliation required |

All nine repositories are public, use MIT licensing and Brian Locke authorship, use `main` as the
default branch, have Issues enabled, and are not archived. The template alone is configured as a
GitHub template. All static applications use workflow-based GitHub Pages with HTTPS.

All six Core consumers pin the official Core v0.4.1 wheel by exact release URL and SHA-256
`d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b`.

## Preserved evidence used

- Numerical/formula ownership and B01-B08 parity:
  `lanes/corrected-release-set-lane-ab.md`, `lanes/core-likelihood-final-ab.md`,
  `results/core-v0.4.1-baseline-parity.json`, and the preserved independent audit drivers.
- Cold start and release provenance:
  `lanes/corrected-release-set-lane-cd.md`,
  `lanes/focused-docs-only-final-release-supplement.md`,
  `lanes/catalog-template-v0.1.1-cdef.md`, the repository-specific CDEF ledgers, and
  `lanes/integrated-v0.2.5-cdef.md`.
- Browser, privacy, accessibility, mobile containment, and recovery:
  `browser/browser-summary.json`, the three corrected browser result files, and their preserved
  drivers.
- Exact commands and release identity:
  `commands/README_COMMANDS.md` and
  `inventory/release-inventory.json`.
- Final synthesis and machine binding:
  `docs/PORTFOLIO_VALIDATION_REPORT.md`, `data/validation_status.json`,
  `data/tools.json`, and `validation-evidence/index.json`.

## Ticket-by-ticket acceptance

The criterion counts below correspond one-for-one to the bullet acceptance criteria at the cited
ticket locators.

| Ticket | Acceptance locator | Criteria | Disposition | Direct evidence summary |
|---|---|---:|---|---|
| CC-MIG-00 | `tickets/00_freeze_integrated_baseline.md:394-407` | 14 | PASS | Source/environment freeze, 22 B01-B08 cases, deterministic 50-artifact corpus, strict JSON/export schemas, negative control, baseline tag/release, metadata audit, and clean verification. |
| CC-MIG-01 | `tickets/01_extract_wald_inference_core.md:460-473` | 14 | PASS | Public MIT Core; pure typed package; one formula owner; nine effects/six rules; finite/undefined/property/reference tests; 23,095-value parity; reproducible wheel/sdist; clean-wheel smoke; CI; docs; exact checksums; stable v0.4.1 release. |
| CC-MIG-02 | `tickets/02_rewire_integrated_workbench.md:326-337` | 12 | PASS | Exact released Core pin; no app formula fork; legacy API and 22 golden cases; strict JSON; browser; deterministic staging; one local/Pages path; documented ownership; retained URL; release notes; clean checkout. |
| CC-MIG-03 | `tickets/03_create_scientific_applet_template.md:328-338` | 11 | PASS | Public MIT GitHub template; disposable initializer/self-test; no required placeholders or domain formulas; reproducible generic staging; strict browser contract; accessibility/privacy; CI/Pages; usage/release/maintenance metadata; stable v0.1.1 release. |
| CC-MIG-04 | `tickets/04_build_compatibility_curve.md:314-326` | 13 | PASS | Focused compatibility scope; nine effects; B01-B03/B08 parity; negative-scope contract; CSV/PNG/caption/errors; strict JSON; Chromium/WebKit; privacy/accessibility; complete docs; exact visible Core pin; accurate cross-links. |
| CC-MIG-05 | `tickets/05_build_wald_likelihood_support.md:327-337` | 11 | PASS | Core support primitives; focused repo/Pages; legacy likelihood/S-minus-2 parity; analytic generic intervals; log-safe pairwise support; negative-scope contract; strict JSON; exports; browser/privacy/accessibility; exact-versus-approximate wording; exact Core pin. |
| CC-MIG-06 | `tickets/06_build_critical_effect_size.md:342-352` | 11 | PASS | Released detectability API; focused repo/Pages; exact critical effect primary; separately labeled legacy benchmark; one/two-sided and CI/direct-SE references; ratio behavior; negative-scope contract; exports; browser/privacy/accessibility; complete limitations/docs. |
| CC-MIG-07 | `tickets/07_build_type_s_m_calibrator.md:320-331` | 12 | PASS | Six rules; B04/B05/B07 parity; negative-scope contract; conditioning/nonposterior wording; direct-SE/CI modes; ratio-scale Type M; null/undefined strict JSON; uncapped exports; browser/privacy/accessibility; complete docs; exact Core pin. |
| CC-MIG-08 | `tickets/08_build_precision_guardrail_planner.md:342-352` | 11 | PASS | Released joint/sensitivity API; focused repo/Pages; B06/B07 parity; per-target/joint semantics; binding/infeasibility; sufficient-current multiplier; caveated sample-size option; negative-scope contract; exports; browser/privacy/accessibility; assumptions/non-goals. |
| CC-MIG-09 | `tickets/09_build_catalog_and_crosslinks.md:267-277` | 11 | PASS at carrier-source boundary | Public MIT catalog/Pages predecessor; question cards; conditioning table; strict manifest; live links; exact final app/Core versions; app cross-links; no statistical code; accessibility/privacy; CI/Pages workflows; maintenance/update docs. Stable v0.2.0 publication is the external gate. |
| CC-MIG-10 | `tickets/10_finalize_integrated_workbench.md:249-259` | 11 | PASS | v0.2.5 preserves URLs/imports, 22 cases, 208 non-E2E and 49 Chromium tests plus WebKit smoke; no formula fork; exact catalog/focused links; paradigm distinction; maintenance/templates; synchronized metadata; exact Pages/release assets; clean detached verification. |
| CC-MIG-11 | `tickets/11_independent_portfolio_validation.md:345-358` | 14 | PASS under carrier invariants | Every repository/release and documented command identified; B01-B08 and formula ownership; scope separation; cold installs/builds/two-engine browser; artifacts/checksums; privacy/accessibility; Brian Locke/MIT reconciliation; complete A-H scores; explicit verdict; fail-closed status; report/status/index hash binding; fixes isolated and independently rerun. |

Coverage arithmetic:
`14 + 14 + 12 + 11 + 13 + 11 + 11 + 12 + 11 + 11 + 11 + 14 = 145`.

## Additional non-bullet constraints

| Locator | Requirement | Prepublication disposition |
|---|---|---|
| `tickets/01_extract_wald_inference_core.md:28` | First stable Core release reproduces the baseline | PASS: v0.4.1 is stable and the frozen/independent parity evidence passes. |
| `tickets/01_extract_wald_inference_core.md:428` | First stable version should normally be 0.1.0 | PASS with recorded version rationale: “normally” is nonbinding; v0.4.1 is the first stable artifact after the corrective prerelease sequence, without changing the frozen authority. |
| `tickets/09_build_catalog_and_crosslinks.md:238` | Stable catalog release records the initial portfolio versions | EXTERNAL PUBLICATION GATE: the v0.2.0 carrier source records the exact final set; its stable release state must be verified after publication. |
| `tickets/11_independent_portfolio_validation.md:60-71` | Report/status in catalog, checksum-addressed, no early pass | PASS only under the carrier invariants above: report, status, inventory, and evidence index are committed and mutually hash-bound; publication is not used as evidence for the verdict. |

## Public wording and nonblocking limitations

Public lifecycle wording is internally consistent:

- Core v0.4.1 and template v0.1.1 are stable releases.
- The five focused scientific apps and integrated v0.2.5 are explicitly experimental
  prereleases.
- The catalog v0.2.0 source candidate describes itself as the stable validation-bearing release;
  that statement becomes externally confirmed only after publication.
- No repository claims clinical validation, exact fitted-model profile-likelihood recovery,
  posterior interpretation, or patient-level suitability.

Unsigned annotated tags, lack of PyPI distribution, no manual assistive-technology study, and
external CDN/GitHub availability are documented nonblocking limitations. They do not weaken the
scientific contracts or the explicit validation threshold.

## Required external v0.2.0 reconciliation

After the carrier is merged and published, an independent external audit must verify:

1. the annotated `v0.2.0` tag object peels to the reviewed merge commit and names Brian Locke;
2. the GitHub release is non-draft, stable (`prerelease=false`), and the repository's latest
   stable release;
3. release, CI, and Pages workflows succeed at that exact commit;
4. the Pages deployment and live `data/tools.json`, report, status, and evidence index resolve to
   the exact carrier bytes;
5. every release asset matches its GitHub digest and `SHA256SUMS`;
6. the source archive, site archive, report, status, tools manifest, evidence index, and evidence
   archive reproduce from a fresh detached-tag checkout;
7. `make verify`, `make live-check`, documented build/serve checks, and clean-tree checks pass from
   that checkout;
8. the external 145-row acceptance matrix is refreshed and checksum-addressed with the actual
   catalog tag/release/Pages identity.

Only that external reconciliation closes the overall migration goal. It may not retroactively
serve as evidence inside the v0.2.0 tag.
