# CC-MIG-11 resolved command ledger

Audit date: 2026-07-30 UTC

This ledger separates the commands actually retained as audit drivers from
normalized, rerunnable expansions of lane wrappers. The lane reports and JSON
results record the observed outputs, tag objects, peeled commits, workflow
runs, asset digests, numerical differences, and command outcomes. The blocks
below contain resolved repository/tag pairs rather than unresolved owner/name
or tag tokens.

## Content-addressed release identity and hosted provenance

The final inventory is collected from the GitHub API and live Pages sites. Its
timestamp is supplied by the final machine-readable status rather than being
invented in this ledger:

```bash
validated_at="$(jq -er '.validated_at' data/validation_status.json)"
node validation-evidence/drivers/collect_release_inventory.mjs \
  --validated-at "$validated_at" \
  --output validation-evidence/inventory/release-inventory.json
```

The collector's final resolved target set is:

```text
reblocke/wald-inference-core v0.4.1
reblocke/scientific-applet-template v0.1.1
reblocke/compatibility-curve v0.1.3
reblocke/wald-likelihood-support v0.1.2
reblocke/critical-effect-size v0.1.3
reblocke/type-s-m-calibrator v0.1.3
reblocke/precision-guardrail-planner v0.1.2
reblocke/wald-inference-tools v0.1.1
reblocke/conf_curve_likelihood v0.2.5
```

The following executable expansion shows the exact repository/tag inputs used
for repository, annotated-tag-object, release, workflow, and deployment
queries. Values such as tag-object SHA and deployment ID are resolved from the
preceding API response rather than represented by a placeholder:

```bash
while read -r repository tag; do
  gh repo view "$repository" \
    --json nameWithOwner,url,visibility,isTemplate,licenseInfo,defaultBranchRef
  tag_object_sha="$(
    gh api "repos/$repository/git/ref/tags/$tag" --jq '.object.sha'
  )"
  gh api "repos/$repository/git/tags/$tag_object_sha"
  gh release view "$tag" --repo "$repository" \
    --json tagName,isPrerelease,isDraft,publishedAt,url,assets,name,targetCommitish
  gh run list --repo "$repository" --limit 100 \
    --json databaseId,workflowName,status,conclusion,headSha,headBranch,event,url,createdAt,updatedAt
  if [ "$repository" != "reblocke/wald-inference-core" ]; then
    gh api "repos/$repository/deployments?environment=github-pages&per_page=100"
  fi
done <<'TARGETS'
reblocke/wald-inference-core v0.4.1
reblocke/scientific-applet-template v0.1.1
reblocke/compatibility-curve v0.1.3
reblocke/wald-likelihood-support v0.1.2
reblocke/critical-effect-size v0.1.3
reblocke/type-s-m-calibrator v0.1.3
reblocke/precision-guardrail-planner v0.1.2
reblocke/wald-inference-tools v0.1.1
reblocke/conf_curve_likelihood v0.2.5
TARGETS
```

The collector fails closed unless each tag ref points to an annotated tag
object, the object peels to the release commit, the applicable Release
workflow succeeded at that commit, and the matching Pages deployment
succeeded. For staged-package sites, the live manifest must name the same
`source_commit`. The Core has no Pages site. The catalog predecessor
intentionally has no manifest `source_commit`; its live provenance is instead
bound by the Pages deployment SHA, exact `catalog_version`, and live-static-file
byte comparison.

Annotated-tag objects and peeled commits are content-addressed. The associated
tag refs and GitHub release records are not immutable: all audited tags are
unsigned, and a privileged maintainer can move or delete a ref or edit or
delete a release. The inventory therefore records both object identities and
the observed GitHub state at the audit time.

Release assets were downloaded and verified with this resolved matrix:

```bash
asset_root="$(mktemp -d "${TMPDIR:-/tmp}/cc-mig-11-assets.XXXXXX")"
while read -r repository tag; do
  repository_name="${repository#reblocke/}"
  destination="$asset_root/$repository_name-$tag"
  mkdir -p "$destination"
  gh release download "$tag" --repo "$repository" --dir "$destination"
  (
    cd "$destination"
    shasum -a 256 -c SHA256SUMS
  )
done <<'TARGETS'
reblocke/wald-inference-core v0.4.1
reblocke/scientific-applet-template v0.1.1
reblocke/compatibility-curve v0.1.3
reblocke/wald-likelihood-support v0.1.2
reblocke/critical-effect-size v0.1.3
reblocke/type-s-m-calibrator v0.1.3
reblocke/precision-guardrail-planner v0.1.2
reblocke/wald-inference-tools v0.1.1
reblocke/conf_curve_likelihood v0.2.5
TARGETS
```

GitHub API `assets[].digest` values and local SHA-256 values were also compared
in the release-specific lane records.

## Cold clones and repository verification

The following normalized expansion gives every exact clone/tag input. Each
lane used a new temporary parent and detached checkout; the lane report, not
the loop syntax here, is the authority for the original shell transcript and
exit status.

```bash
audit_root="$(mktemp -d "${TMPDIR:-/tmp}/cc-mig-11-cold.XXXXXX")"
while read -r repository tag; do
  repository_name="${repository#reblocke/}"
  checkout="$audit_root/$repository_name"
  gh repo clone "$repository" "$checkout"
  git -C "$checkout" fetch --force --tags origin
  git -C "$checkout" checkout --detach "$tag"
  git -C "$checkout" cat-file -t "refs/tags/$tag"
  git -C "$checkout" rev-parse "refs/tags/$tag"
  git -C "$checkout" rev-parse "refs/tags/$tag^{commit}"
  git -C "$checkout" status --short
done <<'TARGETS'
reblocke/wald-inference-core v0.4.1
reblocke/scientific-applet-template v0.1.1
reblocke/compatibility-curve v0.1.3
reblocke/wald-likelihood-support v0.1.2
reblocke/critical-effect-size v0.1.3
reblocke/type-s-m-calibrator v0.1.3
reblocke/precision-guardrail-planner v0.1.2
reblocke/wald-inference-tools v0.1.1
reblocke/conf_curve_likelihood v0.2.5
TARGETS
```

Exact-tag verification then used:

```bash
(
  cd "$audit_root/wald-inference-core"
  uv sync --locked --all-groups
  make verify
  uv build
)
for repository_name in \
  scientific-applet-template \
  compatibility-curve \
  wald-likelihood-support \
  critical-effect-size \
  type-s-m-calibrator \
  precision-guardrail-planner \
  conf_curve_likelihood
do
  (
    cd "$audit_root/$repository_name"
    uv sync --locked
    uv run playwright install chromium webkit
    make verify
  )
done
(
  cd "$audit_root/conf_curve_likelihood"
  uv run python scripts/generate_golden_baseline.py --check
  uv run python scripts/compare_golden_baseline.py
  uv run pytest -q tests/integration/test_golden_baseline.py
)
(
  cd "$audit_root/wald-inference-tools"
  uv sync --locked
  uv run playwright install chromium webkit
  make verify
  make live-check
)
```

The catalog predecessor's `make live-check` observation is tied to its audit
window; later catalog publication can legitimately make that historical live
comparison stale. Exact per-repository test counts, dependency versions,
package builds, stage comparisons, and clean-worktree results are retained in
`validation-evidence/lanes/`.

## Bounded local-server checks and exit-code provenance

Browser repositories were served sequentially on their documented fixed port
to avoid port collisions. The retained procedure bounded readiness, required
HTTP 200 for the listed routes, intentionally interrupted the long-running
server, recorded that controlled-stop exit separately, and confirmed that no
listener remained:

```bash
serve_check() {
  checkout="$1"
  shift
  serve_log="$(mktemp "${TMPDIR:-/tmp}/cc-mig-11-serve.XXXXXX")"
  (
    cd "$checkout"
    make serve
  ) >"$serve_log" 2>&1 &
  serve_pid="$!"

  ready=0
  for attempt in $(seq 1 60); do
    if curl -fsS "http://127.0.0.1:8000/" >/dev/null; then
      ready=1
      break
    fi
    sleep 1
  done
  test "$ready" -eq 1
  for route in "$@"; do
    curl -fsS "http://127.0.0.1:8000$route" >/dev/null
  done

  kill -INT "$serve_pid"
  set +e
  wait "$serve_pid"
  serve_exit="$?"
  set -e
  printf '%s\tmake serve controlled-stop exit\t%s\n' "$checkout" "$serve_exit"
  case "$serve_exit" in
    1|130) ;;
    *) exit "$serve_exit" ;;
  esac
  ! lsof -nP -iTCP:8000 -sTCP:LISTEN
}

serve_check "$audit_root/scientific-applet-template" \
  /assets/py/manifest.json /pyodide_worker.js
serve_check "$audit_root/compatibility-curve" \
  /assets/py/manifest.json /pyodide_worker.js
serve_check "$audit_root/wald-likelihood-support" \
  /assets/py/manifest.json /pyodide_worker.js
serve_check "$audit_root/critical-effect-size" \
  /assets/py/manifest.json /pyodide_worker.js
serve_check "$audit_root/type-s-m-calibrator" \
  /assets/py/manifest.json /pyodide_worker.js
serve_check "$audit_root/precision-guardrail-planner" \
  /assets/py/manifest.json /pyodide_worker.js
serve_check "$audit_root/conf_curve_likelihood" \
  /assets/py/manifest.json /pyodide_worker.js
serve_check "$audit_root/wald-inference-tools" \
  /data/tools.json /docs/PRIVACY.md
```

The C/D lane reports preserve HTTP success before shutdown, the controlled
nonzero `make serve` outcome (reported as exit 1 where the shell wrapper
captured it), and the no-listener result. A deliberately discarded parallel
probe that collided on port 8000 is identified separately in those reports and
is not counted as repository evidence.

## Numerical and cross-application checks

The retained audit drivers were placed at the root of each corresponding
exact-tag checkout before invocation:

```bash
cp validation-evidence/drivers/audit_focused_diffs.py \
  "$audit_root/compatibility-curve/audit_focused_diffs.py"
(cd "$audit_root/compatibility-curve" && .venv/bin/python audit_focused_diffs.py compatibility)

cp validation-evidence/drivers/audit_focused_diffs.py \
  "$audit_root/critical-effect-size/audit_focused_diffs.py"
(cd "$audit_root/critical-effect-size" && .venv/bin/python audit_focused_diffs.py critical)

cp validation-evidence/drivers/audit_focused_diffs.py \
  "$audit_root/type-s-m-calibrator/audit_focused_diffs.py"
(cd "$audit_root/type-s-m-calibrator" && .venv/bin/python audit_focused_diffs.py type-sm)

cp validation-evidence/drivers/audit_focused_diffs.py \
  "$audit_root/precision-guardrail-planner/audit_focused_diffs.py"
cp validation-evidence/drivers/audit_precision_app_repairs.py \
  "$audit_root/precision-guardrail-planner/audit_precision_app_repairs.py"
(cd "$audit_root/precision-guardrail-planner" && .venv/bin/python audit_focused_diffs.py precision)
(cd "$audit_root/precision-guardrail-planner" && .venv/bin/python audit_precision_app_repairs.py)

cp validation-evidence/drivers/audit_integrated_diff.py \
  "$audit_root/conf_curve_likelihood/audit_integrated_diff.py"
(cd "$audit_root/conf_curve_likelihood" && .venv/bin/python audit_integrated_diff.py)
```

Core frozen parity, focused-app anchors, the precision boundary scan,
strict-JSON cases, integrated B01-B08 golden cases, and pairwise support
identity are captured in `validation-evidence/results/`.

## Live browser, responsive layout, privacy, and recovery

The retained Playwright drivers are directly executable from this catalog
checkout. The final run must capture both the Python process status and the
semantic JSON assertion; a process exit alone is insufficient because the
full live driver records per-site exceptions in JSON.

```bash
uv sync --locked
uv run playwright install chromium webkit

set +e
uv run python validation-evidence/drivers/live_browser_audit.py
live_driver_exit="$?"
jq -e \
  '[.sites[] | .chromium_desktop.ok, .chromium_mobile_390.ok, .webkit_smoke.ok] | all' \
  validation-evidence/browser/corrected-live-browser-results.json
live_assertion_exit="$?"

uv run python validation-evidence/drivers/mobile_containment_audit.py
mobile_driver_exit="$?"
jq -e '[.sites[].pass] | all' \
  validation-evidence/browser/corrected-mobile-containment.json
mobile_assertion_exit="$?"

uv run python validation-evidence/drivers/required_error_recovery_audit.py
recovery_driver_exit="$?"
jq -e '[(.sites // .)[].pass] | all' \
  validation-evidence/browser/corrected-required-error-recovery.json
recovery_assertion_exit="$?"

uv run python validation-evidence/drivers/focused_error_links_audit.py
focused_links_driver_exit="$?"
jq -e \
  '[.[] | (.error_role == "alert" and .link_present == true and .link_focuses_target == true and .aria_invalid == "true")] | all' \
  /private/tmp/cc-mig-11-ef-error-links.json
focused_links_assertion_exit="$?"
set -e

printf '%s\n' \
  "live driver=$live_driver_exit assertion=$live_assertion_exit" \
  "mobile driver=$mobile_driver_exit assertion=$mobile_assertion_exit" \
  "recovery driver=$recovery_driver_exit assertion=$recovery_assertion_exit" \
  "focused-links driver=$focused_links_driver_exit assertion=$focused_links_assertion_exit"
test "$live_driver_exit" -eq 0
test "$live_assertion_exit" -eq 0
test "$mobile_driver_exit" -eq 0
test "$mobile_assertion_exit" -eq 0
test "$recovery_driver_exit" -eq 0
test "$recovery_assertion_exit" -eq 0
test "$focused_links_driver_exit" -eq 0
test "$focused_links_assertion_exit" -eq 0
```

The final three JSON records under `validation-evidence/browser/` preserve the
released URL, viewport, interaction, export, recovery, network, storage,
driver hash, and audit window. The focused-links driver is the retained
precursor to the stricter recovery driver; its temporary output is not a
separate final evidence artifact.

## Evidence and catalog release artifacts

After all source evidence is final, the evidence index is generated and
validated with the same status timestamp:

```bash
validated_at="$(jq -er '.validated_at' data/validation_status.json)"
node validation-evidence/drivers/build_evidence_index.mjs \
  --root validation-evidence \
  --catalog-version 0.2.0 \
  --validated-at "$validated_at"
uv run python scripts/validate_validation_evidence.py
uv run python scripts/validate_validation_status.py
```

The catalog release artifacts are built twice and compared byte-for-byte:

```bash
release_root="$(mktemp -d "$PWD/.cc-mig-11-catalog-release.XXXXXX")"
cleanup_release_root() {
  case "${release_root:-}" in
    "$PWD"/.cc-mig-11-catalog-release.*)
      rm -rf -- "$release_root"
      ;;
    *)
      printf 'Refusing to remove unexpected release root: %s\n' "${release_root:-<unset>}" >&2
      return 1
      ;;
  esac
}
trap cleanup_release_root EXIT
uv run python scripts/build_release_artifacts.py \
  --version 0.2.0 --output "$release_root/release-a"
uv run python scripts/build_release_artifacts.py \
  --version 0.2.0 --output "$release_root/release-b"
diff -rq "$release_root/release-a" "$release_root/release-b"
(
  cd "$release_root/release-a"
  shasum -a 256 -c SHA256SUMS
)
(
  cd "$release_root/release-b"
  shasum -a 256 -c SHA256SUMS
)
```

The release builder requires a dedicated output directory inside the
repository. `mktemp` therefore creates both comparison roots under `$PWD`, and
the `EXIT` trap removes only a path that retains the guarded audit prefix.
Temporary build directories are not committed. The release workflow repeats the
deterministic build from the content-addressed commit reached by the published
`v0.2.0` annotated tag; the tag ref and GitHub release remain mutable
administrative objects.

## Core v0.4.2 final release-set refresh (2026-07-31)

This section records the command families used for the final stable/immutable
release set. Historical commands above remain preserved as evidence of the
earlier corrective sequence.

### Fresh-context Lane A/B

For each exact remote tag, the numerical lane used a fresh clone and detached
checkout, then resolved the annotated tag object and peeled commit:

    git clone --no-local https://github.com/reblocke/REPOSITORY.git CHECKOUT
    git -C CHECKOUT checkout --detach TAG^{}
    git -C CHECKOUT ls-remote origin refs/tags/TAG refs/tags/TAG^{}
    (cd CHECKOUT && uv sync --locked && make test)
    (cd CHECKOUT && git status --porcelain)

Core additionally used:

    uv sync --locked --all-groups
    make parity

The independent SciPy/normal-identity recomputation, formula-ownership scans,
staged-file byte comparisons, and B01-B08 comparison commands are described in
lanes/final-release-set-v0.4.2-lane-ab.md. Machine results are in
results/core-v0.4.2-baseline-parity.json and
results/core-v0.4.2-independent-recomputation.json.

### Fresh-context Lane C/D

Each published release was downloaded into an isolated parent and used a
release-specific fresh uv cache:

    git clone --no-local https://github.com/reblocke/REPOSITORY.git PARENT/REPOSITORY
    git -C PARENT/REPOSITORY checkout --detach TAG^{}
    env UV_CACHE_DIR=FRESH_CACHE uv sync --locked
    env PLAYWRIGHT_BROWSERS_PATH=FRESH_BROWSER_CACHE uv run playwright install chromium webkit
    make verify
    git status --porcelain
    gh release download TAG --repo reblocke/REPOSITORY --dir RELEASE_ASSETS
    (cd RELEASE_ASSETS && shasum -a 256 -c SHA256SUMS)
    gh release verify TAG --repo reblocke/REPOSITORY
    gh release view TAG --repo reblocke/REPOSITORY --json tagName,isDraft,isPrerelease,isImmutable,targetCommitish,assets
    gh api repos/reblocke/REPOSITORY/git/ref/tags/TAG
    gh api repos/reblocke/REPOSITORY/git/tags/TAG_OBJECT

Core reproducibility and official-wheel smoke used:

    uv run python scripts/build_release_artifacts.py --version 0.4.2 --output REBUILT_CORE
    cmp REBUILT_CORE/wald_inference-0.4.2-py3-none-any.whl RELEASE_ASSETS/wald_inference-0.4.2-py3-none-any.whl
    cmp REBUILT_CORE/wald_inference-0.4.2.tar.gz RELEASE_ASSETS/wald_inference-0.4.2.tar.gz
    uv venv OFFICIAL_WHEEL_VENV
    env UV_CACHE_DIR=FRESH_WHEEL_CACHE uv pip install --python OFFICIAL_WHEEL_VENV/bin/python RELEASE_ASSETS/wald_inference-0.4.2-py3-none-any.whl
    OFFICIAL_WHEEL_VENV/bin/python -c 'import wald_inference; print(wald_inference.__version__)'

Live manifest bytes were downloaded with curl --fail --location and compared
with each release manifest asset and staged file records. Exact results are in
lanes/final-release-set-v0.4.2-lane-cd.md and
results/final-release-set-v0.4.2-cold-start.json.

### Refreshed Lane E browser records

    CC_MIG_11_BROWSER_ARTIFACT_DIR=/private/tmp/cc-mig-11-v042-browser-artifacts \
      uv run python validation-evidence/drivers/live_browser_audit.py
    jq -e '[.sites[] | .chromium_desktop.ok, .chromium_mobile_390.ok, .webkit_smoke.ok] | all' \
      validation-evidence/browser/corrected-live-browser-results.json
    CC_MIG_11_BROWSER_ARTIFACT_DIR=/private/tmp/cc-mig-11-v042-browser-artifacts \
      uv run python validation-evidence/drivers/mobile_containment_audit.py
    jq -e '[.sites[].pass] | all' \
      validation-evidence/browser/corrected-mobile-containment.json
    uv run python validation-evidence/drivers/required_error_recovery_audit.py
    jq -e '[.sites[].pass] | all' \
      validation-evidence/browser/corrected-required-error-recovery.json

All three semantic assertions returned true. The independent E/F lane used the
same preserved driver from a separate temporary root and independently
inspected exact release snapshots, manifests, links, rights, and public copy.

### Final inventory, checksum chain, and catalog carrier

The final freeze uses one RFC 3339 UTC timestamp in the status, inventory,
browser summary, evidence index, and report:

    validated_at="$(jq -er '.validated_at' data/validation_status.json)"
    node validation-evidence/drivers/collect_release_inventory.mjs \
      --validated-at "$validated_at" \
      --output validation-evidence/inventory/release-inventory.json
    node validation-evidence/drivers/build_evidence_index.mjs \
      --root validation-evidence \
      --catalog-version 0.2.1 \
      --validated-at "$validated_at"
    shasum -a 256 validation-evidence/index.json
    shasum -a 256 docs/PORTFOLIO_VALIDATION_REPORT.md
    uv run python scripts/validate_validation_evidence.py
    uv run python scripts/validate_validation_status.py --require-releasable
    make verify
    make live-check
    git diff --check

Catalog v0.2.1 artifacts are built twice and compared:

    release_root="$(mktemp -d "$PWD/.cc-mig-11-catalog-v021.XXXXXX")"
    uv run python scripts/build_release_artifacts.py \
      --version 0.2.1 --output "$release_root/release-a"
    uv run python scripts/build_release_artifacts.py \
      --version 0.2.1 --output "$release_root/release-b"
    diff -rq "$release_root/release-a" "$release_root/release-b"
    (cd "$release_root/release-a" && shasum -a 256 -c SHA256SUMS)
    (cd "$release_root/release-b" && shasum -a 256 -c SHA256SUMS)

The repository-owner-approved release model deliberately omits cryptographic
tag signing and an Administration-read release-settings token. It retains
annotated tag-object identity, exact commit/main containment, stable
non-prerelease publication, immutable releases, deterministic checksummed
assets, draft-first publication, exact release-workflow identity, and
post-publication byte verification.
