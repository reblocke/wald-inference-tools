from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_catalog_release_is_a_candidate_until_independent_validation() -> None:
    workflow = (PROJECT_ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    maintenance = (PROJECT_ROOT / "docs/MAINTENANCE.md").read_text(encoding="utf-8")
    maintenance_text = " ".join(maintenance.split())

    assert "--prerelease" in workflow
    assert "independent portfolio-validation" in maintenance_text
    assert "Stable promotion is an explicit post-validation action" in maintenance_text
