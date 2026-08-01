from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

if __package__:
    from scripts.validate_portfolio_report import (
        REPOSITORY_ORDER,
        validate_portfolio_report,
    )
    from scripts.validate_tools_manifest import PROJECT_ROOT, load_manifest
else:
    from validate_portfolio_report import (  # type: ignore[import-not-found]
        REPOSITORY_ORDER,
        validate_portfolio_report,
    )
    from validate_tools_manifest import (  # type: ignore[import-not-found]
        PROJECT_ROOT,
        load_manifest,
    )

STATUS_PATH = PROJECT_ROOT / "data" / "validation_status.json"
REPORT_PATH = PROJECT_ROOT / "docs" / "PORTFOLIO_VALIDATION_REPORT.md"
RELEASE_INVENTORY_PATH = (
    PROJECT_ROOT / "validation-evidence" / "inventory" / "release-inventory.json"
)

EXPECTED_REPOSITORIES = set(REPOSITORY_ORDER)
NON_MANIFEST_RELEASES = {
    "reblocke/scientific-applet-template": "v0.1.3",
    "reblocke/wald-inference-tools": "v0.2.1",
}
TOP_LEVEL_FIELDS = {
    "schema_version",
    "validated_at",
    "verdict",
    "core_version",
    "repositories",
    "report_sha256",
}
REPOSITORY_FIELDS = {
    "name",
    "commit",
    "release",
    "status",
    "blocking_findings",
}
VERDICT_TO_STATUS = {
    "Validated for release.": "validated",
    "Validated with nonblocking limitations.": "conditionally-validated",
    "Not validated; release blockers remain.": "validation-failed",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ASSET_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
TAG_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
REPORT_INVENTORY_START = "<!-- validation-inventory:start -->"
REPORT_INVENTORY_END = "<!-- validation-inventory:end -->"
REPOSITORY_STATUSES = {
    "validated",
    "conditionally-validated",
    "validation-failed",
}
RELEASE_INVENTORY_FIELDS = {
    "schema_version",
    "audited_at",
    "catalog_evidence_carrier",
    "repositories",
}
RELEASE_INVENTORY_REPOSITORY_FIELDS = {
    "name",
    "repository_url",
    "visibility",
    "default_branch",
    "is_template",
    "license",
    "release",
    "tag_object",
    "peeled_commit",
    "tag_ref",
    "tag_target",
    "tagger",
    "release_record",
    "release_workflow",
    "release_verification",
    "successful_ci_runs",
    "pages",
    "live",
}
RELEASE_RECORD_FIELDS = {
    "tag_name",
    "url",
    "name",
    "published_at",
    "is_draft",
    "is_prerelease",
    "is_immutable",
    "assets",
}
ASSET_FIELDS = {"name", "size", "digest", "url"}
WORKFLOW_RUN_FIELDS = {
    "databaseId",
    "workflowName",
    "status",
    "conclusion",
    "headSha",
    "headBranch",
    "event",
    "url",
    "createdAt",
    "updatedAt",
}
RELEASE_VERIFICATION_FIELDS = {
    "verified_at",
    "release_attestation_verified",
    "workflow_exception",
}
POST_PUBLICATION_ATTESTATION_RACE_RUNS = {
    ("reblocke/compatibility-curve", "v0.1.5"): 30672853190,
    ("reblocke/type-s-m-calibrator", "v0.1.5"): 30677268367,
}
PAGES_FIELDS = {
    "deployment_id",
    "sha",
    "created_at",
    "status",
    "environment_url",
    "workflow_runs",
}
LIVE_FIELDS = {
    "url",
    "sha256",
    "source_commit",
    "catalog_version",
    "bundle_sha256",
    "packages",
    "staged_files_verified",
}
TAGGER_FIELDS = {"name", "email", "date"}
TAG_OBJECT_FIELDS = {"type", "sha"}
TAG_REF_FIELDS = {"name", *TAG_OBJECT_FIELDS}
STAGED_FILE_FIELDS = {"path", "bytes", "sha256"}
FOCUSED_PACKAGE_FIELDS = {
    "role",
    "distribution",
    "import_name",
    "version",
    "artifact_url",
    "artifact_sha256",
    "files",
    "package_sha256",
}
INTEGRATED_PACKAGE_FIELDS = {
    "role",
    "distribution",
    "import_name",
    "version",
    "files",
}
CATALOG_NAME = "reblocke/wald-inference-tools"
CORE_NAME = "reblocke/wald-inference-core"
TEMPLATE_NAME = "reblocke/scientific-applet-template"
INTEGRATED_NAME = "reblocke/conf_curve_likelihood"
STABLE_AUDITED_RELEASES = EXPECTED_REPOSITORIES
TEMPLATE_LIVE_URL = "https://reblocke.github.io/scientific-applet-template/assets/py/manifest.json"
TEMPLATE_DISTRIBUTION = "scientific-applet-template-package"
CATALOG_LIVE_URL = "https://reblocke.github.io/wald-inference-tools/data/tools.json"
EXPECTED_TAGGER_NAME = "Brian Locke"
CORE_DISTRIBUTION = "wald-inference"
CORE_ARTIFACT_URL = (
    "https://github.com/reblocke/wald-inference-core/releases/download/"
    "v0.4.2/wald_inference-0.4.2-py3-none-any.whl"
)


class ValidationStatusError(ValueError):
    """Raised when the portfolio validation status is internally inconsistent."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValidationStatusError(f"duplicate JSON key: {key!r}")
        value[key] = item
    return value


def _exact_fields(value: dict[str, Any], expected: set[str], location: str) -> None:
    missing = expected - value.keys()
    extra = value.keys() - expected
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing {sorted(missing)}")
        if extra:
            details.append(f"unexpected {sorted(extra)}")
        raise ValidationStatusError(f"{location}: {'; '.join(details)}")


def _nonempty_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValidationStatusError(f"{location} must be a non-empty, trimmed string")
    return value


def _staged_record_digest(records: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for record in sorted(records, key=lambda item: item["path"]):
        digest.update((f"{record['path']}\0{record['sha256']}\0{record['bytes']}\n").encode())
    return digest.hexdigest()


def _validate_staged_files(
    files: Any,
    *,
    location: str,
) -> tuple[tuple[str, int, str], ...]:
    if not isinstance(files, list) or not files:
        raise ValidationStatusError(f"{location} must be a non-empty array")
    normalized: list[tuple[str, int, str]] = []
    for index, record in enumerate(files):
        record_location = f"{location}[{index}]"
        if not isinstance(record, dict):
            raise ValidationStatusError(f"{record_location} must be an object")
        _exact_fields(record, STAGED_FILE_FIELDS, record_location)
        path_text = _nonempty_string(record["path"], f"{record_location}.path")
        path = PurePosixPath(path_text)
        if (
            path.is_absolute()
            or path.as_posix() != path_text
            or ".." in path.parts
            or not path.parts
        ):
            raise ValidationStatusError(f"{record_location}.path is not canonical")
        if type(record["bytes"]) is not int or record["bytes"] < 0:
            raise ValidationStatusError(f"{record_location}.bytes must be a nonnegative integer")
        if not isinstance(record["sha256"], str) or not SHA256_RE.fullmatch(record["sha256"]):
            raise ValidationStatusError(f"{record_location}.sha256 must be a SHA-256")
        normalized.append((path_text, record["bytes"], record["sha256"]))
    if normalized != sorted(normalized):
        raise ValidationStatusError(f"{location} must use canonical path ordering")
    if len({record[0] for record in normalized}) != len(normalized):
        raise ValidationStatusError(f"{location} contains duplicate paths")
    return tuple(normalized)


def _validate_live_packages(
    packages: Any,
    *,
    location: str,
    name: str,
    expected_packages: dict[str, str],
    bundle_sha256: Any,
    core_artifact_digest: str,
) -> tuple[tuple[str, int, str], ...] | None:
    if not isinstance(packages, list) or not packages:
        raise ValidationStatusError(f"{location} must be a non-empty array")
    expected_order = list(expected_packages)
    if (
        len(packages) != len(expected_order)
        or [
            package.get("distribution") if isinstance(package, dict) else None
            for package in packages
        ]
        != expected_order
    ):
        raise ValidationStatusError(
            f"{location} packages do not exactly match the expected staged set"
        )
    observed_order: list[str] = []
    all_file_records: list[dict[str, Any]] = []
    core_files: tuple[tuple[str, int, str], ...] | None = None
    for index, package in enumerate(packages):
        package_location = f"{location}[{index}]"
        if not isinstance(package, dict):
            raise ValidationStatusError(f"{package_location} must be an object")
        expected_fields = (
            INTEGRATED_PACKAGE_FIELDS if name == INTEGRATED_NAME else FOCUSED_PACKAGE_FIELDS
        )
        _exact_fields(package, expected_fields, package_location)
        distribution = _nonempty_string(package["distribution"], f"{package_location}.distribution")
        observed_order.append(distribution)
        expected_version = expected_packages.get(distribution)
        if expected_version is None or package["version"] != expected_version:
            raise ValidationStatusError(
                f"{location} has no unique {distribution} {expected_version} package"
            )
        _nonempty_string(package["import_name"], f"{package_location}.import_name")
        expected_role = "core" if distribution == CORE_DISTRIBUTION else "app"
        if package["role"] != expected_role:
            raise ValidationStatusError(f"{package_location}.role must equal {expected_role}")
        normalized_files = _validate_staged_files(
            package["files"],
            location=f"{package_location}.files",
        )
        all_file_records.extend(package["files"])

        if name != INTEGRATED_NAME:
            observed_package_sha = _staged_record_digest(package["files"])
            if package["package_sha256"] != observed_package_sha:
                raise ValidationStatusError(
                    f"{package_location}.package_sha256 does not match its staged files"
                )
            if distribution == CORE_DISTRIBUTION:
                if (
                    package["artifact_url"] != CORE_ARTIFACT_URL
                    or package["artifact_sha256"] != core_artifact_digest
                ):
                    raise ValidationStatusError(
                        f"{package_location} does not bind the audited Core wheel"
                    )
            elif package["artifact_url"] is not None or package["artifact_sha256"] is not None:
                raise ValidationStatusError(
                    f"{package_location} app package must not claim an external artifact"
                )
        if distribution == CORE_DISTRIBUTION:
            core_files = normalized_files

    if observed_order != expected_order:
        raise ValidationStatusError(
            f"{location} packages do not exactly match the expected staged set"
        )
    if not isinstance(bundle_sha256, str) or not SHA256_RE.fullmatch(bundle_sha256):
        raise ValidationStatusError(f"{location} bundle_sha256 must be a SHA-256")
    if bundle_sha256 != _staged_record_digest(all_file_records):
        raise ValidationStatusError(
            f"{location} bundle_sha256 does not match the staged file records"
        )
    return core_files


def _expected_release_assets(name: str, release: str) -> tuple[set[str], str | None]:
    version = release.removeprefix("v")
    repository = name.split("/", 1)[1]
    if name == CORE_NAME:
        return (
            {
                "SHA256SUMS",
                "baseline-parity.json",
                f"wald_inference-{version}-py3-none-any.whl",
                f"wald_inference-{version}.tar.gz",
            },
            None,
        )
    if name == CATALOG_NAME:
        live_asset = f"tools-{release}.json"
        return (
            {
                "SHA256SUMS",
                live_asset,
                f"PORTFOLIO_VALIDATION_REPORT-{release}.md",
                f"validation_status-{release}.json",
                f"validation-evidence-index-{release}.json",
                f"portfolio-validation-evidence-{release}.tar.gz",
                f"{repository}-site-{release}.zip",
                f"{repository}-{release}.tar.gz",
            },
            live_asset,
        )
    if name == "reblocke/conf_curve_likelihood":
        live_asset = "browser-stage-manifest.json"
        return (
            {
                "SHA256SUMS",
                live_asset,
                f"conf_curve_likelihood-{version}.tar.gz",
            },
            live_asset,
        )
    live_asset = f"browser-stage-manifest-{release}.json"
    return (
        {
            "SHA256SUMS",
            live_asset,
            f"{repository}-{release}.tar.gz",
        },
        live_asset,
    )


def load_status(path: Path = STATUS_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ValidationStatusError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationStatusError("validation status root must be an object")
    return value


def load_release_inventory(path: Path = RELEASE_INVENTORY_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ValidationStatusError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationStatusError("release inventory root must be an object")
    return value


def _validate_successful_run(
    run: Any,
    *,
    location: str,
    workflow_name: str,
    commit: str,
    branch: str | None = None,
) -> None:
    if not isinstance(run, dict):
        raise ValidationStatusError(f"{location} must be an object")
    _exact_fields(run, WORKFLOW_RUN_FIELDS, location)
    if type(run["databaseId"]) is not int or run["databaseId"] <= 0:
        raise ValidationStatusError(f"{location}.databaseId must be a positive integer")
    if (
        run["workflowName"] != workflow_name
        or run["status"] != "completed"
        or run["conclusion"] != "success"
        or run["headSha"] != commit
        or run["event"] != "push"
    ):
        raise ValidationStatusError(
            f"{location} is not a successful {workflow_name} run for {commit}"
        )
    if branch is not None and run["headBranch"] != branch:
        raise ValidationStatusError(f"{location}.headBranch must equal {branch}")
    for field in ("url", "createdAt", "updatedAt"):
        _nonempty_string(run[field], f"{location}.{field}")


def _validate_release_run(
    run: Any,
    verification: Any,
    *,
    location: str,
    name: str,
    release: str,
    commit: str,
    audited_at: str,
) -> None:
    verification_location = f"{location}.release_verification"
    if not isinstance(verification, dict):
        raise ValidationStatusError(f"{verification_location} must be an object")
    _exact_fields(verification, RELEASE_VERIFICATION_FIELDS, verification_location)
    if verification["verified_at"] != audited_at:
        raise ValidationStatusError(
            f"{verification_location}.verified_at must equal the inventory audit time"
        )
    if verification["release_attestation_verified"] is not True:
        raise ValidationStatusError(
            f"{verification_location} must record successful current attestation verification"
        )

    expected_race_run = POST_PUBLICATION_ATTESTATION_RACE_RUNS.get((name, release))
    exception = verification["workflow_exception"]
    if expected_race_run is None:
        if exception is not None:
            raise ValidationStatusError(
                f"{verification_location}.workflow_exception is not authorized for {name}@{release}"
            )
        _validate_successful_run(
            run,
            location=f"{location}.release_workflow",
            workflow_name="Release",
            commit=commit,
            branch=release,
        )
        return

    if exception != "post-publication-attestation-race":
        raise ValidationStatusError(
            f"{verification_location}.workflow_exception must identify the documented race"
        )
    run_location = f"{location}.release_workflow"
    if not isinstance(run, dict):
        raise ValidationStatusError(f"{run_location} must be an object")
    _exact_fields(run, WORKFLOW_RUN_FIELDS, run_location)
    if (
        run["databaseId"] != expected_race_run
        or run["workflowName"] != "Release"
        or run["status"] != "completed"
        or run["conclusion"] != "failure"
        or run["headSha"] != commit
        or run["headBranch"] != release
        or run["event"] != "push"
    ):
        raise ValidationStatusError(
            f"{run_location} does not match the exact documented attestation-race run"
        )
    for field in ("url", "createdAt", "updatedAt"):
        _nonempty_string(run[field], f"{run_location}.{field}")


def validate_release_inventory(
    inventory: dict[str, Any],
    *,
    status: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    """Bind the decision to content-addressed objects and observed hosting state."""

    _exact_fields(inventory, RELEASE_INVENTORY_FIELDS, "release inventory")
    if type(inventory["schema_version"]) is not int or inventory["schema_version"] != 1:
        raise ValidationStatusError("release inventory schema_version must equal 1")
    if inventory["audited_at"] != status["validated_at"]:
        raise ValidationStatusError(
            "release inventory audited_at must equal validation status validated_at"
        )

    carrier = inventory["catalog_evidence_carrier"]
    if not isinstance(carrier, dict):
        raise ValidationStatusError("catalog_evidence_carrier must be an object")
    _exact_fields(carrier, {"release", "note"}, "catalog_evidence_carrier")
    if carrier["release"] != f"v{manifest['catalog_version']}":
        raise ValidationStatusError(
            "catalog evidence-carrier release does not match catalog_version"
        )
    _nonempty_string(carrier["note"], "catalog_evidence_carrier.note")

    repositories = inventory["repositories"]
    if not isinstance(repositories, list):
        raise ValidationStatusError("release inventory repositories must be an array")
    names = [entry.get("name") if isinstance(entry, dict) else None for entry in repositories]
    if names != list(REPOSITORY_ORDER):
        raise ValidationStatusError(
            "release inventory repositories must use canonical portfolio order"
        )
    status_by_name = {repository["name"]: repository for repository in status["repositories"]}
    tools_by_name = {_repository_name(tool["repository_url"]): tool for tool in manifest["tools"]}
    core_artifact_digest: str | None = None
    canonical_core_files: tuple[tuple[str, int, str], ...] | None = None
    core_package_count = 0

    for index, entry in enumerate(repositories):
        location = f"release inventory repositories[{index}]"
        if not isinstance(entry, dict):
            raise ValidationStatusError(f"{location} must be an object")
        _exact_fields(entry, RELEASE_INVENTORY_REPOSITORY_FIELDS, location)
        name = entry["name"]
        expected = status_by_name[name]
        if entry["repository_url"] != f"https://github.com/{name}":
            raise ValidationStatusError(f"{location}.repository_url is not canonical")
        if entry["visibility"] != "PUBLIC":
            raise ValidationStatusError(f"{location}.visibility must be PUBLIC")
        if entry["default_branch"] != "main":
            raise ValidationStatusError(f"{location}.default_branch must be main")
        if entry["license"] != "mit":
            raise ValidationStatusError(f"{location}.license must be MIT")
        if entry["is_template"] is not (name == TEMPLATE_NAME):
            raise ValidationStatusError(f"{location}.is_template is inconsistent")
        if entry["release"] != expected["release"]:
            raise ValidationStatusError(f"{location}.release does not match validation status")
        if entry["peeled_commit"] != expected["commit"]:
            raise ValidationStatusError(
                f"{location}.peeled_commit does not match validation status"
            )
        if not isinstance(entry["tag_object"], str) or not COMMIT_RE.fullmatch(entry["tag_object"]):
            raise ValidationStatusError(f"{location}.tag_object must be a full Git SHA")
        if entry["tag_object"] == entry["peeled_commit"]:
            raise ValidationStatusError(
                f"{location}.tag_object must identify an annotated tag object"
            )
        tag_ref = entry["tag_ref"]
        if not isinstance(tag_ref, dict):
            raise ValidationStatusError(f"{location}.tag_ref must be an object")
        _exact_fields(tag_ref, TAG_REF_FIELDS, f"{location}.tag_ref")
        if (
            tag_ref["name"] != expected["release"]
            or tag_ref["type"] != "tag"
            or tag_ref["sha"] != entry["tag_object"]
        ):
            raise ValidationStatusError(
                f"{location}.tag_ref does not bind the annotated release tag object"
            )
        tag_target = entry["tag_target"]
        if not isinstance(tag_target, dict):
            raise ValidationStatusError(f"{location}.tag_target must be an object")
        _exact_fields(tag_target, TAG_OBJECT_FIELDS, f"{location}.tag_target")
        if tag_target != {"type": "commit", "sha": entry["peeled_commit"]}:
            raise ValidationStatusError(
                f"{location}.tag_target does not bind the peeled release commit"
            )

        tagger = entry["tagger"]
        if not isinstance(tagger, dict):
            raise ValidationStatusError(f"{location}.tagger must be an object")
        _exact_fields(tagger, TAGGER_FIELDS, f"{location}.tagger")
        for field in TAGGER_FIELDS:
            _nonempty_string(tagger[field], f"{location}.tagger.{field}")
        if tagger["name"] != EXPECTED_TAGGER_NAME:
            raise ValidationStatusError(
                f"{location}.tagger.name must equal the approved author {EXPECTED_TAGGER_NAME}"
            )

        release_record = entry["release_record"]
        if not isinstance(release_record, dict):
            raise ValidationStatusError(f"{location}.release_record must be an object")
        _exact_fields(
            release_record,
            RELEASE_RECORD_FIELDS,
            f"{location}.release_record",
        )
        if release_record["tag_name"] != expected["release"]:
            raise ValidationStatusError(
                f"{location}.release_record.tag_name does not match the audited release"
            )
        expected_release_url = f"https://github.com/{name}/releases/tag/{expected['release']}"
        if release_record["url"] != expected_release_url:
            raise ValidationStatusError(
                f"{location}.release_record.url does not match the audited release"
            )
        if release_record["is_draft"] is not False:
            raise ValidationStatusError(f"{location}.release_record must not be a draft")
        expected_prerelease = name not in STABLE_AUDITED_RELEASES
        if release_record["is_prerelease"] is not expected_prerelease:
            raise ValidationStatusError(
                f"{location}.release_record prerelease state contradicts the report"
            )
        expected_immutable = True
        if release_record["is_immutable"] is not expected_immutable:
            raise ValidationStatusError(
                f"{location}.release_record immutable state contradicts the audited release"
            )
        _nonempty_string(release_record["name"], f"{location}.release_record.name")
        _nonempty_string(
            release_record["published_at"],
            f"{location}.release_record.published_at",
        )
        assets = release_record["assets"]
        if not isinstance(assets, list) or not assets:
            raise ValidationStatusError(
                f"{location}.release_record.assets must be a non-empty array"
            )
        assets_by_name: dict[str, dict[str, Any]] = {}
        for asset_index, asset in enumerate(assets):
            asset_location = f"{location}.release_record.assets[{asset_index}]"
            if not isinstance(asset, dict):
                raise ValidationStatusError(f"{asset_location} must be an object")
            _exact_fields(asset, ASSET_FIELDS, asset_location)
            asset_name = _nonempty_string(asset["name"], f"{asset_location}.name")
            expected_asset_url = (
                f"https://github.com/{name}/releases/download/{expected['release']}/{asset_name}"
            )
            if asset["url"] != expected_asset_url:
                raise ValidationStatusError(
                    f"{asset_location}.url does not match the canonical release asset URL"
                )
            if type(asset["size"]) is not int or asset["size"] <= 0:
                raise ValidationStatusError(f"{asset_location}.size must be positive")
            if not isinstance(asset["digest"], str) or not ASSET_DIGEST_RE.fullmatch(
                asset["digest"]
            ):
                raise ValidationStatusError(
                    f"{asset_location}.digest must be a GitHub SHA-256 digest"
                )
            if asset["name"] in assets_by_name:
                raise ValidationStatusError(f"{location}.release_record.assets has duplicate names")
            assets_by_name[asset["name"]] = asset
        expected_assets, live_asset_name = _expected_release_assets(
            name,
            expected["release"],
        )
        if set(assets_by_name) != expected_assets:
            raise ValidationStatusError(
                f"{location}.release_record.assets do not match the expected release set"
            )
        if name == CORE_NAME:
            core_wheel_name = (
                f"wald_inference-{expected['release'].removeprefix('v')}-py3-none-any.whl"
            )
            core_artifact_digest = assets_by_name[core_wheel_name]["digest"].removeprefix("sha256:")

        _validate_release_run(
            entry["release_workflow"],
            entry["release_verification"],
            location=location,
            name=name,
            release=expected["release"],
            commit=expected["commit"],
            audited_at=inventory["audited_at"],
        )
        ci_runs = entry["successful_ci_runs"]
        if not isinstance(ci_runs, list) or not ci_runs:
            raise ValidationStatusError(f"{location}.successful_ci_runs must be a non-empty array")
        for run_index, run in enumerate(ci_runs):
            _validate_successful_run(
                run,
                location=f"{location}.successful_ci_runs[{run_index}]",
                workflow_name="CI",
                commit=expected["commit"],
            )

        pages = entry["pages"]
        live = entry["live"]
        if name == CORE_NAME:
            if pages is not None or live is not None:
                raise ValidationStatusError(f"{location}: Core must not claim Pages evidence")
            continue
        if not isinstance(pages, dict):
            raise ValidationStatusError(f"{location}.pages must be an object")
        _exact_fields(pages, PAGES_FIELDS, f"{location}.pages")
        if (
            type(pages["deployment_id"]) is not int
            or pages["deployment_id"] <= 0
            or pages["sha"] != expected["commit"]
            or pages["status"] != "success"
        ):
            raise ValidationStatusError(
                f"{location}.pages is not a successful deployment of the audited commit"
            )
        for field in ("created_at", "environment_url"):
            _nonempty_string(pages[field], f"{location}.pages.{field}")
        page_runs = pages["workflow_runs"]
        if not isinstance(page_runs, list) or not page_runs:
            raise ValidationStatusError(f"{location}.pages.workflow_runs must be a non-empty array")
        for run_index, run in enumerate(page_runs):
            _validate_successful_run(
                run,
                location=f"{location}.pages.workflow_runs[{run_index}]",
                workflow_name="Deploy Pages",
                commit=expected["commit"],
            )

        if not isinstance(live, dict):
            raise ValidationStatusError(f"{location}.live must be an object")
        _exact_fields(live, LIVE_FIELDS, f"{location}.live")
        _nonempty_string(live["url"], f"{location}.live.url")
        if not isinstance(live["sha256"], str) or not SHA256_RE.fullmatch(live["sha256"]):
            raise ValidationStatusError(f"{location}.live.sha256 must be a SHA-256")
        if (
            live_asset_name is None
            or assets_by_name[live_asset_name]["digest"] != f"sha256:{live['sha256']}"
        ):
            raise ValidationStatusError(
                f"{location}.live bytes do not match the released live-data asset"
            )
        if name == CATALOG_NAME:
            if (
                live["url"] != CATALOG_LIVE_URL
                or live["source_commit"] is not None
                or live["catalog_version"] != expected["release"].removeprefix("v")
                or live["bundle_sha256"] is not None
                or live["packages"] is not None
                or live["staged_files_verified"] is not None
            ):
                raise ValidationStatusError(
                    f"{location}.live does not match the audited catalog predecessor"
                )
            continue
        if (
            live["source_commit"] != expected["commit"]
            or live["catalog_version"] is not None
            or not isinstance(live["bundle_sha256"], str)
            or not isinstance(live["packages"], list)
            or not live["packages"]
            or live["staged_files_verified"] is not True
        ):
            raise ValidationStatusError(
                f"{location}.live does not identify the audited deployed commit"
            )
        if name == TEMPLATE_NAME:
            expected_live_url = TEMPLATE_LIVE_URL
            expected_packages = {TEMPLATE_DISTRIBUTION: expected["release"].removeprefix("v")}
        else:
            tool = tools_by_name[name]
            expected_live_url = tool["manifest_url"]
            expected_packages = {
                tool["app_distribution"]: tool["app_version"],
                "wald-inference": tool["core_version"],
            }
        if live["url"] != expected_live_url:
            raise ValidationStatusError(
                f"{location}.live.url does not match the cataloged manifest URL"
            )
        if core_artifact_digest is None:
            raise ValidationStatusError("Core wheel digest was not established before app records")
        core_files = _validate_live_packages(
            live["packages"],
            location=f"{location}.live.packages",
            name=name,
            expected_packages=expected_packages,
            bundle_sha256=live["bundle_sha256"],
            core_artifact_digest=core_artifact_digest,
        )
        if core_files is not None:
            core_package_count += 1
            if canonical_core_files is None:
                canonical_core_files = core_files
            elif core_files != canonical_core_files:
                raise ValidationStatusError(
                    f"{location}.live Core staged files differ from the portfolio Core bytes"
                )

    if core_package_count != 6 or canonical_core_files is None:
        raise ValidationStatusError(
            "release inventory must bind identical Core staged files in all six scientific apps"
        )


def load_report_inventory(report_path: Path = REPORT_PATH) -> dict[str, Any]:
    report = report_path.read_text(encoding="utf-8")
    if report.count(REPORT_INVENTORY_START) != 1 or report.count(REPORT_INVENTORY_END) != 1:
        raise ValidationStatusError(
            "report must contain exactly one machine-readable validation inventory"
        )
    start = report.index(REPORT_INVENTORY_START) + len(REPORT_INVENTORY_START)
    end = report.index(REPORT_INVENTORY_END)
    if end <= start:
        raise ValidationStatusError("report validation inventory markers are out of order")
    try:
        value = json.loads(report[start:end], object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ValidationStatusError(f"report validation inventory is invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationStatusError("report validation inventory must be an object")
    expected = TOP_LEVEL_FIELDS - {"schema_version", "report_sha256"}
    _exact_fields(value, expected, "report validation inventory")
    return value


def _repository_name(repository_url: str) -> str:
    parsed = urlsplit(repository_url)
    path = parsed.path.strip("/")
    if parsed.netloc != "github.com" or path.count("/") != 1:
        raise ValidationStatusError(
            f"manifest repository URL is not canonical GitHub: {repository_url}"
        )
    return path.removesuffix(".git")


def validate_status(
    status: dict[str, Any],
    *,
    report_path: Path = REPORT_PATH,
    manifest_path: Path | None = None,
    release_inventory_path: Path = RELEASE_INVENTORY_PATH,
    require_releasable: bool = False,
) -> None:
    _exact_fields(status, TOP_LEVEL_FIELDS, "validation status")
    if type(status["schema_version"]) is not int or status["schema_version"] != 1:
        raise ValidationStatusError("schema_version must equal 1")

    validated_at = _nonempty_string(status["validated_at"], "validated_at")
    if not RFC3339_UTC_RE.fullmatch(validated_at):
        raise ValidationStatusError("validated_at must be YYYY-MM-DDTHH:MM:SSZ")
    try:
        datetime.strptime(validated_at, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValidationStatusError("validated_at must be a valid RFC 3339 timestamp") from exc

    verdict = _nonempty_string(status["verdict"], "verdict")
    expected_status = VERDICT_TO_STATUS.get(verdict)
    if expected_status is None:
        raise ValidationStatusError("verdict is not one of the three CC-MIG-11 decisions")

    core_version = _nonempty_string(status["core_version"], "core_version")
    if not SEMVER_RE.fullmatch(core_version):
        raise ValidationStatusError("core_version must be an exact X.Y.Z release")

    report_sha256 = _nonempty_string(status["report_sha256"], "report_sha256")
    if not SHA256_RE.fullmatch(report_sha256):
        raise ValidationStatusError("report_sha256 must be a lowercase SHA-256 digest")
    observed_report_sha256 = hashlib.sha256(report_path.read_bytes()).hexdigest()
    if report_sha256 != observed_report_sha256:
        raise ValidationStatusError(
            f"report_sha256 mismatch: recorded {report_sha256}, observed {observed_report_sha256}"
        )
    report_inventory = load_report_inventory(report_path)
    status_inventory = {
        key: status[key] for key in TOP_LEVEL_FIELDS - {"schema_version", "report_sha256"}
    }
    if status_inventory != report_inventory:
        raise ValidationStatusError(
            "validation status inventory does not exactly match the report inventory"
        )

    repositories = status["repositories"]
    if not isinstance(repositories, list):
        raise ValidationStatusError("repositories must be an array")
    names: list[str] = []
    blocking_count = 0
    repository_statuses: list[str] = []
    for index, repository in enumerate(repositories):
        location = f"repositories[{index}]"
        if not isinstance(repository, dict):
            raise ValidationStatusError(f"{location} must be an object")
        _exact_fields(repository, REPOSITORY_FIELDS, location)
        name = _nonempty_string(repository["name"], f"{location}.name")
        names.append(name)
        commit = _nonempty_string(repository["commit"], f"{location}.commit")
        if not COMMIT_RE.fullmatch(commit):
            raise ValidationStatusError(f"{location}.commit must be a full lowercase Git SHA")
        release = _nonempty_string(repository["release"], f"{location}.release")
        if not TAG_RE.fullmatch(release):
            raise ValidationStatusError(f"{location}.release must be an exact vX.Y.Z tag")
        repository_status = _nonempty_string(repository["status"], f"{location}.status")
        if repository_status not in REPOSITORY_STATUSES:
            raise ValidationStatusError(
                f"{location}.status is not a recognized repository validation status"
            )
        repository_statuses.append(repository_status)
        findings = repository["blocking_findings"]
        if not isinstance(findings, list) or not all(
            isinstance(finding, str) and finding.strip() == finding and finding
            for finding in findings
        ):
            raise ValidationStatusError(
                f"{location}.blocking_findings must be an array of non-empty strings"
            )
        if repository_status == "validation-failed" and not findings:
            raise ValidationStatusError(
                f"{location} with validation-failed status must identify a blocking finding"
            )
        if repository_status != "validation-failed" and findings:
            raise ValidationStatusError(
                f"{location} must not contain blocking findings without validation-failed status"
            )
        blocking_count += len(findings)

    if len(names) != len(set(names)):
        raise ValidationStatusError("repository names must be unique")
    if set(names) != EXPECTED_REPOSITORIES:
        raise ValidationStatusError(
            "repositories must contain the exact portfolio: "
            f"expected {sorted(EXPECTED_REPOSITORIES)}"
        )
    if names != list(REPOSITORY_ORDER):
        raise ValidationStatusError("repositories must use canonical portfolio order")
    if verdict == "Not validated; release blockers remain." and blocking_count == 0:
        raise ValidationStatusError("a failed validation verdict must identify a blocking finding")
    if verdict != "Not validated; release blockers remain." and blocking_count:
        raise ValidationStatusError("a validated verdict must not contain blocking findings")
    derived_status = (
        "validation-failed"
        if "validation-failed" in repository_statuses
        else (
            "conditionally-validated"
            if "conditionally-validated" in repository_statuses
            else "validated"
        )
    )
    if derived_status != expected_status:
        raise ValidationStatusError(
            f"repository statuses derive {derived_status!r}, not verdict status {expected_status!r}"
        )

    manifest = load_manifest(manifest_path) if manifest_path is not None else load_manifest()
    if manifest["core"]["latest_validated_release"] != core_version:
        raise ValidationStatusError("core_version does not match the catalog manifest")
    if manifest["portfolio_status"] != expected_status:
        raise ValidationStatusError("portfolio_status does not match the validation verdict")
    if manifest["core"]["validation_status"] != expected_status:
        raise ValidationStatusError("core.validation_status does not match the validation verdict")
    if any(tool["validation_status"] != expected_status for tool in manifest["tools"]):
        raise ValidationStatusError(
            "every tool validation_status must match the validation verdict"
        )

    repositories_by_name = {repository["name"]: repository for repository in repositories}
    core_name = _repository_name(manifest["core"]["repository"])
    if repositories_by_name[core_name]["release"] != f"v{core_version}":
        raise ValidationStatusError("Core release does not match the catalog manifest")
    for tool in manifest["tools"]:
        name = _repository_name(tool["repository_url"])
        expected_release = f"v{tool['app_version']}"
        if repositories_by_name[name]["release"] != expected_release:
            raise ValidationStatusError(
                f"{name} release does not match the catalog manifest: expected {expected_release}"
            )

    for name, expected_release in NON_MANIFEST_RELEASES.items():
        if repositories_by_name[name]["release"] != expected_release:
            raise ValidationStatusError(
                f"{name} release must be the audited predecessor {expected_release}"
            )

    validate_release_inventory(
        load_release_inventory(release_inventory_path),
        status=status,
        manifest=manifest,
    )
    validate_portfolio_report(
        report_path,
        verdict=verdict,
        blocking_count=blocking_count,
        catalog_version=manifest["catalog_version"],
        validated_at=status["validated_at"],
    )
    if require_releasable and expected_status == "validation-failed":
        raise ValidationStatusError(
            "release requires a validated or conditionally validated portfolio verdict"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the portfolio status and its evidence bindings."
    )
    parser.add_argument(
        "--require-releasable",
        action="store_true",
        help="reject a coherent status whose verdict still reports release blockers",
    )
    args = parser.parse_args(argv)
    status = load_status()
    validate_status(status, require_releasable=args.require_releasable)
    print(f"Validated portfolio status for {len(status['repositories'])} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
