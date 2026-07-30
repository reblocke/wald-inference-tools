from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from scripts import build_release_artifacts


def test_validation_evidence_is_a_direct_checksummed_release_asset(
    tmp_path: Path, monkeypatch
) -> None:
    project_root = tmp_path / "project"
    (project_root / "data").mkdir(parents=True)
    (project_root / "docs").mkdir()
    (project_root / "site").mkdir()
    evidence_root = project_root / "validation-evidence"
    evidence_root.mkdir()
    evidence_index = evidence_root / "index.json"
    evidence_index.write_text('{"schema_version": 1}\n', encoding="utf-8")
    (evidence_root / "lane.md").write_text("# Preserved lane\n", encoding="utf-8")
    (project_root / "data" / "tools.json").write_text(
        '{"catalog_version": "0.2.0"}\n',
        encoding="utf-8",
    )
    report = project_root / "docs" / "PORTFOLIO_VALIDATION_REPORT.md"
    status = project_root / "data" / "validation_status.json"
    report.write_text("# Portfolio validation\n", encoding="utf-8")
    status.write_text('{"schema_version": 1}\n', encoding="utf-8")

    monkeypatch.setattr(build_release_artifacts, "PROJECT_ROOT", project_root)
    monkeypatch.setattr(build_release_artifacts, "build_site", lambda _site: None)
    monkeypatch.setattr(build_release_artifacts, "_tar_bytes", lambda _version: b"source")
    monkeypatch.setattr(build_release_artifacts, "_site_zip_bytes", lambda _site: b"site")
    monkeypatch.setattr(
        build_release_artifacts,
        "_evidence_tar_bytes",
        lambda _version, _root: b"evidence",
    )
    monkeypatch.setattr(
        build_release_artifacts,
        "load_manifest",
        lambda _path: {"catalog_version": "0.2.0"},
    )
    monkeypatch.setattr(build_release_artifacts, "validate_manifest", lambda _manifest: None)
    monkeypatch.setattr(build_release_artifacts, "load_status", lambda _path: {})
    monkeypatch.setattr(
        build_release_artifacts,
        "validate_status",
        lambda _status, **_kwargs: None,
    )
    monkeypatch.setattr(build_release_artifacts, "load_evidence_index", lambda _path: {})
    monkeypatch.setattr(
        build_release_artifacts,
        "validate_evidence_index",
        lambda _index, **_kwargs: None,
    )

    output = project_root / "release"
    artifacts = build_release_artifacts.build_release("0.2.0", output)

    report_asset = output / "PORTFOLIO_VALIDATION_REPORT-v0.2.0.md"
    status_asset = output / "validation_status-v0.2.0.json"
    evidence_asset = output / "portfolio-validation-evidence-v0.2.0.tar.gz"
    evidence_index_asset = output / "validation-evidence-index-v0.2.0.json"
    assert report_asset.read_bytes() == report.read_bytes()
    assert status_asset.read_bytes() == status.read_bytes()
    assert evidence_asset.read_bytes() == b"evidence"
    assert evidence_index_asset.read_bytes() == evidence_index.read_bytes()
    assert report_asset in artifacts
    assert status_asset in artifacts
    assert evidence_asset in artifacts
    assert evidence_index_asset in artifacts

    checksums = (output / "SHA256SUMS").read_text(encoding="utf-8")
    assert f"{hashlib.sha256(report.read_bytes()).hexdigest()}  {report_asset.name}\n" in checksums
    assert f"{hashlib.sha256(status.read_bytes()).hexdigest()}  {status_asset.name}\n" in checksums
    assert f"{hashlib.sha256(b'evidence').hexdigest()}  {evidence_asset.name}\n" in checksums
    assert (
        f"{hashlib.sha256(evidence_index.read_bytes()).hexdigest()}  "
        f"{evidence_index_asset.name}\n" in checksums
    )


def test_release_build_rejects_missing_validation_evidence(tmp_path: Path, monkeypatch) -> None:
    project_root = tmp_path / "project"
    (project_root / "data").mkdir(parents=True)
    (project_root / "docs").mkdir()
    (project_root / "data" / "tools.json").write_text(
        '{"catalog_version": "0.2.0"}\n',
        encoding="utf-8",
    )
    (project_root / "docs" / "PORTFOLIO_VALIDATION_REPORT.md").write_text(
        "# Portfolio validation\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_release_artifacts, "PROJECT_ROOT", project_root)
    monkeypatch.setattr(
        build_release_artifacts,
        "load_manifest",
        lambda _path: {"catalog_version": "0.2.0"},
    )
    monkeypatch.setattr(build_release_artifacts, "validate_manifest", lambda _manifest: None)

    with pytest.raises(FileNotFoundError, match="validation release evidence is missing"):
        build_release_artifacts.build_release("0.2.0", project_root / "release")


def test_release_build_requires_catalog_version(tmp_path: Path, monkeypatch) -> None:
    project_root = tmp_path / "project"
    (project_root / "data").mkdir(parents=True)
    (project_root / "data" / "tools.json").write_text(
        '{"catalog_version": "0.2.0"}\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(build_release_artifacts, "PROJECT_ROOT", project_root)
    monkeypatch.setattr(
        build_release_artifacts,
        "load_manifest",
        lambda _path: {"catalog_version": "0.2.0"},
    )
    monkeypatch.setattr(build_release_artifacts, "validate_manifest", lambda _manifest: None)

    with pytest.raises(ValueError, match="release version"):
        build_release_artifacts.build_release("0.1.0", project_root / "release")
    assert not (project_root / "release").exists()


def test_invalid_status_creates_no_release_artifact(tmp_path: Path, monkeypatch) -> None:
    project_root = tmp_path / "project"
    (project_root / "data").mkdir(parents=True)
    (project_root / "docs").mkdir()
    evidence_root = project_root / "validation-evidence"
    evidence_root.mkdir()
    (evidence_root / "index.json").write_text("{}\n", encoding="utf-8")
    (project_root / "data" / "tools.json").write_text(
        '{"catalog_version": "0.2.0"}\n',
        encoding="utf-8",
    )
    (project_root / "data" / "validation_status.json").write_text("{}\n", encoding="utf-8")
    (project_root / "docs" / "PORTFOLIO_VALIDATION_REPORT.md").write_text(
        "# Invalid\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(build_release_artifacts, "PROJECT_ROOT", project_root)
    monkeypatch.setattr(
        build_release_artifacts,
        "load_manifest",
        lambda _path: {"catalog_version": "0.2.0"},
    )
    monkeypatch.setattr(build_release_artifacts, "validate_manifest", lambda _manifest: None)
    monkeypatch.setattr(build_release_artifacts, "load_status", lambda _path: {})
    monkeypatch.setattr(
        build_release_artifacts,
        "validate_status",
        lambda _status, **_kwargs: (_ for _ in ()).throw(ValueError("invalid status")),
    )

    with pytest.raises(ValueError, match="invalid status"):
        build_release_artifacts.build_release("0.2.0", project_root / "release")
    assert not (project_root / "release").exists()
