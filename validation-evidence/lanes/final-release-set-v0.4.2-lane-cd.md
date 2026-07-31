# Final Core v0.4.2 release-set Lane C/D audit

Audit window: after 2026-07-31T13:02:45Z through 2026-07-31T13:41:49Z.
Mode: independent, read-only, fresh-context cold-start, artifact, and release
provenance review.

## Verdict

**PASS with bounded nonblocking limitations for all eight published targets.**
Every published artifact passed independent tag, release, checksum, cold-start,
staging, and provenance checks. Catalog v0.2.1 was intentionally still
unpublished at this lane snapshot; its source carrier is tested before merge and
its own tag, release, Pages, and asset identity are terminal external gates.

No production repository, Git ref, GitHub setting, or release was modified.

## Environment

- macOS 26.5.2 build 25F84, Darwin 25.5.0, arm64
- uv 0.11.11; Git 2.50.1; GitHub CLI 2.92.0
- Core/integrated: Python 3.11.10
- Template/focused apps: Python 3.12.13
- Focused/template browser tooling: Playwright 1.61.0, Chromium
  149.0.7827.55, WebKit 26.5
- Integrated browser tooling: Playwright 1.58.0, Chromium 145.0.7632.6
- Fresh-clone root: /private/tmp/ticket11-cd.aDilVj

## Exact release identities and cold-start results

Every tag was an annotated tag object that peeled to the listed commit. Each
commit equaled remote main. Every GitHub release was non-draft, non-prerelease,
stable, and immutable.

| Repository | Release | Tag object | Peeled/main commit | Cold-start result |
|---|---|---|---|---|
| wald-inference-core | v0.4.2 | 26ea4a721b2dfa07f75c2f388a42d6272c88477c | 8afd0a463cc1d2586b8ce5cf92f40900647c3190 | 396 tests; parity pass |
| scientific-applet-template | v0.1.2 | accc5cf8855f4c03140348f17c87fe960996feb8 | 04353d7bb07ee74ae0585107431563db89387f05 | 38 non-E2E; 5 Chromium; 1 WebKit |
| compatibility-curve | v0.1.4 | 50ed9acd5391984e1b9164773ff7d6902fdb6a7c | eeaff9a374bc022c2d5ca16fdb3c59fbdfcd90f4 | 64 non-E2E; 7 Chromium; 1 WebKit |
| wald-likelihood-support | v0.1.3 | 917ab253d92fc8754a4c7701fac17247fd0b734e | beb18d87939f3ba9738b97e1c2e10724e31c5945 | 80 non-E2E; 11 Chromium; 1 WebKit |
| critical-effect-size | v0.1.4 | f1b40c7b48dd6f55735fd2abaaa6763bf475a85b | 1c451fe9ed7d7d21fe732ec5da178248053fe912 | 67 non-E2E; 12 Chromium; 1 WebKit |
| type-s-m-calibrator | v0.1.4 | b92bb2e510bf2ab6ea77e75d458719aa6958039c | bb4372c55a2e839b9f57d8424f797c944f5b4eb0 | 84 non-E2E; 21 Chromium; 1 WebKit; 8 focused rerun |
| precision-guardrail-planner | v0.1.3 | 795c1d4dd19193d3a8e61062a94a4da4468316f5 | a88926b966766a94b00a61799539351cce44581a | 60 non-E2E; 6 Chromium; 1 WebKit; 5 focused rerun |
| conf_curve_likelihood | v0.2.6 | 1694d1727d7e071689ad7fa301f34ac32e547b34 | 60ca0e3f5d6f05bb943cb4b7b7d02ed5a1d5714a | 219 non-E2E; 50 Chromium; 22 goldens; 20 links |

Core parity compared 23,095 values across 14 successful numeric cases, six
matched errors, and two explicit app-owned exclusions. Maximum absolute and
relative differences were 5.329070518200751e-15 and
4.449372536648163e-16.

## Exact released asset hashes

Each downloaded SHA256SUMS validated the complete and exact hosted asset set.

| Repository | Manifest or parity SHA-256 | Archive/wheel SHA-256 | Other archive SHA-256 | SHA256SUMS SHA-256 |
|---|---|---|---|---|
| Core | 18d020e6a00746646ffed913eb88f1e4b148aa2725872db647823019f1e65dba | wheel 225331d7b9d7b70e2508eecb92851a92a8c4e245baf412a1eb0f464d85da1349 | sdist 86808922f5ab9164523380e0838b324e24bed6a7228deb37ce2ca4cc19f06fe3 | 00c56879f2a5b9ee0bdd60ace46a5c9bbec9b6f5c424681b3a84e5a38ec8f785 |
| Template | eece3892a028aa512701926039b9ba8c94b8b9ce26047f0a5a22357908840544 | 746da90a83d904e2bf8023d9e4e2337e4182365dc0a909873b77b1f454638271 | — | 006754850025a2fce8eda9932f93486639a7f8073beeb138ec4350874e9e5e19 |
| Compatibility | 5dcf381340688e73bd23cb577aaabe19ff4294f05b49c3db7d8420904a66daae | 78b2f521a9b57c3789fca275128adeffd516c68357c7737585580b819284a0f3 | — | ff58a0be57d4fad726d55f69deaadeeff5cbd1f613bac2a4e3a790d4376bcf5a |
| Likelihood | c4dd0ba582177cfb352af9825dd7c6cb0f3b6881674e1912b2634e8aff2b7952 | f7f9afea124a20b8a7339b5073937941a97b68f6a2668841ae5d81c92636b2d7 | — | e227b52f5bc460733f1b8a29aab682c74bfe911b121a788ab3c495ff1463c49c |
| Critical effect | 4a57f9659d1d039ee5a366bbe73583cb9bad6bcf7f3b908b1cd0f70d1894c2b0 | feb5e375a65fab8d1e13284b620b155f2bf6c6df13a77f5ea0eaf48ebb4156f9 | — | 8d7b25b9843949583df4fd5bc4cdb53d42d3067c0db9a25c59e689696c0cc059 |
| Type S/M | d978e3ca1f4a8626899dbf5e980e633c5e02cb31caa924adffa8bc1be51973d2 | b081a4168522a9574dd2745b9f87e9e7028f579126332463a936379124bb88f9 | — | e9a83c6db76f1e1d26523e9ebfd07b6aa98fb939e899d1491f192c03b704c85c |
| Precision | 19cc748d4778e80c55fa7232ea4d0737c4d628f777fcb8039e8feef1b99576c7 | d375680d503298e91232831d6b0e22f0321485f6326ea71689746a1b0a5382ce | — | 560a4581db85a38e0928e0570a2e013b894f60c0747738eeb572feaac3f089fa |
| Integrated | 6093fcd4e2de7fdf3ad9ffc28d92d406e8c0ea745019c3d7cc01246bf3e54e25 | 8e1a05dd709b1801564331e1428e1008c2c877a2772fae5675b587305ddcbfb0 | — | 0bbc9d7a4557ea6ca636e90270b4449197871d6f5154f883ce7625a7dca73d76 |

Every regenerated manifest was byte-identical to its release asset and the live
Pages manifest. Each live manifest identified the exact release commit and
package versions. Focused manifests bound Core 0.4.2 to its official URL and
wheel hash. Integrated bound Core 0.4.2 through staged file hashes and retained
the official artifact identity in source, lock, and ADR records.

## Determinism and provenance

- Core's release builder reproduced the hosted wheel and sdist byte-for-byte.
  The downloaded wheel passed distribution inspection and a cold installed-API
  smoke test.
- GitHub SLSA attestations verified both Core artifacts against the release
  workflow, tag v0.4.2, commit 8afd0a463cc1d2586b8ce5cf92f40900647c3190,
  and run 30629025349.
- All app archives regenerated to decompressed tar streams byte-identical to
  the hosted archives.
- All repositories ended clean, git diff --check passed, and no generated
  web/assets/py file was tracked.
- All eight use the same MIT license bytes, SHA-256
  a85556603ffa0e647d623c27670a751da6d5a632cc45101d8063916e415524f8.
  Project and CFF versions matched, and runtime provenance separated
  repository code from third-party dependencies.

## Command families

    git clone --branch TAG --single-branch https://github.com/reblocke/REPOSITORY.git
    env UV_CACHE_DIR=EMPTY_PER_REPOSITORY_CACHE uv sync --locked
    uv run playwright install chromium webkit
    make verify
    git status --short
    git diff --check
    gh release download TAG --repo reblocke/REPOSITORY
    shasum -a 256 -c SHA256SUMS
    gh release verify TAG --repo reblocke/REPOSITORY

Core additionally used its release builder, distribution inspector, installed
package smoke driver, and GitHub attestation verification. Live manifests were
fetched independently and compared by bytes and staged-file hashes.

## Nonblocking limitations

- App archive decompressed tar streams were byte-identical, but macOS and
  Ubuntu emitted different gzip DEFLATE bytes. gzip -n removes timestamps but
  does not normalize cross-implementation compression output. Hosted checksums
  remain valid; no archive-content difference was observed.
- The locally regenerated Core parity JSON had a different checksum from the
  hosted JSON only because platform-level floating maxima differed inside the
  declared tolerance. The underlying 23,095 comparisons passed.
- Integrated make verify has no WebKit target; 50 Chromium tests passed and
  both engines were installed. The independent E/F lane supplies the required
  integrated WebKit smoke.
- A separate long-running make serve process was not held open; passing browser
  suites exercised locally served built artifacts.
