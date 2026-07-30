from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.validate_tools_manifest import ManifestError, load_manifest, validate_manifest


def test_checked_in_manifest_is_strict_and_complete() -> None:
    manifest = load_manifest()
    validate_manifest(manifest)
    assert len(manifest["tools"]) == 6
    assert {tool["conditioning"] for tool in manifest["tools"]} == {
        "observed-data",
        "design",
        "mixed",
    }


def test_duplicate_json_key_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
    with pytest.raises(ManifestError, match="duplicate JSON key"):
        load_manifest(path)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda value: value["tools"].append(deepcopy(value["tools"][0])), "unique"),
        (
            lambda value: value["tools"][0].update({"conditioning": "design"}),
            "conditioning",
        ),
        (
            lambda value: value["tools"][0].update(
                {"hosted_url": "https://example.test/?estimate=1.2"}
            ),
            "input-free",
        ),
        (
            lambda value: value["tools"][0].pop("primary_limitation"),
            "missing",
        ),
    ],
)
def test_semantic_contract_rejects_invalid_metadata(mutation, message: str) -> None:
    manifest = load_manifest()
    mutation(manifest)
    with pytest.raises(ManifestError, match=message):
        validate_manifest(manifest)


def test_manifest_serialization_has_no_nonstandard_numbers() -> None:
    raw = json.dumps(load_manifest(), allow_nan=False, sort_keys=True)
    assert "NaN" not in raw
    assert "Infinity" not in raw
