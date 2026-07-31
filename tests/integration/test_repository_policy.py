from __future__ import annotations

import json
import re
import subprocess
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_ROOT = PROJECT_ROOT / ".github" / "workflows"
GH_CLI_VERSION = "2.93.0"
GH_CLI_LINUX_AMD64_SHA256 = "02d1290eba130e0b896f3709ffff22e1c75a51475ddb70476a85abc6b5807af0"
EXPECTED_ACTION_PINS = {
    "actions/checkout": (
        "3d3c42e5aac5ba805825da76410c181273ba90b1",
        "7.0.1",
    ),
    "actions/setup-python": (
        "5fda3b95a4ea91299a34e894583c3862153e4b97",
        "7.0.0",
    ),
    "astral-sh/setup-uv": (
        "c771a70e6277c0a99b617c7a806ffedaca235ff9",
        "9.0.0",
    ),
    "actions/upload-artifact": (
        "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
        "7.0.1",
    ),
    "actions/download-artifact": (
        "3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
        "8.0.1",
    ),
    "actions/configure-pages": (
        "45bfe0192ca1faeb007ade9deae92b16b8254a0d",
        "6.0.0",
    ),
    "actions/upload-pages-artifact": (
        "fc324d3547104276b827a68afc52ff2a11cc49c9",
        "5.0.0",
    ),
    "actions/deploy-pages": (
        "cd2ce8fcbc39b97be8ca5fce6e763baed58fa128",
        "5.0.0",
    ),
}
EXPECTED_RELEASE_ASSETS = {
    "PORTFOLIO_VALIDATION_REPORT-v${version}.md",
    "SHA256SUMS",
    "portfolio-validation-evidence-v${version}.tar.gz",
    "tools-v${version}.json",
    "validation-evidence-index-v${version}.json",
    "validation_status-v${version}.json",
    "wald-inference-tools-site-v${version}.zip",
    "wald-inference-tools-v${version}.tar.gz",
}


def _workflow(name: str) -> str:
    return (WORKFLOW_ROOT / name).read_text(encoding="utf-8")


def test_makefile_exposes_catalog_release_gates() -> None:
    makefile = (PROJECT_ROOT / "Makefile").read_text(encoding="utf-8")

    for target in [
        "fmt:",
        "fmt-check:",
        "lint:",
        "validate:",
        "test:",
        "build-site:",
        "e2e:",
        "e2e-webkit:",
        "verify:",
        "live-check:",
        "serve:",
    ]:
        assert target in makefile


def test_required_check_names_and_live_metadata_policy_stay_exact() -> None:
    ci = _workflow("ci.yml")
    pages = _workflow("pages.yml")
    release = _workflow("release.yml")

    assert "\n  test:\n    name: test\n" in ci
    assert "\n  live-metadata:\n    name: live-metadata\n" in ci
    assert "\n  browsers:\n    name: browsers (${{ matrix.browser }})\n" in ci
    assert "browser: [chromium, webkit]" in ci
    assert "make e2e" in ci
    assert "make e2e-webkit" in ci

    assert "make live-check" in ci
    assert "make live-check" in pages
    assert "make live-check" in release
    assert "GITHUB_TOKEN: ${{ github.token }}" in ci
    assert "GITHUB_TOKEN: ${{ github.token }}" in pages
    assert "GITHUB_TOKEN: ${{ github.token }}" in release


def test_workflows_pin_retained_action_major_families_to_full_shas() -> None:
    use_value_pattern = re.compile(r"^\s*(?:-\s+)?uses:\s+(?P<value>\S+)(?:\s+#.*)?$")
    external_use_pattern = re.compile(
        r"^\s*(?:-\s+)?uses:\s+"
        r"(?P<action>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_./-]+)?)"
        r"@(?P<sha>[0-9a-f]{40})"
        r"\s+#\s+v(?P<version>\d+\.\d+\.\d+)\s*$"
    )
    violations: list[str] = []
    observed_actions: set[str] = set()
    external_uses_count = 0
    workflows = sorted({*WORKFLOW_ROOT.glob("*.yml"), *WORKFLOW_ROOT.glob("*.yaml")})

    for workflow in workflows:
        for line_number, line in enumerate(
            workflow.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            if "uses:" not in line:
                continue
            parsed_use = use_value_pattern.fullmatch(line)
            if parsed_use is None:
                violations.append(f"{workflow.name}:{line_number}:{line.strip()}")
                continue
            if parsed_use.group("value").startswith("./"):
                continue
            external_uses_count += 1
            pinned_use = external_use_pattern.fullmatch(line)
            if pinned_use is None:
                violations.append(f"{workflow.name}:{line_number}:{line.strip()}")
                continue
            action = pinned_use.group("action")
            observed_actions.add(action)
            expected = EXPECTED_ACTION_PINS.get(action)
            if expected != (pinned_use.group("sha"), pinned_use.group("version")):
                violations.append(f"{workflow.name}:{line_number}:{line.strip()}")

    assert external_uses_count > 0
    assert observed_actions == set(EXPECTED_ACTION_PINS)
    assert violations == []


def test_workflow_permissions_credentials_concurrency_and_release_cache_are_fail_closed() -> None:
    ci = _workflow("ci.yml")
    pages = _workflow("pages.yml")
    release = _workflow("release.yml")

    assert "permissions:\n  contents: read" in ci
    assert "group: ci-${{ github.workflow }}-${{ github.ref }}" in ci
    assert "cancel-in-progress: true" in ci

    assert "permissions: {}" in pages
    assert "build:\n    name: build\n    permissions:\n      contents: read" in pages
    assert "deploy:\n    needs: build\n    name: deploy\n    permissions:" in pages
    assert "pages: write # Required to publish the Pages deployment." in pages
    assert "id-token: write # Required for GitHub Pages OIDC deployment." in pages
    pages_build, pages_deploy = pages.split("\n  deploy:", maxsplit=1)
    assert "id-token: write" not in pages_build
    assert "pages: write" not in pages_build
    assert "actions/configure-pages@" not in pages_build
    assert "contents: read" not in pages_deploy
    assert "actions/configure-pages@" in pages_deploy

    assert "permissions: {}" in release
    assert (
        "verify-and-build:\n    name: verify-and-build\n    permissions:\n      contents: read"
        in release
    )
    verify_build, publish = release.split("\n  publish:", maxsplit=1)
    assert "enable-cache: true" not in verify_build
    assert "enable-cache: false" in verify_build
    assert "attestations: read" not in verify_build
    assert release.count("attestations: read") == 1
    assert "attestations: read # Required only to verify immutable release attestations." in publish
    assert release.count("contents: write") == 1
    assert "publish:\n    name: publish\n    needs: verify-and-build\n    permissions:" in release
    assert (
        "contents: write # Required only to create and publish this repository's release."
        in release
    )
    assert "pages: write" not in publish
    assert "id-token: write" not in publish
    assert "cancel-in-progress: false" in release

    workflow_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted({*WORKFLOW_ROOT.glob("*.yml"), *WORKFLOW_ROOT.glob("*.yaml")})
    )
    checkout_count = workflow_text.count("uses: actions/checkout@")
    assert checkout_count > 0
    assert workflow_text.count("persist-credentials: false") == checkout_count


def test_release_binds_annotated_remote_tag_and_protected_main_before_repository_code() -> None:
    release = _workflow("release.yml")

    assert 'git cat-file -t "$GITHUB_REF_NAME"' in release
    assert 'git rev-parse "$GITHUB_REF_NAME^{commit}"' in release
    assert "/git/ref/tags/${GITHUB_REF_NAME}" in release
    assert 'git rev-parse "refs/tags/$GITHUB_REF_NAME"' in release
    assert "--jq '.tag'" in release
    assert ".verification.verified" not in release
    assert ".verification.reason" not in release
    assert "--jq '.object.sha'" in release
    assert "--jq '.object.type'" in release
    assert ')" = "commit"' in release
    assert '"https://github.com/${GITHUB_REPOSITORY}.git"' in release
    assert "+refs/heads/main:refs/remotes/origin/main" in release
    containment = 'git merge-base --is-ancestor "$GITHUB_SHA" refs/remotes/origin/main'
    assert containment in release

    assert release.index("Bind the remote annotated tag to the event commit") < release.index(
        "git fetch"
    )
    assert release.index(containment) < release.index("actions/setup-python@")
    assert release.index(containment) < release.index("scripts/check_release_metadata.py")
    assert release.index(containment) < release.index("uv sync --locked")


def test_release_builds_and_transfers_exact_current_version_notes_and_assets() -> None:
    release = _workflow("release.yml")

    assert 'version="${GITHUB_REF_NAME#v}"' in release
    assert 'scripts/build_release_artifacts.py \\\n            --version "$version"' in release
    assert 'test "$(grep -Ec "^## \\\\[$version\\\\] - " CHANGELOG.md)" -eq 1' in release
    assert 'awk -v version="$version"' in release
    assert "--notes-file dist/release-notes.md" in release
    assert "--notes-file CHANGELOG.md" not in release
    assert 'test "$(find "$assets" -maxdepth 1 -type f | wc -l)" -eq 8' in release
    assert 'test "$(wc -l < "$assets/SHA256SUMS")" -eq 7' in release
    assert "sha256sum --check SHA256SUMS" in release
    for asset in EXPECTED_RELEASE_ASSETS:
        assert f'"{asset}"' in release

    assert "actions/upload-artifact@" in release
    assert "actions/download-artifact@" in release
    assert "dist/expected-assets.txt" in release
    assert "cmp --silent dist/expected-assets.txt" in release


def test_release_requires_a_releasable_verdict_before_build_and_transfer() -> None:
    release = _workflow("release.yml")
    guard = "uv run --no-sync python scripts/validate_validation_status.py --require-releasable"
    verify_build, publish = release.split("\n  publish:", maxsplit=1)

    assert release.count("--require-releasable") == 1
    assert guard in verify_build.replace("\n          ", " ")
    assert "--require-releasable" not in publish
    assert release.index("--require-releasable") < release.index(
        "Build the exact deterministic release and evidence assets"
    )
    assert release.index("--require-releasable") < release.index(
        "Transfer the complete release bundle"
    )


def test_release_rejects_whitespace_only_notes_before_transfer_and_publish() -> None:
    release = _workflow("release.yml")
    verify_build, publish = release.split("\n  publish:", maxsplit=1)

    assert "grep --quiet '[^[:space:]]' \"$bundle/release-notes.md\"" in verify_build
    assert "grep --quiet '[^[:space:]]' dist/release-notes.md" in publish
    assert 'test -s "$bundle/release-notes.md"' not in release
    assert "test -s dist/release-notes.md" not in release
    assert release.count("grep --quiet '[^[:space:]]'") == 2

    def notes_pass_guard(notes: str) -> bool:
        result = subprocess.run(
            ["grep", "--quiet", "[^[:space:]]"],
            input=notes,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0

    for notes in ("", " ", "\t", "\n", " \t\r\n"):
        assert not notes_pass_guard(notes)
    for notes in ("Release note", "\n- Preserve exact release provenance.\n"):
        assert notes_pass_guard(notes)


def test_release_is_new_draft_first_stable_exact_and_immutable() -> None:
    release = _workflow("release.yml")

    assert '"repos/${GITHUB_REPOSITORY}/immutable-releases"' not in release
    assert "RELEASE_SETTINGS_READ_TOKEN" not in release
    assert "A release already exists" in release
    assert "--draft" in release
    assert "--verify-tag" in release
    assert "--prerelease" not in release
    assert "jq --exit-status --join-output '.body'" in release
    assert "cmp --silent dist/release-notes.md" in release
    assert "GH_REPO: ${{ github.repository }}" in release
    assert "gh release download" in release
    assert "diff --recursive --brief dist/assets remote-dist" in release
    assert "--draft=false" in release
    assert "--json isImmutable" in release
    assert "--json isPrerelease" in release
    assert "gh release verify" in release
    assert "gh release verify-asset" in release
    assert (
        release.index("gh release create")
        < release.index("gh release download")
        < release.index("--draft=false")
    )


def test_release_installs_checksummed_github_cli_before_credentialed_commands() -> None:
    release = _workflow("release.yml")

    assert f'GH_CLI_VERSION: "{GH_CLI_VERSION}"' in release
    assert f'GH_CLI_LINUX_AMD64_SHA256: "{GH_CLI_LINUX_AMD64_SHA256}"' in release
    assert release.count("Install checksummed GitHub CLI") == 2
    assert release.count("sha256sum --check --strict -") == 2
    assert release.count("Confirm the checksummed GitHub CLI is selected") == 2
    assert release.index("Install checksummed GitHub CLI") < release.index(
        "Bind the remote annotated tag to the event commit"
    )
    publish = release[release.index("\n  publish:") :]
    assert publish.index("Install checksummed GitHub CLI") < publish.index("gh release create")
    assert publish.index("Confirm the checksummed GitHub CLI is selected") < publish.index(
        "gh release create"
    )


def test_dependabot_covers_locked_python_and_actions_without_auto_merge() -> None:
    dependabot = (PROJECT_ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8")

    assert 'package-ecosystem: "uv"' in dependabot
    assert 'package-ecosystem: "github-actions"' in dependabot
    assert dependabot.count('interval: "weekly"') == 2
    assert dependabot.count("default-days: 7") == 2
    assert "python-dependencies:" in dependabot
    assert "github-actions:" in dependabot
    assert "automerge" not in dependabot.lower()


def test_public_coordination_preserves_private_reporting_and_catalog_scope() -> None:
    security = (PROJECT_ROOT / "SECURITY.md").read_text(encoding="utf-8")
    normalized_security = " ".join(security.lower().split())
    contributing = (PROJECT_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    normalized_contributing = " ".join(contributing.lower().split())
    issue_config = (PROJECT_ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(
        encoding="utf-8"
    )
    engineering_issue = (
        PROJECT_ROOT / ".github" / "ISSUE_TEMPLATE" / "engineering-bug.yml"
    ).read_text(encoding="utf-8")
    accessibility_issue = (
        PROJECT_ROOT / ".github" / "ISSUE_TEMPLATE" / "accessibility-report.yml"
    ).read_text(encoding="utf-8")
    security_contact = (
        PROJECT_ROOT / ".github" / "ISSUE_TEMPLATE" / "security-contact.yml"
    ).read_text(encoding="utf-8")
    pull_request = (PROJECT_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(
        encoding="utf-8"
    )

    assert "/security/advisories/new" in security
    assert "Do not disclose vulnerability details in a public issue" in security
    assert "protected health information" in security.lower()
    assert "synthetic" in security.lower()
    assert "do not establish clinical decision support" in normalized_security
    assert "does not own any wald formula" in normalized_contributing
    assert "`data/tools.json` metadata contract" in contributing
    assert "successful ci, pages, or release automation" in normalized_contributing
    assert "without storing an account-level token in actions" in normalized_contributing
    assert "release_settings_read_token" not in normalized_contributing
    assert "blank_issues_enabled: false" in issue_config
    assert "/security/advisories/new" in issue_config
    assert "protected health information" in engineering_issue.lower()
    assert "catalog-owned behavior" in engineering_issue.lower()
    assert "assistive technology" in accessibility_issue.lower()
    assert "protected health information" in accessibility_issue.lower()
    assert "include no vulnerability details" in security_contact.lower()
    assert "protected health information" in security_contact.lower()
    assert "successful automation" in pull_request.lower()
    assert "make live-check" in pull_request


def test_catalog_version_and_validation_semantics_remain_v020() -> None:
    project = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    manifest = json.loads((PROJECT_ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
    status = json.loads(
        (PROJECT_ROOT / "data" / "validation_status.json").read_text(encoding="utf-8")
    )
    evidence_index = json.loads(
        (PROJECT_ROOT / "validation-evidence" / "index.json").read_text(encoding="utf-8")
    )
    citation = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8")
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert project["version"] == "0.2.0"
    assert manifest["catalog_version"] == "0.2.0"
    assert evidence_index["catalog_version"] == "0.2.0"
    assert status["verdict"] == "Validated for release."
    assert "version: 0.2.0" in citation
    assert changelog.count("## [0.2.0] - ") == 1


def test_runtime_provenance_records_nonruntime_boundary_and_exact_tools() -> None:
    runtime = (PROJECT_ROOT / "docs" / "RUNTIME_DEPENDENCIES.md").read_text(encoding="utf-8")
    normalized = " ".join(runtime.split())

    assert "no third-party browser runtime" in normalized
    assert "checked-in same-origin" in normalized
    assert "GitHub CLI 2.93.0" in runtime
    assert GH_CLI_LINUX_AMD64_SHA256 in runtime
    assert "seven-day eligibility cooldown" in normalized
    assert "zizmor 1.28.0" in runtime
    assert "MIT licensed" in runtime
