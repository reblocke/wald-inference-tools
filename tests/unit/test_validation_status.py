from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.validate_validation_status import (
    ValidationStatusError,
    load_report_inventory,
    load_status,
    validate_status,
)

RELEASES = {
    "reblocke/wald-inference-core": "v0.4.1",
    "reblocke/scientific-applet-template": "v0.1.1",
    "reblocke/compatibility-curve": "v0.1.2",
    "reblocke/wald-likelihood-support": "v0.1.2",
    "reblocke/critical-effect-size": "v0.1.2",
    "reblocke/type-s-m-calibrator": "v0.1.2",
    "reblocke/precision-guardrail-planner": "v0.1.1",
    "reblocke/wald-inference-tools": "v0.1.1",
    "reblocke/conf_curve_likelihood": "v0.2.2",
}


def _manifest(validation_status: str = "conditionally-validated") -> dict:
    app_versions = {name: release.removeprefix("v") for name, release in RELEASES.items()}
    tool_names = [
        "reblocke/compatibility-curve",
        "reblocke/wald-likelihood-support",
        "reblocke/critical-effect-size",
        "reblocke/type-s-m-calibrator",
        "reblocke/precision-guardrail-planner",
        "reblocke/conf_curve_likelihood",
    ]
    return {
        "catalog_version": "0.2.0",
        "core": {
            "repository": "https://github.com/reblocke/wald-inference-core",
            "latest_validated_release": "0.4.1",
            "validation_status": validation_status,
        },
        "portfolio_status": validation_status,
        "tools": [
            {
                "repository_url": f"https://github.com/{name}",
                "app_version": app_versions[name],
                "validation_status": validation_status,
            }
            for name in tool_names
        ],
    }


def _status(
    verdict: str = "Validated with nonblocking limitations.",
    repository_status: str = "conditionally-validated",
    *,
    blocking: bool = False,
) -> dict:
    return {
        "schema_version": 1,
        "validated_at": "2026-07-30T14:00:00Z",
        "verdict": verdict,
        "core_version": "0.4.1",
        "repositories": [
            {
                "name": name,
                "commit": f"{index + 1:040x}",
                "release": release,
                "status": (
                    "validation-failed"
                    if blocking and index == 0
                    else ("validated" if blocking else repository_status)
                ),
                "blocking_findings": (
                    ["Release blocker remains."] if blocking and index == 0 else []
                ),
            }
            for index, (name, release) in enumerate(RELEASES.items())
        ],
        "report_sha256": "0" * 64,
    }


@pytest.fixture(autouse=True)
def _isolate_report_linter(monkeypatch) -> None:
    monkeypatch.setattr(
        "scripts.validate_validation_status.validate_portfolio_report",
        lambda *args, **kwargs: None,
    )


def _write_report(path: Path, status: dict) -> None:
    inventory = {
        key: value
        for key, value in status.items()
        if key not in {"schema_version", "report_sha256"}
    }
    path.write_text(
        "# Portfolio validation\n\n"
        "<!-- validation-inventory:start -->\n"
        f"{json.dumps(inventory, indent=2, sort_keys=True)}\n"
        "<!-- validation-inventory:end -->\n",
        encoding="utf-8",
    )


def _complete_status(tmp_path: Path, status: dict | None = None) -> tuple[dict, Path]:
    value = deepcopy(status) if status is not None else _status()
    report = tmp_path / "report.md"
    _write_report(report, value)
    value["report_sha256"] = hashlib.sha256(report.read_bytes()).hexdigest()
    return value, report


def test_checked_status_matches_report_inventory_and_manifest(tmp_path: Path, monkeypatch) -> None:
    value, report = _complete_status(tmp_path)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    validate_status(value, report_path=report)


@pytest.mark.parametrize(
    ("verdict", "repository_status", "blocking"),
    [
        ("Validated for release.", "validated", False),
        (
            "Validated with nonblocking limitations.",
            "conditionally-validated",
            False,
        ),
        ("Not validated; release blockers remain.", "validation-failed", True),
    ],
)
def test_all_three_cc_mig_11_verdict_paths(
    tmp_path: Path,
    monkeypatch,
    verdict: str,
    repository_status: str,
    blocking: bool,
) -> None:
    value, report = _complete_status(
        tmp_path,
        _status(verdict, repository_status, blocking=blocking),
    )
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(repository_status),
    )

    validate_status(value, report_path=report)


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        ("# Missing inventory\n", "exactly one"),
        (
            "<!-- validation-inventory:start -->\n{}\n"
            "<!-- validation-inventory:end -->\n"
            "<!-- validation-inventory:start -->\n{}\n"
            "<!-- validation-inventory:end -->\n",
            "exactly one",
        ),
        (
            "<!-- validation-inventory:end -->\n{}\n<!-- validation-inventory:start -->\n",
            "out of order",
        ),
    ],
)
def test_report_inventory_rejects_missing_duplicate_or_reversed_markers(
    tmp_path: Path,
    contents: str,
    message: str,
) -> None:
    report = tmp_path / "report.md"
    report.write_text(contents, encoding="utf-8")

    with pytest.raises(ValidationStatusError, match=message):
        load_report_inventory(report)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda value: value["repositories"].pop(),
            "exact portfolio",
        ),
        (
            lambda value: value["repositories"][0].update(
                {"blocking_findings": ["unresolved blocker"]}
            ),
            "must not contain blocking",
        ),
        (
            lambda value: value.update({"verdict": "Looks fine"}),
            "three CC-MIG-11 decisions",
        ),
    ],
)
def test_status_rejects_inconsistent_evidence(
    tmp_path: Path, monkeypatch, mutation, message: str
) -> None:
    value = _status()
    mutation(value)
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match=message):
        validate_status(value, report_path=report)


def test_status_rejects_report_digest_mismatch(tmp_path: Path, monkeypatch) -> None:
    value, report = _complete_status(tmp_path)
    value["report_sha256"] = "0" * 64
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="report_sha256 mismatch"):
        validate_status(value, report_path=report)


def test_status_rejects_report_inventory_mismatch(tmp_path: Path, monkeypatch) -> None:
    value, report = _complete_status(tmp_path)
    value["repositories"][0]["release"] = "v9.9.9"
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="does not exactly match"):
        validate_status(value, report_path=report)


def test_status_rejects_manifest_release_mismatch(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["repositories"][2]["release"] = "v9.9.9"
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="does not match the catalog manifest"):
        validate_status(value, report_path=report)


def test_status_rejects_non_manifest_predecessor_release(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["repositories"][1]["release"] = "v0.1.2"
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="audited predecessor"):
        validate_status(value, report_path=report)


def test_status_requires_canonical_repository_order(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["repositories"][0], value["repositories"][1] = (
        value["repositories"][1],
        value["repositories"][0],
    )
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="canonical portfolio order"):
        validate_status(value, report_path=report)


def test_status_loader_rejects_duplicate_keys(tmp_path: Path) -> None:
    path = tmp_path / "validation_status.json"
    path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")

    with pytest.raises(ValidationStatusError, match="duplicate JSON key"):
        load_status(path)


@pytest.mark.parametrize("schema_version", [True, 1.0, "1"])
def test_status_rejects_non_integer_schema_version(
    tmp_path: Path, monkeypatch, schema_version
) -> None:
    value = _status()
    value["schema_version"] = schema_version
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="schema_version must equal 1"):
        validate_status(value, report_path=report)


def test_status_rejects_noncanonical_timestamp(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["validated_at"] = "2026-07-30 14:00:00Z"
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="YYYY-MM-DDTHH:MM:SSZ"):
        validate_status(value, report_path=report)


@pytest.mark.parametrize("core_version", ["01.2.3", "1.02.3", "1.2.03"])
def test_status_rejects_semver_leading_zero(tmp_path: Path, monkeypatch, core_version: str) -> None:
    value = _status()
    value["core_version"] = core_version
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="exact X.Y.Z"):
        validate_status(value, report_path=report)
