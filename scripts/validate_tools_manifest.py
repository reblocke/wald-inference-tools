from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "data" / "tools.json"

EXPECTED_SLUGS = {
    "compatibility-curve",
    "wald-likelihood-support",
    "critical-effect-size",
    "type-s-m-calibrator",
    "precision-guardrail-planner",
    "conf_curve_likelihood",
}
CONDITIONING_BY_SLUG = {
    "compatibility-curve": "observed-data",
    "wald-likelihood-support": "observed-data",
    "critical-effect-size": "design",
    "type-s-m-calibrator": "design",
    "precision-guardrail-planner": "design",
    "conf_curve_likelihood": "mixed",
}
TOP_LEVEL_FIELDS = {"schema_version", "catalog_version", "portfolio_status", "core", "tools"}
CORE_FIELDS = {"repository", "latest_validated_release", "release_url", "validation_status"}
TOOL_FIELDS = {
    "slug",
    "name",
    "question",
    "conditioning",
    "x_axis",
    "inputs",
    "outputs",
    "non_goals",
    "primary_limitation",
    "requires_assumed_truth",
    "requires_selection_rule",
    "repository_url",
    "hosted_url",
    "app_version",
    "core_version",
    "validation_status",
    "citation_url",
    "manifest_url",
    "app_distribution",
    "adjacent_slug",
}
VALID_STATUSES = {
    "release-candidate",
    "validated",
    "conditionally-validated",
    "not-validated",
    "validation-failed",
}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class ManifestError(ValueError):
    """Raised when checked-in catalog metadata violates its contract."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ManifestError(f"duplicate JSON key: {key!r}")
        value[key] = item
    return value


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ManifestError("manifest root must be an object")
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
        raise ManifestError(f"{location}: {'; '.join(details)}")


def _nonempty_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ManifestError(f"{location} must be a non-empty, trimmed string")
    return value


def _string_list(value: Any, location: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ManifestError(f"{location} must be a non-empty array")
    return [_nonempty_string(item, f"{location}[{index}]") for index, item in enumerate(value)]


def _semver(value: Any, location: str) -> tuple[int, int, int]:
    text = _nonempty_string(value, location)
    if not SEMVER_RE.fullmatch(text):
        raise ManifestError(f"{location} must be an exact X.Y.Z release")
    return tuple(int(part) for part in text.split("."))  # type: ignore[return-value]


def _https_url(value: Any, location: str, *, input_free: bool = False) -> str:
    text = _nonempty_string(value, location)
    parsed = urlsplit(text)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ManifestError(f"{location} must be an absolute HTTPS URL")
    if parsed.username or parsed.password:
        raise ManifestError(f"{location} must not contain credentials")
    if input_free and (parsed.query or parsed.fragment):
        raise ManifestError(f"{location} must be an input-free URL without query or fragment")
    return text


def validate_manifest(manifest: dict[str, Any]) -> None:
    _exact_fields(manifest, TOP_LEVEL_FIELDS, "manifest")
    if manifest["schema_version"] != 1:
        raise ManifestError("schema_version must equal 1")
    _semver(manifest["catalog_version"], "catalog_version")
    if manifest["portfolio_status"] not in VALID_STATUSES:
        raise ManifestError("portfolio_status is not a recognized evidence status")

    core = manifest["core"]
    if not isinstance(core, dict):
        raise ManifestError("core must be an object")
    _exact_fields(core, CORE_FIELDS, "core")
    core_latest = _semver(core["latest_validated_release"], "core.latest_validated_release")
    _https_url(core["repository"], "core.repository", input_free=True)
    expected_core_release = f"{core['repository']}/releases/tag/v{core['latest_validated_release']}"
    if core["release_url"] != expected_core_release:
        raise ManifestError("core.release_url does not match repository/latest release")
    if core["validation_status"] not in VALID_STATUSES:
        raise ManifestError("core.validation_status is not a recognized evidence status")

    tools = manifest["tools"]
    if not isinstance(tools, list):
        raise ManifestError("tools must be an array")
    slugs: list[str] = []
    repositories: list[str] = []
    hosted_urls: list[str] = []
    for index, tool in enumerate(tools):
        location = f"tools[{index}]"
        if not isinstance(tool, dict):
            raise ManifestError(f"{location} must be an object")
        _exact_fields(tool, TOOL_FIELDS, location)
        slug = _nonempty_string(tool["slug"], f"{location}.slug")
        if not SLUG_RE.fullmatch(slug):
            raise ManifestError(f"{location}.slug has invalid characters")
        slugs.append(slug)
        _nonempty_string(tool["name"], f"{location}.name")
        question = _nonempty_string(tool["question"], f"{location}.question")
        if not question.endswith("?"):
            raise ManifestError(f"{location}.question must end in a question mark")
        if tool["conditioning"] != CONDITIONING_BY_SLUG.get(slug):
            raise ManifestError(f"{location}.conditioning does not match the portfolio contract")
        _nonempty_string(tool["x_axis"], f"{location}.x_axis")
        for field in ("inputs", "outputs", "non_goals"):
            _string_list(tool[field], f"{location}.{field}")
        _nonempty_string(tool["primary_limitation"], f"{location}.primary_limitation")
        truth = tool["requires_assumed_truth"]
        rule = tool["requires_selection_rule"]
        allowed_requirement = {"yes", "no", "for-design-views"}
        if truth not in allowed_requirement or rule not in allowed_requirement:
            raise ManifestError(f"{location} has an invalid requirement value")
        repository = _https_url(
            tool["repository_url"], f"{location}.repository_url", input_free=True
        )
        hosted = _https_url(tool["hosted_url"], f"{location}.hosted_url", input_free=True)
        repositories.append(repository)
        hosted_urls.append(hosted)
        app_version = _semver(tool["app_version"], f"{location}.app_version")
        del app_version
        tool_core = _semver(tool["core_version"], f"{location}.core_version")
        if tool_core > core_latest:
            raise ManifestError(f"{location}.core_version exceeds the catalog Core release")
        if tool_core[0] != core_latest[0]:
            raise ManifestError(f"{location}.core_version has an incompatible major version")
        if tool["validation_status"] not in VALID_STATUSES:
            raise ManifestError(f"{location}.validation_status is not recognized")
        _https_url(tool["citation_url"], f"{location}.citation_url", input_free=True)
        _https_url(tool["manifest_url"], f"{location}.manifest_url", input_free=True)
        _nonempty_string(tool["app_distribution"], f"{location}.app_distribution")
        _nonempty_string(tool["adjacent_slug"], f"{location}.adjacent_slug")

    if len(slugs) != len(set(slugs)):
        raise ManifestError("tool slugs must be unique")
    if set(slugs) != EXPECTED_SLUGS:
        raise ManifestError(
            f"tools must contain the exact portfolio: expected {sorted(EXPECTED_SLUGS)}"
        )
    if len(repositories) != len(set(repositories)):
        raise ManifestError("repository URLs must be unique")
    if len(hosted_urls) != len(set(hosted_urls)):
        raise ManifestError("hosted URLs must be unique")
    for index, tool in enumerate(tools):
        if tool["adjacent_slug"] not in set(slugs):
            raise ManifestError(f"tools[{index}].adjacent_slug is unknown")
        if tool["adjacent_slug"] == tool["slug"]:
            raise ManifestError(f"tools[{index}].adjacent_slug must name another tool")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)
    validate_manifest(manifest)
    print(f"Validated {len(manifest['tools'])} tools in {args.manifest}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
