from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import subprocess
import tarfile
import zipfile
from pathlib import Path

if __package__:
    from scripts.build_site import build_site
    from scripts.validate_tools_manifest import (
        PROJECT_ROOT,
        load_manifest,
        validate_manifest,
    )
    from scripts.validate_validation_evidence import (
        EVIDENCE_ROOT,
        load_evidence_index,
        validate_evidence_index,
    )
    from scripts.validate_validation_status import load_status, validate_status
else:
    from build_site import build_site  # type: ignore[import-not-found]
    from validate_tools_manifest import (  # type: ignore[import-not-found]
        PROJECT_ROOT,
        load_manifest,
        validate_manifest,
    )
    from validate_validation_evidence import (  # type: ignore[import-not-found]
        EVIDENCE_ROOT,
        load_evidence_index,
        validate_evidence_index,
    )
    from validate_validation_status import (  # type: ignore[import-not-found]
        load_status,
        validate_status,
    )


def _source_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
    )
    relatives = [Path(item.decode()) for item in result.stdout.split(b"\0") if item]
    paths = [PROJECT_ROOT / relative for relative in relatives]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"tracked release source is missing: {missing[0]}")
    return paths


def _tar_bytes(version: str) -> bytes:
    raw = io.BytesIO()
    prefix = f"wald-inference-tools-v{version}"
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for path in _source_files():
            relative = path.relative_to(PROJECT_ROOT)
            data = path.read_bytes()
            info = tarfile.TarInfo(f"{prefix}/{relative.as_posix()}")
            info.size = len(data)
            info.mode = 0o755 if path.suffix == ".sh" else 0o644
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            archive.addfile(info, io.BytesIO(data))
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=0) as stream:
        stream.write(raw.getvalue())
    return compressed.getvalue()


def _site_zip_bytes(site: Path) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(
        output, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path in sorted(item for item in site.rglob("*") if item.is_file()):
            relative = path.relative_to(site).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            archive.writestr(info, path.read_bytes())
    return output.getvalue()


def _evidence_tar_bytes(version: str, evidence_root: Path = EVIDENCE_ROOT) -> bytes:
    raw = io.BytesIO()
    prefix = f"portfolio-validation-evidence-v{version}"
    paths = sorted(path for path in evidence_root.rglob("*") if path.is_file())
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for path in paths:
            relative = path.relative_to(evidence_root)
            data = path.read_bytes()
            info = tarfile.TarInfo(f"{prefix}/{relative.as_posix()}")
            info.size = len(data)
            info.mode = 0o644
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            archive.addfile(info, io.BytesIO(data))
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=0) as stream:
        stream.write(raw.getvalue())
    return compressed.getvalue()


def build_release(version: str, output: Path) -> list[Path]:
    manifest_path = PROJECT_ROOT / "data" / "tools.json"
    manifest = load_manifest(manifest_path)
    validate_manifest(manifest)
    if version != manifest["catalog_version"]:
        raise ValueError(
            f"release version {version} != catalog version {manifest['catalog_version']}"
        )

    output = output.resolve()
    if output == PROJECT_ROOT or PROJECT_ROOT not in output.parents:
        raise ValueError("release output must be a dedicated directory inside the repository")
    report_source = PROJECT_ROOT / "docs" / "PORTFOLIO_VALIDATION_REPORT.md"
    status_source = PROJECT_ROOT / "data" / "validation_status.json"
    evidence_root = PROJECT_ROOT / "validation-evidence"
    evidence_index_source = evidence_root / "index.json"
    missing_evidence = [
        path for path in (report_source, status_source, evidence_index_source) if not path.is_file()
    ]
    if missing_evidence:
        raise FileNotFoundError(f"validation release evidence is missing: {missing_evidence[0]}")
    validate_status(
        load_status(status_source),
        report_path=report_source,
        manifest_path=manifest_path,
    )
    validate_evidence_index(
        load_evidence_index(evidence_index_source),
        evidence_root=evidence_root,
        expected_catalog_version=version,
    )

    output.mkdir(parents=True, exist_ok=True)
    for path in output.iterdir():
        if path.is_file():
            path.unlink()
    site = PROJECT_ROOT / "site"
    build_site(site)
    artifacts = [
        output / f"wald-inference-tools-v{version}.tar.gz",
        output / f"wald-inference-tools-site-v{version}.zip",
        output / f"tools-v{version}.json",
        output / f"portfolio-validation-evidence-v{version}.tar.gz",
        output / f"validation-evidence-index-v{version}.json",
    ]
    artifacts[0].write_bytes(_tar_bytes(version))
    artifacts[1].write_bytes(_site_zip_bytes(site))
    artifacts[2].write_bytes(manifest_path.read_bytes())
    artifacts[3].write_bytes(_evidence_tar_bytes(version, evidence_root))
    artifacts[4].write_bytes(evidence_index_source.read_bytes())
    validation_sources = [
        (
            report_source,
            output / f"PORTFOLIO_VALIDATION_REPORT-v{version}.md",
        ),
        (
            status_source,
            output / f"validation_status-v{version}.json",
        ),
    ]
    for source, destination in validation_sources:
        destination.write_bytes(source.read_bytes())
        artifacts.append(destination)
    checksum_lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in artifacts
    ]
    checksums = output / "SHA256SUMS"
    checksums.write_text("".join(checksum_lines), encoding="utf-8", newline="\n")
    return [*artifacts, checksums]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "release")
    args = parser.parse_args()
    artifacts = build_release(args.version, args.output)
    for artifact in artifacts:
        print(f"{hashlib.sha256(artifact.read_bytes()).hexdigest()}  {artifact.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
