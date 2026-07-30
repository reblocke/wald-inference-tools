# CC-MIG-11 lane C/D/E/F evidence: conf_curve_likelihood v0.2.2

## Decision

**FAIL — lanes C, D, and E pass, but Lane F has release-documentation blockers.**

`reblocke/conf_curve_likelihood` v0.2.2 is **not independently validated for release** under
the complete ticket pack. The numerical/browser product and its release artifacts passed the
cold-start, provenance, deployed-browser, accessibility, and privacy checks below. The failure is
specific, reproducible, and documentary:

1. The canonical ticket-pack `VALIDATION_MATRIX.md` says that every scientific repository must
   contain `docs/SCIENTIFIC_SCOPE.md` and `docs/VALIDATION.md`. Both paths are absent from the exact
   v0.2.2 tag.
2. CC-MIG-10 requires the integrated-workbench release to state the current Core version, focused
   tool links, B01-B08 parity evidence, and maintenance policy. The latest v0.2.2 GitHub release
   body contains only the mobile-label delta and a behavior-preserving statement. The older v0.2.0
   release body contains the required categories but describes superseded Core v0.4.0; v0.2.1 is
   tagged but has no GitHub release.

The missing documents are not substituted by having related content distributed across README,
ADRs, tests, and historical migration records. The ticket pack made the files explicit release
deliverables, and the current repository lacks a single current validation record naming the exact
v0.2.2 commit/release and completed evidence.

This was a read-only audit of GitHub, the release, and the deployed site. Local verification used a
fresh temporary parent and detached exact-tag checkout. No existing worktree, production source, or
GitHub state was mutated.

Audit window: 2026-07-30T15:30:19Z through 2026-07-30T16:05:38Z.

## Audited identity

- Repository: `https://github.com/reblocke/conf_curve_likelihood`
- Hosted app: `https://reblocke.github.io/conf_curve_likelihood/`
- Release: `v0.2.2`
- Annotated tag object: `045a23f58ebfe444cb40355ebbb317d731812612`
- Peeled commit: `78d189ac03ec223a69778843497d27c70a8720c2`
- Expected commit: `78d189ac03ec223a69778843497d27c70a8720c2`
- Remote `main`: `78d189ac03ec223a69778843497d27c70a8720c2`
- Tagger: Brian Locke, 2026-07-30T15:16:25Z
- Tag message: `Release v0.2.2`
- Tag type: annotated Git object (`git cat-file -t` returned `tag`)
- Tag signature: unsigned (`git tag -v v0.2.2` exit 1, `no signature found`)
- GitHub release: published 2026-07-30T15:27:45Z, draft false, prerelease true
- Release workflow:
  `https://github.com/reblocke/conf_curve_likelihood/actions/runs/30555863567`;
  head SHA exact; verify-build and release jobs completed successfully
- Pages workflow:
  `https://github.com/reblocke/conf_curve_likelihood/actions/runs/30555099460`;
  head SHA exact; build and deploy jobs completed successfully
- Commit check runs: seven successful checks — test, Chromium E2E, WebKit smoke, Pages build,
  Pages deploy, release verify-build, and release publication
- GitHub repository metadata: public, active/not archived, MIT detected, `main` default, current
  integrated-workbench description, and canonical Pages homepage
- Superseded Node-runtime issue #5: closed as completed on 2026-07-30

## Environment

- Host: macOS 26.5.2 build 25F84, arm64
- Kernel: Darwin 25.5.0
- Git: 2.50.1 (Apple Git-155)
- GitHub CLI: 2.92.0
- uv: 0.11.11
- Host Python: 3.14.4
- Locked project Python: 3.11.10
- Node/npm (environment only): 25.9.0 / 11.12.1
- `confcurve`: 0.2.2
- `wald-inference`: 0.4.1
- NumPy/SciPy: 2.2.6 / 1.14.1
- pytest: 9.0.2
- Ruff: 0.15.1
- Hypothesis: 6.151.9
- Playwright: 1.58.0
- Chromium: 145.0.7632.6
- WebKit: 26.0
- Fresh parent:
  `/private/tmp/conf-curve-v022-audit.PDY2hE`
- Detached checkout:
  `/private/tmp/conf-curve-v022-audit.PDY2hE/conf_curve_likelihood`
- Release assets:
  `/private/tmp/conf-curve-v022-assets.gVD8dl`
- Live evidence:
  `/private/tmp/conf-curve-v022-live.uSByJH`

## Lane C — cold-start reproducibility

Fresh-clone command results:

| Command | Exit | Result |
|---|---:|---|
| `git clone --filter=blob:none https://github.com/reblocke/conf_curve_likelihood.git <fresh>/conf_curve_likelihood` | 0 | New clone |
| fetch and detach `refs/tags/v0.2.2^{}` | 0 | Exact detached commit |
| `uv sync --locked` | 0 | Clean Python 3.11 environment; no sibling checkout |
| `uv run playwright install chromium webkit` | 0 | Browser binaries installed/available |
| `make stage-web` | 0 | Exact source commit and package manifest below |
| `make fmt-check` | 0 | 34 files already formatted |
| `make lint` | 0 | All checks passed |
| `make golden-check` | 0 | 22 B01-B08 cases passed at `rtol=1e-12`, `atol=1e-14` |
| `make portfolio-links` | 0 | 20 checked-in requirements passed |
| `uv run python scripts/check_portfolio_links.py --live` | 0 | 20 checked-in requirements and 10 public targets passed |
| `make test` | 0 | 205 non-E2E tests passed |
| `make verify` | 0 | Staging, format, lint, links, golden, 205 non-E2E, and 49 Chromium E2E passed |
| documented WebKit initial-render smoke | 0 | One WebKit smoke test passed |
| `make serve` | controlled stop | Served `127.0.0.1:8000`; index HTTP 200; local manifest identity exact; Ctrl-C then exit 1 as expected |
| `uv run python scripts/generate_golden_baseline.py --check` | 0 | Integrity and definitions passed for 22 cases |
| `uv run python scripts/compare_golden_baseline.py` | 0 | Comparator passed for 22 cases |
| focused public-API/golden tests | 0 | 45 tests passed |
| `git diff --check` | 0 | No whitespace errors |
| `uv tree` | 0 | Dependency tree resolved |
| `git status --short` | 0 | Empty tracked status |
| `git diff --exit-code` / `git diff --cached --exit-code` | 0 / 0 | No tracked changes |

The ignored post-verification products were limited to the fresh `.venv`, generated
`web/assets/py/`, test/tool caches, egg metadata, and `__pycache__` directories. No manual source
edit, sibling repository, editable external Core checkout, localhost dependency, or global Python
package was required. No server remained listening after the controlled `make serve` stop.

Locked runtime dependency observations:

- `confcurve==0.2.2`
- `wald-inference==0.4.1`
- `numpy==2.2.6`
- `scipy==1.14.1`
- `hypothesis==6.151.9`
- `playwright==1.58.0`
- `pytest==9.0.2`
- `ruff==0.15.1`

Installed distribution provenance:

- `confcurve` is the exact fresh detached checkout installed editable.
- `wald-inference` records the official v0.4.1 release wheel URL, not a path/sibling checkout.
- `pyproject.toml`, `uv.lock`, and staging constants all record the exact wheel URL and SHA-256
  `d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b`.

### Independent B01-B08 difference measurement

The repository comparator passed all 22 cases. A separate recursive float-cell audit measured:

- overall maximum absolute difference:
  `5.329070518200751e-15`;
- overall maximum relative difference:
  `4.449372536648163e-16`;
- largest path:
  `response.meta.threshold_support_summaries[0].likelihood_ratio_threshold_to_null`;
- B05, B06, all B07 edge/error cases except the disabled-design ordinary contract, and all B08
  finite-extreme summaries were exactly equal in every compared float cell;
- all declared identity fields, errors, key order, nulls, strings, integers, and booleans passed
  the repository's exact comparison rules.

Evidence:

- script:
  `/private/tmp/conf-curve-v022-live.uSByJH/golden_diff_audit.py`,
  SHA-256
  `8ab1549dd261aa7001322fbbebf294fc86d06036d1d9eaa70c7b9fb79d387e74`;
- output:
  `/private/tmp/conf-curve-v022-live.uSByJH/golden_diff_audit.json`,
  SHA-256
  `fe617866588d438f2673149bffc19bcf80b518488c66c5442eb2614791738960`.

## Lane D — release and dependency provenance

Release assets and independently measured SHA-256:

| Asset | Bytes | SHA-256 | Check |
|---|---:|---|---|
| `browser-stage-manifest.json` | 4,308 | `b81f7b5781d77ae0ed1f95b513d6f7f3f27ac853ae2b552d2ea5aebb4210e073` | GitHub digest, `SHA256SUMS`, and local digest agree |
| `conf_curve_likelihood-0.2.2.tar.gz` | 466,407 | `2b3c752dd1c6e25fb81bb2c495fdec23c8d724a7db219575e28a5ce78e07f5f1` | GitHub digest, `SHA256SUMS`, and local digest agree |
| `SHA256SUMS` | 195 | `4c64b4ad316fa58842a8a790b229251ea429bfb51ff5efca38ef7b7bb9bb5dd3` | GitHub digest agrees |
| Core wheel `wald_inference-0.4.1-py3-none-any.whl` | 37,939 | `d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b` | Direct release URL HTTP 200; wheel metadata says `wald-inference` 0.4.1, Brian Locke, MIT |

`shasum -a 256 -c SHA256SUMS` returned OK for the two listed application assets.

Source archive checks:

- Decompressed release tar SHA-256:
  `45fd5820c4bfbe91e173ddb1fb426ca62ac4526adbc350b84019c9ef59f88167`.
- The decompressed release tar is byte-identical to
  `git archive --format=tar --prefix='conf_curve_likelihood-0.2.2/' 78d189ac...`.
- It contains 147 regular files, exactly matching 147 recursive tag-tree entries.
- It contains no `.git`, `.venv`, generated `web/assets/py`, `__pycache__`, or test-result entry.
- macOS `gzip -n` produced a different compressed stream, but decompression gave the exact same tar
  bytes. The release workflow independently compared two CI-produced archives before publication;
  cross-implementation compressed-byte equality is not assumed.

Stage manifest checks:

- Strict JSON parse passed.
- Locally regenerated, downloaded-release, and cache-busted live manifests are byte-identical.
- Manifest SHA-256:
  `b81f7b5781d77ae0ed1f95b513d6f7f3f27ac853ae2b552d2ea5aebb4210e073`.
- Source commit:
  `78d189ac03ec223a69778843497d27c70a8720c2`.
- App package:
  `confcurve` 0.2.2, 7 files.
- Core package:
  `wald-inference` 0.4.1, 14 files.
- Pyodide:
  0.29.3.
- Aggregate bundle:
  `b6e487540a5f5fa349ce22aa631916ab8d4d5a6b83145ad3acd2714fad22f592`.
- All 21 files were independently matched to their manifest byte counts and SHA-256 digests; the
  ordered aggregate bundle descriptor recomputed exactly.
- Browser startup requested every staged file with its declared SHA-256 as a query parameter and
  imported neither package until manifest/file/aggregate checks passed.
- The manifest intentionally describes the staged package files rather than duplicating the Core
  wheel URL. Exact Core artifact URL/digest enforcement is in `pyproject.toml`, `uv.lock`, and
  `src/confcurve/staging.py`, and its release wheel was independently downloaded and verified.
- No hand-edited or tracked external Core copy exists; `web/assets/py/` is ignored and regenerated.

Traceability:

- Remote `main`, annotated tag peel, release workflow head, Pages workflow head, release manifest,
  and deployed manifest all identify the same commit.
- GitHub reports seven successful check runs on the commit.
- The release workflow verified the annotated tag/version, format, lint, generated bundle, golden
  baseline, live links, non-browser suite, Chromium suite, WebKit smoke, clean generated state,
  deterministic release bundle, checksums, and release publication.
- The Pages workflow staged from the same lock/commit, checked links/clean state, then built and
  deployed the exact site.

## Lane E — live browser, privacy, accessibility, and links

Hosted URL tested:
`https://reblocke.github.io/conf_curve_likelihood/`.

Cache-busted direct HTTP checks:

- Index HTTP 200, SHA-256
  `4402dc137f5585d994ddcbf95a58619c681ddee0e5041086bed42c41479e2edf`.
- Runtime JS HTTP 200, SHA-256
  `4e371f159ada5282c35b08a0c2cad64cf184676981611d5f7d3003014878633e`.
- Config JS HTTP 200, SHA-256
  `ca83b877b2870e1766a841f5ba64cf2c026bd891d0a904480d0954b9efb1c29d`.
- Live manifest HTTP 200 over verified TLS and exact to local/release manifest.
- Runtime text:
  `confcurve app 0.2.2 · wald-inference core 0.4.1`.

### Chromium workflow

The exact hosted deployment passed:

- initial load and calculation;
- desktop sidebar collapse/restore, with plot width changing from 1,034 to 1,350 CSS pixels and
  Plotly resizing to the surface;
- 390 × 844 mobile breakpoint and compact rendering;
- mobile control collapse/restore;
- keyboard sequence from effect selector to estimate, then lower CI;
- both-panel, compatibility-only, and likelihood-only modes with the expected 2/1/1 traces;
- advanced compatibility-cutoff hide/show;
- additive effect switch with linear axis;
- invalid nonpositive ratio input, bounded authored error without traceback/local path, and
  successful corrected-input recovery;
- six-panel A-F design mode, design table, reviewer text, figure caption, and exact six traces;
- status, text summary, commentary, design table, caption, and reviewer-text alternatives;
- all ten related-tool links and all three methodology-source links exactly matching policy;
- canonical URL unchanged by every numerical input.

At 390 × 844:

- plot surface width was 312 CSS pixels within document width 390;
- document `scrollWidth` and `clientWidth` were both exactly 390;
- compact A/B and A-F panel headings were horizontally inside the plot and viewport;
- no panel-heading pair overlapped;
- no panel heading overlapped an x-axis title;
- the six A-F heading right edges ranged from 275.875 to 296.781, within plot right edge 351;
- Plotly intentionally positions the first title line in its title margin, about 22 CSS pixels
  above the `.plot-surface` content rectangle. It was visible, horizontally bounded, and clear of
  other labels; vertical containment in the surface rectangle is not the repository's authored
  mobile criterion.

Explicit exports after user action:

| Export | Observation |
|---|---|
| CSV | `wald-confidence-curves.csv`; 802 lines including header; exact 16 documented design-enabled columns |
| Dashboard PNG | `wald-confidence-curves.png`; 618,978 bytes; 2800 × 3200 |
| Manuscript PNG | `wald-confidence-curves-manuscript.png`; 579,380 bytes; 2800 × 3000 |
| Caption copy | Success; retained explicit “not exact fitted-model profile likelihood” limitation |
| Reviewer copy | Success and nonempty |

### WebKit smoke

- WebKit 26.0 live load returned HTTP 200 at 390 × 844.
- Runtime reached `Curves updated.`
- Technical versions were exact.
- Compact A/B headings were horizontally contained and non-overlapping.

### Accessibility

- All 41 rendered inputs, selects, authored buttons, and Plotly toolbar buttons had an associated
  label, ARIA name, or nonempty button text.
- `html[lang]` was `en`.
- The status region used `aria-live="polite"` and announced the recoverable invalid input.
- The Plotly surface had a descriptive ARIA label.
- Non-visual summary/commentary/design/caption/reviewer text was nonempty.
- Keyboard-only traversal of the basic numerical workflow passed.

Accessibility evidence:

- script:
  `/private/tmp/conf-curve-v022-live.uSByJH/accessibility_audit.py`,
  SHA-256
  `91d129bd8fb72c1659fec3ee08b5e9acd7d747a69ff67c8d6d2063883dbd2185`;
- output:
  `/private/tmp/conf-curve-v022-live.uSByJH/accessibility_audit.json`,
  SHA-256
  `bb92bf6b203f80135514012644c280a7ee7d40a9eba2e59e3a1bbbe6489f1bbd`.

### Privacy and network

Captured after initial load, the nine-digit threshold sentinel, view/effect changes, invalid-input
recovery, and six-panel design computation:

- 43 requests and 43 responses;
- all requests were GET;
- no request had a body;
- no request failed and no response was 400 or greater;
- only `reblocke.github.io`, `cdn.plot.ly`, and `cdn.jsdelivr.net` were contacted;
- the exact sentinel `1.234567891` was absent from every captured request URL, body, header, and
  console message;
- no WebSocket, popup, page error, or automatic download occurred;
- zero localStorage, sessionStorage, IndexedDB databases, Cache Storage keys, cookies, context
  cookies, and service workers;
- explicit exports occurred only after clicks;
- no telemetry, analytics, backend, tracking pixel, upload, or input-bearing URL was observed.

Static inspection found only documented same-origin manifest/package fetches and version-pinned CDN
runtime dependencies. Pyodide 0.29.3 and Plotly 3.1.0 use HTTPS, `crossorigin="anonymous"`, and
SHA-384 Subresource Integrity values. Fresh downloads recomputed to the exact declared SRI values:

- Pyodide:
  `Hcsv6LxK5rH9vVB+a/+cLJZR3kIIM2Y851r6waxy+9JInvSROiD1bTMk748pYdat`;
- Plotly:
  `DAxS2fhSGacPW3IdpTjDpu+KotwjM8aHsfrkZRnfYyJIhAHoDav7jAJ+NmYcp6PL`.

All ten public portfolio targets passed the repository's live link checker:

1. `https://reblocke.github.io/wald-inference-tools/`
2. `https://reblocke.github.io/compatibility-curve/`
3. `https://reblocke.github.io/wald-likelihood-support/`
4. `https://reblocke.github.io/critical-effect-size/`
5. `https://reblocke.github.io/type-s-m-calibrator/`
6. `https://reblocke.github.io/precision-guardrail-planner/`
7. `https://reblocke.github.io/conf_curve_likelihood/`
8. `https://github.com/reblocke/conf_curve_likelihood`
9. `https://github.com/reblocke/wald-inference-core/releases/tag/v0.4.1`
10. `https://github.com/reblocke/conf_curve_likelihood/blob/main/docs/PRIVACY.md`

The final live interaction/network script is
`/private/tmp/conf-curve-v022-live.uSByJH/live_integrated_audit.py`,
SHA-256
`0fb62a163e8be2798f0af187f44e2412dce37eb7ac053d80d0f66469995d5806`.
Its output is
`/private/tmp/conf-curve-v022-live.uSByJH/live_integrated_audit.json`,
SHA-256
`c53c3b6e88ca0515dea084f7a6001fb50838843d3da54ed208e298b59808f2d9`.

Audit-harness disclosure:

- The first live attempt waited for the complete nine-digit sentinel in a rendered annotation.
  The UI intentionally formats reference labels to three significant digits, so the final harness
  waited for `Reference threshold 1.23` while continuing to search all captured network/console
  data for the complete sentinel.
- The next attempt incorrectly required Plotly panel titles to remain vertically inside
  `.plot-surface`; Plotly intentionally uses the adjacent title margin. The final check follows the
  repository's rendered mobile criterion: numeric horizontal bounding boxes plus overlap tests.
- Both corrections changed only the temporary audit harness. The final expanded run exited 0.
- The in-app Browser runtime exposed no available browser (`agent.browsers.list()` returned `[]`),
  so no in-app screenshot was captured. The exact live deployment was instead exercised with the
  repository-locked Playwright in Chromium and WebKit. This is an audit-tool limitation, not an app
  finding.

## Lane F — documentation, rights, citation, and maintenance

Canonical documentation matrix:

| Required path | State |
|---|---|
| `README.md` | Present |
| `LICENSE` | Present |
| `CITATION.cff` | Present |
| `AGENTS.md` | Present |
| `CHANGELOG.md` | Present |
| `docs/SCIENTIFIC_SCOPE.md` | **Missing — blocker** |
| `docs/VALIDATION.md` | **Missing — blocker** |
| `docs/PRIVACY.md` | Present |
| `docs/DECISIONS.md` / ADR | Present |
| `docs/MAINTENANCE.md` | Present |
| `llms.txt` | Present |

### Passing documentation and rights checks

- README setup and deployed-link commands were executed in the clean checkout.
- README clearly positions the maintained integrated workbench, recommends focused tools for
  single questions, distinguishes observed reconstruction from assumed-truth repeated-study
  design, and states what the app does and does not do.
- Public copy explicitly rejects exact fitted-model profile-likelihood, posterior, clinical
  decision-support, and medical-device interpretations.
- README, package, runtime, manifest, changelog, CFF, and source version agree on app v0.2.2.
- README, package lock, staging code, manifest, changelog, decisions/ADR, and `llms.txt` agree on
  Core v0.4.1 and the exact released wheel digest.
- Maintenance policy explicitly covers supported changes, normally out-of-scope changes,
  semantic versioning/deprecation, Core-upgrade gates, URL compatibility, and human-only archival.
- Feature-request and pull-request templates route changes to focused repositories and require
  compatibility/Core-upgrade checks.
- Current workflows use Node 24-compatible action majors and all current commit checks passed.
- Author/maintainer identity is consistently Brian Locke across active public metadata.
  Historical Reed Blocke/Brian W. Locke/placeholder references are explicitly labeled provenance,
  not active identity.
- MIT `LICENSE` SHA-256:
  `a85556603ffa0e647d623c27670a751da6d5a632cc45101d8063916e415524f8`.
- `CITATION.cff` parses as CFF 1.2 metadata for Brian Locke, MIT, v0.2.2, release date
  2026-07-30, and the canonical repository URL. SHA-256:
  `7af3da981c2e719694e0b2c9dfbabf16d5975b7d84f5f28c3a4438a84586c989`.
- Privacy documentation matches the observed deployed data flow.
- Official publisher pages match the three source links and their title/author/year roles:
  Zampieri et al. (evidential likelihood/support/S-minus-2), Perugini et al. (critical-effect-size
  rationale), and Gelman & Carlin (Type S/M).
- The repository states that no external figure, table, or substantial source text is copied.
  Tracked-file inspection found no publisher PDF or third-party figure/image/font. The sole tracked
  binary is the 10-entry repository-authored historical Type S/M Codex ticket archive.
- CDN assets are version-pinned and SRI-protected; Core and app package files are
  checksum-addressed.

### Blocking documentation findings

#### F-001 — required scientific-scope document absent

`docs/SCIENTIFIC_SCOPE.md` does not exist. README and the linked Core scope describe much of the
science, but the canonical ticket pack requires a repository-local scope document for each
scientific repository. It should state:

- the integrated app's local scientific responsibility versus Core ownership;
- supported effect families/working scales and CI-based Wald assumptions;
- observed versus repeated-study conditioning;
- benchmark versus exact critical-effect behavior;
- undefined/extreme-value conventions;
- limitations/non-goals and non-clinical status;
- the exact Core release authority.

#### F-002 — required current validation document absent

`docs/VALIDATION.md` does not exist. Historical migration records and tests are not a current
release validation record. The file should name the exact app tag/commit, Core tag/commit/artifact
digest, environment, command results/counts, B01-B08 tolerances and measured maximum differences,
manifest/release/Page traceability, browser/privacy/accessibility evidence, and remaining
limitations.

#### F-003 — current integrated release notes omit required release fields

The v0.2.2 release body contains the compact-label change and contract-preservation statement only.
It omits the current Core v0.4.1 identification, focused-tool links, B01-B08 parity report, and
maintenance-policy summary required by CC-MIG-10. The v0.2.0 release body contains those categories
for Core v0.4.0, which is no longer current; v0.2.1 has an annotated tag but no GitHub release.

### Secondary documentation staleness

- `docs/migration/MIGRATION_LOG.md` lines 285-315 still describe the Core v0.4.1 app adoption as a
  pre-tag candidate with a planned v0.2.1 prerelease, pending PR, pending app hashes, and portfolio
  validation blocked until tag/deploy. v0.2.2 is now tagged, released, and deployed.
- `docs/migration/METADATA_AUDIT.md` explicitly calls its table a release-candidate snapshot, but
  its remaining-follow-up list still asks to record the Ticket 10 release and update GitHub
  description/homepage; both external actions already occurred. Its table remains at app v0.2.0.
- The v0.2.2 release tag is unsigned.
- GitHub marks v0.2.2 as a prerelease, as expected before independent portfolio validation.

The historical documents are not independently blockers because they declare snapshot/provenance
scope. They should nevertheless be reconciled or explicitly closed when F-001/F-002 are fixed so a
reader does not need to infer current release state from scattered sources.

## Project-standard evidence contribution

This C/D/E/F lane supports the following repository-domain scores; Lane A scientific formula
review should supply the final domain-A score:

| Domain | Suggested score | Evidence/gap |
|---|---:|---|
| B. Data provenance/rights/security | 3/3 | No research data; explicit no-PHI/privacy boundary; exact dependency checksums; SRI; source/rights review |
| C. Computational reproducibility | 3/3 | Exact-tag cold clone, locked install, full verify, local serve, clean tracked tree |
| D. Verification/testing/independent review | 3/3 | 22 golden cases, 205 unit/integration/property tests, 49 Chromium E2E, WebKit, independent live audit |
| E. Readability/maintainability | 3/3 | Thin adapter/core boundary, maintenance policy, ADRs, focused skills, current workflows |
| F. Documentation/replicator usability | 1/3 | Extensive content exists, but two mandated canonical documents and current release-note fields are absent |
| G. Version control/change management | 3/3 | Annotated exact tag, clean history/tree, successful CI/Pages/release checks, issue/PR routing |
| H. Output traceability/dissemination/preservation | 3/3 | Checksummed source/manifest assets, exact live manifest, release/Pages commit traceability |

The documentary blocker overrides the otherwise high score. Do not average it away.

## Required remediation and rerun

Use a separate focused documentation change; do not rewrite the immutable v0.2.2 tag.

1. Add `docs/SCIENTIFIC_SCOPE.md`.
2. Add `docs/VALIDATION.md` with current exact evidence and an explicit non-clinical validation
   boundary.
3. Link both from README and `llms.txt`.
4. Close the stale corrective-release migration entry with actual app tag/release/manifest/source
   asset hashes, or mark its historical snapshot as superseded by the current validation record.
5. Publish a new annotated app release whose notes include current Core v0.4.1, all focused links,
   B01-B08 parity, maintenance status, and behavior/scientific-impact boundaries.
6. Rerun at least Lane F plus exact-tag cold setup, golden comparison, manifest/release/Page
   traceability, deployed Chromium, and WebKit smoke. A new release commit requires a new exact-tag
   audit, not reuse of this v0.2.2 verdict.

## Nonblocking limitations after remediation

If the blocking documentation findings are fixed and the new tag reruns cleanly, the following
would remain nonblocking under current policy:

1. Annotated tags are not cryptographically signed; policy requires annotated tags, not signed
   tags.
2. GitHub releases are intentionally prereleases until portfolio validation is complete.
3. Compressed release bytes are not necessarily reproducible across gzip implementations, while
   the decompressed tar is exact to the Git tag.
4. No in-app Browser screenshot was available; exact live Chromium/WebKit automation and numeric
   SVG bounding boxes provide the browser evidence.
5. This audit verifies software/statistical contracts, not clinical validity or fitness for
   clinical decision support.

## Exact command families

The audit used:

```text
git clone --filter=blob:none ...
git fetch / git checkout --detach refs/tags/v0.2.2^{}
git cat-file -t/-p; git rev-parse; git for-each-ref; git tag -v; git ls-remote
gh run view; gh release view/download; gh api
uv sync --locked
uv run playwright install chromium webkit
make stage-web
make fmt-check
make lint
make golden-check
make portfolio-links
uv run python scripts/check_portfolio_links.py --live
make test
make verify
make serve
uv run python scripts/generate_golden_baseline.py --check
uv run python scripts/compare_golden_baseline.py
uv run pytest <public API and golden tests>
git diff --check
git status --short
git diff --exit-code
git diff --cached --exit-code
uv tree
shasum -a 256; shasum -a 256 -c SHA256SUMS
git archive; gzip -dc; cmp; tar -tzf
curl --fail --location --proto '=https' --tlsv1.2
openssl dgst -sha384 -binary | openssl base64 -A
uv run python <read-only manifest and numerical-difference verifiers>
uv run python /private/tmp/conf-curve-v022-live.uSByJH/live_integrated_audit.py
uv run python /private/tmp/conf-curve-v022-live.uSByJH/accessibility_audit.py
```

## Final state

- Lanes C, D, and E: pass.
- Lane F: fail.
- Release blockers: F-001, F-002, F-003.
- Production/source changes made by this audit: none.
- GitHub/external mutations made by this audit: none.
- Fresh checkout tracked status after verification: clean.
- Overall v0.2.2 verdict: **Not validated; release-documentation blockers remain.**
