from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_validated_catalog_release_is_published_stable() -> None:
    workflow = (PROJECT_ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    maintenance = (PROJECT_ROOT / "docs/MAINTENANCE.md").read_text(encoding="utf-8")
    maintenance_text = " ".join(maintenance.split())

    assert "--prerelease" not in workflow
    assert "--draft" in workflow
    assert "--draft=false" in workflow
    assert "--json isPrerelease" in workflow
    assert "--json isImmutable" in workflow
    assert "independent portfolio-validation" in maintenance_text
    assert "v0.2.0 and later validation-bearing tags publish as stable releases" in maintenance_text
