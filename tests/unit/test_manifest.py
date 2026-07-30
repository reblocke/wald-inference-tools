from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.check_links import (
    LinkError,
    _annotated_tag_commit,
    _validate_hosted_release_commit,
    validate_related_tools_footer,
    validate_related_tools_readme,
)
from scripts.validate_tools_manifest import ManifestError, load_manifest, validate_manifest


def test_checked_in_manifest_is_strict_and_complete() -> None:
    manifest = load_manifest()
    validate_manifest(manifest)
    assert len(manifest["tools"]) == 6
    assert {tool["conditioning"] for tool in manifest["tools"]} == {
        "observed-data",
        "design",
        "mixed",
    }


def test_duplicate_json_key_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
    with pytest.raises(ManifestError, match="duplicate JSON key"):
        load_manifest(path)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda value: value["tools"].append(deepcopy(value["tools"][0])), "unique"),
        (
            lambda value: value["tools"][0].update({"conditioning": "design"}),
            "conditioning",
        ),
        (
            lambda value: value["tools"][0].update(
                {"hosted_url": "https://example.test/?estimate=1.2"}
            ),
            "input-free",
        ),
        (
            lambda value: value["tools"][0].pop("primary_limitation"),
            "missing",
        ),
    ],
)
def test_semantic_contract_rejects_invalid_metadata(mutation, message: str) -> None:
    manifest = load_manifest()
    mutation(manifest)
    with pytest.raises(ManifestError, match=message):
        validate_manifest(manifest)


def test_manifest_serialization_has_no_nonstandard_numbers() -> None:
    raw = json.dumps(load_manifest(), allow_nan=False, sort_keys=True)
    assert "NaN" not in raw
    assert "Infinity" not in raw


def test_annotated_tag_commit_resolves_exact_peeled_commit(monkeypatch) -> None:
    tag_sha = "a" * 40
    commit_sha = "b" * 40
    responses = {
        "https://api.github.com/repos/reblocke/example/git/ref/tags/v0.1.2": {
            "object": {"type": "tag", "sha": tag_sha}
        },
        f"https://api.github.com/repos/reblocke/example/git/tags/{tag_sha}": {
            "object": {"type": "commit", "sha": commit_sha}
        },
    }

    monkeypatch.setattr(
        "scripts.check_links._request",
        lambda url, *, expect_json=False, attempts=3: responses[url],
    )

    assert _annotated_tag_commit("https://github.com/reblocke/example", "0.1.2") == commit_sha


@pytest.mark.parametrize(
    "response",
    [
        {"object": {"type": "commit", "sha": "a" * 40}},
        {"object": {"type": "tag", "sha": "not-a-commit"}},
    ],
)
def test_annotated_tag_commit_rejects_invalid_tag_ref(monkeypatch, response: dict) -> None:
    monkeypatch.setattr(
        "scripts.check_links._request",
        lambda url, *, expect_json=False, attempts=3: response,
    )

    with pytest.raises(LinkError, match="not an annotated"):
        _annotated_tag_commit("https://github.com/reblocke/example", "0.1.2")


def test_annotated_tag_commit_rejects_noncommit_target(monkeypatch) -> None:
    tag_sha = "a" * 40

    def request(url: str, *, expect_json: bool = False, attempts: int = 3):
        if url.endswith("/git/ref/tags/v0.1.2"):
            return {"object": {"type": "tag", "sha": tag_sha}}
        return {"object": {"type": "tree", "sha": "b" * 40}}

    monkeypatch.setattr("scripts.check_links._request", request)

    with pytest.raises(LinkError, match="does not peel"):
        _annotated_tag_commit("https://github.com/reblocke/example", "0.1.2")


def test_hosted_release_commit_must_match_annotated_tag(monkeypatch) -> None:
    tool = {
        "slug": "example",
        "repository_url": "https://github.com/reblocke/example",
        "app_version": "0.1.2",
    }
    release_commit = "b" * 40
    monkeypatch.setattr(
        "scripts.check_links._annotated_tag_commit",
        lambda repository_url, version: release_commit,
    )

    assert (
        _validate_hosted_release_commit(
            tool,
            {"source_commit": release_commit},
        )
        == release_commit
    )
    with pytest.raises(LinkError, match="hosted commit"):
        _validate_hosted_release_commit(
            tool,
            {"source_commit": "c" * 40},
        )
    with pytest.raises(LinkError, match="source_commit is invalid"):
        _validate_hosted_release_commit(
            tool,
            {"source_commit": "not-a-commit"},
        )


def _related_tools_block(tool: dict, adjacent: dict, integrated: dict) -> str:
    core_repository = "https://github.com/reblocke/wald-inference-core"
    return f"""# Example

## Related Wald tools

- Choose a tool: https://reblocke.github.io/wald-inference-tools/
- Closest adjacent tool: {adjacent["hosted_url"]}
- Integrated workbench: {integrated["hosted_url"]}
- App repository: {tool["repository_url"]}
- Numerical dependency: wald-inference Core v{tool["core_version"]}
  ({core_repository}/releases/tag/v{tool["core_version"]})
- Privacy: calculations stay in this browser.

## Next section
"""


def _related_tools_footer(tool: dict, adjacent: dict, integrated: dict) -> str:
    core_repository = "https://github.com/reblocke/wald-inference-core"
    return f"""<!doctype html>
<footer>
  <p>Related Wald tools · wald-inference Core v{tool["core_version"]} · Privacy: browser-only.</p>
  <a href="https://reblocke.github.io/wald-inference-tools/">Choose a tool</a>
  <a href="{adjacent["hosted_url"]}">Adjacent</a>
  <a href="{integrated["hosted_url"]}">Integrated workbench</a>
  <a href="{tool["repository_url"]}">App repository</a>
  <a href="{core_repository}/releases/tag/v{tool["core_version"]}">Core release</a>
</footer>
"""


def test_readme_portfolio_block_matches_manifest() -> None:
    manifest = load_manifest()
    tools = {tool["slug"]: tool for tool in manifest["tools"]}
    tool = tools["critical-effect-size"]
    validate_related_tools_readme(
        _related_tools_block(
            tool,
            tools[tool["adjacent_slug"]],
            tools["conf_curve_likelihood"],
        ),
        tool=tool,
        adjacent_tool=tools[tool["adjacent_slug"]],
        integrated_tool=tools["conf_curve_likelihood"],
        core_repository=manifest["core"]["repository"],
    )


def test_hosted_footer_matches_manifest() -> None:
    manifest = load_manifest()
    tools = {tool["slug"]: tool for tool in manifest["tools"]}
    tool = tools["critical-effect-size"]
    validate_related_tools_footer(
        _related_tools_footer(
            tool,
            tools[tool["adjacent_slug"]],
            tools["conf_curve_likelihood"],
        ),
        tool=tool,
        adjacent_tool=tools[tool["adjacent_slug"]],
        integrated_tool=tools["conf_curve_likelihood"],
        core_repository=manifest["core"]["repository"],
    )


@pytest.mark.parametrize(
    ("removed", "message"),
    [
        ("## Related Wald tools", "missing"),
        ("https://reblocke.github.io/wald-inference-tools/", "catalog URL"),
        ("wald-inference Core v0.4.1", "pinned Core version"),
        ("Privacy", "privacy note"),
    ],
)
def test_readme_portfolio_block_rejects_missing_metadata(removed: str, message: str) -> None:
    manifest = load_manifest()
    tools = {tool["slug"]: tool for tool in manifest["tools"]}
    tool = tools["critical-effect-size"]
    readme = _related_tools_block(
        tool,
        tools[tool["adjacent_slug"]],
        tools["conf_curve_likelihood"],
    ).replace(removed, "")
    with pytest.raises(LinkError, match=message):
        validate_related_tools_readme(
            readme,
            tool=tool,
            adjacent_tool=tools[tool["adjacent_slug"]],
            integrated_tool=tools["conf_curve_likelihood"],
            core_repository=manifest["core"]["repository"],
        )


@pytest.mark.parametrize(
    ("removed", "message"),
    [
        ("<footer>", "linked footer"),
        ("https://reblocke.github.io/wald-inference-tools/", "catalog URL"),
        ("wald-inference Core v0.4.1", "pinned Core version"),
        ("Privacy", "privacy note"),
    ],
)
def test_hosted_footer_rejects_missing_metadata(removed: str, message: str) -> None:
    manifest = load_manifest()
    tools = {tool["slug"]: tool for tool in manifest["tools"]}
    tool = tools["critical-effect-size"]
    hosted_html = _related_tools_footer(
        tool,
        tools[tool["adjacent_slug"]],
        tools["conf_curve_likelihood"],
    ).replace(removed, "")
    with pytest.raises(LinkError, match=message):
        validate_related_tools_footer(
            hosted_html,
            tool=tool,
            adjacent_tool=tools[tool["adjacent_slug"]],
            integrated_tool=tools["conf_curve_likelihood"],
            core_repository=manifest["core"]["repository"],
        )
