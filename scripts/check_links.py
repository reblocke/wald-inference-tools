from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

if __package__:
    from scripts.validate_tools_manifest import (
        DEFAULT_MANIFEST,
        PROJECT_ROOT,
        load_manifest,
        validate_manifest,
    )
else:
    from validate_tools_manifest import (  # type: ignore[import-not-found]
        DEFAULT_MANIFEST,
        PROJECT_ROOT,
        load_manifest,
        validate_manifest,
    )


class LinkError(RuntimeError):
    """Raised when a local or public catalog target is inconsistent."""


CATALOG_URL = "https://reblocke.github.io/wald-inference-tools/"
RELATED_TOOLS_HEADING = "## Related Wald tools"


class _ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        field = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if field and attributes.get(field):
            self.references.append(str(attributes[field]))


class _FooterParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_footer = False
        self.links: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "footer":
            self.in_footer = True
        elif self.in_footer and tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "footer":
            self.in_footer = False

    def handle_data(self, data: str) -> None:
        if self.in_footer:
            self.text.append(data)


def check_local_links(root: Path = PROJECT_ROOT) -> list[str]:
    parser = _ReferenceParser()
    parser.feed((root / "index.html").read_text(encoding="utf-8"))
    checked: list[str] = []
    for reference in parser.references:
        parsed = urlsplit(reference)
        if parsed.scheme in {"http", "https"}:
            checked.append(reference)
            continue
        if parsed.scheme or reference.startswith("//"):
            raise LinkError(f"unsupported reference in index.html: {reference}")
        target = root / parsed.path
        if parsed.path and not target.is_file():
            raise LinkError(f"missing local target in index.html: {reference}")
        checked.append(reference)
    return checked


def _request(url: str, *, expect_json: bool = False, attempts: int = 3) -> Any:
    headers = {
        "Accept": "application/vnd.github+json" if "api.github.com" in url else "*/*",
        "User-Agent": "wald-inference-tools-catalog-validator/0.1.0",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status != 200:
                    raise LinkError(f"{url} returned HTTP {response.status}")
                payload = response.read()
            return json.loads(payload) if expect_json else payload
        except (OSError, json.JSONDecodeError, urllib.error.HTTPError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(0.5 * (attempt + 1))
    raise LinkError(f"could not fetch {url}: {last_error}") from last_error


def _github_coordinates(repository_url: str) -> tuple[str, str]:
    parsed = urlsplit(repository_url)
    parts = parsed.path.strip("/").split("/")
    if parsed.netloc != "github.com" or len(parts) != 2:
        raise LinkError(f"unsupported GitHub repository URL: {repository_url}")
    return parts[0], parts[1]


def _package_version(hosted_manifest: dict[str, Any], distribution: str) -> str:
    versions = [
        package.get("version")
        for package in hosted_manifest.get("packages", [])
        if package.get("distribution") == distribution
    ]
    if len(versions) != 1 or not isinstance(versions[0], str):
        raise LinkError(f"hosted manifest has no unique {distribution!r} package")
    return versions[0]


def validate_related_tools_readme(
    readme: str,
    *,
    tool: dict[str, Any],
    adjacent_tool: dict[str, Any],
    integrated_tool: dict[str, Any],
    core_repository: str,
) -> None:
    """Verify the public README's compact portfolio block against catalog metadata."""

    section_start = readme.find(RELATED_TOOLS_HEADING)
    if section_start < 0:
        raise LinkError(f"{tool['slug']}: README is missing {RELATED_TOOLS_HEADING!r}")
    section_end = readme.find("\n## ", section_start + len(RELATED_TOOLS_HEADING))
    section = readme[section_start : section_end if section_end >= 0 else None]

    core_marker = f"wald-inference Core v{tool['core_version']}"
    required_text = {
        "catalog URL": CATALOG_URL,
        "adjacent hosted URL": adjacent_tool["hosted_url"],
        "integrated-workbench hosted URL": integrated_tool["hosted_url"],
        "app repository URL": tool["repository_url"],
        "pinned Core release": f"{core_repository}/releases/tag/v{tool['core_version']}",
        "pinned Core version marker": core_marker,
    }
    missing = [label for label, value in required_text.items() if value not in section]
    if "privacy" not in section.lower():
        missing.append("privacy note")
    if missing:
        raise LinkError(
            f"{tool['slug']}: README related-tools block is missing {', '.join(missing)}"
        )


def validate_related_tools_footer(
    hosted_html: str,
    *,
    tool: dict[str, Any],
    adjacent_tool: dict[str, Any],
    integrated_tool: dict[str, Any],
    core_repository: str,
) -> None:
    """Verify that the deployed app footer exposes the compact portfolio navigation."""

    parser = _FooterParser()
    parser.feed(hosted_html)
    if not parser.links:
        raise LinkError(f"{tool['slug']}: hosted HTML has no linked footer")

    core_release = f"{core_repository}/releases/tag/v{tool['core_version']}"
    required_links = {
        "catalog URL": CATALOG_URL,
        "adjacent hosted URL": adjacent_tool["hosted_url"],
        "integrated-workbench hosted URL": integrated_tool["hosted_url"],
        "app repository URL": tool["repository_url"],
        "pinned Core release": core_release,
    }
    missing = [label for label, value in required_links.items() if value not in parser.links]
    footer_text = " ".join(parser.text)
    if f"wald-inference Core v{tool['core_version']}" not in footer_text:
        missing.append("pinned Core version marker")
    if "privacy" not in footer_text.lower():
        missing.append("privacy note")
    if missing:
        raise LinkError(f"{tool['slug']}: hosted footer is missing {', '.join(missing)}")


def check_live_metadata(manifest: dict[str, Any]) -> list[str]:
    checked: list[str] = []
    repositories = [manifest["core"]["repository"]]
    releases = [(manifest["core"]["repository"], manifest["core"]["latest_validated_release"])]
    repository_metadata: dict[str, dict[str, Any]] = {}

    for repository in repositories + [tool["repository_url"] for tool in manifest["tools"]]:
        owner, name = _github_coordinates(repository)
        metadata = _request(
            f"https://api.github.com/repos/{owner}/{name}",
            expect_json=True,
        )
        if (
            not isinstance(metadata, dict)
            or metadata.get("archived") is True
            or not isinstance(metadata.get("default_branch"), str)
        ):
            raise LinkError(f"repository is unavailable, archived, or malformed: {repository}")
        repository_metadata[repository] = metadata
        checked.append(repository)

    tools_by_slug = {tool["slug"]: tool for tool in manifest["tools"]}
    integrated_tool = tools_by_slug["conf_curve_likelihood"]
    for tool in manifest["tools"]:
        releases.append((tool["repository_url"], tool["app_version"]))
        hosted_payload = _request(tool["hosted_url"])
        try:
            hosted_html = hosted_payload.decode("utf-8")
        except (AttributeError, UnicodeDecodeError) as exc:
            raise LinkError(f"{tool['slug']}: hosted HTML is not valid UTF-8") from exc
        validate_related_tools_footer(
            hosted_html,
            tool=tool,
            adjacent_tool=tools_by_slug[tool["adjacent_slug"]],
            integrated_tool=integrated_tool,
            core_repository=manifest["core"]["repository"],
        )
        checked.append(tool["hosted_url"])
        _request(tool["citation_url"])
        checked.append(tool["citation_url"])
        hosted_manifest = _request(tool["manifest_url"], expect_json=True)
        if not isinstance(hosted_manifest, dict):
            raise LinkError(f"{tool['manifest_url']} did not return a JSON object")
        app_version = _package_version(hosted_manifest, tool["app_distribution"])
        core_version = _package_version(hosted_manifest, "wald-inference")
        if app_version != tool["app_version"]:
            raise LinkError(
                f"{tool['slug']}: hosted app {app_version} != catalog {tool['app_version']}"
            )
        if core_version != tool["core_version"]:
            raise LinkError(
                f"{tool['slug']}: hosted Core {core_version} != catalog {tool['core_version']}"
            )
        checked.append(tool["manifest_url"])

        owner, name = _github_coordinates(tool["repository_url"])
        default_branch = repository_metadata[tool["repository_url"]]["default_branch"]
        readme_url = (
            f"https://raw.githubusercontent.com/{owner}/{name}/"
            f"{quote(default_branch, safe='')}/README.md"
        )
        readme_payload = _request(readme_url)
        try:
            readme = readme_payload.decode("utf-8")
        except (AttributeError, UnicodeDecodeError) as exc:
            raise LinkError(f"{tool['slug']}: public README is not valid UTF-8") from exc
        validate_related_tools_readme(
            readme,
            tool=tool,
            adjacent_tool=tools_by_slug[tool["adjacent_slug"]],
            integrated_tool=integrated_tool,
            core_repository=manifest["core"]["repository"],
        )
        checked.append(readme_url)

    for repository, version in releases:
        owner, name = _github_coordinates(repository)
        release = _request(
            f"https://api.github.com/repos/{owner}/{name}/releases/tags/v{version}",
            expect_json=True,
        )
        if not isinstance(release, dict) or release.get("draft") is True:
            raise LinkError(f"missing public non-draft release: {repository} v{version}")
        checked.append(f"{repository}/releases/tag/v{version}")
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="also query public release/Pages URLs")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    validate_manifest(manifest)
    local = check_local_links()
    print(f"Validated {len(local)} references in index.html.")
    if args.live:
        public = check_live_metadata(manifest)
        print(
            f"Validated {len(public)} public release, repository, README, citation, "
            "and Pages targets."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
