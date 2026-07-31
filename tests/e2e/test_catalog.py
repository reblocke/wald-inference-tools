from __future__ import annotations

from urllib.parse import urlsplit

from playwright.sync_api import Page, expect


def _ready(page: Page, catalog_url: str) -> None:
    page.goto(catalog_url)
    expect(page.locator(".tool-card")).to_have_count(6)
    expect(page.locator("#catalog-status")).to_have_text("6 tools shown.")


def test_question_cards_and_comparison_render_from_manifest(page: Page, catalog_url: str) -> None:
    _ready(page, catalog_url)
    expect(page.locator("h1")).to_have_text("What question are you trying to answer?")
    expect(page.locator("#comparison-body tr")).to_have_count(6)
    expect(page.locator(".tool-card").first.locator(".primary-action")).to_have_attribute(
        "href", "https://reblocke.github.io/compatibility-curve/"
    )
    expect(page.locator(".tool-card").first).to_contain_text("Do not use this tool when")
    expect(page.locator(".tool-card").first.locator(".non-goals li")).to_have_count(3)
    expect(page.locator(".tool-card").first).to_contain_text("Clinical decision support")
    expect(page.locator(".validation-badge").first).to_have_text("Software validated")
    expect(page.locator(".scope-note").last).to_contain_text("does not mean clinical validation")
    expect(page.locator("#catalog-version")).to_contain_text("Catalog 0.2.1")
    expect(page.locator("#core-repository-link")).to_have_attribute(
        "href", "https://github.com/reblocke/wald-inference-core"
    )
    expect(page.locator("#core-repository-link")).not_to_have_attribute("aria-disabled", "true")


def test_conditioning_filters_preserve_integrated_boundary(page: Page, catalog_url: str) -> None:
    _ready(page, catalog_url)
    page.get_by_label("Observed data").check()
    expect(page.locator(".tool-card:visible")).to_have_count(3)
    expect(page.locator("#catalog-status")).to_have_text("3 tools shown.")
    page.get_by_label("Design").check()
    expect(page.locator(".tool-card:visible")).to_have_count(4)
    expect(page.locator("#catalog-status")).to_have_text("4 tools shown.")
    page.get_by_label("All").check()
    expect(page.locator(".tool-card:visible")).to_have_count(6)


def test_mobile_keyboard_and_visible_focus(page: Page, catalog_url: str) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    _ready(page, catalog_url)
    page.locator(".skip-link").focus()
    expect(page.locator(".skip-link")).to_be_focused()
    assert page.locator(".skip-link").evaluate(
        "(node) => getComputedStyle(node).transform !== 'none'"
    )
    page.keyboard.press("Enter")
    expect(page.locator("#main-content")).to_be_focused()
    page.get_by_label("Observed data").focus()
    page.keyboard.press("ArrowRight")
    expect(page.get_by_label("Design")).to_be_checked()
    expect(page.locator(".tool-card:visible")).to_have_count(4)
    assert page.locator("body").evaluate(
        "(node) => node.scrollWidth <= document.documentElement.clientWidth"
    )


def test_initial_load_is_same_origin_static_and_leaves_no_state(
    page: Page, catalog_url: str
) -> None:
    requests: list[tuple[str, str, str | None]] = []
    page.on(
        "request",
        lambda request: requests.append((request.method, request.url, request.post_data)),
    )
    _ready(page, catalog_url)
    origin = urlsplit(catalog_url)
    assert requests
    assert all(method == "GET" and body is None for method, _, body in requests)
    assert all(
        (urlsplit(url).scheme, urlsplit(url).netloc) == (origin.scheme, origin.netloc)
        for _, url, _ in requests
    )
    assert {urlsplit(url).path for _, url, _ in requests} <= {
        "/",
        "/app.js",
        "/styles.css",
        "/data/tools.json",
    }
    assert page.evaluate("localStorage.length") == 0
    assert page.evaluate("sessionStorage.length") == 0
    assert page.evaluate("document.cookie") == ""
    assert (
        page.evaluate("'serviceWorker' in navigator && !!navigator.serviceWorker.controller")
        is False
    )
