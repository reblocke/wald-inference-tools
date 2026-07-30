from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from scripts.validate_validation_evidence import (
    REQUIRED_FINAL_RECORDS,
    REQUIRED_KINDS,
    ValidationEvidenceError,
    evidence_index_sha256,
    load_evidence_index,
    validate_evidence_index,
)

LIVE_SITES = {
    "compatibility-curve",
    "wald-likelihood-support",
    "critical-effect-size",
    "type-s-m-calibrator",
    "precision-guardrail-planner",
    "conf_curve_likelihood",
    "scientific-applet-template",
    "wald-inference-tools",
}
SCIENTIFIC_SITES = LIVE_SITES - {"wald-inference-tools"}
RECOVERY_TARGETS = {
    "compatibility-curve": "#ci-lower",
    "wald-likelihood-support": "#ci-lower",
    "critical-effect-size": "#target-probability",
    "type-s-m-calibrator": "#null-value",
    "precision-guardrail-planner": "#target-true-effect",
    "scientific-applet-template": "#first-value",
}


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(f"{json.dumps(value, indent=2, sort_keys=True)}\n", encoding="utf-8")


def _empty_storage() -> dict[str, Any]:
    return {
        "cacheStorage": [],
        "contextCookies": [],
        "documentCookie": "",
        "indexedDB": [],
        "localStorage": [],
        "serviceWorkerController": False,
        "serviceWorkers": [],
        "sessionStorage": [],
    }


def _safe_network() -> dict[str, Any]:
    return {
        "methods": {"GET": 1},
        "non_get_requests": [],
        "sentinel_in_any_request_or_websocket": False,
        "sentinel_in_post_input_request": False,
        "telemetry_matches": [],
        "websockets": [],
    }


def _keyboard_result(site: str, *, camel_case: bool = False) -> dict[str, Any]:
    if site == "conf_curve_likelihood":
        key = "automaticWorkflowCompleted" if camel_case else "automatic_workflow_completed"
        return {key: True}
    if site == "wald-inference-tools":
        return {
            "skip_target": "main-content",
            "design_checked": True,
            "visible_cards": 4,
        }
    return {"reached": True}


def _live_site_result(site: str) -> dict[str, Any]:
    desktop: dict[str, Any] = {
        "console_errors": [],
        "labels_and_text": {
            "controls": [{"id": "control"}],
            "unlabelled_enabled_controls": [],
            "visible_images_missing_alt": [],
        },
        "network": _safe_network(),
        "storage": _empty_storage(),
    }
    if site == "wald-inference-tools":
        desktop.update({"comparison_row_count": 6, "tool_card_count": 6})
    else:
        error_attributes = {
            "ariaLive": "polite" if site == "conf_curve_likelihood" else None,
            "dataState": "error" if site == "conf_curve_likelihood" else None,
        }
        desktop.update(
            {
                "copies": [
                    {
                        "clipboard_length": 20,
                        "enabled": True,
                        "nonempty": True,
                        "present": True,
                        "visible": True,
                    }
                ],
                "downloads": [
                    {
                        "bytes": 20,
                        "enabled": True,
                        "filename": "results.csv",
                        "png_signature": False,
                        "present": True,
                        "visible": True,
                    }
                ],
                "error_and_recovery": {
                    "error_attributes": error_attributes,
                    "error_text": "Correct the invalid input.",
                    "recovered": True,
                    "recovery_status": "Calculation updated.",
                    "safe_no_traceback_or_local_path": True,
                },
                "page_errors": [],
                "url_unchanged": site != "scientific-applet-template",
            }
        )
    mobile = {
        "controls_visible": True,
        "keyboard": _keyboard_result(site),
        "network": _safe_network(),
        "no_horizontal_overflow": True,
        "results_visible": True,
        "storage": _empty_storage(),
        "url_unchanged": site != "wald-inference-tools",
        "viewport": {
            "bodyScrollWidth": 390,
            "documentClientWidth": 390,
            "documentScrollWidth": 390,
            "innerWidth": 390,
        },
    }
    webkit = {
        "console_errors": [],
        "page_errors": [],
        "smoke_status": "Ready.",
        "storage": _empty_storage(),
    }
    return {
        "url": f"https://reblocke.github.io/{site}/",
        "chromium_desktop": {"ok": True, "result": desktop},
        "chromium_mobile_390": {"ok": True, "result": mobile},
        "webkit_smoke": {"ok": True, "result": webkit},
    }


def _write_browser_fixture(root: Path) -> None:
    live_driver = root / "drivers/live_browser_audit.py"
    mobile_driver = root / "drivers/mobile_containment_audit.py"
    recovery_driver = root / "drivers/required_error_recovery_audit.py"
    live_driver.write_text("print('live audit')\n", encoding="utf-8")
    mobile_driver.write_text("print('mobile audit')\n", encoding="utf-8")
    recovery_driver.write_text("print('recovery audit')\n", encoding="utf-8")
    live_driver_sha = hashlib.sha256(live_driver.read_bytes()).hexdigest()
    mobile_driver_sha = hashlib.sha256(mobile_driver.read_bytes()).hexdigest()
    recovery_driver_sha = hashlib.sha256(recovery_driver.read_bytes()).hexdigest()

    live = {
        "schema_version": 1,
        "artifact_directory": "/tmp/browser-artifacts",
        "started_at": "2026-07-30T14:00:00Z",
        "completed_at": "2026-07-30T14:01:00Z",
        "driver": {
            "path": "validation-evidence/drivers/live_browser_audit.py",
            "sha256": live_driver_sha,
        },
        "environment": {
            "playwright": "1.61.0",
            "chromium_version": "149.0.7827.55",
            "webkit_version": "26.5",
        },
        "sites": {site: _live_site_result(site) for site in LIVE_SITES},
    }
    mobile = {
        "schema_version": 1,
        "artifact_directory": "/tmp/browser-artifacts",
        "chromiumVersion": "149.0.7827.55",
        "started_at": "2026-07-30T14:02:00Z",
        "completed_at": "2026-07-30T14:03:00Z",
        "driver": {
            "path": "validation-evidence/drivers/mobile_containment_audit.py",
            "sha256": mobile_driver_sha,
        },
        "source_driver_sha256": live_driver_sha,
        "sites": {
            site: {
                "bodyScrollWidth": 390,
                "consoleErrors": [],
                "documentClientWidth": 390,
                "documentScrollWidth": 390,
                "innerWidth": 390,
                "keyboard": _keyboard_result(site, camel_case=True),
                "pageErrors": [],
                "pass": True,
                "plotSvgs": [{"left": 20, "right": 370}],
                "plots": [{"left": 20, "right": 370}],
                "tables": [],
                "uncontainedOffenders": [],
            }
            for site in SCIENTIFIC_SITES
        },
    }
    recovery = {
        "schema_version": 1,
        "started_at": "2026-07-30T14:04:00Z",
        "completed_at": "2026-07-30T14:05:00Z",
        "driver": {
            "path": "validation-evidence/drivers/required_error_recovery_audit.py",
            "sha256": recovery_driver_sha,
        },
        "source_driver_sha256": live_driver_sha,
        "sites": {
            site: {
                "ariaInvalid": "true",
                "consoleErrors": [],
                "errorRole": "alert",
                "errorText": "Correct the invalid input.",
                "linkHref": target,
                "linkKeyboardFocusesTarget": True,
                "linkPresent": True,
                "pageErrors": [],
                "pass": True,
                "recovered": True,
            }
            for site, target in RECOVERY_TARGETS.items()
        },
    }
    summary = {
        "schema_version": 1,
        "audited_at": "2026-07-30T15:00:00Z",
        "environment": {
            "playwright": "1.61.0",
            "chromium": "149.0.7827.55",
            "webkit": "26.5",
        },
        "coverage": {
            "released_pages_sites": 7,
            "chromium_desktop_passes": 7,
            "chromium_390px_passes": 7,
            "webkit_smoke_passes": 7,
            "explicit_error_recovery_passes": 7,
        },
        "responsive_layout": {
            "viewport_width_px": 390,
            "sites_with_document_width_exactly_matching_viewport": 7,
            "uncontained_visible_elements": 0,
        },
        "privacy": {
            "non_get_requests": 0,
            "websockets": 0,
            "telemetry_matches": 0,
            "sentinel_input_observed_in_any_request": False,
            "cookies": 0,
            "local_storage_entries": 0,
            "session_storage_entries": 0,
            "indexed_db_databases": 0,
            "cache_storage_entries": 0,
            "service_workers": 0,
            "service_worker_controllers": 0,
            "post_input_network_observation": (
                "Two local blob-image GET observations per calculation site; "
                "no HTTP request followed user input."
            ),
        },
        "accessibility_and_recovery": {
            "keyboard_focus_paths_checked": 7,
            "input_label_sets_checked": 7,
            "error_messages_exposed_to_assistive_technology": True,
            "explicit_error_link_focus_passes": 6,
            "integrated_error_surface": "aria-live polite status with successful recovery",
            "valid_input_recovers_after_error": True,
            "automated_only": True,
        },
        "source_files": [
            "browser/corrected-live-browser-results.json",
            "browser/corrected-mobile-containment.json",
            "browser/corrected-required-error-recovery.json",
        ],
    }
    _write_json(root / "browser/corrected-live-browser-results.json", live)
    _write_json(root / "browser/corrected-mobile-containment.json", mobile)
    _write_json(root / "browser/corrected-required-error-recovery.json", recovery)
    _write_json(root / "browser/browser-summary.json", summary)


def _write_evidence(root: Path) -> tuple[dict, Path]:
    root.mkdir(parents=True)
    paths_and_kinds: dict[str, str] = {}
    for relative, kind in REQUIRED_FINAL_RECORDS.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"Evidence for {kind}.\n", encoding="utf-8")
        paths_and_kinds[relative] = kind
    covered_kinds = set(REQUIRED_FINAL_RECORDS.values())
    for index, kind in enumerate(sorted(REQUIRED_KINDS - covered_kinds)):
        relative = f"records/{index:02d}-{kind}.txt"
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"Evidence for {kind}.\n", encoding="utf-8")
        paths_and_kinds[relative] = kind
    _write_browser_fixture(root)
    files = []
    for relative, kind in paths_and_kinds.items():
        path = root / relative
        files.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "kind": kind,
                "description": f"Preserved {kind} evidence.",
            }
        )
    files.sort(key=lambda record: record["path"])
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


def _mutate_json_evidence(
    root: Path,
    index: dict[str, Any],
    relative: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    path = root / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    _write_json(path, value)
    record = next(record for record in index["files"] if record["path"] == relative)
    record["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()


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


@pytest.mark.parametrize(
    ("relative", "mutate", "message"),
    [
        (
            "browser/corrected-live-browser-results.json",
            lambda value: value["sites"].pop("compatibility-curve"),
            "must contain exactly",
        ),
        (
            "browser/corrected-live-browser-results.json",
            lambda value: value["sites"]["compatibility-curve"]["webkit_smoke"].update(
                {"ok": False}
            ),
            r"webkit_smoke\.ok must be true",
        ),
        (
            "browser/corrected-live-browser-results.json",
            lambda value: value["sites"]["compatibility-curve"]["chromium_desktop"]["result"][
                "network"
            ]["non_get_requests"].append({"method": "POST"}),
            "non_get_requests must be empty",
        ),
        (
            "browser/corrected-mobile-containment.json",
            lambda value: value["sites"]["compatibility-curve"].update({"pass": False}),
            r"\.pass must be true",
        ),
        (
            "browser/corrected-mobile-containment.json",
            lambda value: value["sites"]["compatibility-curve"].update(
                {"documentScrollWidth": 391}
            ),
            "documentScrollWidth must equal 390",
        ),
        (
            "browser/corrected-required-error-recovery.json",
            lambda value: value["sites"]["compatibility-curve"].update(
                {"linkKeyboardFocusesTarget": False}
            ),
            "linkKeyboardFocusesTarget must be true",
        ),
        (
            "browser/browser-summary.json",
            lambda value: value["environment"].update({"chromium": "stale"}),
            "environment must match",
        ),
        (
            "browser/browser-summary.json",
            lambda value: value.update({"audited_at": "2026-07-30T14:00:00Z"}),
            "at or after all raw browser runs",
        ),
        (
            "browser/corrected-mobile-containment.json",
            lambda value: value.update({"source_driver_sha256": "0" * 64}),
            "source_driver_sha256 must match",
        ),
    ],
    ids=[
        "missing-live-site",
        "failed-webkit-run",
        "non-get-request",
        "failed-mobile-run",
        "mobile-overflow",
        "failed-error-link-focus",
        "stale-summary-environment",
        "stale-summary-time",
        "broken-source-driver-chain",
    ],
)
def test_evidence_index_rejects_hash_correct_semantically_false_browser_evidence(
    tmp_path: Path,
    relative: str,
    mutate: Callable[[dict[str, Any]], None],
    message: str,
) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    _mutate_json_evidence(root, index, relative, mutate)

    with pytest.raises(ValidationEvidenceError, match=message):
        validate_evidence_index(index, evidence_root=root)


def test_evidence_index_rejects_hash_correct_non_json_browser_summary(tmp_path: Path) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    summary_path = root / "browser/browser-summary.json"
    summary_path.write_text("Browser checks passed.\n", encoding="utf-8")
    record = next(
        record for record in index["files"] if record["path"] == "browser/browser-summary.json"
    )
    record["sha256"] = hashlib.sha256(summary_path.read_bytes()).hexdigest()

    with pytest.raises(ValidationEvidenceError, match="invalid JSON"):
        validate_evidence_index(index, evidence_root=root)


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
    removed = next(record for record in index["files"] if record["kind"] == "lane-b-parity")
    index["files"].remove(removed)
    (root / removed["path"]).unlink()

    with pytest.raises(ValidationEvidenceError, match="missing required kinds"):
        validate_evidence_index(index, evidence_root=root)


def test_evidence_index_requires_named_final_records(tmp_path: Path) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    required_path = "lanes/all-ticket-acceptance-final.md"
    index["files"] = [record for record in index["files"] if record["path"] != required_path]
    (root / required_path).unlink()

    with pytest.raises(ValidationEvidenceError, match="required final records"):
        validate_evidence_index(index, evidence_root=root)


def test_evidence_index_rejects_misclassified_final_record(tmp_path: Path) -> None:
    root = tmp_path / "validation-evidence"
    index, _ = _write_evidence(root)
    required_path = "lanes/integrated-v0.2.5-cdef.md"
    next(record for record in index["files"] if record["path"] == required_path)["kind"] = (
        "lane-d-provenance"
    )

    with pytest.raises(ValidationEvidenceError, match="incorrect kinds"):
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
