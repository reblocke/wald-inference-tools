from __future__ import annotations

import hashlib
import re
from pathlib import Path

from scripts.build_release_artifacts import build_release
from scripts.build_site import build_site
from scripts.check_links import check_local_links
from scripts.validate_tools_manifest import PROJECT_ROOT, load_manifest


def test_local_document_references_resolve() -> None:
    checked = check_local_links()
    assert "data/tools.json" in checked
    assert "app.js" in checked
    assert "styles.css" in checked


def test_catalog_contains_no_calculation_runtime_or_tracking() -> None:
    inspected = [
        PROJECT_ROOT / "index.html",
        PROJECT_ROOT / "app.js",
        PROJECT_ROOT / "styles.css",
    ]
    content = "\n".join(path.read_text(encoding="utf-8").lower() for path in inspected)
    prohibited = [
        "pyodide",
        "google-analytics",
        "googletagmanager",
        "segment.io",
        "mixpanel",
        "localstorage.setitem",
        "sessionstorage.setitem",
        "document.cookie =",
        "<form",
    ]
    assert not [term for term in prohibited if term in content]
    assert not re.findall(r"<script[^>]+src=[\"']https?://", content)


def test_manifest_urls_are_plain_and_input_free() -> None:
    for tool in load_manifest()["tools"]:
        for field in ("hosted_url", "repository_url", "citation_url", "manifest_url"):
            assert "?" not in tool[field]
            assert "#" not in tool[field]


def test_site_build_is_exact_allowlist(tmp_path: Path) -> None:
    output = PROJECT_ROOT / "site-test-output"
    try:
        build_site(output)
        files = {
            path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()
        }
        assert {"index.html", "styles.css", "app.js", "data/tools.json", ".nojekyll"} <= files
        assert "pyproject.toml" not in files
        assert not [path for path in files if path.endswith(".py")]
    finally:
        if output.exists():
            import shutil

            shutil.rmtree(output)


def test_release_artifacts_are_byte_reproducible() -> None:
    first = PROJECT_ROOT / "release-test-one"
    second = PROJECT_ROOT / "release-test-two"
    try:
        first_artifacts = build_release("0.1.0", first)
        second_artifacts = build_release("0.1.0", second)
        first_hashes = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in first_artifacts
        }
        second_hashes = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in second_artifacts
        }
        assert first_hashes == second_hashes
    finally:
        import shutil

        for output in (first, second):
            if output.exists():
                shutil.rmtree(output)
