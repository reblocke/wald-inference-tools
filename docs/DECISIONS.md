# Catalog decisions

## 2026-07-30 — Corrective release metadata remains evidence-limited

The catalog records Core v0.4.1, focused apps v0.1.1, and integrated workbench v0.2.1 only after
their exact tags and hosted manifests agree. Metadata synchronization does not itself establish
portfolio validation: all entries remain `release-candidate` until the independent audit is
rerun and its report and machine-readable status are committed.

## D001: Keep the catalog a separate static product

**Status:** Accepted, 2026-07-30.

The portfolio catalog is a separate repository and GitHub Pages site. Its task is navigation:
match a reader's question to a focused app, preserve the distinction between observed-data
reconstruction and assumed-truth design calibration, and expose checked release metadata.

The separation is deliberate:

- A catalog update cannot change an app's numerical behavior.
- An app remains independently citable, versioned, deployable, and reproducible.
- The catalog cannot become a hidden shared runtime or single point of calculation failure.
- Readers can inspect the exact app/Core pairing before opening a tool.

The implementation is plain HTML, CSS, and JavaScript. `data/tools.json` is the single source for
card copy, comparison fields, release versions, and tool links. The browser renders that file
without accepting inputs or loading third-party code.

Rejected alternatives were a shared calculation shell, passing values between tools, duplicating a
mini-catalog in every app, and adding analytics. Those approaches would blur repository authority,
conditioning, privacy, or release boundaries.

## D002: Treat validation status as evidence, not marketing copy

**Status:** Accepted, 2026-07-30.

`validation_status` records the current evidence state. A released app is not automatically labeled
scientifically validated. Status changes require a recorded review and must be synchronized with
the portfolio validation report.

## D003: Pin and verify app/Core pairs

**Status:** Accepted, 2026-07-30.

The catalog checks an app's release tag and hosted staged-package manifest. The app and Core
versions displayed on a card must match the public deployment. These versions are metadata only;
the catalog does not download or execute Core.
