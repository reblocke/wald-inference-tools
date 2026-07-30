from __future__ import annotations

import hashlib
import json
import os
import re
import traceback
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from playwright.sync_api import Browser, BrowserContext, Page, TimeoutError, sync_playwright

EVIDENCE_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = Path(
    os.environ.get(
        "CC_MIG_11_BROWSER_ARTIFACT_DIR",
        "/private/tmp/cc-mig-11-final-browser-artifacts",
    )
)
RESULT_PATH = EVIDENCE_ROOT / "browser" / "corrected-live-browser-results.json"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

TIMEOUT = 180_000
TELEMETRY_RE = re.compile(
    r"(google-analytics|googletagmanager|segment|mixpanel|amplitude|sentry|"
    r"newrelic|fullstory|hotjar|plausible|matomo|telemetry|analytics)",
    re.IGNORECASE,
)


SITES: list[dict[str, Any]] = [
    {
        "slug": "scientific-applet-template",
        "url": "https://reblocke.github.io/scientific-applet-template/",
        "kind": "app",
        "ready_selector": "#runtime-status",
        "ready_text": "Runtime ready.",
        "success_selector": "#runtime-status",
        "success_text": "Calculation complete.",
        "calculate": "#calculate",
        "sentinel_selector": "#first-value",
        "sentinel": "12345.67891",
        "invalid_selector": "#first-value",
        "invalid": "",
        "recover": "4",
        "error_selector": "#error-summary",
        "result_selectors": ["#result-summary", "#result-table", "#caption"],
        "downloads": ["#export-csv", "#export-figure", "#export-dashboard"],
        "copies": ["#copy-caption"],
    },
    {
        "slug": "compatibility-curve",
        "url": "https://reblocke.github.io/compatibility-curve/",
        "kind": "app",
        "ready_selector": "#runtime-status",
        "ready_text": "Runtime ready.",
        "success_selector": "#runtime-status",
        "success_text": "Compatibility curve updated.",
        "calculate": "#calculate",
        "sentinel_selector": "#ci-lower",
        "sentinel": "1.234567891",
        "invalid_selector": "#ci-lower",
        "invalid": "-1",
        "recover": "1.2",
        "error_selector": "#error-summary",
        "result_selectors": [
            "#result-summary",
            "#reconstruction-summary",
            "#threshold-table",
            "#figure-caption",
        ],
        "downloads": ["#export-csv", "#export-manuscript", "#export-dashboard"],
        "copies": ["#copy-caption"],
    },
    {
        "slug": "wald-likelihood-support",
        "url": "https://reblocke.github.io/wald-likelihood-support/",
        "kind": "app",
        "ready_selector": "#runtime-status",
        "ready_text": "Runtime ready.",
        "success_selector": "#runtime-status",
        "success_text": "Likelihood-support curve updated.",
        "calculate": "#calculate",
        "sentinel_selector": "#ci-lower",
        "sentinel": "1.234567892",
        "invalid_selector": "#ci-lower",
        "invalid": "-1",
        "recover": "1.2",
        "error_selector": "#error-summary",
        "result_selectors": [
            "#result-summary",
            "#reconstruction-summary",
            "#support-interval-summary",
            "#reference-table",
            "#figure-caption",
        ],
        "downloads": ["#export-csv", "#export-manuscript", "#export-dashboard"],
        "copies": ["#copy-caption"],
    },
    {
        "slug": "critical-effect-size",
        "url": "https://reblocke.github.io/critical-effect-size/",
        "kind": "app",
        "ready_selector": "#runtime-status",
        "ready_text": "Runtime ready.",
        "success_selector": "#runtime-status",
        "success_text": "Calculation complete.",
        "calculate": "#calculate",
        "sentinel_selector": "#meaningful-effect",
        "sentinel": "1.234567893",
        "invalid_selector": "#alpha",
        "invalid": "1",
        "recover": "0.05",
        "error_selector": "#error-summary",
        "result_selectors": [
            "#result-summary",
            "#current-critical-summary",
            "#reference-table",
            "#figure-caption",
        ],
        "downloads": ["#export-csv", "#export-figure", "#export-dashboard"],
        "copies": ["#copy-caption"],
    },
    {
        "slug": "type-s-m-calibrator",
        "url": "https://reblocke.github.io/type-s-m-calibrator/",
        "kind": "app",
        "ready_selector": "#runtime-status",
        "ready_text": "Runtime ready.",
        "success_selector": "#runtime-status",
        "success_text": "Calculation complete.",
        "calculate": "#calculate",
        "sentinel_selector": "#observed-estimate",
        "sentinel": "0.4234567891",
        "invalid_selector": "#standard-error",
        "invalid": "0",
        "recover": "0.2",
        "error_selector": "#error-summary",
        "result_selectors": [
            "#result-summary",
            "#scenario-table",
            "#figure-caption",
            "#reviewer-text",
        ],
        "downloads": ["#export-csv", "#export-figure", "#export-dashboard"],
        "copies": ["#copy-caption", "#copy-reviewer"],
    },
    {
        "slug": "precision-guardrail-planner",
        "url": "https://reblocke.github.io/precision-guardrail-planner/",
        "kind": "app",
        "ready_selector": "#runtime-status",
        "ready_text": "Runtime ready.",
        "success_selector": "#runtime-status",
        "success_text": "Calculation complete.",
        "calculate": "#calculate",
        "sentinel_selector": "#target-true-effect",
        "sentinel": "0.2345678914",
        "invalid_selector": "#alpha",
        "invalid": "0",
        "recover": "0.05",
        "error_selector": "#error-summary",
        "result_selectors": [
            "#result-summary",
            "#joint-status",
            "#target-table",
            "#figure-caption",
            "#reviewer-text",
        ],
        "downloads": [
            "#export-scenario-csv",
            "#export-sensitivity-csv",
            "#export-figure",
            "#export-dashboard",
        ],
        "copies": ["#copy-caption", "#copy-reviewer"],
        "prepare_exports": "precision_sensitivity",
    },
    {
        "slug": "conf_curve_likelihood",
        "url": "https://reblocke.github.io/conf_curve_likelihood/",
        "kind": "integrated",
        "ready_selector": "#status-card",
        "ready_text": "Curves updated",
        "success_selector": "#status-card",
        "success_text": "Curves updated",
        "calculate": None,
        "sentinel_selector": "#thresholds",
        "sentinel": "1.2345678915",
        "invalid_selector": "#ci-lower",
        "invalid": "0",
        "recover": "1.2",
        "error_selector": "#status-card",
        "result_selectors": [
            "#summary-grid",
            "#comparison-takeaway",
            "#commentary-text",
            "#figure-caption",
        ],
        "downloads": ["#export-csv", "#export-png", "#export-manuscript-png"],
        "copies": ["#copy-caption", "#copy-reviewer-text"],
        "prepare_exports": "integrated_design",
    },
    {
        "slug": "wald-inference-tools",
        "url": "https://reblocke.github.io/wald-inference-tools/",
        "kind": "catalog",
        "ready_selector": "#catalog-status",
        "ready_text": "6 tools shown.",
        "result_selectors": [".tool-grid", "#comparison-table", "#catalog-status"],
    },
]


def wait_contains(page: Page, selector: str, text: str, timeout: int = TIMEOUT) -> None:
    page.wait_for_function(
        """([selector, expected]) => {
          const node = document.querySelector(selector);
          return Boolean(node && (node.textContent || "").includes(expected));
        }""",
        arg=[selector, text],
        timeout=timeout,
    )


def wait_ready(page: Page, site: dict[str, Any]) -> None:
    if site["kind"] == "app":
        page.locator(site["ready_selector"]).wait_for(state="attached", timeout=TIMEOUT)
        page.wait_for_function(
            (
                """selector => document.querySelector(selector)"""
                """?.getAttribute("data-state") === "ready" """
            ),
            arg=site["ready_selector"],
            timeout=TIMEOUT,
        )
    else:
        wait_contains(page, site["ready_selector"], site["ready_text"])


def attach_network(page: Page) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    requests: list[dict[str, Any]] = []
    websockets: list[dict[str, Any]] = []

    def on_request(request: Any) -> None:
        try:
            post_data = request.post_data
        except Exception:
            post_data = None
        requests.append(
            {
                "method": request.method,
                "url": request.url,
                "resource_type": request.resource_type,
                "post_data": post_data,
            }
        )

    def on_websocket(ws: Any) -> None:
        record: dict[str, Any] = {"url": ws.url, "sent": [], "received": []}
        websockets.append(record)
        ws.on("framesent", lambda payload: record["sent"].append(str(payload)))
        ws.on("framereceived", lambda payload: record["received"].append(str(payload)))

    page.on("request", on_request)
    page.on("websocket", on_websocket)
    return requests, websockets


def storage_state(page: Page, context: BrowserContext) -> dict[str, Any]:
    state = page.evaluate(
        """async () => {
          const indexed = indexedDB.databases
            ? await indexedDB.databases().then(rows => rows.map(row => row.name || ""))
            : "unsupported";
          const registrations = "serviceWorker" in navigator
            ? await navigator.serviceWorker.getRegistrations()
                .then(rows => rows.map(row => row.scope))
            : [];
          const cacheKeys = "caches" in window ? await caches.keys() : [];
          return {
            localStorage: Object.keys(localStorage),
            sessionStorage: Object.keys(sessionStorage),
            documentCookie: document.cookie,
            indexedDB: indexed,
            serviceWorkers: registrations,
            serviceWorkerController: Boolean(navigator.serviceWorker?.controller),
            cacheStorage: cacheKeys,
          };
        }"""
    )
    state["contextCookies"] = [
        {
            "name": row["name"],
            "domain": row["domain"],
            "path": row["path"],
            "sameSite": row["sameSite"],
        }
        for row in context.cookies()
    ]
    return state


def accessibility_inventory(page: Page, result_selectors: list[str]) -> dict[str, Any]:
    controls = page.evaluate(
        """() => {
          const seen = new Set();
          const roots = document.querySelectorAll(
            ".controls input, .controls select, .controls textarea, .controls button, " +
            ".sidebar input, .sidebar select, .sidebar textarea, .sidebar button, " +
            "main form input, main form select, main form textarea, main form button, " +
            "main > button, main fieldset input"
          );
          const visible = (node) => {
            const style = getComputedStyle(node);
            const rect = node.getBoundingClientRect();
            return style.display !== "none" && style.visibility !== "hidden" &&
              rect.width > 0 && rect.height > 0 && node.type !== "hidden";
          };
          return Array.from(roots).filter(node => {
            if (seen.has(node) || !visible(node)) return false;
            seen.add(node);
            return true;
          }).map(node => {
            const labels = Array.from(node.labels || [])
              .map(label => (label.textContent || "").trim()).filter(Boolean);
            const labelledBy = node.getAttribute("aria-labelledby");
            const labelledByText = labelledBy
              ? labelledBy.split(/\\s+/).map(id => document.getElementById(id)?.textContent?.trim())
                  .filter(Boolean)
              : [];
            const accessibleName = (
              node.getAttribute("aria-label") ||
              labels.join(" ") ||
              labelledByText.join(" ") ||
              node.textContent ||
              node.getAttribute("title") ||
              ""
            ).trim();
            return {
              tag: node.tagName.toLowerCase(),
              type: node.getAttribute("type"),
              id: node.id,
              name: node.getAttribute("name"),
              accessibleName,
              disabled: Boolean(node.disabled),
              ariaInvalid: node.getAttribute("aria-invalid"),
            };
          });
        }"""
    )
    announcements = page.evaluate(
        """() => Array.from(document.querySelectorAll(
          '[role="alert"], [role="status"], [aria-live], #error-summary, #status-card'
        )).map(node => ({
          id: node.id,
          role: node.getAttribute("role"),
          ariaLive: node.getAttribute("aria-live"),
          ariaAtomic: node.getAttribute("aria-atomic"),
          text: (node.textContent || "").trim().slice(0, 500),
          hidden: Boolean(node.hidden),
        }))"""
    )
    missing_alt = page.evaluate(
        """() => Array.from(document.querySelectorAll("img[src]:not([alt])"))
          .filter(node => {
            const rect = node.getBoundingClientRect();
            return rect.width > 0 && rect.height > 0;
          }).map(node => node.getAttribute("src"))"""
    )
    text_alternatives: list[dict[str, Any]] = []
    for selector in result_selectors:
        locator = page.locator(selector).first
        text_alternatives.append(
            {
                "selector": selector,
                "count": page.locator(selector).count(),
                "visible": locator.is_visible() if locator.count() else False,
                "text_length": len(locator.inner_text())
                if locator.count() and locator.is_visible()
                else 0,
            }
        )
    return {
        "controls": controls,
        "unlabelled_enabled_controls": [
            row for row in controls if not row["disabled"] and not row["accessibleName"]
        ],
        "announcement_regions": announcements,
        "visible_images_missing_alt": missing_alt,
        "text_alternatives": text_alternatives,
    }


def request_summary(
    requests: list[dict[str, Any]],
    websockets: list[dict[str, Any]],
    site_url: str,
    sentinel: str | None,
    input_start: int,
) -> dict[str, Any]:
    origin = urlsplit(site_url)
    hosts = Counter(urlsplit(row["url"]).netloc for row in requests)
    methods = Counter(row["method"] for row in requests)
    resource_types = Counter(row["resource_type"] for row in requests)
    external = [row for row in requests if urlsplit(row["url"]).netloc != origin.netloc]
    after_input = requests[input_start:]
    serialized = json.dumps(
        {"requests": requests, "websockets": websockets},
        sort_keys=True,
        ensure_ascii=False,
    )
    serialized_after_input = json.dumps(after_input, sort_keys=True, ensure_ascii=False)
    telemetry = sorted({row["url"] for row in requests if TELEMETRY_RE.search(row["url"])})
    return {
        "request_count": len(requests),
        "after_input_request_count": len(after_input),
        "hosts": dict(sorted(hosts.items())),
        "methods": dict(sorted(methods.items())),
        "resource_types": dict(sorted(resource_types.items())),
        "external_requests": external,
        "websockets": websockets,
        "telemetry_matches": telemetry,
        "sentinel_in_any_request_or_websocket": bool(sentinel and sentinel in serialized),
        "sentinel_in_post_input_request": bool(sentinel and sentinel in serialized_after_input),
        "non_get_requests": [row for row in requests if row["method"] != "GET"],
    }


def fill_by_keyboard(page: Page, selector: str, value: str) -> None:
    page.locator(selector).focus()
    page.keyboard.press("Meta+A")
    page.keyboard.type(value)


def keyboard_to_target(page: Page, start: str, target: str, limit: int = 100) -> dict[str, Any]:
    page.locator(start).focus()
    path: list[str] = []
    reached = False
    for _ in range(limit):
        active = page.evaluate(
            """() => {
              const node = document.activeElement;
              return node ? {
                id: node.id,
                tag: node.tagName.toLowerCase(),
                type: node.getAttribute("type"),
                text: (node.textContent || "").trim().slice(0, 80),
              } : null;
            }"""
        )
        path.append(json.dumps(active, sort_keys=True))
        if active and f"#{active['id']}" == target:
            reached = True
            break
        page.keyboard.press("Tab")
    if reached:
        page.keyboard.press("Enter")
    return {"reached": reached, "focus_path": path}


def prepare_exports(page: Page, site: dict[str, Any]) -> None:
    if site.get("prepare_exports") == "precision_sensitivity":
        details = page.get_by_text("Sensitivity across assumed true effects", exact=True)
        if details.count() and not page.locator("#sensitivity-enabled").is_visible():
            details.click()
        page.locator("#sensitivity-enabled").check()
        page.locator("#sensitivity-min").fill("0")
        page.locator("#sensitivity-max").fill("0.4")
        page.locator("#sensitivity-points").fill("3")
        page.locator(site["calculate"]).click()
        wait_contains(page, site["success_selector"], site["success_text"])
    elif site.get("prepare_exports") == "integrated_design":
        if not page.locator("#design-enabled").is_checked():
            page.locator("#design-enabled").check()
        wait_contains(page, site["success_selector"], site["success_text"])


def test_downloads(page: Page, site: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for selector in site.get("downloads", []):
        locator = page.locator(selector)
        record: dict[str, Any] = {
            "selector": selector,
            "present": bool(locator.count()),
            "enabled": False,
        }
        if not locator.count():
            results.append(record)
            continue
        record["enabled"] = locator.is_enabled()
        if not locator.is_enabled():
            results.append(record)
            continue
        try:
            with page.expect_download(timeout=TIMEOUT) as download_info:
                locator.click()
            download = download_info.value
            target = (
                ARTIFACT_DIR
                / f"{site['slug']}-{selector.lstrip('#')}-{download.suggested_filename}"
            )
            download.save_as(target)
            content = target.read_bytes()
            record.update(
                {
                    "filename": download.suggested_filename,
                    "path": str(target),
                    "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "signature_hex": content[:8].hex(),
                    "png_signature": content.startswith(b"\x89PNG\r\n\x1a\n"),
                }
            )
        except Exception as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"
        results.append(record)
    return results


def test_copies(page: Page, site: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for selector in site.get("copies", []):
        locator = page.locator(selector)
        record: dict[str, Any] = {
            "selector": selector,
            "present": bool(locator.count()),
            "visible": bool(locator.count() and locator.is_visible()),
            "enabled": bool(locator.count() and locator.is_enabled()),
        }
        if not record["present"] or not record["visible"] or not record["enabled"]:
            results.append(record)
            continue
        try:
            locator.click()
            page.wait_for_timeout(250)
            text = page.evaluate("navigator.clipboard.readText()")
            record.update(
                {
                    "clipboard_length": len(text),
                    "clipboard_sha256": hashlib.sha256(text.encode()).hexdigest(),
                    "nonempty": bool(text.strip()),
                }
            )
        except Exception as exc:
            record["error"] = f"{type(exc).__name__}: {exc}"
        results.append(record)
    return results


def test_error_recovery(page: Page, site: dict[str, Any]) -> dict[str, Any]:
    invalid_selector = site["invalid_selector"]
    page.locator(invalid_selector).fill(site["invalid"])
    if site["calculate"]:
        page.locator(site["calculate"]).click()
    else:
        page.locator(invalid_selector).blur()
        page.wait_for_timeout(250)
    error_locator = page.locator(site["error_selector"])
    try:
        if site["kind"] == "integrated":
            wait_contains(page, site["error_selector"], "could not be completed")
        else:
            page.wait_for_function(
                """selector => {
                  const node = document.querySelector(selector);
                  return Boolean(node && !node.hidden && (node.textContent || "").trim());
                }""",
                arg=site["error_selector"],
                timeout=TIMEOUT,
            )
    except TimeoutError:
        pass
    error_text = error_locator.inner_text() if error_locator.count() else ""
    invalid_aria = page.locator(invalid_selector).get_attribute("aria-invalid")
    error_attrs = (
        error_locator.evaluate(
            """node => ({
              role: node.getAttribute("role"),
              ariaLive: node.getAttribute("aria-live"),
              ariaAtomic: node.getAttribute("aria-atomic"),
              dataState: node.getAttribute("data-state"),
            })"""
        )
        if error_locator.count()
        else {}
    )
    link = page.locator(f"{site['error_selector']} a").first
    link_record: dict[str, Any] = {
        "present": bool(link.count()),
        "href": link.get_attribute("href") if link.count() else None,
        "focuses_control": None,
    }
    if link.count():
        link.focus()
        page.keyboard.press("Enter")
        link_record["focuses_control"] = page.evaluate(
            "selector => document.activeElement === document.querySelector(selector)",
            invalid_selector,
        )

    page.locator(invalid_selector).fill(site["recover"])
    if site["calculate"]:
        page.locator(site["calculate"]).click()
    else:
        page.locator(invalid_selector).blur()
        page.wait_for_timeout(250)
    wait_contains(page, site["success_selector"], site["success_text"])
    return {
        "error_text": error_text[:1200],
        "error_attributes": error_attrs,
        "safe_no_traceback_or_local_path": "Traceback" not in error_text
        and "/Users/" not in error_text,
        "invalid_control_aria_invalid": invalid_aria,
        "error_link": link_record,
        "recovered": True,
        "recovery_status": page.locator(site["success_selector"]).inner_text()[:500],
    }


def related_links(page: Page) -> list[str]:
    return sorted(
        set(
            page.locator("a").evaluate_all(
                """links => links.map(link => link.href).filter(href =>
                  href.includes("reblocke.github.io") ||
                  href.includes("github.com/reblocke")
                )"""
            )
        )
    )


def run_catalog_desktop(browser: Browser, site: dict[str, Any]) -> dict[str, Any]:
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    requests, websockets = attach_network(page)
    console_errors: list[str] = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.goto(site["url"], wait_until="domcontentloaded", timeout=TIMEOUT)
    wait_ready(page, site)
    result = {
        "title": page.title(),
        "url": page.url,
        "tool_card_count": page.locator(".tool-card").count(),
        "comparison_row_count": page.locator("#comparison-body tr").count(),
        "labels_and_text": accessibility_inventory(page, site["result_selectors"]),
        "storage": storage_state(page, context),
        "network": request_summary(requests, websockets, site["url"], None, len(requests)),
        "related_links": related_links(page),
        "script_sources": page.locator("script[src]").evaluate_all(
            "nodes => nodes.map(node => node.src)"
        ),
        "console_errors": console_errors,
    }
    context.close()
    return result


def run_app_desktop(browser: Browser, site: dict[str, Any]) -> dict[str, Any]:
    context = browser.new_context(accept_downloads=True)
    parsed_site = urlsplit(site["url"])
    context.grant_permissions(
        ["clipboard-read", "clipboard-write"],
        origin=f"{parsed_site.scheme}://{parsed_site.netloc}",
    )
    page = context.new_page()
    requests, websockets = attach_network(page)
    console_errors: list[str] = []
    page_errors: list[str] = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    page.goto(site["url"], wait_until="domcontentloaded", timeout=TIMEOUT)
    wait_ready(page, site)
    initial_url = page.url
    input_start = len(requests)
    page.locator(site["sentinel_selector"]).fill(site["sentinel"])
    if site["calculate"]:
        page.locator(site["calculate"]).click()
    else:
        page.locator(site["sentinel_selector"]).blur()
        page.wait_for_timeout(250)
    wait_contains(page, site["success_selector"], site["success_text"])
    labels_before_error = accessibility_inventory(page, site["result_selectors"])
    error_recovery = test_error_recovery(page, site)
    prepare_exports(page, site)
    downloads = test_downloads(page, site)
    copies = test_copies(page, site)
    result = {
        "title": page.title(),
        "initial_url": initial_url,
        "final_url": page.url,
        "url_unchanged": page.url == initial_url,
        "success_status": page.locator(site["success_selector"]).inner_text()[:500],
        "labels_and_text": labels_before_error,
        "error_and_recovery": error_recovery,
        "downloads": downloads,
        "copies": copies,
        "storage": storage_state(page, context),
        "network": request_summary(
            requests, websockets, site["url"], site["sentinel"], input_start
        ),
        "related_links": related_links(page),
        "script_sources": page.locator("script[src]").evaluate_all(
            "nodes => nodes.map(node => node.src)"
        ),
        "console_errors": console_errors,
        "page_errors": page_errors,
    }
    context.close()
    return result


def run_mobile(browser: Browser, site: dict[str, Any]) -> dict[str, Any]:
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        screen={"width": 390, "height": 844},
        accept_downloads=False,
    )
    page = context.new_page()
    requests, websockets = attach_network(page)
    page.goto(site["url"], wait_until="domcontentloaded", timeout=TIMEOUT)
    wait_ready(page, site)
    initial_url = page.url
    input_start = len(requests)
    if site["kind"] == "catalog":
        page.locator(".skip-link").focus()
        page.keyboard.press("Enter")
        skip_target = page.evaluate("document.activeElement && document.activeElement.id")
        page.get_by_label("Observed data").focus()
        page.keyboard.press("ArrowRight")
        keyboard = {
            "skip_target": skip_target,
            "design_checked": page.get_by_label("Design").is_checked(),
            "visible_cards": page.locator(".tool-card:visible").count(),
        }
        sentinel = None
    elif site["kind"] == "integrated":
        fill_by_keyboard(page, site["sentinel_selector"], site["sentinel"])
        page.keyboard.press("Tab")
        wait_contains(page, site["success_selector"], site["success_text"])
        keyboard = {
            "sentinel_field": site["sentinel_selector"],
            "active_after_tab": page.evaluate(
                "document.activeElement && "
                "(document.activeElement.id || document.activeElement.tagName)"
            ),
            "automatic_workflow_completed": True,
        }
        sentinel = site["sentinel"]
    else:
        fill_by_keyboard(page, site["sentinel_selector"], site["sentinel"])
        keyboard = keyboard_to_target(page, site["sentinel_selector"], site["calculate"])
        if keyboard["reached"]:
            wait_contains(page, site["success_selector"], site["success_text"])
        sentinel = site["sentinel"]
    page.wait_for_timeout(500)
    metrics = page.evaluate(
        """() => ({
          innerWidth: window.innerWidth,
          documentClientWidth: document.documentElement.clientWidth,
          documentScrollWidth: document.documentElement.scrollWidth,
          bodyScrollWidth: document.body.scrollWidth,
        })"""
    )
    result = {
        "url_unchanged": page.url == initial_url,
        "keyboard": keyboard,
        "viewport": metrics,
        "no_horizontal_overflow": (
            metrics["documentScrollWidth"] <= metrics["documentClientWidth"]
            and metrics["bodyScrollWidth"] <= metrics["documentClientWidth"]
        ),
        "controls_visible": (
            page.locator(".controls").is_visible() if page.locator(".controls").count() else True
        ),
        "results_visible": (
            page.locator(".results").is_visible() if page.locator(".results").count() else True
        ),
        "storage": storage_state(page, context),
        "network": request_summary(requests, websockets, site["url"], sentinel, input_start),
    }
    context.close()
    return result


def run_webkit_smoke(browser: Browser, site: dict[str, Any]) -> dict[str, Any]:
    context = browser.new_context()
    page = context.new_page()
    console_errors: list[str] = []
    page_errors: list[str] = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    page.goto(site["url"], wait_until="domcontentloaded", timeout=TIMEOUT)
    wait_ready(page, site)
    if site["kind"] == "app":
        page.locator(site["calculate"]).click()
        wait_contains(page, site["success_selector"], site["success_text"])
    elif site["kind"] == "integrated":
        wait_contains(page, site["success_selector"], site["success_text"])
    result = {
        "title": page.title(),
        "url": page.url,
        "smoke_status": page.locator(site["ready_selector"]).inner_text()[:500],
        "console_errors": console_errors,
        "page_errors": page_errors,
        "storage": storage_state(page, context),
    }
    context.close()
    return result


def safe_run(label: str, function: Any, *args: Any) -> dict[str, Any]:
    try:
        return {"ok": True, "result": function(*args)}
    except Exception as exc:
        slug = args[-1]["slug"] if args and isinstance(args[-1], dict) else label
        screenshot = ARTIFACT_DIR / f"{slug}-{label}-failure.png"
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
            "screenshot_attempted": str(screenshot),
        }


def main() -> None:
    results: dict[str, Any] = {
        "schema_version": 1,
        "started_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "driver": {
            "path": "validation-evidence/drivers/live_browser_audit.py",
            "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "artifact_directory": str(ARTIFACT_DIR),
        "sites": {},
    }
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        webkit = playwright.webkit.launch()
        results["environment"] = {
            "playwright": "1.61.0",
            "chromium_version": chromium.version,
            "webkit_version": webkit.version,
        }
        for site in SITES:
            if site["kind"] == "catalog":
                desktop = safe_run("chromium_desktop", run_catalog_desktop, chromium, site)
            else:
                desktop = safe_run("chromium_desktop", run_app_desktop, chromium, site)
            mobile = safe_run("chromium_mobile_390", run_mobile, chromium, site)
            webkit_result = safe_run("webkit_smoke", run_webkit_smoke, webkit, site)
            results["sites"][site["slug"]] = {
                "url": site["url"],
                "chromium_desktop": desktop,
                "chromium_mobile_390": mobile,
                "webkit_smoke": webkit_result,
            }
            RESULT_PATH.write_text(
                json.dumps(results, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            print(
                json.dumps(
                    {
                        "slug": site["slug"],
                        "desktop": desktop["ok"],
                        "mobile": mobile["ok"],
                        "webkit": webkit_result["ok"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        chromium.close()
        webkit.close()
    results["completed_at"] = (
        datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    RESULT_PATH.write_text(
        json.dumps(results, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(str(RESULT_PATH))


if __name__ == "__main__":
    main()
