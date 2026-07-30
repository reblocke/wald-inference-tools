from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

EVIDENCE_ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).with_name("live_browser_audit.py")
OUTPUT = EVIDENCE_ROOT / "browser" / "corrected-mobile-containment.json"
ARTIFACTS = Path(
    os.environ.get(
        "CC_MIG_11_BROWSER_ARTIFACT_DIR",
        "/private/tmp/cc-mig-11-final-browser-artifacts",
    )
)
ARTIFACTS.mkdir(parents=True, exist_ok=True)
STARTED_AT = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

spec = importlib.util.spec_from_file_location("cc_mig_11_original_audit", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load audit driver: {SOURCE}")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

ready_slugs = {
    "scientific-applet-template",
    "compatibility-curve",
    "wald-likelihood-support",
    "critical-effect-size",
    "type-s-m-calibrator",
    "precision-guardrail-planner",
    "conf_curve_likelihood",
}
sites = [site for site in audit.SITES if site["slug"] in ready_slugs]


def geometry(page):
    return page.evaluate(
        """() => {
          const visible = node => {
            const style = getComputedStyle(node);
            const rect = node.getBoundingClientRect();
            return style.display !== "none" && style.visibility !== "hidden" &&
              rect.width > 0 && rect.height > 0;
          };
          const describe = node => {
            const rect = node.getBoundingClientRect();
            const style = getComputedStyle(node);
            const plot = node.classList.contains("js-plotly-plot") ? node : null;
            return {
              tag: node.tagName.toLowerCase(),
              id: node.id,
              className: typeof node.className === "string"
                ? node.className
                : (node.className && node.className.baseVal) || "",
              left: Math.round(rect.left * 100) / 100,
              right: Math.round(rect.right * 100) / 100,
              width: Math.round(rect.width * 100) / 100,
              clientWidth: node.clientWidth,
              scrollWidth: node.scrollWidth,
              minWidth: style.minWidth,
              overflowX: style.overflowX,
              plotlyFullLayoutWidth: plot?._fullLayout?.width || null,
              plotlyFullLayoutHeight: plot?._fullLayout?.height || null,
            };
          };
          const plots = Array.from(document.querySelectorAll(".js-plotly-plot"))
            .filter(visible).map(describe);
          const plotSvgs = Array.from(
            document.querySelectorAll(".js-plotly-plot svg.main-svg")
          ).filter(visible).map(describe);
          const viewportWidth = document.documentElement.clientWidth;
          const boundedScrollAncestor = node => {
            let parent = node.parentElement;
            while (parent && parent !== document.body) {
              const style = getComputedStyle(parent);
              if (["auto", "scroll"].includes(style.overflowX)) {
                const rect = parent.getBoundingClientRect();
                return {
                  node: describe(parent),
                  contained: rect.left >= -0.5 && rect.right <= viewportWidth + 0.5,
                };
              }
              parent = parent.parentElement;
            }
            return null;
          };
          const tables = Array.from(document.querySelectorAll("table")).filter(visible)
            .map(node => {
              const scroll = boundedScrollAncestor(node);
              return {
                table: describe(node),
                scrollAncestor: scroll?.node || null,
                boundedByScroller: Boolean(scroll?.contained),
              };
            });
          const allVisible = Array.from(document.querySelectorAll("body *")).filter(visible);
          const rawOffenders = allVisible.filter(node => {
            const rect = node.getBoundingClientRect();
            return rect.right > viewportWidth + 0.5 || rect.left < -0.5;
          });
          const uncontainedOffenders = rawOffenders.filter(node => {
            if (node.id === "js-plotly-tester" || node.closest("#js-plotly-tester")) return false;
            if (node.classList.contains("js-reference-point")) return false;
            if (node.closest(".js-plotly-plot")) return false;
            const scroll = boundedScrollAncestor(node);
            return !scroll?.contained;
          }).slice(0, 40).map(describe);
          return {
            innerWidth: window.innerWidth,
            documentClientWidth: viewportWidth,
            documentScrollWidth: document.documentElement.scrollWidth,
            bodyScrollWidth: document.body.scrollWidth,
            plots,
            plotSvgs,
            tables,
            rawOffenderCount: rawOffenders.length,
            uncontainedOffenders,
          };
        }"""
    )


results = {}
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    browser_version = browser.version
    for site in sites:
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            screen={"width": 390, "height": 844},
        )
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
        audit.fill_by_keyboard(page, site["sentinel_selector"], site["sentinel"])
        if site["kind"] == "integrated":
            page.keyboard.press("Tab")
            keyboard = {
                "sentinelField": site["sentinel_selector"],
                "automaticWorkflowCompleted": True,
            }
        else:
            keyboard = audit.keyboard_to_target(page, site["sentinel_selector"], site["calculate"])
            if not keyboard["reached"]:
                raise AssertionError(f"{site['slug']}: keyboard did not reach calculate")
        audit.wait_contains(
            page, site["success_selector"], site["success_text"], timeout=audit.TIMEOUT
        )
        page.locator(".js-plotly-plot").first.wait_for(state="visible", timeout=audit.TIMEOUT)
        page.locator(".js-plotly-plot svg.main-svg").first.wait_for(
            state="visible", timeout=audit.TIMEOUT
        )
        page.wait_for_timeout(750)
        measured = geometry(page)
        measured["keyboard"] = keyboard
        measured["consoleErrors"] = console_errors
        measured["pageErrors"] = page_errors
        measured["pass"] = (
            measured["documentScrollWidth"] <= measured["documentClientWidth"]
            and measured["bodyScrollWidth"] <= measured["documentClientWidth"]
            and len(measured["plots"]) > 0
            and all(
                row["left"] >= -0.5 and row["right"] <= measured["documentClientWidth"] + 0.5
                for row in measured["plots"]
            )
            and all(
                row["left"] >= -0.5 and row["right"] <= measured["documentClientWidth"] + 0.5
                for row in measured["plotSvgs"]
            )
            and len(measured["uncontainedOffenders"]) == 0
            and not console_errors
            and not page_errors
        )
        screenshot = ARTIFACTS / f"{site['slug']}-corrected-mobile-viewport.png"
        page.screenshot(path=screenshot)
        plot_screenshot = ARTIFACTS / f"{site['slug']}-corrected-mobile-plot.png"
        page.locator(".js-plotly-plot").first.screenshot(path=plot_screenshot)
        measured["screenshot"] = str(screenshot)
        measured["plotScreenshot"] = str(plot_screenshot)
        results[site["slug"]] = measured
        print(
            json.dumps(
                {
                    "slug": site["slug"],
                    "pass": measured["pass"],
                    "documentWidth": measured["documentScrollWidth"],
                    "plots": len(measured["plots"]),
                    "uncontainedOffenders": len(measured["uncontainedOffenders"]),
                },
                sort_keys=True,
            ),
            flush=True,
        )
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
                "path": ("validation-evidence/drivers/mobile_containment_audit.py"),
                "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            },
            "source_driver_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "artifact_directory": str(ARTIFACTS),
            "chromiumVersion": browser_version,
            "sites": results,
        },
        indent=2,
        sort_keys=True,
    ),
    encoding="utf-8",
)
print(OUTPUT)
