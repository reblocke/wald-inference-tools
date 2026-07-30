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
