from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

EVIDENCE_ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).with_name("live_browser_audit.py")
OUTPUT = EVIDENCE_ROOT / "browser" / "corrected-required-error-recovery.json"
STARTED_AT = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

spec = importlib.util.spec_from_file_location("cc_mig_11_original_audit", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load audit driver: {SOURCE}")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

cases = {
    "scientific-applet-template": ("#first-value", "4"),
    "compatibility-curve": ("#ci-lower", "1.2"),
    "wald-likelihood-support": ("#ci-lower", "1.2"),
    "critical-effect-size": ("#target-probability", "0.8"),
    "type-s-m-calibrator": ("#null-value", "0"),
    "precision-guardrail-planner": ("#target-true-effect", "0.2"),
}
sites = {site["slug"]: site for site in audit.SITES if site["slug"] in cases}
results = {}

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for slug, (selector, recovery) in cases.items():
        site = sites[slug]
        context = browser.new_context()
        page = context.new_page()
        console_errors = []
        page_errors = []
        page.on(
            "console",
            lambda message, errors=console_errors: (
                errors.append(message.text) if message.type == "error" else None
            ),
        )
        page.on(
            "pageerror",
            lambda error, errors=page_errors: errors.append(str(error)),
        )
        page.goto(site["url"], wait_until="domcontentloaded", timeout=audit.TIMEOUT)
        audit.wait_ready(page, site)
        page.locator(selector).fill("")
        page.locator(site["calculate"]).click()
        summary = page.locator("#error-summary")
        summary.wait_for(state="visible", timeout=audit.TIMEOUT)
        link = summary.locator(f'a[href="{selector}"]').first
        link_present = link.count() == 1 and link.is_visible()
        if link_present:
            link.focus()
            page.keyboard.press("Enter")
        focused = page.evaluate(
            "(selector) => document.activeElement === document.querySelector(selector)",
            selector,
        )
        record = {
            "errorText": summary.inner_text(),
            "errorRole": summary.get_attribute("role"),
            "errorAriaLive": summary.get_attribute("aria-live"),
            "linkPresent": link_present,
            "linkHref": link.get_attribute("href") if link_present else None,
            "linkKeyboardFocusesTarget": focused,
            "ariaInvalid": page.locator(selector).get_attribute("aria-invalid"),
            "consoleErrors": console_errors,
            "pageErrors": page_errors,
        }
        page.locator(selector).fill(recovery)
        page.locator(site["calculate"]).click()
        audit.wait_contains(
            page, site["success_selector"], site["success_text"], timeout=audit.TIMEOUT
        )
        record["recovered"] = True
        record["pass"] = (
            record["errorRole"] == "alert"
            and record["linkPresent"]
            and record["linkKeyboardFocusesTarget"]
            and record["ariaInvalid"] == "true"
            and not record["consoleErrors"]
            and not record["pageErrors"]
        )
        results[slug] = record
        print(json.dumps({"slug": slug, "pass": record["pass"]}), flush=True)
        context.close()
    browser.close()

OUTPUT.write_text(
    json.dumps(
        {
            "schema_version": 1,
            "started_at": STARTED_AT,
            "completed_at": (
                datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            ),
            "driver": {
                "path": ("validation-evidence/drivers/required_error_recovery_audit.py"),
                "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            },
            "source_driver_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "sites": results,
        },
        indent=2,
        sort_keys=True,
    ),
    encoding="utf-8",
)
print(OUTPUT)
