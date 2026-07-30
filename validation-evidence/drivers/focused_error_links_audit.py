from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

SITES = [
    (
        "scientific-applet-template",
        "https://reblocke.github.io/scientific-applet-template/",
        "#first-value",
    ),
    ("compatibility-curve", "https://reblocke.github.io/compatibility-curve/", "#ci-lower"),
    ("wald-likelihood-support", "https://reblocke.github.io/wald-likelihood-support/", "#ci-lower"),
    (
        "critical-effect-size",
        "https://reblocke.github.io/critical-effect-size/",
        "#target-probability",
    ),
    ("type-s-m-calibrator", "https://reblocke.github.io/type-s-m-calibrator/", "#null-value"),
    (
        "precision-guardrail-planner",
        "https://reblocke.github.io/precision-guardrail-planner/",
        "#target-true-effect",
    ),
]

results = {}
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for slug, url, selector in SITES:
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=180_000)
        page.wait_for_function(
            """() => document.querySelector("#runtime-status")?.dataset.state === "ready" """,
            timeout=180_000,
        )
        page.locator(selector).fill("")
        page.locator("#calculate").click()
        page.locator("#error-summary").wait_for(state="visible", timeout=30_000)
        link = page.locator("#error-summary a").first
        record = {
            "error_role": page.locator("#error-summary").get_attribute("role"),
            "error_text": page.locator("#error-summary").inner_text(),
            "link_present": bool(link.count()),
            "link_href": link.get_attribute("href") if link.count() else None,
            "aria_invalid": page.locator(selector).get_attribute("aria-invalid"),
            "link_focuses_target": None,
        }
        if link.count():
            link.focus()
            page.keyboard.press("Enter")
            record["link_focuses_target"] = page.evaluate(
                "selector => document.activeElement === document.querySelector(selector)",
                selector,
            )
        results[slug] = record
        context.close()
    browser.close()

Path("/private/tmp/cc-mig-11-ef-error-links.json").write_text(
    json.dumps(results, indent=2, sort_keys=True),
    encoding="utf-8",
)
print("/private/tmp/cc-mig-11-ef-error-links.json")
