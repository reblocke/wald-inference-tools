# Maintenance

## Ownership and status

- Maintenance owner: Brian Locke
- Product status: maintained static catalog
- Public site: <https://reblocke.github.io/wald-inference-tools/>
- Metadata authority: `data/tools.json`

## Updating an existing app

1. Wait for the app release and Pages deployment.
2. Record the exact app version, Core version, repository, hosted URL, citation file, app
   distribution, and hosted manifest URL in `data/tools.json`.
3. Keep `release-candidate` or another evidence-limited status until the validation record supports
   a stronger label.
4. Run `make verify` and `make live-check`.
5. Review the rendered card and comparison row at mobile and desktop widths.
6. Confirm the app's public `## Related Wald tools` README block names the same pinned Core release
   and links the catalog, adjacent tool, integrated workbench, app repository, and privacy note.
7. Open a narrow catalog PR. If related-tool links changed, use separate narrow PRs in affected
   apps.

## Adding an app

Add a complete manifest object and update the validator's expected portfolio only after the new
tool's scope is approved. The card must state its inferential question, conditioning, x-axis
meaning, inputs, outputs, non-goals, and primary limitation. Do not infer a scientific validation
status from the existence of a release.

## Release policy

Catalog releases are stable only when all listed release tags and hosted app/Core manifests agree.
The tag must match `catalog_version`, `CITATION.cff`, and `CHANGELOG.md`. The release workflow runs
all local browser gates, repeats the live metadata check, and publishes deterministic source/site
artifacts with checksums.

CI and Pages also run the live check. This prevents a manifest whose public release, hosted stage,
or README block is stale from reaching the catalog site before the release workflow runs.

If a deployed app becomes inconsistent, correct the app or catalog in an isolated PR and mark its
validation status conservatively until verification is rerun. Never silently point a released
catalog tag at unreleased behavior.
