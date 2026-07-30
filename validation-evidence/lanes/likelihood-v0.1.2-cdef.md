# CC-MIG-11 lane C/D/E/F evidence: wald-likelihood-support v0.1.2

## Decision

**PASS — no release blocker found for `reblocke/wald-likelihood-support` v0.1.2.**

This was a read-only audit of GitHub, the release, and the deployed site. Local verification used a
fresh temporary parent and detached tag checkout. No existing worktree or GitHub state was
mutated.

Audit window: 2026-07-30T15:06:43Z through 2026-07-30T15:26:41Z.

## Audited identity

- Repository: `https://github.com/reblocke/wald-likelihood-support`
- Release: `v0.1.2`
- Annotated tag object: `5285b792379cb538bfa93859ecc9d18f07ec2dbb`
- Peeled commit: `7f5557d2a93235e25215261ef5890868b3fb07bb`
- Expected commit: `7f5557d2a93235e25215261ef5890868b3fb07bb`
- Remote `main`: `7f5557d2a93235e25215261ef5890868b3fb07bb`
- Tagger: Brian Locke, 2026-07-30T15:05:15Z
- Tag message: `Wald Likelihood Support v0.1.2`
- Tag type: annotated Git object (`git cat-file -t` returned `tag`)
- Tag signature: unsigned (`git tag -v v0.1.2` exit 1, `no signature found`)
- GitHub release: published 2026-07-30T15:08:44Z, draft false, prerelease true
- Release workflow:
  `https://github.com/reblocke/wald-likelihood-support/actions/runs/30554945801`;
  head SHA exact; completed success at 2026-07-30T15:08:48Z
- Pages workflow:
  `https://github.com/reblocke/wald-likelihood-support/actions/runs/30554568057`;
  head SHA exact; build and deploy completed success at 2026-07-30T15:01:29Z

## Environment

- Host: macOS 26.5.2, arm64
- Git: 2.50.1 (Apple Git-155)
- GitHub CLI: 2.92.0
- uv: 0.11.11
- Host Python: 3.14.4
- Locked project Python: 3.12.13
- Playwright: 1.61.0
- Live Chromium: 149.0.7827.55
- Live WebKit: 26.5
- Node/npm (recorded for environment only): 25.9.0 / 11.12.1
- Fresh parent:
  `/private/tmp/wald-likelihood-v012-audit.yMl4Uf`
- Release assets:
  `/private/tmp/wald-likelihood-v012-assets.henUE5`

## Lane C — cold-start reproducibility

Fresh-clone command results:

| Command | Exit | Result |
|---|---:|---|
| `git clone --filter=blob:none https://github.com/reblocke/wald-likelihood-support.git <fresh>/wald-likelihood-support` | 0 | New clone |
| `git fetch origin refs/tags/v0.1.2:refs/tags/v0.1.2` | 0 | Tag fetched |
| `git checkout --detach refs/tags/v0.1.2^{}` | 0 | Exact detached commit |
| `uv sync --locked` | 0 | 25 packages checked; no sibling checkout |
| `uv run playwright install chromium webkit` | 0 | Browser binaries available |
| `make stage-web` | 0 | Exact source commit and package hashes below |
| `make fmt-check` | 0 | 30 files already formatted |
| `make lint` | 0 | All checks passed |
| `make test` | 0 | 73 non-E2E tests passed |
| `make e2e` | 0 | 11 Chromium E2E tests passed |
| `make e2e-webkit-smoke` | 0 | 1 WebKit smoke test passed |
| `make verify` | 0 | Formatting, lint, 73 non-E2E, 11 Chromium, and 1 WebKit all passed |
| `make serve` | controlled stop | Server started on `127.0.0.1:8000`; index HTTP 200; manifest identity predicate true; Ctrl-C then exited 1 as expected |
| `git diff --check` | 0 | No whitespace errors |
| `uv tree` | 0 | Dependency tree resolved |
| `git status --porcelain=v1 --untracked-files=all` | 0 | Empty output |
| `git diff --exit-code` / `git diff --cached --exit-code` | 0 / 0 | No tracked changes |

Locked runtime dependency observations:

- `wald-likelihood-support==0.1.2`
- `wald-inference==0.4.1`
- `numpy==2.2.6`
- `scipy==1.14.1`
- `ruff==0.16.0`
- `pytest==8.4.2`
- `pytest-playwright==0.8.0`
- `playwright==1.61.0`
- `hypothesis==6.163.0`

Tracked status was clean after verification. Ignored verification products were limited to the
local `.venv`, generated `web/assets/`, test/tool caches, egg metadata, and `__pycache__`
directories.

No manual source edit, sibling repository, editable external Core, localhost dependency, or
global Python package was required. `make serve` was tested literally, then deliberately stopped.

Audit-harness disclosure: the first `uv sync --locked` invocation completed successfully, but its
shell wrapper then assigned to zsh's reserved `status` variable and reported wrapper exit 1. The
same command was immediately rerun with a corrected wrapper and exited 0. This was not a product
or dependency failure.

## Lane D — release and dependency provenance

Release assets and independently measured SHA-256:

| Asset | Bytes | SHA-256 | Check |
|---|---:|---|---|
| `browser-stage-manifest-v0.1.2.json` | 4,576 | `21be10dd5197300594401f69605288b95d95a533d448c0284cea2870bfd023b0` | GitHub digest, `SHA256SUMS`, and local digest agree |
| `wald-likelihood-support-v0.1.2.tar.gz` | 100,839 | `f0a457dfc153a39f1b3183af142a443361e1e965bcd1d76c7f825371ee294bac` | GitHub digest, `SHA256SUMS`, and local digest agree |
| `SHA256SUMS` | 205 | `4d6d4e8732dddfefbf71ac6f441c630df600da6dee314685e2adabfc4226ce81` | GitHub digest agrees |
| Core wheel `wald_inference-0.4.1-py3-none-any.whl` | 37,939 | `d7272023f65088729d3ff997cab7cac57b84f22ac6108244ec2170434557d99b` | Direct release URL downloaded HTTP 200; metadata says name `wald-inference`, version 0.4.1, MIT, Brian Locke |

`shasum -a 256 -c SHA256SUMS` returned OK for both listed app assets.

Source archive checks:

- The decompressed release tar SHA-256 is
  `27096c84b0bfff14553f6a713dbeb52f169c1ae0796a6e7d2dd90c2d7be61704`.
- It is byte-identical to
  `git archive --format=tar --prefix='wald-likelihood-support-v0.1.2/' 7f5557d...`.
- It contains 56 regular files, exactly matching 56 recursive tag-tree entries.
- It contains no `.git`, `.venv`, generated `web/assets/py`, `__pycache__`, or test-result entry.
- A macOS `gzip -n` recompression produced a different compressed stream but the same exact tar
  bytes. Therefore the published compressed checksum is authoritative; cross-implementation gzip
  byte reproduction is not assumed.

Stage manifest checks:

- Strict JSON parse passed with no nonstandard constants.
- Release manifest is byte-identical to the independently regenerated local manifest.
- Source commit:
  `7f5557d2a93235e25215261ef5890868b3fb07bb`.
- App version/package:
  `0.1.2`,
  `0a7bcf5549c12e0f75b7c698c3b40571f199c3e3d6a9e0b88857be09aeebb1b3`.
- Core version/package:
  `0.4.1`,
  `44c52ba0189155e0d976e283d383f17f3db0679563ec6dc6d45b9829c4a43b4d`.
- Core artifact URL is the official v0.4.1 wheel URL and records exact wheel SHA above.
- Aggregate bundle:
  `b9c5247cba1dc13a004959e8354f1c96c00381aca5e31cda84a121b260316db0`.
- All 19 staged files were independently size- and SHA-256-verified; both package descriptors and
  aggregate bundle descriptor recomputed exactly.
- App/Core/Pyodide versions agree across `pyproject.toml`, `uv.lock`, `browser-stage.toml`,
  source version, JS config, HTML footer, README, CFF, runtime docs, and the manifest.
- No hand-edited or tracked external Core copy exists; `web/assets/py/` is ignored and regenerated.

Traceability:

- Remote main, annotated tag peel, release workflow head, Pages workflow head, release manifest,
  and live manifest all identify the same commit.
- GitHub reported six successful check runs on the commit: test, Chromium E2E, WebKit smoke, Pages
  build, Pages deploy, and verify-and-release.

## Lane E — live browser, privacy, accessibility, and links

Hosted URL tested:
`https://reblocke.github.io/wald-likelihood-support/`.

Cache-busted direct HTTP checks:

- Index HTTP 200.
- JS config HTTP 200.
- Manifest HTTP 200 over verified TLS.
- Live manifest SHA-256:
  `21be10dd5197300594401f69605288b95d95a533d448c0284cea2870bfd023b0`.
- Live manifest is byte-identical to release and local regenerated manifests.
- Live runtime text:
  `wald-likelihood-support 0.1.2 · wald-inference 0.4.1`.
- Live source commit and Core wheel SHA are exact.

Mobile Plotly title audit used Chromium 149 at 390 × 844, device scale factor 1. Plot bounds were
`x=33..357`; viewport bounds were `x=0..390`. Every rendered title was inside both. Coordinates:

| Effect | Normalized title `[left,right]` | Log title `[left,right]` |
|---|---:|---:|
| Odds ratio | `[72.094,317.906]` | `[72.500,317.500]` |
| Risk ratio | `[77.133,312.867]` | `[72.500,317.500]` |
| Hazard ratio | `[62.773,327.227]` | `[72.500,317.500]` |
| Incidence rate ratio | `[75.148,314.852]` | `[72.500,317.500]` |
| Ratio of means | `[82.242,307.758]` | `[72.500,317.500]` |
| Mean difference | `[82.242,307.758]` | `[72.500,317.500]` |
| Risk difference | `[82.242,307.758]` | `[72.500,317.500]` |
| Rate difference | `[82.242,307.758]` | `[72.500,317.500]` |
| Regression coefficient | `[70.172,319.828]` | `[66.805,323.195]` |

The document was exactly 390 CSS pixels wide (`scrollWidth=390`, `clientWidth=390`). No title
relied on document-width containment alone.

Additional live checks:

- Initial Chromium load and calculation passed.
- Live WebKit 26.5 load and calculation passed at 390 × 844.
- Keyboard sequence from effect selector reached estimate, then lower CI.
- All nine core controls had exactly one label.
- Polite status and alert error regions were present.
- Invalid positive-ratio input produced a bounded error without traceback/path and recovered.
- Text result and plot-description alternatives were nonempty.
- Explicit CSV export had the exact five-column header and 802 lines including header.
- Explicit caption copy completed and retained the required approximation/original-likelihood
  limitations.
- Related-tool links in the DOM exactly matched repository policy.

Live privacy/network observations after calculation across all nine effects and both views:

- 40 requests / 40 responses; all GET; no request body; no failed response.
- Only static hosts were contacted:
  `reblocke.github.io`, `cdn.plot.ly`, and `cdn.jsdelivr.net`.
- Synthetic sentinel `1.234567891` was absent from every request URL/body/header and console text.
- Page URL remained exactly the canonical hosted URL.
- Zero localStorage, sessionStorage, IndexedDB databases, Cache Storage keys, cookies, service
  workers, WebSockets, page errors, popups, or automatic downloads.
- CSV and clipboard output occurred only after explicit clicks.
- No telemetry, analytics, backend, upload, or input-bearing URL was observed.

All six related links returned HTTP 200:

1. `https://reblocke.github.io/wald-inference-tools/`
2. `https://reblocke.github.io/compatibility-curve/`
3. `https://reblocke.github.io/conf_curve_likelihood/`
4. `https://github.com/reblocke/wald-likelihood-support`
5. `https://github.com/reblocke/wald-inference-core/releases/tag/v0.4.1`
6. `https://github.com/reblocke/wald-likelihood-support/blob/main/docs/PRIVACY.md`

The final live audit script is
`/private/tmp/wald-likelihood-v012-live.MBSLQt/live_mobile_audit.py`,
SHA-256
`133880e1b4644fb8c4b8298b06898bb28e654aa1d591c2ad1d4ebdd036b0b7c1`.

Audit-harness disclosure: the first custom live run timed out because the script attempted to
select the hidden view control without opening the authored “Advanced display controls” details.
After opening that control, the same live audit passed. The expanded final run above exited 0.
This was a harness interaction error, not a rendering or application failure.

The in-app Browser runtime exposed no available browser (`agent.browsers.list()` returned `[]`),
so no in-app screenshot was captured. The exact hosted deployment was instead exercised directly
with the repository-locked Playwright version in both Chromium and WebKit; this is an audit-tool
limitation, not an app finding.

## Lane F — documentation, rights, citation, and maintenance

Required files were present and nonempty:

- `README.md`
- `docs/SCIENTIFIC_SCOPE.md`
- `docs/VALIDATION.md`
- `docs/PRIVACY.md`
- `docs/DECISIONS.md`
- `docs/MAINTENANCE.md`
- `CHANGELOG.md`
- `LICENSE`
- `CITATION.cff`
- `AGENTS.md`
- `llms.txt`

Findings:

- README commands were executed literally in the clean checkout.
- Hosted and repository URLs, version 0.1.2, Core 0.4.1, the Core wheel URL/checksum, experimental
  status, and limitations are mutually consistent.
- Author/maintainer/license identity is consistently Brian Locke; no Reed/Blocke identity remains.
- MIT license is present; `LICENSE` SHA-256 is
  `a85556603ffa0e647d623c27670a751da6d5a632cc45101d8063916e415524f8`.
- CFF 1.2 metadata identifies Brian Locke, MIT, version 0.1.2, and release date 2026-07-30;
  `CITATION.cff` SHA-256 is
  `7ea3a61b54d501838948f5888cd2ac3c74e2a9b96b4ec8ab19e168e4421ffa08`.
- Scientific scope consistently says normalized approximate Wald reconstruction, not original
  exact likelihood, posterior probability, clinical tool, or clinical validation.
- Privacy documentation matches observed client-side data flow.
- Maintenance and decision records identify release/dependency gates and preserve the historical
  v0.2.1 Core adoption as history while current metadata points to v0.4.1.
- Template provenance, frozen-baseline provenance, dependency provenance, and licenses are
  explicit.
- The primary publisher page confirms the cited 2025 AJRCCM article title, author list, DOI,
  volume/pages, open-access status, and CC BY-NC-ND 4.0 terms:
  `https://academic.oup.com/ajrccm/article/211/9/1610/8300617`.
- The repository states that the article is cited for terminology and no figure, table, code, or
  substantial text was copied. Independent tracked-file inspection found only source/text/JSON
  files and no tracked figure, archive, wheel, PDF, or other binary third-party candidate.
- Production policy tests passed for no persistence/telemetry/input URL, safe external source
  link attributes, exact related-link block, scope separation, root-public Core delegation, MIT
  identity, and exact release-only Core dependency.

## Nonblocking limitations

1. The annotated Git tag is not cryptographically signed. Repository policy requires an annotated
   tag, not a signed tag.
2. Pyodide and Plotly CDN URLs are HTTPS and version-pinned, but CDN responses are not
   content-hashed by the generated stage manifest. This is explicitly documented.
3. The release's gzip stream is checksummed and its decompressed tar exactly reproduces the Git
   tag, but compressed bytes are not reproducible across different gzip implementations.
4. The GitHub release remained an expected experimental prerelease as of this audit; promotion is
   a separate portfolio decision.
5. No in-app Browser screenshot was available; exact live Chromium/WebKit automation and numeric
   SVG bounding boxes supply the visual evidence.

None is a blocker under the repository's documented release gates.

## Exact command families

The audit used:

```text
git clone --filter=blob:none ...
git fetch origin refs/tags/v0.1.2:refs/tags/v0.1.2
git checkout --detach refs/tags/v0.1.2^{}
git cat-file -t/-p; git rev-parse; git tag -v; git ls-remote
gh run view/list; gh release view/download; gh api
uv sync --locked
uv run playwright install chromium webkit
make stage-web
make fmt-check
make lint
make test
make e2e
make e2e-webkit-smoke
make verify
make serve
git diff --check
uv tree
git status --porcelain=v1 --untracked-files=all
shasum -a 256; shasum -a 256 -c SHA256SUMS
git archive ... | gzip -n
gzip -dc; cmp; tar -tzf
curl -fsSL / curl -L
uv run python <read-only manifest verifier>
uv run python /private/tmp/wald-likelihood-v012-live.MBSLQt/live_mobile_audit.py
```

No skipped product check or unresolved release finding remains for this repository/version.
