# Changelog

All notable changes to this project are documented here.

## [Unreleased]

## [0.2.0] - 2026-07-30

### Added

- Publish the independent CC-MIG-11 portfolio validation report, machine-readable status, exact
  command ledger, release inventory, browser/network summary, lane ledgers, audit drivers, and
  checksum-addressed evidence index.
- Attach the report, status, evidence index, and deterministic evidence archive directly to the
  catalog release.

### Changed

- Record the final audited release set: Core v0.4.1; template v0.1.1; compatibility v0.1.3;
  likelihood v0.1.2; critical effect v0.1.3; Type S/M v0.1.3; precision v0.1.2; integrated
  workbench v0.2.5; and catalog predecessor v0.1.1.
- Change every portfolio status from `release-candidate` to `validated` only after the independent
  report closed all release blockers and passed the fail-closed evidence gates.
- Publish this validation-bearing catalog tag as a stable GitHub release.

## [0.1.1] - 2026-07-30

### Changed

- Record the corrective `wald-inference` Core v0.4.1 release, the exact v0.1.2 compatibility,
  likelihood, critical-effect, and Type S/M releases, the v0.1.1 precision release, and the
  v0.2.2 integrated-workbench release.
- Keep every entry at `release-candidate` until the independent portfolio audit is rerun against
  the tagged and deployed corrective set.

## [0.1.0] - 2026-07-30

### Added

- Added a question-based catalog for the five focused Wald applets and integrated workbench.
- Added a machine-readable tool manifest, comparison table, and explicit use boundaries.
- Added local/live metadata validation, static Pages build, accessibility/privacy browser tests,
  and maintenance documentation.

[Unreleased]: https://github.com/reblocke/wald-inference-tools/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/reblocke/wald-inference-tools/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/reblocke/wald-inference-tools/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/reblocke/wald-inference-tools/releases/tag/v0.1.0
