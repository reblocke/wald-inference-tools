from __future__ import annotations

import argparse
import os

if __package__:
    from scripts.validate_tools_manifest import PROJECT_ROOT, load_manifest, validate_manifest
else:
    from validate_tools_manifest import (  # type: ignore[import-not-found]
        PROJECT_ROOT,
        load_manifest,
        validate_manifest,
    )


def check_release_metadata(tag: str) -> str:
    manifest = load_manifest()
    validate_manifest(manifest)
    version = manifest["catalog_version"]
    if tag != f"v{version}":
        raise ValueError(f"tag {tag!r} does not match catalog version v{version}")
    cff = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8")
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    license_text = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")
    required = {
        "CITATION.cff": f"version: {version}",
        "CHANGELOG.md": f"## [{version}]",
        "pyproject.toml": f'version = "{version}"',
        "LICENSE": "Copyright (c) 2026 Brian Locke",
    }
    values = {
        "CITATION.cff": cff,
        "CHANGELOG.md": changelog,
        "pyproject.toml": pyproject,
        "LICENSE": license_text,
    }
    for name, needle in required.items():
        if needle not in values[name]:
            raise ValueError(f"{name} does not contain release marker {needle!r}")
    return version


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", default=os.environ.get("GITHUB_REF_NAME"))
    args = parser.parse_args()
    if not args.tag:
        parser.error("--tag is required outside a tag workflow")
    version = check_release_metadata(args.tag)
    print(f"Release metadata agrees on v{version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
