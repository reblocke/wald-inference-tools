from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


class Diff:
    def __init__(self) -> None:
        self.count = 0
        self.max_abs = 0.0
        self.max_rel = 0.0
        self.max_abs_label = ""
        self.max_rel_label = ""
        self.max_abs_values = (0.0, 0.0)
        self.max_rel_values = (0.0, 0.0)

    def add(self, label: str, actual: float, expected: float) -> None:
        actual = float(actual)
        expected = float(expected)
        absolute = abs(actual - expected)
        relative = absolute / abs(expected) if expected else (0.0 if absolute == 0.0 else math.inf)
        self.count += 1
        if absolute > self.max_abs:
            self.max_abs = absolute
            self.max_abs_label = label
            self.max_abs_values = (actual, expected)
        if relative > self.max_rel:
            self.max_rel = relative
            self.max_rel_label = label
            self.max_rel_values = (actual, expected)

    def report(self, mode: str) -> None:
        print(f"mode={mode}")
        print(f"numeric_count={self.count}")
        print(
            f"max_abs={self.max_abs:.17g}",
            f"label={self.max_abs_label!r}",
            f"actual_expected={self.max_abs_values!r}",
        )
        print(
            f"max_rel={self.max_rel:.17g}",
            f"label={self.max_rel_label!r}",
            f"actual_expected={self.max_rel_values!r}",
        )


def compatibility(diff: Diff) -> None:
    from compatibility_curve import CompatibilityRequest, calculate

    fixture = json.loads(
        Path("tests/fixtures/legacy_compatibility.json").read_text(encoding="utf-8")
    )
    for case_id in ("B01", "B02", "B03"):
        case = fixture["cases"][case_id]
        response = calculate(CompatibilityRequest.from_mapping(case["request"]))
        expected = case["expected"]
        reconstruction = response["reconstruction"]
        threshold = response["thresholds"][0]
        for key in (
            "estimate_display",
            "estimate_working",
            "standard_error_working",
            "compatibility_at_null",
        ):
            diff.add(f"{case_id}.{key}", reconstruction[key], expected[key])
        diff.add(
            f"{case_id}.threshold_working",
            threshold["effect_working"],
            expected["threshold_working"],
        )
        diff.add(
            f"{case_id}.threshold_compatibility",
            threshold["compatibility"],
            expected["threshold_compatibility"],
        )
        if case_id != "B03":
            diff.add(f"{case_id}.grid_peak", max(response["grid"]["compatibility"]), 1.0)
        else:
            diff.add(
                "B03.display_first",
                response["grid"]["effect_display"][0],
                expected["display_first"],
            )
            diff.add(
                "B03.display_last",
                response["grid"]["effect_display"][-1],
                expected["display_last"],
            )
    for case_id in (
        "B08a-additive-midpoint",
        "B08b-s-minus-2-clipping",
        "B08c-log-likelihood-fallback",
        "B08d-ratio-natural-clipping",
    ):
        case = fixture["cases"][case_id]
        response = calculate(CompatibilityRequest.from_mapping(case["request"]))
        for key, expected in case["expected"].items():
            diff.add(f"{case_id}.{key}", response["reconstruction"][key], expected)


def critical(diff: Diff) -> None:
    from critical_effect_size import CriticalEffectRequest, calculate

    fixture = json.loads(
        Path("tests/fixtures/integrated_baseline/critical_effect_scenarios.json").read_text(
            encoding="utf-8"
        )
    )
    for index, case in enumerate(fixture["cases"]):
        response = calculate(
            CriticalEffectRequest(
                precision_mode="direct_se",
                effect_type="mean_difference",
                observed_estimate=None,
                ci_lower=None,
                ci_upper=None,
                standard_error=case["standard_error"],
                null_value=0.0,
                alpha=0.05,
                selection_rule="two_sided_p_lt_alpha",
                target_probability=0.8,
                meaningful_effect=None,
                information_multiplier=1.0,
                display_min=None,
                display_max=None,
            )
        )
        positive = next(
            row
            for row in response.critical_effect["current"]["solutions"]
            if row["direction"] == "positive"
        )
        diff.add(
            f"case{index}.exact_positive_working",
            positive["critical_effect_working"],
            case["exact_positive_working"],
        )
        diff.add(
            f"case{index}.legacy_distance_working",
            response.legacy_benchmark_optional["current"]["working_distance_from_null"],
            case["legacy_distance_working"],
        )


def type_sm(diff: Diff) -> None:
    from type_sm_calibrator import CalibrationRequest, calculate

    fixture = json.loads(
        Path("tests/fixtures/integrated_baseline/type_sm_scenarios.json").read_text(
            encoding="utf-8"
        )
    )
    for case in fixture["cases"]:
        result = calculate(CalibrationRequest.from_mapping(case["request"]))
        case_id = case["id"]
        diff.add(
            f"{case_id}.current_se",
            result.precision["current_se_working"],
            case["expected_current_se"],
        )
        for display, expected_values in case["expected_scenarios"].items():
            row = min(
                result.scenarios,
                key=lambda candidate: abs(candidate["true_effect_display"] - float(display)),
            )
            actual_values = (
                row["selected_claim_probability"],
                row["type_s"],
                row["type_m"],
                row["observed_exaggeration"],
            )
            for key, actual, expected in zip(
                ("selected_probability", "type_s", "type_m", "observed_exaggeration"),
                actual_values,
                expected_values,
                strict=True,
            ):
                if expected is None:
                    if actual is not None:
                        raise AssertionError(f"{case_id}.{display}.{key}: expected None")
                else:
                    diff.add(f"{case_id}.{display}.{key}", actual, expected)


def precision(diff: Diff) -> None:
    from precision_guardrail import PlanningRequest, calculate

    fixture = json.loads(
        Path("tests/fixtures/integrated_baseline/precision_b06_b07.json").read_text(
            encoding="utf-8"
        )
    )
    payload: dict[str, Any] = {
        "precision_mode": "direct_se",
        "effect_type": "mean_difference",
        "standard_error": 0.15816617164664273,
        "ci_lower": None,
        "ci_upper": None,
        "null_value": 0.0,
        "target_true_effect": 0.2,
        "alpha": 0.05,
        "selection_rule": "two_sided_p_lt_alpha",
        "claim_direction": "positive",
        "claim_threshold": None,
        "minimum_selected_claim_probability": 0.8,
        "maximum_type_s": 0.01,
        "maximum_type_m": 1.25,
        "sensitivity_enabled": False,
        "sensitivity_min": None,
        "sensitivity_max": None,
        "sensitivity_points": 19,
        "sample_size_projection_enabled": False,
        "current_effective_n": None,
    }
    response = calculate(PlanningRequest.from_mapping(payload)).to_payload()
    diff.add(
        "B06.current_se",
        response["current_precision"]["current_se_working"],
        fixture["b06"]["current_se_working"],
    )
    key_pairs = (
        ("requested_value", "requested_value"),
        ("required_se_working", "required_se"),
        ("required_information_multiplier", "required_information_multiplier"),
        ("approx_95_ci_width_working", "approx_95_ci_width_working"),
        ("achieved_selected_claim_probability", "achieved_power"),
        ("achieved_type_s", "achieved_type_s"),
        ("achieved_type_m", "achieved_type_m"),
    )
    for index, (actual, expected) in enumerate(
        zip(response["per_target_results"], fixture["b06"]["targets"], strict=True)
    ):
        if actual["target_key"] != expected["target"]:
            raise AssertionError(f"B06 target order mismatch at {index}")
        for actual_key, expected_key in key_pairs:
            diff.add(
                f"B06.target{index}.{actual_key}",
                actual[actual_key],
                expected[expected_key],
            )

    null_payload = {**payload, "target_true_effect": 0.0}
    null = calculate(PlanningRequest.from_mapping(null_payload)).to_payload()
    if null["per_target_results"][0]["solver_note"] != fixture["b07"]["null_target_note"]:
        raise AssertionError("B07 null note mismatch")
    threshold_payload = {
        **payload,
        "target_true_effect": 0.1,
        "selection_rule": "ci_excludes_mcid",
        "claim_threshold": 0.2,
        "maximum_type_s": None,
        "maximum_type_m": None,
    }
    threshold = calculate(PlanningRequest.from_mapping(threshold_payload)).to_payload()
    if (
        threshold["per_target_results"][0]["solver_note"]
        != fixture["b07"]["threshold_infeasible_note"]
    ):
        raise AssertionError("B07 threshold note mismatch")
    print("B07_messages_exact=true")


def main() -> None:
    mode = sys.argv[1]
    function = {
        "compatibility": compatibility,
        "critical": critical,
        "type-sm": type_sm,
        "precision": precision,
    }[mode]
    diff = Diff()
    function(diff)
    diff.report(mode)


if __name__ == "__main__":
    main()
