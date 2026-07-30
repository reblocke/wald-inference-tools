from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from scripts.validate_portfolio_report import (
    CONDITIONAL_MIN_NUMERATOR,
    DOMAINS,
    ORIGINAL_BLOCKERS,
    REQUIRED_HEADINGS,
    SCORE_ORDER,
    SCORES_END,
    SCORES_START,
    VALIDATED_MIN_NUMERATOR,
    WEIGHTS_TENTHS,
    PortfolioReportError,
    validate_portfolio_report,
)
from scripts.validate_validation_evidence import REQUIRED_KINDS


def _write_evidence(root: Path) -> tuple[Path, str]:
    root.mkdir(parents=True)
    files = []
    for index, kind in enumerate(sorted(REQUIRED_KINDS)):
        relative = f"records/{index:02d}-{kind}.txt"
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"Evidence for {kind}.\n", encoding="utf-8")
        files.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "kind": kind,
                "description": f"Preserved {kind} evidence.",
            }
        )
    index_path = root / "index.json"
    index = {
        "schema_version": 1,
        "catalog_version": "0.2.0",
        "validated_at": "2026-07-30T15:00:00Z",
        "files": files,
    }
    index_path.write_text(
        f"{json.dumps(index, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return index_path, hashlib.sha256(index_path.read_bytes()).hexdigest()


def _domains(verdict: str) -> dict[str, int]:
    if verdict == "Validated for release.":
        return {domain: 3 for domain in DOMAINS}
    if verdict == "Validated with nonblocking limitations.":
        result = {domain: 2 for domain in DOMAINS}
        for domain in ("A", "D", "H"):
            result[domain] = 3
        return result
    return {domain: 1 for domain in DOMAINS}


def _scores(verdict: str) -> dict:
    portfolio_domains = _domains(verdict)
    records = []
    for name in SCORE_ORDER:
        domains = portfolio_domains if name == "portfolio" else {domain: 3 for domain in DOMAINS}
        records.append(
            {
                "name": name,
                "domains": domains,
                "weighted_numerator": sum(
                    domains[domain] * WEIGHTS_TENTHS[domain] for domain in DOMAINS
                ),
            }
        )
    return {
        "schema_version": 1,
        "weights_tenths": WEIGHTS_TENTHS,
        "validated_min_numerator": VALIDATED_MIN_NUMERATOR,
        "conditional_min_numerator": CONDITIONAL_MIN_NUMERATOR,
        "scores": records,
    }


def _write_report(
    path: Path,
    *,
    verdict: str = "Validated with nonblocking limitations.",
    evidence_sha: str,
) -> None:
    sections = []
    for heading in REQUIRED_HEADINGS:
        body = "Completed evidence.\n"
        if heading == "## Executive verdict":
            body = f"**{verdict}**\n"
        elif heading == "## Project-standard scores":
            body = (
                f"{SCORES_START}\n"
                f"{json.dumps(_scores(verdict), indent=2, sort_keys=True)}\n"
                f"{SCORES_END}\n"
            )
        elif heading == "## Release blockers":
            rows = "\n".join(
                f"| {blocker} | closed | exact evidence |" for blocker in ORIGINAL_BLOCKERS
            )
            body = f"| ID | Status | Evidence |\n|---|---|---|\n{rows}\n"
        elif heading == "## Nonblocking limitations":
            body = "- Annotated tags are unsigned but exact objects were verified.\n"
        elif heading == "## Exact commands":
            body = (
                "Every invocation and exit code is preserved in "
                "`validation-evidence/commands/README_COMMANDS.md`.\n"
            )
        sections.append(f"{heading}\n\n{body}")
    path.write_text(
        "# Portfolio validation report\n\n"
        f"Evidence index: `validation-evidence/index.json`.\n"
        f"<!-- validation-evidence-index-sha256:{evidence_sha} -->\n\n" + "\n".join(sections),
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    ("verdict", "blocking_count"),
    [
        ("Validated for release.", 0),
        ("Validated with nonblocking limitations.", 0),
        ("Not validated; release blockers remain.", 1),
    ],
)
def test_report_linter_accepts_all_three_rubric_paths(
    tmp_path: Path,
    verdict: str,
    blocking_count: int,
) -> None:
    evidence_root = tmp_path / "validation-evidence"
    index_path, evidence_sha = _write_evidence(evidence_root)
    report = tmp_path / "report.md"
    _write_report(report, verdict=verdict, evidence_sha=evidence_sha)

    validate_portfolio_report(
        report,
        verdict=verdict,
        blocking_count=blocking_count,
        catalog_version="0.2.0",
        evidence_root=evidence_root,
        evidence_index_path=index_path,
    )


def test_report_linter_rejects_placeholders_and_missing_headings(tmp_path: Path) -> None:
    evidence_root = tmp_path / "validation-evidence"
    index_path, evidence_sha = _write_evidence(evidence_root)
    report = tmp_path / "report.md"
    _write_report(report, evidence_sha=evidence_sha)
    report.write_text(
        report.read_text(encoding="utf-8")
        .replace("Completed evidence.", "PENDING", 1)
        .replace("## Numerical findings", "## Removed numerical section"),
        encoding="utf-8",
    )

    with pytest.raises(PortfolioReportError, match="missing required headings"):
        validate_portfolio_report(
            report,
            verdict="Validated with nonblocking limitations.",
            blocking_count=0,
            catalog_version="0.2.0",
            evidence_root=evidence_root,
            evidence_index_path=index_path,
        )


def test_report_linter_enforces_exact_score_math_and_verdict(tmp_path: Path) -> None:
    evidence_root = tmp_path / "validation-evidence"
    index_path, evidence_sha = _write_evidence(evidence_root)
    report = tmp_path / "report.md"
    _write_report(report, evidence_sha=evidence_sha)
    report.write_text(
        report.read_text(encoding="utf-8").replace(
            '"weighted_numerator": 2475',
            '"weighted_numerator": 2474',
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(PortfolioReportError, match="exact unrounded"):
        validate_portfolio_report(
            report,
            verdict="Validated with nonblocking limitations.",
            blocking_count=0,
            catalog_version="0.2.0",
            evidence_root=evidence_root,
            evidence_index_path=index_path,
        )


def test_report_linter_rejects_evidence_index_digest_mismatch(tmp_path: Path) -> None:
    evidence_root = tmp_path / "validation-evidence"
    index_path, _ = _write_evidence(evidence_root)
    report = tmp_path / "report.md"
    _write_report(report, evidence_sha="0" * 64)

    with pytest.raises(PortfolioReportError, match="evidence-index SHA-256 mismatch"):
        validate_portfolio_report(
            report,
            verdict="Validated with nonblocking limitations.",
            blocking_count=0,
            catalog_version="0.2.0",
            evidence_root=evidence_root,
            evidence_index_path=index_path,
        )
