from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path.cwd() / "scripts"))
import golden_baseline as gb  # noqa: E402


def collect(
    expected: Any,
    actual: Any,
    *,
    path: str,
    values: list[tuple[str, float, float]],
) -> None:
    if isinstance(expected, dict):
        for key, nested in expected.items():
            collect(nested, actual[key], path=f"{path}.{key}", values=values)
    elif isinstance(expected, list):
        for index, (nested, observed) in enumerate(zip(expected, actual, strict=True)):
            collect(nested, observed, path=f"{path}[{index}]", values=values)
    elif isinstance(expected, float):
        values.append((path, float(actual), expected))


def main() -> None:
    manifest = json.loads(gb.MANIFEST_PATH.read_text(encoding="utf-8"))
    case_map = {case.case_id: case for case in gb._cases()}
    all_values: list[tuple[str, float, float]] = []
    for record in manifest["cases"]:
        case_id = record["id"]
        expected = json.loads(
            (gb.GOLDEN_ROOT / record["expected_file"]).read_text(encoding="utf-8")
        )
        actual = gb._evaluate_case(case_map[case_id])
        case_values: list[tuple[str, float, float]] = []
        collect(expected, actual, path=f"${case_id}", values=case_values)
        all_values.extend(case_values)
        max_abs = max(
            ((abs(actual - expected), path) for path, actual, expected in case_values),
            default=(0.0, ""),
        )
        max_rel = max(
            (
                (
                    abs(actual - expected) / abs(expected)
                    if expected
                    else (0.0 if actual == expected else float("inf")),
                    path,
                )
                for path, actual, expected in case_values
            ),
            default=(0.0, ""),
        )
        print(
            "CASE",
            case_id,
            f"float_count={len(case_values)}",
            f"max_abs={max_abs[0]:.17g}",
            f"max_abs_path={max_abs[1]!r}",
            f"max_rel={max_rel[0]:.17g}",
            f"max_rel_path={max_rel[1]!r}",
        )

    absolute, absolute_path, absolute_actual, absolute_expected = max(
        ((abs(actual - expected), path, actual, expected) for path, actual, expected in all_values),
        default=(0.0, "", 0.0, 0.0),
    )
    relative, relative_path, relative_actual, relative_expected = max(
        (
            (
                abs(actual - expected) / abs(expected)
                if expected
                else (0.0 if actual == expected else float("inf")),
                path,
                actual,
                expected,
            )
            for path, actual, expected in all_values
        ),
        default=(0.0, "", 0.0, 0.0),
    )
    print(f"total_float_count={len(all_values)}")
    print(
        f"max_abs={absolute:.17g}",
        f"path={absolute_path!r}",
        f"actual_expected={(absolute_actual, absolute_expected)!r}",
    )
    print(
        f"max_rel={relative:.17g}",
        f"path={relative_path!r}",
        f"actual_expected={(relative_actual, relative_expected)!r}",
    )


if __name__ == "__main__":
    main()
