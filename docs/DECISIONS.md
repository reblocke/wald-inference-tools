# Catalog decisions

## 2026-07-31 — Maintenance-only releases inherit bounded scientific validation

Catalog v0.2.2 records the final dependency, workflow, and version-only patch releases produced
after the Core v0.4.2 portfolio audit. Core, the scientific implementation modules, the pinned
Core wheel, and the frozen integrated golden corpus are unchanged. A bounded predecessor-diff
review, exact-tag verification, full repository CI, regenerated live-package checks, and renewed
browser/privacy/accessibility observations therefore supplement rather than replace the prior
independent numerical validation.

The catalog carrier audits immutable predecessor v0.2.1. Its own v0.2.2 tag, release assets,
workflows, and Pages bytes remain terminal external reconciliation gates after publication. This
is a genuine metadata refresh for newly released app versions, not a release created solely to
describe the preceding catalog carrier.

## 2026-07-31 — Validation carrier updates use a released catalog predecessor

Catalog v0.2.1 refreshes the independent portfolio evidence for Core v0.4.2 and the corresponding
template, focused-app, and integrated-workbench releases. Its checked-in catalog row audits the
already published v0.2.0 predecessor. The v0.2.1 tag object, stable immutable release, exact eight
assets, successful workflows, and Pages bytes are the terminal external reconciliation after
publication.

This boundary is intentional: a commit cannot contain the digest and publication identity of its
own immutable release assets. Publishing v0.2.2 solely to describe v0.2.1 would move, not solve,
that self-reference. The external reconciliation therefore closes v0.2.1 without being used as
evidence for the scientific verdict carried inside v0.2.1.

## 2026-07-31 — Release integrity does not require account-level credentials

At the repository owner's direction, new releases no longer require GitHub's verified-signature
status for tag objects or a fine-grained Administration-read token stored as an Actions secret.
Those gates required account reauthentication and persistent release credentials without changing
the catalog's scientific evidence or release contents.

Version tags remain annotated and must resolve through the exact remote tag object to the event
commit already contained in protected `main`. The workflow still verifies the version, releasable
validation verdict, deterministic asset set, release body, checksums, and downloaded bytes before
publishing a draft once. Repository release immutability is enabled as an operator precondition,
and the workflow fails unless the published release reports immutable status. The signed-tag and
settings-token portions of the 2026-07-30 governance decision are superseded; its remaining
integrity controls continue unchanged.

## 2026-07-30 — Governance hardening does not change portfolio evidence

Repository automation now pins reviewed GitHub Actions by full commit, retains the required
`test`, `live-metadata`, `browsers (chromium)`, and `browsers (webkit)` contexts, and applies
least-privilege permissions and concurrency controls. Future release workflows fail closed on a
signed annotated remote tag, exact event-commit binding, and protected-`main` containment before
project metadata is read or repository code executes.

The release path independently rejects a validation verdict that still reports release blockers,
then builds the existing deterministic source, site, manifest, report, status, evidence archive,
evidence index, and checksum assets; transfers the complete bundle; requires immutable-release
configuration; creates a stable draft; then redownloads and compares the exact body, names, bytes,
and checksums before one-time publication. These are repository-integrity controls, not
independent scientific validation.

This change deliberately leaves catalog version 0.2.0, `data/tools.json`, the portfolio report,
machine-readable validation status, evidence files and hashes, public site behavior, and existing
v0.2.0 tag/release assets unchanged. A future evidence or metadata change still requires the
independent review defined below and must continue to pass `make live-check`.

## 2026-07-30 — Validation-bearing v0.2.0 is stable

Independent CC-MIG-11 review resolved content-addressed annotated-tag objects, peeled commits, and
deployed commits for all nine repositories, reran the six review lanes, closed the five original
release blockers, and recorded no remaining blocker. The catalog may therefore change its manifest
from `release-candidate` to `validated` only in the same commit that adds the digest-bound report,
machine-readable status, and checksum-addressed evidence.

The report audits catalog v0.1.1 as the released predecessor. Catalog v0.2.0 is the evidence
carrier, so its successful publication is verified after the verdict but is not circularly used
to establish that verdict. Validation-bearing catalog tags publish directly as stable releases.

## 2026-07-30 — Corrective release metadata remains evidence-limited (historical)

**Status:** Superseded on 2026-07-30 by the validation-bearing v0.2.0 decision above. The versions
and `release-candidate` state below record the earlier checkpoint and are not current catalog
policy.

The catalog records Core v0.4.1; compatibility, likelihood, critical-effect, and Type S/M
v0.1.2; precision v0.1.1; and integrated workbench v0.2.2 only after their exact tags and hosted
manifests agree. Metadata synchronization does not itself establish portfolio validation: all
entries remain `release-candidate` until the independent audit is rerun and its report and
machine-readable status are committed.

The live metadata gate resolves every app's annotated tag to its peeled commit and requires the
deployed staged-package manifest to name that exact `source_commit`. Matching version strings alone
is insufficient because a Pages deployment can otherwise drift ahead of its release.

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
