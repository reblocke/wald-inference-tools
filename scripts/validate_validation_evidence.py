from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

if __package__:
    from scripts.validate_tools_manifest import PROJECT_ROOT
else:
    from validate_tools_manifest import PROJECT_ROOT  # type: ignore[import-not-found]

EVIDENCE_ROOT = PROJECT_ROOT / "validation-evidence"
INDEX_PATH = EVIDENCE_ROOT / "index.json"

TOP_LEVEL_FIELDS = {
    "schema_version",
    "catalog_version",
    "validated_at",
    "files",
}
FILE_FIELDS = {"path", "sha256", "kind", "description"}
REQUIRED_KINDS = {
    "lane-a-numerical",
    "lane-b-parity",
    "lane-c-cold-start",
    "lane-d-provenance",
    "lane-e-browser-privacy-accessibility",
    "lane-f-docs-rights",
    "command-ledger",
    "release-inventory",
    "audit-driver",
    "browser-result",
}
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class ValidationEvidenceError(ValueError):
    """Raised when preserved portfolio evidence is incomplete or inconsistent."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValidationEvidenceError(f"duplicate JSON key: {key!r}")
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
        raise ValidationEvidenceError(f"{location}: {'; '.join(details)}")


def _nonempty_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValidationEvidenceError(f"{location} must be a non-empty, trimmed string")
    return value


def load_evidence_index(path: Path = INDEX_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise ValidationEvidenceError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationEvidenceError("validation evidence index root must be an object")
    return value


def validate_evidence_index(
    index: dict[str, Any],
    *,
    evidence_root: Path = EVIDENCE_ROOT,
    expected_catalog_version: str | None = None,
) -> None:
    _exact_fields(index, TOP_LEVEL_FIELDS, "validation evidence index")
    if type(index["schema_version"]) is not int or index["schema_version"] != 1:
        raise ValidationEvidenceError("schema_version must equal 1")

    catalog_version = _nonempty_string(index["catalog_version"], "catalog_version")
    if not SEMVER_RE.fullmatch(catalog_version):
        raise ValidationEvidenceError("catalog_version must be an exact X.Y.Z release")
    if expected_catalog_version is not None and catalog_version != expected_catalog_version:
        raise ValidationEvidenceError(
            f"evidence catalog_version {catalog_version} != expected {expected_catalog_version}"
        )

    validated_at = _nonempty_string(index["validated_at"], "validated_at")
    if not RFC3339_UTC_RE.fullmatch(validated_at):
        raise ValidationEvidenceError("validated_at must be YYYY-MM-DDTHH:MM:SSZ")
    try:
        datetime.strptime(validated_at, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValidationEvidenceError("validated_at must be a valid RFC 3339 timestamp") from exc

    files = index["files"]
    if not isinstance(files, list) or not files:
        raise ValidationEvidenceError("files must be a non-empty array")
    indexed_paths: list[str] = []
    observed_kinds: set[str] = set()
    for position, entry in enumerate(files):
        location = f"files[{position}]"
        if not isinstance(entry, dict):
            raise ValidationEvidenceError(f"{location} must be an object")
        _exact_fields(entry, FILE_FIELDS, location)
        relative_text = _nonempty_string(entry["path"], f"{location}.path")
        relative = PurePosixPath(relative_text)
        if (
            relative.is_absolute()
            or relative_text != relative.as_posix()
            or ".." in relative.parts
            or relative.name == "index.json"
        ):
            raise ValidationEvidenceError(f"{location}.path is not a safe evidence path")
        indexed_paths.append(relative_text)

        digest = _nonempty_string(entry["sha256"], f"{location}.sha256")
        if not SHA256_RE.fullmatch(digest):
            raise ValidationEvidenceError(f"{location}.sha256 must be a lowercase SHA-256 digest")
        kind = _nonempty_string(entry["kind"], f"{location}.kind")
        observed_kinds.add(kind)
        _nonempty_string(entry["description"], f"{location}.description")

        path = evidence_root / Path(*relative.parts)
        if path.is_symlink() or not path.is_file():
            raise ValidationEvidenceError(f"indexed evidence file is missing: {relative_text}")
        if path.stat().st_size == 0:
            raise ValidationEvidenceError(f"indexed evidence file is empty: {relative_text}")
        observed_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed_digest != digest:
            raise ValidationEvidenceError(
                f"evidence SHA-256 mismatch for {relative_text}: "
                f"recorded {digest}, observed {observed_digest}"
            )

    if indexed_paths != sorted(indexed_paths):
        raise ValidationEvidenceError("evidence files must use canonical path ordering")
    if len(indexed_paths) != len(set(indexed_paths)):
        raise ValidationEvidenceError("evidence file paths must be unique")

    actual_paths = sorted(
        path.relative_to(evidence_root).as_posix()
        for path in evidence_root.rglob("*")
        if path.is_file() and path != evidence_root / "index.json"
    )
    if actual_paths != indexed_paths:
        raise ValidationEvidenceError(
            "evidence index must enumerate every preserved evidence file exactly once"
        )

    missing_kinds = REQUIRED_KINDS - observed_kinds
    if missing_kinds:
        raise ValidationEvidenceError(
            f"evidence index is missing required kinds: {sorted(missing_kinds)}"
        )


def evidence_index_sha256(path: Path = INDEX_PATH) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    index = load_evidence_index()
    validate_evidence_index(index)
    print(f"Validated {len(index['files'])} preserved portfolio evidence files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
