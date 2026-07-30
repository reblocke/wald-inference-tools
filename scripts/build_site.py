from __future__ import annotations

import argparse
import shutil
from pathlib import Path

if __package__:
    from scripts.check_links import check_local_links
    from scripts.validate_tools_manifest import PROJECT_ROOT, load_manifest, validate_manifest
else:
    from check_links import check_local_links  # type: ignore[import-not-found]
    from validate_tools_manifest import (  # type: ignore[import-not-found]
        PROJECT_ROOT,
        load_manifest,
        validate_manifest,
    )

SITE_FILES = ("index.html", "styles.css", "app.js")
SITE_DIRECTORIES = ("data", "docs")


def build_site(output: Path) -> None:
    output = output.resolve()
    if output == PROJECT_ROOT or PROJECT_ROOT not in output.parents:
        raise ValueError("site output must be a dedicated directory inside the repository")
    validate_manifest(load_manifest())
    check_local_links()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for relative in SITE_FILES:
        shutil.copy2(PROJECT_ROOT / relative, output / relative)
    for relative in SITE_DIRECTORIES:
        shutil.copytree(PROJECT_ROOT / relative, output / relative)
    (output / ".nojekyll").write_bytes(b"")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "site")
    args = parser.parse_args()
    build_site(args.output)
    print(f"Built static catalog at {args.output.resolve()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
