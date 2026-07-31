# Final Core v0.4.2 release-set Lane E/F audit

Audit window: 2026-07-31T13:17:49Z through 2026-07-31T13:27:58Z. Mode:
independent, read-only, fresh-context live-browser, privacy, accessibility,
documentation, licensing, and provenance review.

## Verdict

**PASS with bounded nonblocking limitations.** All seven released scientific or
template Pages sites passed Chromium desktop, Chromium at 390 by 844 pixels, and
WebKit initial-load/default-calculation smoke. Catalog predecessor v0.2.0 passed
its calculation-free catalog workflow against its own released portfolio. No
release-blocking public-copy, privacy, accessibility, licensing, authorship, or
provenance finding was identified.

The catalog v0.2.0 result is predecessor evidence only. Catalog v0.2.1's own
Pages bytes and release artifacts are a terminal external reconciliation after
publication and are not evidence inside their own tag.

## Environment and independent evidence root

- macOS 26.5.2 build 25F84, arm64
- Python 3.12.13; uv 0.11.11
- Playwright 1.61.0
- Chromium 149.0.7827.55; WebKit 26.5
- Fresh evidence root: /private/tmp/cc-mig11-laneef-fresh.8Xcrxe
- Independent raw live-browser JSON SHA-256:
  e3f996738bb53aaabe975b82a457ec83b54f00abc1201d1fb68f114d5b01945b
- Preserved browser-driver SHA-256:
  67490befd6a85c2147d93e6057edf0632f25f953a09ade21b77c570cfaff0377

## Exact release and live-site coverage

| Repository | Release / commit | Chromium desktop / 390 px / WebKit | Live manifest SHA-256 |
|---|---|---|---|
| scientific-applet-template | v0.1.2 / 04353d7bb07ee74ae0585107431563db89387f05 | PASS / PASS / PASS | eece3892a028aa512701926039b9ba8c94b8b9ce26047f0a5a22357908840544 |
| compatibility-curve | v0.1.4 / eeaff9a374bc022c2d5ca16fdb3c59fbdfcd90f4 | PASS / PASS / PASS | 5dcf381340688e73bd23cb577aaabe19ff4294f05b49c3db7d8420904a66daae |
| wald-likelihood-support | v0.1.3 / beb18d87939f3ba9738b97e1c2e10724e31c5945 | PASS / PASS / PASS | c4dd0ba582177cfb352af9825dd7c6cb0f3b6881674e1912b2634e8aff2b7952 |
| critical-effect-size | v0.1.4 / 1c451fe9ed7d7d21fe732ec5da178248053fe912 | PASS / PASS / PASS | 4a57f9659d1d039ee5a366bbe73583cb9bad6bcf7f3b908b1cd0f70d1894c2b0 |
| type-s-m-calibrator | v0.1.4 / bb4372c55a2e839b9f57d8424f797c944f5b4eb0 | PASS / PASS / PASS | d978e3ca1f4a8626899dbf5e980e633c5e02cb31caa924adffa8bc1be51973d2 |
| precision-guardrail-planner | v0.1.3 / a88926b966766a94b00a61799539351cce44581a | PASS / PASS / PASS | 19cc748d4778e80c55fa7232ea4d0737c4d628f777fcb8039e8feef1b99576c7 |
| conf_curve_likelihood | v0.2.6 / 60ca0e3f5d6f05bb943cb4b7b7d02ed5a1d5714a | PASS / PASS / PASS | 6093fcd4e2de7fdf3ad9ffc28d92d406e8c0ea745019c3d7cc01246bf3e54e25 |
| catalog predecessor wald-inference-tools | v0.2.0 / ae76d86f731239e7fe2e902d6813093b35e4e69b | PASS / PASS / PASS | 39f2ea1a91caa4e9a8649cd5f6e7be18020910121610b7ef847d62fd196e5653 |

The seven app/template manifests matched the supplied source commit, app
version, and Core 0.4.2 where applicable. The catalog predecessor rendered six
cards and six comparison rows and all 18 rendered portfolio/resource links
returned HTTP 200.

## Browser, export, privacy, and accessibility findings

- Desktop default and edited-input workflows completed without console or page
  errors. Every advertised CSV/PNG export and caption/reviewer copy produced
  nonempty output with the expected scope and PNG signature.
- The 390-pixel runs had exact viewport containment, no uncontained visible
  elements, keyboard-reachable calculation workflows, readable result
  alternatives, and no unlabeled enabled controls or visible images missing alt.
- Invalid input produced bounded, non-traceback error text exposed through an
  alert or polite live status, and valid input recovered successfully. Required
  empty-field paths in the focused/template apps exposed focusable error links
  and aria-invalid=true.
- All observed network requests were GET. Static runtime requests were
  same-origin assets plus pinned Pyodide 0.29.3, SciPy/NumPy where applicable,
  and Plotly 3.1.0. The only post-input observations were two local blob-image
  GETs per calculation site; sentinel values did not appear in any request or
  WebSocket.
- Cookies, local/session storage, IndexedDB, Cache Storage, service workers, and
  service-worker controllers were empty. No telemetry match or WebSocket was
  observed.

## Documentation, rights, and public-copy findings

Core v0.4.2 and the template plus six apps had complete required documentation.
CFF, package, changelog, and release versions agreed. MIT licensing and Brian
Locke authorship agreed. Historical identity appeared only in explicit
provenance records.

Public copy consistently describes educational/research-facing one-parameter
Wald tools, not clinical or regulatory systems. It distinguishes user-supplied
thresholds and assumed true values from clinical or causal truth and exposes
limitations. Exact release snapshots contained no tracked PNG, JPG, GIF, SVG,
PDF, or font assets. Paper, runtime, template, and Core provenance and license
boundaries were explicit; no publisher figure, table, dataset, or substantial
text was represented as copied.

## Exact command families

    CC_MIG_11_BROWSER_ARTIFACT_DIR=/private/tmp/cc-mig11-laneef-fresh.8Xcrxe/artifacts \
      .venv/bin/python validation-evidence/drivers/live_browser_audit.py
    curl --fail --silent --show-error --location https://reblocke.github.io/<slug>/assets/py/manifest.json
    git -C <repository> archive <exact-release-commit>
    .venv/bin/python -m pytest -q -p no:cacheprovider <browser-and-repository-policy-tests>
    git check-ignore web/assets/py/manifest.json
    find <release-snapshot> -type f <media-extension-filter>

The temporary archive-policy runs had one expected .git-absence failure per
app. All substantive tests passed, and ignored/generated-stage policy was rerun
against the exact-head Git checkouts.

## Nonblocking limitations

- WebKit coverage is the ticket-required initial-load/default-calculation smoke,
  not exhaustive export, error, and mobile parity.
- Sentinel testing exercised one distinctive numeric field per app. Source
  scans and repository privacy tests supplement it but cannot prove behavior of
  hypothetical future fields.
- Automated keyboard/semantic checks do not replace manual screen-reader,
  contrast, or zoom/reflow testing beyond 390 pixels. Nonempty semantic errors
  recover correctly but generally reserve focus links and aria-invalid for
  required-empty paths.
- Focused/template Plotly is version-pinned but lacks SRI; integrated uses SRI.
- No licensed publisher full-text corpus was available for a corpus-wide
  plagiarism comparison. The rights conclusion rests on exhaustive tracked
  asset inventory, public-copy/provenance review, and explicit source/license
  records.
