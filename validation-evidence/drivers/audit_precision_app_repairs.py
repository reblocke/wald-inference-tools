from __future__ import annotations

from precision_guardrail import PlanningRequest, calculate
from wald_inference import precision_target_results

CASES = (
    (0.4, "positive", 1.0, 5.0, 0.1),
    (0.4, "positive", 1.0, 10.0, 0.1),
    (0.6, "positive", 1.0, 5.0, 0.2),
    (0.6, "positive", 1.0, 10.0, 0.2),
    (-0.4, "negative", -1.0, 5.0, 0.1),
    (-0.4, "negative", -1.0, 10.0, 0.1),
    (-0.6, "negative", -1.0, 5.0, 0.2),
    (-0.6, "negative", -1.0, 10.0, 0.2),
)


def main() -> None:
    for effect, direction, threshold, current_se, target in CASES:
        request = PlanningRequest.from_mapping(
            {
                "precision_mode": "direct_se",
                "effect_type": "mean_difference",
                "standard_error": current_se,
                "ci_lower": None,
                "ci_upper": None,
                "null_value": 0.0,
                "target_true_effect": effect,
                "alpha": 0.05,
                "selection_rule": "estimate_exceeds_mcid_and_p_lt_alpha",
                "claim_direction": direction,
                "claim_threshold": threshold,
                "minimum_selected_claim_probability": target,
                "maximum_type_s": None,
                "maximum_type_m": None,
                "sensitivity_enabled": False,
                "sensitivity_min": None,
                "sensitivity_max": None,
                "sensitivity_points": 19,
                "sample_size_projection_enabled": False,
                "current_effective_n": None,
            }
        )
        payload = calculate(request).to_payload()
        [app_row] = payload["per_target_results"]
        [core_row] = precision_target_results(
            effect,
            null_working=0.0,
            current_se=current_se,
            alpha=0.05,
            selection_rule="estimate_exceeds_mcid_and_p_lt_alpha",
            claim_direction=direction,
            threshold_working=threshold,
            target_power=target,
        )
        assert core_row.required_se is not None
        assert app_row["required_se_working"] == core_row.required_se
        assert app_row["feasible"] is True
        assert payload["joint_result"]["feasible"] is True
        print(
            "APP_CASE",
            f"effect={effect}",
            f"direction={direction}",
            f"current_se={current_se}",
            f"target={target}",
            f"required_se={app_row['required_se_working']:.17g}",
            f"achieved={app_row['achieved_selected_claim_probability']:.17g}",
        )


if __name__ == "__main__":
    main()
