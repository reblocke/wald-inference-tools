from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from scripts.validate_validation_evidence import (
    REQUIRED_KINDS,
    ValidationEvidenceError,
    evidence_index_sha256,
    load_evidence_index,
    validate_evidence_index,
)


def _write_evidence(root: Path) -> tuple[dict, Path]:
    root.mkdir(parents=True)
    files = []
    for index, kind in enumerate(sorted(REQUIRED_KINDS)):
        relative = f"records/{index:02d}-{kind}.txt"
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"Evidence for {kind}.\n", encoding="utf-8")
        files.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "kind": kind,
                "description": f"Preserved {kind} evidence.",
            }
        )
    index = {
        "schema_version": 1,
        "catalog_version": "0.2.0",
        "validated_at": "2026-07-30T15:00:00Z",
        "files": files,
    }
    index_path = root / "index.json"
    index_path.write_text(
        f"{json.dumps(index, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return index, index_path


def test_evidence_index_hashes_every_preserved_file(tmp_path: Path) -> None:
    root = tmp_path / "validation-evidence"
    index, index_path = _write_evidence(root)

    assert load_evidence_index(index_path) == index
    validate_evidence_index(
        index,
        evidence_root=root,
        expected_catalog_version="0.2.0",
    )
    assert evidence_index_sha256(index_path) == hashlib.sha256(index_path.read_bytes()).hexdigest()


def test_evidence_index_rejects_file_hash_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    (root / index["files"][0]["path"]).write_text("changed\n", encoding="utf-8")

    with pytest.raises(ValidationEvidenceError, match="SHA-256 mismatch"):
        validate_evidence_index(index, evidence_root=root)


def test_evidence_index_rejects_unindexed_file(tmp_path: Path) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    (root / "extra.txt").write_text("unindexed\n", encoding="utf-8")

    with pytest.raises(ValidationEvidenceError, match="every preserved evidence file"):
        validate_evidence_index(index, evidence_root=root)


def test_evidence_index_requires_every_lane_and_driver_kind(tmp_path: Path) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    removed = index["files"].pop()
    (root / removed["path"]).unlink()

    with pytest.raises(ValidationEvidenceError, match="missing required kinds"):
        validate_evidence_index(index, evidence_root=root)


@pytest.mark.parametrize(
    "path",
    [
        "../outside.txt",
        "/absolute.txt",
        "records/../outside.txt",
        "index.json",
    ],
)
def test_evidence_index_rejects_unsafe_paths(tmp_path: Path, path: str) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    index["files"][0]["path"] = path

    with pytest.raises(ValidationEvidenceError, match="safe evidence path"):
        validate_evidence_index(index, evidence_root=root)
