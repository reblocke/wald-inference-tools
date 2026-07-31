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
REQUIRED_FINAL_RECORDS = {
    "browser/browser-summary.json": "browser-result",
    "browser/corrected-live-browser-results.json": ("lane-e-browser-privacy-accessibility"),
    "browser/corrected-mobile-containment.json": ("lane-e-browser-privacy-accessibility"),
    "browser/corrected-required-error-recovery.json": ("lane-e-browser-privacy-accessibility"),
    "commands/README_COMMANDS.md": "command-ledger",
    "drivers/live_browser_audit.py": "audit-driver",
    "drivers/mobile_containment_audit.py": "audit-driver",
    "drivers/required_error_recovery_audit.py": "audit-driver",
    "inventory/release-inventory.json": "release-inventory",
    "lanes/all-ticket-acceptance-final.md": "lane-f-docs-rights",
    "lanes/final-release-set-v0.4.2-lane-ab.md": "lane-b-parity",
    "lanes/final-release-set-v0.4.2-lane-cd.md": "lane-d-provenance",
    "lanes/final-release-set-v0.4.2-lane-ef.md": ("lane-e-browser-privacy-accessibility"),
    "results/core-v0.4.2-baseline-parity.json": "lane-a-numerical",
    "results/core-v0.4.2-independent-recomputation.json": "lane-a-numerical",
    "results/final-release-set-v0.4.2-cold-start.json": "lane-c-cold-start",
}
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
BROWSER_SUMMARY_PATH = "browser/browser-summary.json"
LIVE_BROWSER_RESULTS_PATH = "browser/corrected-live-browser-results.json"
MOBILE_CONTAINMENT_PATH = "browser/corrected-mobile-containment.json"
REQUIRED_ERROR_RECOVERY_PATH = "browser/corrected-required-error-recovery.json"
LIVE_BROWSER_DRIVER_PATH = "drivers/live_browser_audit.py"
MOBILE_CONTAINMENT_DRIVER_PATH = "drivers/mobile_containment_audit.py"
REQUIRED_ERROR_RECOVERY_DRIVER_PATH = "drivers/required_error_recovery_audit.py"

CALCULATION_SITES = {
    "compatibility-curve",
    "wald-likelihood-support",
    "critical-effect-size",
    "type-s-m-calibrator",
    "precision-guardrail-planner",
    "conf_curve_likelihood",
}
TEMPLATE_SITE = "scientific-applet-template"
CATALOG_SITE = "wald-inference-tools"
SCIENTIFIC_SITES = CALCULATION_SITES | {TEMPLATE_SITE}
LIVE_BROWSER_SITES = SCIENTIFIC_SITES | {CATALOG_SITE}
REQUIRED_RECOVERY_SITES = {
    "compatibility-curve",
    "wald-likelihood-support",
    "critical-effect-size",
    "type-s-m-calibrator",
    "precision-guardrail-planner",
    TEMPLATE_SITE,
}
SITE_URLS = {site: f"https://reblocke.github.io/{site}/" for site in LIVE_BROWSER_SITES}
RECOVERY_TARGETS = {
    "compatibility-curve": "#ci-lower",
    "wald-likelihood-support": "#ci-lower",
    "critical-effect-size": "#target-probability",
    "type-s-m-calibrator": "#null-value",
    "precision-guardrail-planner": "#target-true-effect",
    TEMPLATE_SITE: "#first-value",
}

LIVE_BROWSER_FIELDS = {
    "artifact_directory",
    "completed_at",
    "driver",
    "environment",
    "schema_version",
    "sites",
    "started_at",
}
MOBILE_CONTAINMENT_FIELDS = {
    "artifact_directory",
    "chromiumVersion",
    "completed_at",
    "driver",
    "schema_version",
    "sites",
    "source_driver_sha256",
    "started_at",
}
REQUIRED_ERROR_RECOVERY_FIELDS = {
    "completed_at",
    "driver",
    "schema_version",
    "sites",
    "source_driver_sha256",
    "started_at",
}
BROWSER_SUMMARY_FIELDS = {
    "schema_version",
    "audited_at",
    "environment",
    "coverage",
    "responsive_layout",
    "privacy",
    "accessibility_and_recovery",
    "source_files",
}
EMPTY_STORAGE = {
    "cacheStorage": [],
    "contextCookies": [],
    "documentCookie": "",
    "indexedDB": [],
    "localStorage": [],
    "serviceWorkerController": False,
    "serviceWorkers": [],
    "sessionStorage": [],
}


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


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationEvidenceError(message)


def _parse_timestamp(value: Any, location: str) -> datetime:
    timestamp = _nonempty_string(value, location)
    if not RFC3339_UTC_RE.fullmatch(timestamp):
        raise ValidationEvidenceError(f"{location} must be YYYY-MM-DDTHH:MM:SSZ")
    try:
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValidationEvidenceError(f"{location} must be a valid RFC 3339 timestamp") from exc


def _load_evidence_json(evidence_root: Path, relative_path: str) -> dict[str, Any]:
    path = evidence_root / relative_path
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationEvidenceError(f"{relative_path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationEvidenceError(f"{relative_path}: root must be an object")
    return value


def _validate_run_times(
    value: dict[str, Any],
    location: str,
) -> tuple[datetime, datetime]:
    started_at = _parse_timestamp(value.get("started_at"), f"{location}.started_at")
    completed_at = _parse_timestamp(value.get("completed_at"), f"{location}.completed_at")
    _require(
        started_at <= completed_at,
        f"{location}: started_at must not be after completed_at",
    )
    return started_at, completed_at


def _validate_site_set(value: Any, expected: set[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationEvidenceError(f"{location} must be an object")
    observed = set(value)
    if observed != expected:
        raise ValidationEvidenceError(
            f"{location} must contain exactly {sorted(expected)}; observed {sorted(observed)}"
        )
    for site, result in value.items():
        if not isinstance(result, dict):
            raise ValidationEvidenceError(f"{location}.{site} must be an object")
    return value


def _driver_digest(
    value: Any,
    *,
    evidence_root: Path,
    expected_relative_path: str,
    location: str,
) -> str:
    if not isinstance(value, dict):
        raise ValidationEvidenceError(f"{location} must be an object")
    _exact_fields(value, {"path", "sha256"}, location)
    expected_record_path = f"validation-evidence/{expected_relative_path}"
    _require(
        value["path"] == expected_record_path,
        f"{location}.path must equal {expected_record_path!r}",
    )
    digest = _nonempty_string(value["sha256"], f"{location}.sha256")
    _require(
        SHA256_RE.fullmatch(digest) is not None,
        f"{location}.sha256 must be a lowercase SHA-256 digest",
    )
    observed = hashlib.sha256((evidence_root / expected_relative_path).read_bytes()).hexdigest()
    _require(
        digest == observed,
        f"{location}.sha256 does not match preserved driver {expected_relative_path}",
    )
    return digest


def _validate_empty_storage(value: Any, location: str) -> None:
    if not isinstance(value, dict):
        raise ValidationEvidenceError(f"{location} must be an object")
    _exact_fields(value, set(EMPTY_STORAGE), location)
    _require(value == EMPTY_STORAGE, f"{location} must show no persisted browser state")


def _validate_safe_network(value: Any, location: str) -> None:
    if not isinstance(value, dict):
        raise ValidationEvidenceError(f"{location} must be an object")
    for field in ("non_get_requests", "websockets", "telemetry_matches"):
        _require(value.get(field) == [], f"{location}.{field} must be empty")
    for field in (
        "sentinel_in_any_request_or_websocket",
        "sentinel_in_post_input_request",
    ):
        _require(value.get(field) is False, f"{location}.{field} must be false")
    methods = value.get("methods")
    _require(
        isinstance(methods, dict) and methods and set(methods) == {"GET"},
        f"{location}.methods must contain GET only",
    )
    _require(
        type(methods["GET"]) is int and methods["GET"] > 0,
        f"{location}.methods.GET must be a positive integer",
    )


def _validate_keyboard_result(value: Any, site: str, location: str) -> None:
    if not isinstance(value, dict):
        raise ValidationEvidenceError(f"{location} must be an object")
    if site == "conf_curve_likelihood":
        _require(
            value.get("automatic_workflow_completed") is True
            or value.get("automaticWorkflowCompleted") is True,
            f"{location} must record a completed automatic keyboard workflow",
        )
    elif site == CATALOG_SITE:
        _require(
            value.get("skip_target") == "main-content",
            f"{location}.skip_target must equal 'main-content'",
        )
        _require(value.get("design_checked") is True, f"{location}.design_checked must be true")
        _require(
            type(value.get("visible_cards")) is int and value["visible_cards"] > 0,
            f"{location}.visible_cards must be a positive integer",
        )
    else:
        _require(value.get("reached") is True, f"{location}.reached must be true")


def _validate_live_browser_results(
    value: dict[str, Any],
    *,
    evidence_root: Path,
) -> tuple[dict[str, str], datetime]:
    location = LIVE_BROWSER_RESULTS_PATH
    _exact_fields(value, LIVE_BROWSER_FIELDS, location)
    _require(value["schema_version"] == 1, f"{location}.schema_version must equal 1")
    _nonempty_string(value["artifact_directory"], f"{location}.artifact_directory")
    _, completed_at = _validate_run_times(value, location)
    live_driver_digest = _driver_digest(
        value["driver"],
        evidence_root=evidence_root,
        expected_relative_path=LIVE_BROWSER_DRIVER_PATH,
        location=f"{location}.driver",
    )
    environment = value["environment"]
    if not isinstance(environment, dict):
        raise ValidationEvidenceError(f"{location}.environment must be an object")
    _exact_fields(
        environment,
        {"playwright", "chromium_version", "webkit_version"},
        f"{location}.environment",
    )
    for field in environment:
        _nonempty_string(environment[field], f"{location}.environment.{field}")

    sites = _validate_site_set(value["sites"], LIVE_BROWSER_SITES, f"{location}.sites")
    for site, record in sites.items():
        site_location = f"{location}.sites.{site}"
        _exact_fields(
            record,
            {"url", "chromium_desktop", "chromium_mobile_390", "webkit_smoke"},
            site_location,
        )
        _require(
            record["url"] == SITE_URLS[site],
            f"{site_location}.url must equal {SITE_URLS[site]!r}",
        )
        for run_name in ("chromium_desktop", "chromium_mobile_390", "webkit_smoke"):
            run = record[run_name]
            run_location = f"{site_location}.{run_name}"
            if not isinstance(run, dict):
                raise ValidationEvidenceError(f"{run_location} must be an object")
            _exact_fields(run, {"ok", "result"}, run_location)
            _require(run["ok"] is True, f"{run_location}.ok must be true")
            if not isinstance(run["result"], dict):
                raise ValidationEvidenceError(f"{run_location}.result must be an object")

        desktop = record["chromium_desktop"]["result"]
        desktop_location = f"{site_location}.chromium_desktop.result"
        _require(
            desktop.get("console_errors") == [], f"{desktop_location}.console_errors must be empty"
        )
        if site != CATALOG_SITE:
            _require(
                desktop.get("page_errors") == [], f"{desktop_location}.page_errors must be empty"
            )
        _validate_empty_storage(desktop.get("storage"), f"{desktop_location}.storage")
        _validate_safe_network(desktop.get("network"), f"{desktop_location}.network")

        labels = desktop.get("labels_and_text")
        if not isinstance(labels, dict):
            raise ValidationEvidenceError(f"{desktop_location}.labels_and_text must be an object")
        _require(
            labels.get("unlabelled_enabled_controls") == [],
            f"{desktop_location}.labels_and_text.unlabelled_enabled_controls must be empty",
        )
        _require(
            labels.get("visible_images_missing_alt") == [],
            f"{desktop_location}.labels_and_text.visible_images_missing_alt must be empty",
        )
        controls = labels.get("controls")
        _require(
            isinstance(controls, list) and controls,
            f"{desktop_location}.labels_and_text.controls must be non-empty",
        )

        if site == CATALOG_SITE:
            _require(
                type(desktop.get("tool_card_count")) is int and desktop["tool_card_count"] > 0,
                f"{desktop_location}.tool_card_count must be a positive integer",
            )
            _require(
                type(desktop.get("comparison_row_count")) is int
                and desktop["comparison_row_count"] > 0,
                f"{desktop_location}.comparison_row_count must be a positive integer",
            )
        else:
            expected_url_unchanged = site != TEMPLATE_SITE
            _require(
                desktop.get("url_unchanged") is expected_url_unchanged,
                f"{desktop_location}.url_unchanged must reflect only the template error-link hash",
            )
            recovery = desktop.get("error_and_recovery")
            if not isinstance(recovery, dict):
                raise ValidationEvidenceError(
                    f"{desktop_location}.error_and_recovery must be an object"
                )
            _require(
                recovery.get("recovered") is True,
                f"{desktop_location}.error_and_recovery.recovered must be true",
            )
            _require(
                recovery.get("safe_no_traceback_or_local_path") is True,
                f"{desktop_location}.error_and_recovery."
                "safe_no_traceback_or_local_path must be true",
            )
            _nonempty_string(
                recovery.get("error_text"),
                f"{desktop_location}.error_and_recovery.error_text",
            )
            _nonempty_string(
                recovery.get("recovery_status"),
                f"{desktop_location}.error_and_recovery.recovery_status",
            )
            if site == "conf_curve_likelihood":
                attributes = recovery.get("error_attributes")
                _require(
                    isinstance(attributes, dict)
                    and attributes.get("ariaLive") == "polite"
                    and attributes.get("dataState") == "error",
                    f"{desktop_location}.error_and_recovery.error_attributes "
                    "must expose an aria-live polite error state",
                )
            for collection_name in ("downloads", "copies"):
                collection = desktop.get(collection_name)
                _require(
                    isinstance(collection, list) and collection,
                    f"{desktop_location}.{collection_name} must be non-empty",
                )
                for position, item in enumerate(collection):
                    item_location = f"{desktop_location}.{collection_name}[{position}]"
                    if not isinstance(item, dict):
                        raise ValidationEvidenceError(f"{item_location} must be an object")
                    for flag in ("present", "enabled"):
                        _require(item.get(flag) is True, f"{item_location}.{flag} must be true")
                    if collection_name == "downloads":
                        _require(
                            type(item.get("bytes")) is int and item["bytes"] > 0,
                            f"{item_location}.bytes must be a positive integer",
                        )
                        filename = _nonempty_string(
                            item.get("filename"),
                            f"{item_location}.filename",
                        )
                        if filename.endswith(".png"):
                            _require(
                                item.get("png_signature") is True,
                                f"{item_location}.png_signature must be true",
                            )
                    else:
                        _require(
                            item.get("visible") is True,
                            f"{item_location}.visible must be true",
                        )
                        _require(
                            item.get("nonempty") is True, f"{item_location}.nonempty must be true"
                        )
                        _require(
                            type(item.get("clipboard_length")) is int
                            and item["clipboard_length"] > 0,
                            f"{item_location}.clipboard_length must be a positive integer",
                        )

        mobile = record["chromium_mobile_390"]["result"]
        mobile_location = f"{site_location}.chromium_mobile_390.result"
        for field in ("no_horizontal_overflow", "controls_visible", "results_visible"):
            _require(mobile.get(field) is True, f"{mobile_location}.{field} must be true")
        viewport = mobile.get("viewport")
        expected_viewport = {
            "bodyScrollWidth": 390,
            "documentClientWidth": 390,
            "documentScrollWidth": 390,
            "innerWidth": 390,
        }
        _require(
            viewport == expected_viewport,
            f"{mobile_location}.viewport must record exact 390 px containment",
        )
        _validate_keyboard_result(mobile.get("keyboard"), site, f"{mobile_location}.keyboard")
        _validate_empty_storage(mobile.get("storage"), f"{mobile_location}.storage")
        _validate_safe_network(mobile.get("network"), f"{mobile_location}.network")

        webkit = record["webkit_smoke"]["result"]
        webkit_location = f"{site_location}.webkit_smoke.result"
        _require(
            webkit.get("console_errors") == [], f"{webkit_location}.console_errors must be empty"
        )
        _require(webkit.get("page_errors") == [], f"{webkit_location}.page_errors must be empty")
        _nonempty_string(webkit.get("smoke_status"), f"{webkit_location}.smoke_status")
        _validate_empty_storage(webkit.get("storage"), f"{webkit_location}.storage")

    return {
        "playwright": environment["playwright"],
        "chromium": environment["chromium_version"],
        "webkit": environment["webkit_version"],
        "live_driver_sha256": live_driver_digest,
    }, completed_at


def _validate_mobile_containment(
    value: dict[str, Any],
    *,
    evidence_root: Path,
    live_driver_digest: str,
) -> datetime:
    location = MOBILE_CONTAINMENT_PATH
    _exact_fields(value, MOBILE_CONTAINMENT_FIELDS, location)
    _require(value["schema_version"] == 1, f"{location}.schema_version must equal 1")
    _nonempty_string(value["artifact_directory"], f"{location}.artifact_directory")
    _nonempty_string(value["chromiumVersion"], f"{location}.chromiumVersion")
    _, completed_at = _validate_run_times(value, location)
    _driver_digest(
        value["driver"],
        evidence_root=evidence_root,
        expected_relative_path=MOBILE_CONTAINMENT_DRIVER_PATH,
        location=f"{location}.driver",
    )
    _require(
        value["source_driver_sha256"] == live_driver_digest,
        f"{location}.source_driver_sha256 must match the preserved live browser driver",
    )
    sites = _validate_site_set(value["sites"], SCIENTIFIC_SITES, f"{location}.sites")
    for site, result in sites.items():
        result_location = f"{location}.sites.{site}"
        _require(result.get("pass") is True, f"{result_location}.pass must be true")
        for field in (
            "bodyScrollWidth",
            "documentClientWidth",
            "documentScrollWidth",
            "innerWidth",
        ):
            _require(result.get(field) == 390, f"{result_location}.{field} must equal 390")
        _require(
            result.get("uncontainedOffenders") == [],
            f"{result_location}.uncontainedOffenders must be empty",
        )
        _require(
            result.get("consoleErrors") == [], f"{result_location}.consoleErrors must be empty"
        )
        _require(result.get("pageErrors") == [], f"{result_location}.pageErrors must be empty")
        _validate_keyboard_result(result.get("keyboard"), site, f"{result_location}.keyboard")
        for collection_name in ("plots", "plotSvgs"):
            collection = result.get(collection_name)
            _require(
                isinstance(collection, list) and collection,
                f"{result_location}.{collection_name} must be non-empty",
            )
            for position, item in enumerate(collection):
                item_location = f"{result_location}.{collection_name}[{position}]"
                if not isinstance(item, dict):
                    raise ValidationEvidenceError(f"{item_location} must be an object")
                left = item.get("left")
                right = item.get("right")
                _require(
                    isinstance(left, (int, float))
                    and not isinstance(left, bool)
                    and isinstance(right, (int, float))
                    and not isinstance(right, bool)
                    and left >= -0.5
                    and right <= 390.5,
                    f"{item_location} must be contained in the 390 px viewport",
                )
        tables = result.get("tables")
        _require(isinstance(tables, list), f"{result_location}.tables must be an array")
        for position, table in enumerate(tables):
            _require(
                isinstance(table, dict) and table.get("boundedByScroller") is True,
                f"{result_location}.tables[{position}] must be bounded by its scroller",
            )
    return completed_at


def _validate_required_error_recovery(
    value: dict[str, Any],
    *,
    evidence_root: Path,
    live_driver_digest: str,
) -> datetime:
    location = REQUIRED_ERROR_RECOVERY_PATH
    _exact_fields(value, REQUIRED_ERROR_RECOVERY_FIELDS, location)
    _require(value["schema_version"] == 1, f"{location}.schema_version must equal 1")
    _, completed_at = _validate_run_times(value, location)
    _driver_digest(
        value["driver"],
        evidence_root=evidence_root,
        expected_relative_path=REQUIRED_ERROR_RECOVERY_DRIVER_PATH,
        location=f"{location}.driver",
    )
    _require(
        value["source_driver_sha256"] == live_driver_digest,
        f"{location}.source_driver_sha256 must match the preserved live browser driver",
    )
    sites = _validate_site_set(
        value["sites"],
        REQUIRED_RECOVERY_SITES,
        f"{location}.sites",
    )
    for site, result in sites.items():
        result_location = f"{location}.sites.{site}"
        for field in ("pass", "recovered", "linkPresent", "linkKeyboardFocusesTarget"):
            _require(result.get(field) is True, f"{result_location}.{field} must be true")
        _require(
            result.get("ariaInvalid") == "true",
            f"{result_location}.ariaInvalid must equal 'true'",
        )
        _require(
            result.get("errorRole") == "alert", f"{result_location}.errorRole must equal 'alert'"
        )
        _require(
            result.get("linkHref") == RECOVERY_TARGETS[site],
            f"{result_location}.linkHref must equal {RECOVERY_TARGETS[site]!r}",
        )
        _nonempty_string(result.get("errorText"), f"{result_location}.errorText")
        _require(
            result.get("consoleErrors") == [], f"{result_location}.consoleErrors must be empty"
        )
        _require(result.get("pageErrors") == [], f"{result_location}.pageErrors must be empty")
    return completed_at


def _validate_browser_summary(
    value: dict[str, Any],
    *,
    environment: dict[str, str],
    raw_completed_at: datetime,
    index_validated_at: datetime,
) -> None:
    location = BROWSER_SUMMARY_PATH
    _exact_fields(value, BROWSER_SUMMARY_FIELDS, location)
    _require(value["schema_version"] == 1, f"{location}.schema_version must equal 1")
    audited_at = _parse_timestamp(value["audited_at"], f"{location}.audited_at")
    _require(
        raw_completed_at <= audited_at,
        f"{location}.audited_at must be at or after all raw browser runs",
    )
    _require(
        audited_at == index_validated_at,
        f"{location}.audited_at must equal index.validated_at",
    )
    expected_environment = {
        "playwright": environment["playwright"],
        "chromium": environment["chromium"],
        "webkit": environment["webkit"],
    }
    _require(
        value["environment"] == expected_environment,
        f"{location}.environment must match corrected live browser results",
    )
    expected_coverage = {
        "released_pages_sites": 7,
        "chromium_desktop_passes": 7,
        "chromium_390px_passes": 7,
        "webkit_smoke_passes": 7,
        "explicit_error_recovery_passes": 7,
    }
    _require(
        value["coverage"] == expected_coverage,
        f"{location}.coverage must summarize all seven released scientific pages",
    )
    expected_responsive_layout = {
        "viewport_width_px": 390,
        "sites_with_document_width_exactly_matching_viewport": 7,
        "uncontained_visible_elements": 0,
    }
    _require(
        value["responsive_layout"] == expected_responsive_layout,
        f"{location}.responsive_layout must match corrected mobile containment evidence",
    )
    expected_privacy = {
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
    }
    _require(
        value["privacy"] == expected_privacy,
        f"{location}.privacy must match the validated zero-persistence and zero-egress results",
    )
    expected_accessibility = {
        "keyboard_focus_paths_checked": 7,
        "input_label_sets_checked": 7,
        "error_messages_exposed_to_assistive_technology": True,
        "explicit_error_link_focus_passes": 6,
        "integrated_error_surface": "aria-live polite status with successful recovery",
        "valid_input_recovers_after_error": True,
        "automated_only": True,
    }
    _require(
        value["accessibility_and_recovery"] == expected_accessibility,
        f"{location}.accessibility_and_recovery must match corrected browser evidence",
    )
    expected_sources = [
        LIVE_BROWSER_RESULTS_PATH,
        MOBILE_CONTAINMENT_PATH,
        REQUIRED_ERROR_RECOVERY_PATH,
    ]
    _require(
        value["source_files"] == expected_sources,
        f"{location}.source_files must identify the three corrected raw browser records",
    )


def validate_browser_evidence(
    *,
    evidence_root: Path = EVIDENCE_ROOT,
    validated_at: str,
) -> None:
    """Validate browser evidence semantics and its summary-to-source hash chain."""
    live = _load_evidence_json(evidence_root, LIVE_BROWSER_RESULTS_PATH)
    mobile = _load_evidence_json(evidence_root, MOBILE_CONTAINMENT_PATH)
    recovery = _load_evidence_json(evidence_root, REQUIRED_ERROR_RECOVERY_PATH)
    summary = _load_evidence_json(evidence_root, BROWSER_SUMMARY_PATH)

    environment, live_completed_at = _validate_live_browser_results(
        live,
        evidence_root=evidence_root,
    )
    live_driver_digest = environment.pop("live_driver_sha256")
    mobile_completed_at = _validate_mobile_containment(
        mobile,
        evidence_root=evidence_root,
        live_driver_digest=live_driver_digest,
    )
    recovery_completed_at = _validate_required_error_recovery(
        recovery,
        evidence_root=evidence_root,
        live_driver_digest=live_driver_digest,
    )
    _require(
        mobile["chromiumVersion"] == environment["chromium"],
        f"{MOBILE_CONTAINMENT_PATH}.chromiumVersion must match corrected live browser results",
    )
    _validate_browser_summary(
        summary,
        environment=environment,
        raw_completed_at=max(live_completed_at, mobile_completed_at, recovery_completed_at),
        index_validated_at=_parse_timestamp(validated_at, "index.validated_at"),
    )


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

    kinds_by_path = {
        entry["path"]: entry["kind"]
        for entry in files
        if isinstance(entry, dict)
        and isinstance(entry.get("path"), str)
        and isinstance(entry.get("kind"), str)
    }
    missing_final_records = sorted(REQUIRED_FINAL_RECORDS.keys() - kinds_by_path.keys())
    if missing_final_records:
        raise ValidationEvidenceError(
            f"evidence index is missing required final records: {missing_final_records}"
        )
    misclassified_final_records = sorted(
        path
        for path, expected_kind in REQUIRED_FINAL_RECORDS.items()
        if kinds_by_path[path] != expected_kind
    )
    if misclassified_final_records:
        raise ValidationEvidenceError(
            f"required final evidence records have incorrect kinds: {misclassified_final_records}"
        )

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

    validate_browser_evidence(
        evidence_root=evidence_root,
        validated_at=validated_at,
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
