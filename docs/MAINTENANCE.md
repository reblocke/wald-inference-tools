# Maintenance

## Ownership and status

- Maintenance owner: Brian Locke
- Product status: maintained static catalog
- Public site: <https://reblocke.github.io/wald-inference-tools/>
- Metadata authority: `data/tools.json`

## Updating an existing app

1. Wait for the app release and Pages deployment.
2. Record the exact app version, Core version, repository, hosted URL, citation file, app
   distribution, and hosted manifest URL in `data/tools.json`; the deployed manifest's
   `source_commit` must equal the annotated app tag's peeled commit.
3. Keep the existing evidence-limited status until a new independent validation record supports
   changing it. A successful app or catalog release does not establish validation.
4. Run `make verify` and `make live-check`.
5. Review the rendered card and comparison row at mobile and desktop widths.
6. Confirm the app's public `## Related Wald tools` README block names the same pinned Core release
   and links the catalog, adjacent tool, integrated workbench, app repository, and privacy note.
7. Confirm the deployed app footer contains the same compact block.
8. Open a narrow catalog PR. If related-tool links changed, use separate narrow PRs in affected
   apps.

## Adding an app

Add a complete manifest object and update the validator's expected portfolio only after the new
tool's scope is approved. The card must state its inferential question, conditioning, x-axis
meaning, inputs, outputs, non-goals, and primary limitation. Do not infer a scientific validation
status from the existence of a release.

## Release policy

The historical v0.1.x catalog tags were prerelease candidates while the independent
portfolio-validation milestone remained open. Version v0.2.0 and later validation-bearing tags
publish as stable releases only when all listed release tags and hosted app/Core manifests agree,
the report has no unresolved release-blocking finding, and the report/status/evidence hash chain
passes. The tag must match `catalog_version`, `CITATION.cff`, and `CHANGELOG.md`. The release
workflow runs all local browser gates, repeats the live metadata check, and publishes deterministic
source/site/evidence artifacts with checksums.

CI and Pages also run the live check. This prevents a manifest whose public release, exact deployed
commit, hosted stage, README block, or deployed footer is stale from reaching the catalog site
before the release workflow runs.

If a deployed app becomes inconsistent, correct the app or catalog in an isolated PR and mark its
validation status conservatively until verification is rerun. Never silently point a released
catalog tag at unreleased behavior.

## Repository governance and release integrity

Required branch checks remain `test`, `live-metadata`, `browsers (chromium)`, and
`browsers (webkit)`. CI and Pages retain the public live-metadata gate. Every third-party Action is
pinned to a reviewed full commit SHA with a version comment, checkout credentials are not
persisted, and write permissions exist only in the Pages deploy job and the release publish job.
Dependabot proposes grouped weekly lockfile and Actions updates only after a seven-day cooldown;
there is no automatic merge path.

A new version tag must be annotated, equal the catalog version, identify the exact tag event
commit, and target a commit already contained in protected `main`. Remote tag-object binding and
protected-main containment occur before project metadata is read or repository code executes.

The read-only release job runs the status validator with `--require-releasable`, repeats
`make verify` and `make live-check`, then builds exactly:

- the deterministic tracked-source archive;
- the deterministic static-site archive;
- the public tool manifest;
- the portfolio validation report;
- the machine-readable validation status;
- the complete validation-evidence archive;
- the checksum-addressed evidence index; and
- `SHA256SUMS` covering the seven substantive assets.

The publishing job receives only that bundle and the matching current-version changelog section.
Release immutability must be enabled before a tag is created; no account-level token is stored in
Actions. The job creates a draft stable release, verifies the exact body and asset inventory,
redownloads and byte-compares every asset, checks the downloaded checksums, and only then publishes
once and requires the resulting release to report immutable provenance.

The regular status validator accepts all three CC-MIG-11 verdicts so a failed audit can be recorded
coherently. Release-only mode additionally rejects `Not validated; release blockers remain.` before
any release bundle is created or transferred. A conditionally validated verdict remains
releasable only when its limitations are nonblocking and the report/status/rubric checks agree.

Version 0.2.0 predates this hardened release path. Its existing tag, body, and assets remain
historical evidence and must not be moved, rebuilt, replaced, or retroactively relabeled. A failed
future publication leaves its candidate as a draft for inspection; it does not authorize asset
replacement or tag movement.
