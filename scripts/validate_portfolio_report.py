from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

if __package__:
    from scripts.validate_tools_manifest import PROJECT_ROOT
    from scripts.validate_validation_evidence import (
        EVIDENCE_ROOT,
        INDEX_PATH,
        evidence_index_sha256,
        load_evidence_index,
        validate_evidence_index,
    )
else:
    from validate_tools_manifest import PROJECT_ROOT  # type: ignore[import-not-found]
    from validate_validation_evidence import (  # type: ignore[import-not-found]
        EVIDENCE_ROOT,
        INDEX_PATH,
        evidence_index_sha256,
        load_evidence_index,
        validate_evidence_index,
    )

REPORT_PATH = PROJECT_ROOT / "docs" / "PORTFOLIO_VALIDATION_REPORT.md"
SCORES_START = "<!-- validation-scores:start -->"
SCORES_END = "<!-- validation-scores:end -->"
EVIDENCE_SHA_RE = re.compile(r"<!-- validation-evidence-index-sha256:([0-9a-f]{64}) -->")
PLACEHOLDER_RE = re.compile(
    r"\b(?:DRAFT|PENDING|TBD|TODO)\b|"
    r"<(?:repo|tag|version|commit|new-path|empty-directory)>",
)
VERDICTS = {
    "Validated for release.",
    "Validated with nonblocking limitations.",
    "Not validated; release blockers remain.",
}
REQUIRED_HEADINGS = (
    "## Executive verdict",
    "## Portfolio inventory and tested versions",
    "## Methods/environment",
    "## Numerical findings",
    "## Baseline/cross-app parity",
    "## Cold-start results",
    "## Release artifact provenance",
    "## Browser/privacy/accessibility",
    "## Documentation/license/citation",
    "## Project-standard scores",
    "## Release blockers",
    "## Nonblocking limitations",
    "## Issues/PRs opened",
    "## Exact commands",
    "## Appendix: numerical difference table",
    "## Appendix: network/storage observations",
)
REPOSITORY_ORDER = (
    "reblocke/wald-inference-core",
    "reblocke/scientific-applet-template",
    "reblocke/compatibility-curve",
    "reblocke/wald-likelihood-support",
    "reblocke/critical-effect-size",
    "reblocke/type-s-m-calibrator",
    "reblocke/precision-guardrail-planner",
    "reblocke/wald-inference-tools",
    "reblocke/conf_curve_likelihood",
)
SCORE_ORDER = (*REPOSITORY_ORDER, "portfolio")
DOMAINS = tuple("ABCDEFGH")
WEIGHTS_TENTHS = {
    "A": 200,
    "B": 100,
    "C": 150,
    "D": 200,
    "E": 100,
    "F": 100,
    "G": 75,
    "H": 75,
}
VALIDATED_MIN_NUMERATOR = 2550
CONDITIONAL_MIN_NUMERATOR = 2250
SCORE_TOP_LEVEL_FIELDS = {
    "schema_version",
    "weights_tenths",
    "validated_min_numerator",
    "conditional_min_numerator",
    "scores",
}
SCORE_FIELDS = {"name", "domains", "weighted_numerator"}
ORIGINAL_BLOCKERS = ("A-01", "A-02", "A-03", "EF-01", "EF-02")


class PortfolioReportError(ValueError):
    """Raised when the final portfolio report is incomplete or contradicts its rubric."""


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise PortfolioReportError(f"duplicate JSON key: {key!r}")
        value[key] = item
    return value


def _exact_fields(value: dict[str, Any], expected: set[str], location: str) -> None:
    missing = expected - value.keys()
    extra = value.keys() - expected
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing {sorted(missing)}")
        if extra:
            details.append(f"unexpected {sorted(extra)}")
        raise PortfolioReportError(f"{location}: {'; '.join(details)}")


def _extract_one_json_block(report: str, start_marker: str, end_marker: str) -> dict[str, Any]:
    if report.count(start_marker) != 1 or report.count(end_marker) != 1:
        marker_name = start_marker.removeprefix("<!-- ").removesuffix(" -->")
        raise PortfolioReportError(f"report must contain exactly one {marker_name}")
    start = report.index(start_marker) + len(start_marker)
    end = report.index(end_marker)
    if end <= start:
        raise PortfolioReportError(f"{start_marker} and {end_marker} are out of order")
    try:
        value = json.loads(report[start:end], object_pairs_hook=_strict_object)
    except json.JSONDecodeError as exc:
        raise PortfolioReportError(f"report score inventory is invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise PortfolioReportError("report score inventory must be an object")
    return value


def load_score_inventory(report: str) -> dict[str, Any]:
    return _extract_one_json_block(report, SCORES_START, SCORES_END)


def validate_score_inventory(scores: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _exact_fields(scores, SCORE_TOP_LEVEL_FIELDS, "report score inventory")
    if type(scores["schema_version"]) is not int or scores["schema_version"] != 1:
        raise PortfolioReportError("score inventory schema_version must equal 1")
    if scores["weights_tenths"] != WEIGHTS_TENTHS:
        raise PortfolioReportError("score inventory weights differ from the predeclared rubric")
    if scores["validated_min_numerator"] != VALIDATED_MIN_NUMERATOR:
        raise PortfolioReportError("validated threshold differs from the predeclared rubric")
    if scores["conditional_min_numerator"] != CONDITIONAL_MIN_NUMERATOR:
        raise PortfolioReportError("conditional threshold differs from the predeclared rubric")

    records = scores["scores"]
    if not isinstance(records, list):
        raise PortfolioReportError("score inventory scores must be an array")
    names: list[str] = []
    by_name: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        location = f"score inventory scores[{index}]"
        if not isinstance(record, dict):
            raise PortfolioReportError(f"{location} must be an object")
        _exact_fields(record, SCORE_FIELDS, location)
        name = record["name"]
        if not isinstance(name, str) or not name:
            raise PortfolioReportError(f"{location}.name must be non-empty")
        names.append(name)

        domains = record["domains"]
        if not isinstance(domains, dict) or set(domains) != set(DOMAINS):
            raise PortfolioReportError(f"{location}.domains must contain A through H exactly")
        if any(
            type(domains[domain]) is not int or not 0 <= domains[domain] <= 3 for domain in DOMAINS
        ):
            raise PortfolioReportError(f"{location}.domains scores must be integers from 0 to 3")
        expected_numerator = sum(domains[domain] * WEIGHTS_TENTHS[domain] for domain in DOMAINS)
        if (
            type(record["weighted_numerator"]) is not int
            or record["weighted_numerator"] != expected_numerator
        ):
            raise PortfolioReportError(
                f"{location}.weighted_numerator must equal the exact unrounded score numerator"
            )
        by_name[name] = record

    if names != list(SCORE_ORDER):
        raise PortfolioReportError(
            "score inventory must use canonical repository and portfolio order"
        )
    return by_name


def _section(report: str, heading: str) -> str:
    start = report.index(heading) + len(heading)
    match = re.search(r"^## ", report[start:], flags=re.MULTILINE)
    end = start + match.start() if match else len(report)
    return report[start:end]


def _expected_verdict(portfolio_score: dict[str, Any], blocking_count: int) -> str:
    domains = portfolio_score["domains"]
    numerator = portfolio_score["weighted_numerator"]
    if blocking_count or any(domains[domain] < 2 for domain in DOMAINS):
        return "Not validated; release blockers remain."
    if numerator < CONDITIONAL_MIN_NUMERATOR:
        return "Not validated; release blockers remain."
    if numerator >= VALIDATED_MIN_NUMERATOR:
        return "Validated for release."
    return "Validated with nonblocking limitations."


def validate_portfolio_report(
    report_path: Path,
    *,
    verdict: str,
    blocking_count: int,
    catalog_version: str,
    evidence_root: Path = EVIDENCE_ROOT,
    evidence_index_path: Path = INDEX_PATH,
) -> None:
    report = report_path.read_text(encoding="utf-8")
    missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in report]
    if missing_headings:
        raise PortfolioReportError(f"final report is missing required headings: {missing_headings}")
    positions = [report.index(heading) for heading in REQUIRED_HEADINGS]
    if positions != sorted(positions):
        raise PortfolioReportError("final report headings are not in the required order")
    placeholder = PLACEHOLDER_RE.search(report)
    if placeholder:
        raise PortfolioReportError(
            f"final report contains execution placeholder {placeholder.group(0)!r}"
        )

    executive = _section(report, "## Executive verdict")
    observed_verdicts = [candidate for candidate in VERDICTS if candidate in executive]
    if observed_verdicts != [verdict]:
        raise PortfolioReportError("executive verdict must contain exactly the status verdict")

    score_inventory = validate_score_inventory(load_score_inventory(report))
    rubric_verdict = _expected_verdict(score_inventory["portfolio"], blocking_count)
    if verdict != rubric_verdict:
        raise PortfolioReportError(
            f"verdict {verdict!r} contradicts the predeclared scoring rubric ({rubric_verdict!r})"
        )

    limitations = _section(report, "## Nonblocking limitations")
    if verdict == "Validated with nonblocking limitations." and not re.search(
        r"^\s*[-*] .+",
        limitations,
        flags=re.MULTILINE,
    ):
        raise PortfolioReportError(
            "conditional verdict requires a documented nonblocking limitation"
        )

    blocker_section = _section(report, "## Release blockers")
    missing_blockers = [blocker for blocker in ORIGINAL_BLOCKERS if blocker not in blocker_section]
    if missing_blockers:
        raise PortfolioReportError(f"release-blocker closure table is missing {missing_blockers}")
    if verdict != "Not validated; release blockers remain.":
        for blocker in ORIGINAL_BLOCKERS:
            row = next(
                (
                    line
                    for line in blocker_section.splitlines()
                    if line.lstrip().startswith("|") and blocker in line
                ),
                "",
            )
            if "closed" not in row.lower():
                raise PortfolioReportError(f"release blocker {blocker} is not explicitly closed")

    if "validation-evidence/index.json" not in report:
        raise PortfolioReportError("final report must reference the preserved evidence index")
    if "validation-evidence/commands/README_COMMANDS.md" not in report:
        raise PortfolioReportError("final report must reference the exact-command ledger")
    matches = EVIDENCE_SHA_RE.findall(report)
    if len(matches) != 1:
        raise PortfolioReportError(
            "final report must contain exactly one evidence-index SHA-256 marker"
        )
    evidence_index = load_evidence_index(evidence_index_path)
    validate_evidence_index(
        evidence_index,
        evidence_root=evidence_root,
        expected_catalog_version=catalog_version,
    )
    observed_index_sha = evidence_index_sha256(evidence_index_path)
    if matches[0] != observed_index_sha:
        raise PortfolioReportError(
            f"evidence-index SHA-256 mismatch: recorded {matches[0]}, observed {observed_index_sha}"
        )


def main() -> int:
    raise SystemExit(
        "Use scripts/validate_validation_status.py so report, status, and manifest "
        "are validated together."
    )


if __name__ == "__main__":
    main()
