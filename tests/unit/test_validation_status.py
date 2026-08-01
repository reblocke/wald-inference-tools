from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.validate_validation_status import (
    ValidationStatusError,
    load_report_inventory,
    load_status,
    main,
    validate_release_inventory,
    validate_status,
)

RELEASES = {
    "reblocke/wald-inference-core": "v0.4.2",
    "reblocke/scientific-applet-template": "v0.1.3",
    "reblocke/compatibility-curve": "v0.1.5",
    "reblocke/wald-likelihood-support": "v0.1.4",
    "reblocke/critical-effect-size": "v0.1.5",
    "reblocke/type-s-m-calibrator": "v0.1.5",
    "reblocke/precision-guardrail-planner": "v0.1.4",
    "reblocke/wald-inference-tools": "v0.2.1",
    "reblocke/conf_curve_likelihood": "v0.2.7",
}
ATTESTATION_RACE_RUNS = {
    "reblocke/compatibility-curve": 30672853190,
    "reblocke/type-s-m-calibrator": 30677268367,
}


def _manifest(validation_status: str = "conditionally-validated") -> dict:
    app_versions = {name: release.removeprefix("v") for name, release in RELEASES.items()}
    tool_distributions = {
        "reblocke/compatibility-curve": "compatibility-curve",
        "reblocke/wald-likelihood-support": "wald-likelihood-support",
        "reblocke/critical-effect-size": "critical-effect-size",
        "reblocke/type-s-m-calibrator": "type-s-m-calibrator",
        "reblocke/precision-guardrail-planner": "precision-guardrail-planner",
        "reblocke/conf_curve_likelihood": "confcurve",
    }
    return {
        "catalog_version": "0.2.2",
        "core": {
            "repository": "https://github.com/reblocke/wald-inference-core",
            "latest_validated_release": "0.4.2",
            "validation_status": validation_status,
        },
        "portfolio_status": validation_status,
        "tools": [
            {
                "repository_url": f"https://github.com/{name}",
                "app_version": app_versions[name],
                "app_distribution": distribution,
                "core_version": "0.4.2",
                "manifest_url": (
                    f"https://reblocke.github.io/{name.split('/')[1]}/assets/py/manifest.json"
                ),
                "validation_status": validation_status,
            }
            for name, distribution in tool_distributions.items()
        ],
    }


def _status(
    verdict: str = "Validated with nonblocking limitations.",
    repository_status: str = "conditionally-validated",
    *,
    blocking: bool = False,
) -> dict:
    return {
        "schema_version": 1,
        "validated_at": "2026-07-30T14:00:00Z",
        "verdict": verdict,
        "core_version": "0.4.2",
        "repositories": [
            {
                "name": name,
                "commit": f"{index + 1:040x}",
                "release": release,
                "status": (
                    "validation-failed"
                    if blocking and index == 0
                    else ("validated" if blocking else repository_status)
                ),
                "blocking_findings": (
                    ["Release blocker remains."] if blocking and index == 0 else []
                ),
            }
            for index, (name, release) in enumerate(RELEASES.items())
        ],
        "report_sha256": "0" * 64,
    }


def _successful_run(workflow: str, commit: str, branch: str) -> dict:
    return {
        "databaseId": 123,
        "workflowName": workflow,
        "status": "completed",
        "conclusion": "success",
        "headSha": commit,
        "headBranch": branch,
        "event": "push",
        "url": "https://github.com/reblocke/example/actions/runs/123",
        "createdAt": "2026-07-30T14:00:00Z",
        "updatedAt": "2026-07-30T14:01:00Z",
    }


def _release_asset_names(name: str, release: str) -> tuple[set[str], str | None]:
    version = release.removeprefix("v")
    repository = name.split("/", 1)[1]
    if name == "reblocke/wald-inference-core":
        return (
            {
                "SHA256SUMS",
                "baseline-parity.json",
                f"wald_inference-{version}-py3-none-any.whl",
                f"wald_inference-{version}.tar.gz",
            },
            None,
        )
    if name == "reblocke/wald-inference-tools":
        live_asset = f"tools-{release}.json"
        return (
            {
                "SHA256SUMS",
                live_asset,
                f"PORTFOLIO_VALIDATION_REPORT-{release}.md",
                f"validation_status-{release}.json",
                f"validation-evidence-index-{release}.json",
                f"portfolio-validation-evidence-{release}.tar.gz",
                f"{repository}-site-{release}.zip",
                f"{repository}-{release}.tar.gz",
            },
            live_asset,
        )
    if name == "reblocke/conf_curve_likelihood":
        return (
            {
                "SHA256SUMS",
                "browser-stage-manifest.json",
                f"conf_curve_likelihood-{version}.tar.gz",
            },
            "browser-stage-manifest.json",
        )
    live_asset = f"browser-stage-manifest-{release}.json"
    return (
        {
            "SHA256SUMS",
            live_asset,
            f"{repository}-{release}.tar.gz",
        },
        live_asset,
    )


def _staged_digest(records: list[dict]) -> str:
    digest = hashlib.sha256()
    for record in sorted(records, key=lambda item: item["path"]):
        digest.update((f"{record['path']}\0{record['sha256']}\0{record['bytes']}\n").encode())
    return digest.hexdigest()


def _staged_package(
    *,
    distribution: str,
    version: str,
    role: str,
    core_artifact_digest: str,
    integrated: bool = False,
) -> dict:
    import_name = distribution.replace("-", "_")
    path = "wald_inference/core.py" if role == "core" else f"{import_name}/__init__.py"
    contents_digest = hashlib.sha256(path.encode()).hexdigest()
    files = [{"path": path, "bytes": len(path), "sha256": contents_digest}]
    package = {
        "role": role,
        "distribution": distribution,
        "import_name": import_name,
        "version": version,
        "files": files,
    }
    if not integrated:
        package.update(
            {
                "artifact_url": (
                    "https://github.com/reblocke/wald-inference-core/releases/download/"
                    "v0.4.2/wald_inference-0.4.2-py3-none-any.whl"
                    if role == "core"
                    else None
                ),
                "artifact_sha256": core_artifact_digest if role == "core" else None,
                "package_sha256": _staged_digest(files),
            }
        )
    return package


def _release_inventory(status: dict, manifest: dict | None = None) -> dict:
    manifest = _manifest() if manifest is None else manifest
    tools = {
        tool["repository_url"].removeprefix("https://github.com/"): tool
        for tool in manifest["tools"]
    }
    repositories = []
    for index, expected in enumerate(status["repositories"]):
        name = expected["name"]
        commit = expected["commit"]
        release = expected["release"]
        asset_names, live_asset_name = _release_asset_names(name, release)
        pages = None
        live = None
        if name != "reblocke/wald-inference-core":
            pages = {
                "deployment_id": index + 1,
                "sha": commit,
                "created_at": "2026-07-30T14:00:00Z",
                "status": "success",
                "environment_url": f"https://reblocke.github.io/{name.split('/')[1]}/",
                "workflow_runs": [_successful_run("Deploy Pages", commit, "main")],
            }
            if name == "reblocke/wald-inference-tools":
                live = {
                    "url": "https://reblocke.github.io/wald-inference-tools/data/tools.json",
                    "sha256": "a" * 64,
                    "source_commit": None,
                    "catalog_version": "0.2.1",
                    "bundle_sha256": None,
                    "packages": None,
                    "staged_files_verified": None,
                }
            elif name == "reblocke/scientific-applet-template":
                packages = [
                    _staged_package(
                        distribution="scientific-applet-template-package",
                        version="0.1.3",
                        role="app",
                        core_artifact_digest="b" * 64,
                    )
                ]
                live = {
                    "url": (
                        "https://reblocke.github.io/scientific-applet-template/"
                        "assets/py/manifest.json"
                    ),
                    "sha256": "a" * 64,
                    "source_commit": commit,
                    "catalog_version": None,
                    "bundle_sha256": _staged_digest(
                        [record for package in packages for record in package["files"]]
                    ),
                    "packages": packages,
                    "staged_files_verified": True,
                }
            else:
                tool = tools[name]
                integrated = name == "reblocke/conf_curve_likelihood"
                packages = [
                    _staged_package(
                        distribution=tool["app_distribution"],
                        version=tool["app_version"],
                        role="app",
                        core_artifact_digest="b" * 64,
                        integrated=integrated,
                    ),
                    _staged_package(
                        distribution="wald-inference",
                        version=tool["core_version"],
                        role="core",
                        core_artifact_digest="b" * 64,
                        integrated=integrated,
                    ),
                ]
                live = {
                    "url": tool["manifest_url"],
                    "sha256": "a" * 64,
                    "source_commit": commit,
                    "catalog_version": None,
                    "bundle_sha256": _staged_digest(
                        [record for package in packages for record in package["files"]]
                    ),
                    "packages": packages,
                    "staged_files_verified": True,
                }
        repositories.append(
            {
                "name": name,
                "repository_url": f"https://github.com/{name}",
                "visibility": "PUBLIC",
                "default_branch": "main",
                "is_template": name == "reblocke/scientific-applet-template",
                "license": "mit",
                "release": release,
                "tag_object": f"{index + 101:040x}",
                "peeled_commit": commit,
                "tag_ref": {
                    "name": release,
                    "type": "tag",
                    "sha": f"{index + 101:040x}",
                },
                "tag_target": {"type": "commit", "sha": commit},
                "tagger": {
                    "name": "Brian Locke",
                    "email": "reblocke@example.test",
                    "date": "2026-07-30T14:00:00Z",
                },
                "release_record": {
                    "tag_name": release,
                    "url": f"https://github.com/{name}/releases/tag/{release}",
                    "name": release,
                    "published_at": "2026-07-30T14:00:00Z",
                    "is_draft": False,
                    "is_prerelease": False,
                    "is_immutable": True,
                    "assets": [
                        {
                            "name": asset_name,
                            "size": 1,
                            "digest": (
                                f"sha256:{'a' * 64}"
                                if asset_name == live_asset_name
                                else f"sha256:{'b' * 64}"
                            ),
                            "url": (
                                f"https://github.com/{name}/releases/download/"
                                f"{release}/{asset_name}"
                            ),
                        }
                        for asset_name in sorted(asset_names)
                    ],
                },
                "release_workflow": (
                    {
                        **_successful_run("Release", commit, release),
                        "databaseId": ATTESTATION_RACE_RUNS[name],
                        "conclusion": "failure",
                    }
                    if name in ATTESTATION_RACE_RUNS
                    else _successful_run("Release", commit, release)
                ),
                "release_verification": {
                    "verified_at": status["validated_at"],
                    "release_attestation_verified": True,
                    "workflow_exception": (
                        "post-publication-attestation-race"
                        if name in ATTESTATION_RACE_RUNS
                        else None
                    ),
                },
                "successful_ci_runs": [_successful_run("CI", commit, "main")],
                "pages": pages,
                "live": live,
            }
        )
    return {
        "schema_version": 1,
        "audited_at": status["validated_at"],
        "catalog_evidence_carrier": {
            "release": "v0.2.2",
            "note": "The audited predecessor is v0.2.1.",
        },
        "repositories": repositories,
    }


@pytest.fixture(autouse=True)
def _isolate_report_linter(monkeypatch) -> None:
    monkeypatch.setattr(
        "scripts.validate_validation_status.validate_portfolio_report",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "scripts.validate_validation_status.validate_release_inventory",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_release_inventory",
        lambda *args, **kwargs: {},
    )


def _write_report(path: Path, status: dict) -> None:
    inventory = {
        key: value
        for key, value in status.items()
        if key not in {"schema_version", "report_sha256"}
    }
    path.write_text(
        "# Portfolio validation\n\n"
        "<!-- validation-inventory:start -->\n"
        f"{json.dumps(inventory, indent=2, sort_keys=True)}\n"
        "<!-- validation-inventory:end -->\n",
        encoding="utf-8",
    )


def _complete_status(tmp_path: Path, status: dict | None = None) -> tuple[dict, Path]:
    value = deepcopy(status) if status is not None else _status()
    report = tmp_path / "report.md"
    _write_report(report, value)
    value["report_sha256"] = hashlib.sha256(report.read_bytes()).hexdigest()
    return value, report


def test_checked_status_matches_report_inventory_and_manifest(tmp_path: Path, monkeypatch) -> None:
    value, report = _complete_status(tmp_path)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    validate_status(value, report_path=report)


@pytest.mark.parametrize(
    ("verdict", "repository_status", "blocking"),
    [
        ("Validated for release.", "validated", False),
        (
            "Validated with nonblocking limitations.",
            "conditionally-validated",
            False,
        ),
        ("Not validated; release blockers remain.", "validation-failed", True),
    ],
)
def test_all_three_cc_mig_11_verdict_paths(
    tmp_path: Path,
    monkeypatch,
    verdict: str,
    repository_status: str,
    blocking: bool,
) -> None:
    value, report = _complete_status(
        tmp_path,
        _status(verdict, repository_status, blocking=blocking),
    )
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(repository_status),
    )

    validate_status(value, report_path=report)


@pytest.mark.parametrize(
    ("verdict", "repository_status", "blocking", "releasable"),
    [
        ("Validated for release.", "validated", False, True),
        (
            "Validated with nonblocking limitations.",
            "conditionally-validated",
            False,
            True,
        ),
        ("Not validated; release blockers remain.", "validation-failed", True, False),
    ],
)
def test_release_mode_accepts_only_releasable_verdicts(
    tmp_path: Path,
    monkeypatch,
    verdict: str,
    repository_status: str,
    blocking: bool,
    releasable: bool,
) -> None:
    value, report = _complete_status(
        tmp_path,
        _status(verdict, repository_status, blocking=blocking),
    )
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(repository_status),
    )

    if releasable:
        validate_status(value, report_path=report, require_releasable=True)
    else:
        with pytest.raises(
            ValidationStatusError,
            match="release requires a validated or conditionally validated",
        ):
            validate_status(value, report_path=report, require_releasable=True)


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        ([], False),
        (["--require-releasable"], True),
    ],
)
def test_cli_passes_release_mode_to_the_status_validator(
    monkeypatch,
    argv: list[str],
    expected: bool,
) -> None:
    status = {"repositories": []}
    observed: list[bool] = []
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_status",
        lambda: status,
    )

    def capture_mode(value: dict, *, require_releasable: bool = False) -> None:
        assert value is status
        observed.append(require_releasable)

    monkeypatch.setattr(
        "scripts.validate_validation_status.validate_status",
        capture_mode,
    )

    assert main(argv) == 0
    assert observed == [expected]


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        ("# Missing inventory\n", "exactly one"),
        (
            "<!-- validation-inventory:start -->\n{}\n"
            "<!-- validation-inventory:end -->\n"
            "<!-- validation-inventory:start -->\n{}\n"
            "<!-- validation-inventory:end -->\n",
            "exactly one",
        ),
        (
            "<!-- validation-inventory:end -->\n{}\n<!-- validation-inventory:start -->\n",
            "out of order",
        ),
    ],
)
def test_report_inventory_rejects_missing_duplicate_or_reversed_markers(
    tmp_path: Path,
    contents: str,
    message: str,
) -> None:
    report = tmp_path / "report.md"
    report.write_text(contents, encoding="utf-8")

    with pytest.raises(ValidationStatusError, match=message):
        load_report_inventory(report)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda value: value["repositories"].pop(),
            "exact portfolio",
        ),
        (
            lambda value: value["repositories"][0].update(
                {"blocking_findings": ["unresolved blocker"]}
            ),
            "must not contain blocking",
        ),
        (
            lambda value: value.update({"verdict": "Looks fine"}),
            "three CC-MIG-11 decisions",
        ),
    ],
)
def test_status_rejects_inconsistent_evidence(
    tmp_path: Path, monkeypatch, mutation, message: str
) -> None:
    value = _status()
    mutation(value)
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match=message):
        validate_status(value, report_path=report)


def test_status_rejects_report_digest_mismatch(tmp_path: Path, monkeypatch) -> None:
    value, report = _complete_status(tmp_path)
    value["report_sha256"] = "0" * 64
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="report_sha256 mismatch"):
        validate_status(value, report_path=report)


def test_status_rejects_report_inventory_mismatch(tmp_path: Path, monkeypatch) -> None:
    value, report = _complete_status(tmp_path)
    value["repositories"][0]["release"] = "v9.9.9"
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="does not exactly match"):
        validate_status(value, report_path=report)


def test_status_rejects_manifest_release_mismatch(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["repositories"][2]["release"] = "v9.9.9"
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="does not match the catalog manifest"):
        validate_status(value, report_path=report)


def test_status_rejects_non_manifest_predecessor_release(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["repositories"][1]["release"] = "v0.1.1"
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="audited predecessor"):
        validate_status(value, report_path=report)


def test_status_requires_canonical_repository_order(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["repositories"][0], value["repositories"][1] = (
        value["repositories"][1],
        value["repositories"][0],
    )
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="canonical portfolio order"):
        validate_status(value, report_path=report)


def test_status_loader_rejects_duplicate_keys(tmp_path: Path) -> None:
    path = tmp_path / "validation_status.json"
    path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")

    with pytest.raises(ValidationStatusError, match="duplicate JSON key"):
        load_status(path)


@pytest.mark.parametrize("schema_version", [True, 1.0, "1"])
def test_status_rejects_non_integer_schema_version(
    tmp_path: Path, monkeypatch, schema_version
) -> None:
    value = _status()
    value["schema_version"] = schema_version
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="schema_version must equal 1"):
        validate_status(value, report_path=report)


def test_status_rejects_noncanonical_timestamp(tmp_path: Path, monkeypatch) -> None:
    value = _status()
    value["validated_at"] = "2026-07-30 14:00:00Z"
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="YYYY-MM-DDTHH:MM:SSZ"):
        validate_status(value, report_path=report)


def test_release_inventory_binds_status_manifest_and_live_evidence() -> None:
    status = _status()
    manifest = _manifest()

    validate_release_inventory(
        _release_inventory(status, manifest),
        status=status,
        manifest=manifest,
    )


def _mutate_core_file_and_rehash(value: dict) -> None:
    repository = value["repositories"][2]
    core_package = repository["live"]["packages"][1]
    core_package["files"][0]["sha256"] = "f" * 64
    core_package["package_sha256"] = _staged_digest(core_package["files"])
    repository["live"]["bundle_sha256"] = _staged_digest(
        [record for package in repository["live"]["packages"] for record in package["files"]]
    )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda value: value["repositories"][0].update({"peeled_commit": "f" * 40}),
            "peeled_commit does not match",
        ),
        (
            lambda value: value["repositories"][0]["tag_ref"].update({"type": "commit"}),
            "tag_ref does not bind",
        ),
        (
            lambda value: value["repositories"][0]["tag_target"].update({"sha": "f" * 40}),
            "tag_target does not bind",
        ),
        (
            lambda value: value["repositories"][0]["tagger"].update({"name": "Reed Blocke"}),
            "approved author Brian Locke",
        ),
        (
            lambda value: value["repositories"][0]["release_record"].update({"tag_name": "v9.9.9"}),
            "tag_name does not match",
        ),
        (
            lambda value: value["repositories"][0]["release_record"].update({"is_draft": True}),
            "must not be a draft",
        ),
        (
            lambda value: value["repositories"][0]["release_record"]["assets"][0].update(
                {"url": "https://example.test/unbound-asset"}
            ),
            "canonical release asset URL",
        ),
        (
            lambda value: value["repositories"][0]["release_record"].update(
                {"is_prerelease": True}
            ),
            "prerelease state contradicts",
        ),
        (
            lambda value: value["repositories"][0]["release_record"].update(
                {"is_immutable": False}
            ),
            "immutable state contradicts",
        ),
        (
            lambda value: value["repositories"][0]["release_verification"].update(
                {"release_attestation_verified": False}
            ),
            "successful current attestation verification",
        ),
        (
            lambda value: value["repositories"][0].update({"successful_ci_runs": []}),
            "successful_ci_runs must be a non-empty",
        ),
        (
            lambda value: value["repositories"][1]["pages"].update({"workflow_runs": []}),
            "pages.workflow_runs must be a non-empty",
        ),
        (
            lambda value: value["repositories"][2]["live"].update({"source_commit": "f" * 40}),
            "does not identify the audited deployed commit",
        ),
        (
            lambda value: value["repositories"][7]["live"].update({"source_commit": "f" * 40}),
            "does not match the audited catalog predecessor",
        ),
        (
            lambda value: value["repositories"][2]["live"]["packages"][0].update(
                {"version": "9.9.9"}
            ),
            "has no unique compatibility-curve 0.1.5 package",
        ),
        (
            lambda value: value["repositories"][2]["live"]["packages"][1].update(
                {"artifact_sha256": "f" * 64}
            ),
            "does not bind the audited Core wheel",
        ),
        (
            _mutate_core_file_and_rehash,
            "Core staged files differ",
        ),
        (
            lambda value: value["repositories"][2]["live"].update({"bundle_sha256": "f" * 64}),
            "bundle_sha256 does not match",
        ),
        (
            lambda value: value["repositories"][2]["live"].update({"staged_files_verified": False}),
            "does not identify the audited deployed commit",
        ),
        (
            lambda value: value["repositories"][2]["release_record"]["assets"][0].update(
                {
                    "name": "unexpected.bin",
                    "url": (
                        "https://github.com/reblocke/compatibility-curve/releases/"
                        "download/v0.1.5/unexpected.bin"
                    ),
                }
            ),
            "do not match the expected release set",
        ),
        (
            lambda value: next(
                asset
                for asset in value["repositories"][2]["release_record"]["assets"]
                if asset["name"] == "browser-stage-manifest-v0.1.5.json"
            ).update({"digest": f"sha256:{'f' * 64}"}),
            "live bytes do not match the released live-data asset",
        ),
        (
            lambda value: value["repositories"][2]["live"]["packages"].append(
                {"distribution": "unexpected", "version": "1.0.0"}
            ),
            "packages do not exactly match the expected staged set",
        ),
    ],
)
def test_release_inventory_rejects_provenance_drift(mutation, message: str) -> None:
    status = _status()
    manifest = _manifest()
    inventory = _release_inventory(status, manifest)
    mutation(inventory)

    with pytest.raises(ValidationStatusError, match=message):
        validate_release_inventory(
            inventory,
            status=status,
            manifest=manifest,
        )


@pytest.mark.parametrize("core_version", ["01.2.3", "1.02.3", "1.2.03"])
def test_status_rejects_semver_leading_zero(tmp_path: Path, monkeypatch, core_version: str) -> None:
    value = _status()
    value["core_version"] = core_version
    value, report = _complete_status(tmp_path, value)
    monkeypatch.setattr(
        "scripts.validate_validation_status.load_manifest",
        lambda _path=None: _manifest(),
    )

    with pytest.raises(ValidationStatusError, match="exact X.Y.Z"):
        validate_status(value, report_path=report)
