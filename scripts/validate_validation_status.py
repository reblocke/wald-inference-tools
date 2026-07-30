from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
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

EXPECTED_REPOSITORIES = set(REPOSITORY_ORDER)
NON_MANIFEST_RELEASES = {
    "reblocke/scientific-applet-template": "v0.1.1",
    "reblocke/wald-inference-tools": "v0.1.1",
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


def load_status(path: Path = STATUS_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ValidationStatusError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationStatusError("validation status root must be an object")
    return value


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

    validate_portfolio_report(
        report_path,
        verdict=verdict,
        blocking_count=blocking_count,
        catalog_version=manifest["catalog_version"],
    )


def main() -> int:
    status = load_status()
    validate_status(status)
    print(f"Validated portfolio status for {len(status['repositories'])} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
