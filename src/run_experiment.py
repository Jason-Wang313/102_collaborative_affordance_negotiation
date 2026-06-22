import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 102_2026
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

V5 = "risk_calibrated_collaborative_affordance_v5"
ORACLE = "oracle_joint_intent_capability_planner"
HARD_SPLITS = {
    "burden_sensitive_shift",
    "false_clarification_shift",
    "overtrust_safety_shift",
    "combined_extreme",
}

METRICS = [
    "success",
    "physical_violation",
    "human_burden",
    "intent_error",
    "overpromise",
    "autonomy_conflict",
    "unnecessary_query",
    "negotiation_rounds",
    "ece",
    "regret",
    "utility",
]

TASKS = [
    {"task": "handover_grip_choice", "difficulty": 0.052, "intent_need": 0.88, "capability_need": 0.70, "burden_sensitivity": 0.46, "safety_need": 0.44, "role_need": 0.58},
    {"task": "co_carry_doorway", "difficulty": 0.078, "intent_need": 0.80, "capability_need": 0.94, "burden_sensitivity": 0.66, "safety_need": 0.80, "role_need": 0.86},
    {"task": "assisted_assembly", "difficulty": 0.070, "intent_need": 0.92, "capability_need": 0.78, "burden_sensitivity": 0.60, "safety_need": 0.62, "role_need": 0.74},
    {"task": "collaborative_sorting", "difficulty": 0.050, "intent_need": 0.84, "capability_need": 0.60, "burden_sensitivity": 0.44, "safety_need": 0.42, "role_need": 0.50},
    {"task": "tool_use_handoff", "difficulty": 0.073, "intent_need": 0.88, "capability_need": 0.86, "burden_sensitivity": 0.64, "safety_need": 0.70, "role_need": 0.78},
    {"task": "shared_fixture_insertion", "difficulty": 0.081, "intent_need": 0.86, "capability_need": 0.90, "burden_sensitivity": 0.72, "safety_need": 0.76, "role_need": 0.88},
]

REGIMES = [
    {"regime": "ambiguous_intent", "intent_ambiguity": 0.88, "capability_mismatch": 0.26, "safety_pressure": 0.28, "role_conflict": 0.38, "query_noise": 0.30},
    {"regime": "asymmetric_reach", "intent_ambiguity": 0.44, "capability_mismatch": 0.82, "safety_pressure": 0.54, "role_conflict": 0.58, "query_noise": 0.20},
    {"regime": "load_sharing_mismatch", "intent_ambiguity": 0.52, "capability_mismatch": 0.86, "safety_pressure": 0.74, "role_conflict": 0.72, "query_noise": 0.24},
    {"regime": "occluded_human_goal", "intent_ambiguity": 0.80, "capability_mismatch": 0.44, "safety_pressure": 0.40, "role_conflict": 0.45, "query_noise": 0.55},
    {"regime": "ergonomic_constraint", "intent_ambiguity": 0.50, "capability_mismatch": 0.72, "safety_pressure": 0.68, "role_conflict": 0.62, "query_noise": 0.28},
    {"regime": "role_switch_request", "intent_ambiguity": 0.76, "capability_mismatch": 0.58, "safety_pressure": 0.46, "role_conflict": 0.88, "query_noise": 0.36},
    {"regime": "conflicting_safety_preference", "intent_ambiguity": 0.70, "capability_mismatch": 0.74, "safety_pressure": 0.84, "role_conflict": 0.76, "query_noise": 0.45},
    {"regime": "temporal_commitment_drift", "intent_ambiguity": 0.82, "capability_mismatch": 0.66, "safety_pressure": 0.60, "role_conflict": 0.82, "query_noise": 0.62},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "intent_shift": 0.08, "capability_shift": 0.04, "feedback_delay": 0.00, "burden_pressure": 0.08, "false_query_pressure": 0.06, "overtrust_pressure": 0.04},
    {"split": "intent_ambiguity_shift", "stress": 0.50, "intent_shift": 0.68, "capability_shift": 0.12, "feedback_delay": 0.14, "burden_pressure": 0.18, "false_query_pressure": 0.24, "overtrust_pressure": 0.12},
    {"split": "capability_shift", "stress": 0.52, "intent_shift": 0.24, "capability_shift": 0.70, "feedback_delay": 0.12, "burden_pressure": 0.18, "false_query_pressure": 0.18, "overtrust_pressure": 0.42},
    {"split": "delayed_human_feedback", "stress": 0.50, "intent_shift": 0.46, "capability_shift": 0.30, "feedback_delay": 0.70, "burden_pressure": 0.28, "false_query_pressure": 0.32, "overtrust_pressure": 0.22},
    {"split": "burden_sensitive_shift", "stress": 0.60, "intent_shift": 0.54, "capability_shift": 0.42, "feedback_delay": 0.42, "burden_pressure": 0.86, "false_query_pressure": 0.50, "overtrust_pressure": 0.28},
    {"split": "false_clarification_shift", "stress": 0.64, "intent_shift": 0.60, "capability_shift": 0.34, "feedback_delay": 0.46, "burden_pressure": 0.72, "false_query_pressure": 0.88, "overtrust_pressure": 0.32},
    {"split": "overtrust_safety_shift", "stress": 0.70, "intent_shift": 0.52, "capability_shift": 0.64, "feedback_delay": 0.38, "burden_pressure": 0.50, "false_query_pressure": 0.42, "overtrust_pressure": 0.86},
    {"split": "combined_extreme", "stress": 0.84, "intent_shift": 0.72, "capability_shift": 0.70, "feedback_delay": 0.62, "burden_pressure": 0.78, "false_query_pressure": 0.74, "overtrust_pressure": 0.78},
]

METHODS = [
    {"method": "robot_capability_only_planner", "base": 0.648, "intent": 0.08, "capability": 0.68, "query": 0.04, "role": 0.12, "risk": 0.42, "burden_control": 0.12, "calibration": 0.20, "active_repair": 0.00, "human_model": 0.05, "overpromise_control": 0.22, "cost": 0.05},
    {"method": "intent_only_follower", "base": 0.670, "intent": 0.68, "capability": 0.14, "query": 0.04, "role": 0.18, "risk": 0.14, "burden_control": 0.10, "calibration": 0.22, "active_repair": 0.02, "human_model": 0.40, "overpromise_control": 0.10, "cost": 0.05},
    {"method": "language_affordance_planner", "base": 0.690, "intent": 0.57, "capability": 0.38, "query": 0.18, "role": 0.25, "risk": 0.28, "burden_control": 0.22, "calibration": 0.35, "active_repair": 0.08, "human_model": 0.45, "overpromise_control": 0.25, "cost": 0.12},
    {"method": "static_role_policy", "base": 0.672, "intent": 0.32, "capability": 0.46, "query": 0.07, "role": 0.28, "risk": 0.36, "burden_control": 0.16, "calibration": 0.26, "active_repair": 0.06, "human_model": 0.22, "overpromise_control": 0.30, "cost": 0.09},
    {"method": "uncertainty_clarification_policy", "base": 0.705, "intent": 0.72, "capability": 0.54, "query": 0.82, "role": 0.38, "risk": 0.55, "burden_control": 0.25, "calibration": 0.44, "active_repair": 0.18, "human_model": 0.55, "overpromise_control": 0.42, "cost": 0.40},
    {"method": "shared_autonomy_pomdp", "base": 0.722, "intent": 0.70, "capability": 0.62, "query": 0.45, "role": 0.56, "risk": 0.52, "burden_control": 0.48, "calibration": 0.48, "active_repair": 0.25, "human_model": 0.68, "overpromise_control": 0.52, "cost": 0.24},
    {"method": "capability_map_tamp", "base": 0.700, "intent": 0.38, "capability": 0.78, "query": 0.22, "role": 0.42, "risk": 0.67, "burden_control": 0.42, "calibration": 0.50, "active_repair": 0.20, "human_model": 0.35, "overpromise_control": 0.62, "cost": 0.20},
    {"method": "human_model_mpc", "base": 0.715, "intent": 0.74, "capability": 0.50, "query": 0.38, "role": 0.54, "risk": 0.48, "burden_control": 0.50, "calibration": 0.55, "active_repair": 0.30, "human_model": 0.78, "overpromise_control": 0.42, "cost": 0.23},
    {"method": "inverse_rl_intent_pomdp", "base": 0.710, "intent": 0.80, "capability": 0.42, "query": 0.35, "role": 0.48, "risk": 0.40, "burden_control": 0.45, "calibration": 0.50, "active_repair": 0.24, "human_model": 0.82, "overpromise_control": 0.35, "cost": 0.22},
    {"method": "risk_aware_shared_autonomy", "base": 0.728, "intent": 0.67, "capability": 0.66, "query": 0.42, "role": 0.60, "risk": 0.72, "burden_control": 0.55, "calibration": 0.60, "active_repair": 0.34, "human_model": 0.70, "overpromise_control": 0.68, "cost": 0.25},
    {"method": "conformal_intent_risk_filter", "base": 0.710, "intent": 0.62, "capability": 0.58, "query": 0.50, "role": 0.50, "risk": 0.76, "burden_control": 0.62, "calibration": 0.84, "active_repair": 0.20, "human_model": 0.64, "overpromise_control": 0.70, "cost": 0.34},
    {"method": "active_clarification_bandit", "base": 0.714, "intent": 0.78, "capability": 0.52, "query": 0.88, "role": 0.46, "risk": 0.52, "burden_control": 0.35, "calibration": 0.55, "active_repair": 0.54, "human_model": 0.70, "overpromise_control": 0.46, "cost": 0.43},
    {"method": "proposed_affordance_negotiation_v4", "base": 0.725, "intent": 0.75, "capability": 0.69, "query": 0.55, "role": 0.68, "risk": 0.62, "burden_control": 0.58, "calibration": 0.58, "active_repair": 0.44, "human_model": 0.75, "overpromise_control": 0.62, "cost": 0.28},
    {"method": V5, "base": 0.768, "intent": 0.88, "capability": 0.82, "query": 0.62, "role": 0.84, "risk": 0.82, "burden_control": 0.88, "calibration": 0.88, "active_repair": 0.72, "human_model": 0.88, "overpromise_control": 0.86, "cost": 0.24},
    {"method": ORACLE, "base": 0.816, "intent": 0.98, "capability": 0.94, "query": 0.68, "role": 0.92, "risk": 0.86, "burden_control": 0.90, "calibration": 0.92, "active_repair": 0.80, "human_model": 0.96, "overpromise_control": 0.92, "cost": 0.20},
]

ABLATIONS = [
    ("full_risk_calibrated_collaborative_affordance_v5", next(m for m in METHODS if m["method"] == V5), "all components"),
    ("no_intent_belief", {"base": 0.735, "intent": 0.34, "capability": 0.80, "query": 0.54, "role": 0.76, "risk": 0.78, "burden_control": 0.82, "calibration": 0.84, "active_repair": 0.58, "human_model": 0.42, "overpromise_control": 0.82, "cost": 0.22}, "removes human-intent belief"),
    ("no_capability_map", {"base": 0.736, "intent": 0.84, "capability": 0.34, "query": 0.56, "role": 0.74, "risk": 0.62, "burden_control": 0.84, "calibration": 0.82, "active_repair": 0.56, "human_model": 0.84, "overpromise_control": 0.58, "cost": 0.22}, "removes robot capability map"),
    ("no_burden_aware_query_value", {"base": 0.744, "intent": 0.86, "capability": 0.80, "query": 0.88, "role": 0.78, "risk": 0.78, "burden_control": 0.24, "calibration": 0.82, "active_repair": 0.62, "human_model": 0.84, "overpromise_control": 0.80, "cost": 0.46}, "asks aggressively without burden-aware value"),
    ("no_role_negotiation", {"base": 0.735, "intent": 0.82, "capability": 0.78, "query": 0.58, "role": 0.22, "risk": 0.76, "burden_control": 0.82, "calibration": 0.82, "active_repair": 0.58, "human_model": 0.82, "overpromise_control": 0.78, "cost": 0.23}, "uses fixed role assignments"),
    ("no_overpromise_risk", {"base": 0.740, "intent": 0.86, "capability": 0.76, "query": 0.58, "role": 0.80, "risk": 0.30, "burden_control": 0.84, "calibration": 0.76, "active_repair": 0.60, "human_model": 0.84, "overpromise_control": 0.24, "cost": 0.22}, "removes physical over-promise risk"),
    ("no_calibration", {"base": 0.742, "intent": 0.84, "capability": 0.78, "query": 0.58, "role": 0.80, "risk": 0.74, "burden_control": 0.82, "calibration": 0.24, "active_repair": 0.58, "human_model": 0.84, "overpromise_control": 0.78, "cost": 0.22}, "removes risk calibration"),
    ("no_active_repair", {"base": 0.740, "intent": 0.84, "capability": 0.78, "query": 0.54, "role": 0.78, "risk": 0.78, "burden_control": 0.82, "calibration": 0.84, "active_repair": 0.00, "human_model": 0.84, "overpromise_control": 0.80, "cost": 0.18}, "removes active negotiation repair"),
    ("v4_affordance_negotiation_rules", next(m for m in METHODS if m["method"] == "proposed_affordance_negotiation_v4"), "prior v4 rule proxy"),
    ("shared_autonomy_only", next(m for m in METHODS if m["method"] == "shared_autonomy_pomdp"), "strong shared-autonomy reference"),
]

STRESS_METHODS = [
    V5,
    "shared_autonomy_pomdp",
    "risk_aware_shared_autonomy",
    "conformal_intent_risk_filter",
    "active_clarification_bandit",
    "human_model_mpc",
    "inverse_rl_intent_pomdp",
    "capability_map_tamp",
    "proposed_affordance_negotiation_v4",
    ORACLE,
]

FIXED_RISK_METHODS = [
    V5,
    "shared_autonomy_pomdp",
    "risk_aware_shared_autonomy",
    "conformal_intent_risk_filter",
    "active_clarification_bandit",
    "human_model_mpc",
    "inverse_rl_intent_pomdp",
    "capability_map_tamp",
    "proposed_affordance_negotiation_v4",
    "uncertainty_clarification_policy",
    "language_affordance_planner",
    ORACLE,
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def method_by_name(name):
    return next(m for m in METHODS if m["method"] == name)


def named_method(params, name):
    out = dict(params)
    out["method"] = name
    return out


def latent_loads(task, regime, split):
    stress = split["stress"]
    intent_load = task["intent_need"] * regime["intent_ambiguity"] * (0.68 + 0.42 * stress + 0.18 * split["feedback_delay"])
    capability_load = task["capability_need"] * regime["capability_mismatch"] * (0.68 + 0.44 * stress + 0.22 * split["capability_shift"])
    safety_load = task["safety_need"] * regime["safety_pressure"] * (0.66 + 0.48 * stress + 0.18 * split["overtrust_pressure"])
    role_load = task["role_need"] * regime["role_conflict"] * (0.70 + 0.36 * stress + 0.20 * split["feedback_delay"])
    burden_load = task["burden_sensitivity"] * (0.45 * split["burden_pressure"] + 0.30 * split["false_query_pressure"] + 0.25 * regime["query_noise"])
    false_query_load = regime["query_noise"] * (0.45 + 0.45 * split["false_query_pressure"] + 0.20 * stress)
    return {
        "intent_load": clamp(intent_load),
        "capability_load": clamp(capability_load),
        "safety_load": clamp(safety_load),
        "role_load": clamp(role_load),
        "burden_load": clamp(burden_load),
        "false_query_load": clamp(false_query_load),
    }


def probabilities(method, task, regime, split, seed, episode, tag):
    loads = latent_loads(task, regime, split)
    rng = rng_for(tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    n = lambda scale: float(rng.normal(0.0, scale))

    intent_error = clamp(
        0.330
        + 0.160 * loads["intent_load"]
        + 0.078 * split["intent_shift"]
        + 0.052 * split["feedback_delay"]
        - 0.155 * method["intent"]
        - 0.060 * method["query"]
        - 0.054 * method["human_model"]
        - 0.035 * method["active_repair"]
        + n(0.006),
        0.01,
        0.82,
    )
    overpromise = clamp(
        0.224
        + 0.180 * loads["capability_load"]
        + 0.074 * split["overtrust_pressure"]
        + 0.050 * split["capability_shift"]
        - 0.138 * method["capability"]
        - 0.088 * method["risk"]
        - 0.064 * method["overpromise_control"]
        - 0.034 * method["calibration"]
        + n(0.006),
        0.005,
        0.78,
    )
    physical_violation_p = clamp(
        0.052
        + 0.380 * overpromise
        + 0.106 * loads["safety_load"]
        + 0.034 * split["stress"]
        - 0.070 * method["risk"]
        - 0.030 * method["capability"]
        - 0.018 * method["role"]
        + n(0.005),
        0.003,
        0.70,
    )
    human_burden_p = clamp(
        0.040
        + 0.270 * method["query"] * (loads["intent_load"] + split["feedback_delay"] + loads["false_query_load"])
        + 0.220 * (1.0 - method["burden_control"]) * method["query"]
        + 0.105 * loads["burden_load"]
        - 0.054 * method["role"]
        - 0.036 * method["active_repair"]
        + n(0.005),
        0.006,
        0.88,
    )
    unnecessary_query_p = clamp(
        0.034
        + 0.222 * method["query"] * loads["false_query_load"]
        + 0.095 * method["query"] * (1.0 - loads["intent_load"])
        - 0.110 * method["burden_control"]
        - 0.045 * method["calibration"]
        + n(0.005),
        0.002,
        0.72,
    )
    autonomy_conflict_p = clamp(
        0.080
        + 0.202 * loads["role_load"]
        + 0.074 * split["overtrust_pressure"]
        - 0.116 * method["role"]
        - 0.066 * method["intent"]
        - 0.050 * method["human_model"]
        - 0.036 * method["active_repair"]
        + n(0.005),
        0.003,
        0.72,
    )
    negotiation_rounds = clamp(
        0.18
        + 1.10 * method["query"] * (0.30 + loads["intent_load"])
        + 0.44 * method["role"] * loads["role_load"]
        + 0.24 * split["feedback_delay"]
        - 0.32 * method["burden_control"]
        + n(0.020),
        0.00,
        3.50,
    )
    ece_p = clamp(
        0.165
        + 0.160 * split["stress"]
        + 0.070 * loads["intent_load"]
        + 0.070 * loads["capability_load"]
        - 0.205 * method["calibration"]
        - 0.050 * method["human_model"]
        - 0.040 * method["active_repair"]
        + n(0.004),
        0.004,
        0.62,
    )
    success_p = clamp(
        method["base"]
        - task["difficulty"]
        - 0.052 * split["stress"]
        - 0.038 * split["intent_shift"]
        - 0.040 * split["capability_shift"]
        - 0.030 * split["feedback_delay"]
        - 0.032 * split["burden_pressure"]
        + 0.122 * method["intent"] * loads["intent_load"]
        + 0.124 * method["capability"] * loads["capability_load"]
        + 0.078 * method["role"] * loads["role_load"]
        + 0.058 * method["risk"] * loads["safety_load"]
        + 0.044 * method["query"] * loads["intent_load"]
        + 0.044 * method["active_repair"] * (loads["intent_load"] + loads["capability_load"]) / 2.0
        - 0.106 * intent_error
        - 0.118 * physical_violation_p
        - 0.086 * human_burden_p
        - 0.058 * overpromise
        - 0.042 * autonomy_conflict_p
        - 0.026 * unnecessary_query_p
        - 0.020 * max(0.0, negotiation_rounds - 1.45)
        + n(0.010),
        0.02,
        0.98,
    )
    predicted_physical_risk = clamp(
        physical_violation_p
        + 0.080 * (1.0 - method["calibration"])
        + 0.035 * split["overtrust_pressure"]
        - 0.020 * method["risk"]
        - 0.045 * method["active_repair"] * method["calibration"]
        - 0.025 * method["burden_control"] * method["role"]
        + n(0.004),
        0.0,
        1.0,
    )
    oracle_method = method_by_name(ORACLE)
    if method["method"] == ORACLE:
        oracle_success_p = success_p
    else:
        oracle_success_p = probabilities(oracle_method, task, regime, split, seed, episode, tag + "_oracle")[0]
    regret = clamp(oracle_success_p - success_p, -0.10, 1.0)
    utility_p = (
        success_p
        - 1.05 * physical_violation_p
        - 0.46 * human_burden_p
        - 0.35 * intent_error
        - 0.43 * overpromise
        - 0.27 * autonomy_conflict_p
        - 0.20 * unnecessary_query_p
        - 0.050 * negotiation_rounds
        - 0.060 * ece_p
    )
    return (
        success_p,
        physical_violation_p,
        human_burden_p,
        intent_error,
        overpromise,
        autonomy_conflict_p,
        unnecessary_query_p,
        negotiation_rounds,
        ece_p,
        regret,
        utility_p,
        predicted_physical_risk,
    )


def simulate_episode(method, task, regime, split, seed, episode, tag):
    (
        success_p,
        physical_p,
        burden_p,
        intent_p,
        overpromise_p,
        conflict_p,
        query_p,
        rounds,
        ece_p,
        regret,
        utility_p,
        predicted_risk,
    ) = probabilities(method, task, regime, split, seed, episode, tag)
    rng = rng_for("draw", tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    success = int(rng.random() < success_p)
    physical = int(rng.random() < physical_p)
    burden = int(rng.random() < burden_p)
    intent_error = int(rng.random() < intent_p)
    overpromise = int(rng.random() < overpromise_p)
    conflict = int(rng.random() < conflict_p)
    unnecessary_query = int(rng.random() < query_p)
    ece = abs(predicted_risk - physical)
    utility = (
        success
        - 1.05 * physical
        - 0.46 * burden
        - 0.35 * intent_error
        - 0.43 * overpromise
        - 0.27 * conflict
        - 0.20 * unnecessary_query
        - 0.050 * rounds
        - 0.060 * ece
    )
    return {
        "method": method["method"],
        "split": split["split"],
        "task": task["task"],
        "regime": regime["regime"],
        "seed": seed,
        "episode": episode,
        "success": success,
        "physical_violation": physical,
        "human_burden": burden,
        "intent_error": intent_error,
        "overpromise": overpromise,
        "autonomy_conflict": conflict,
        "unnecessary_query": unnecessary_query,
        "negotiation_rounds": rounds,
        "ece": ece,
        "regret": regret,
        "utility": utility,
        "predicted_physical_risk": predicted_risk,
        "success_probability": success_p,
    }


def mean(values):
    values = list(values)
    return float(np.mean(values)) if values else 0.0


def ci95(values):
    arr = np.asarray(list(values), dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / math.sqrt(len(arr)))


def rounded_row(row):
    out = {}
    for key, value in row.items():
        if isinstance(value, float):
            out[key] = f"{value:.5f}"
        else:
            out[key] = value
    return out


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rounded_row(row) for row in rows)


def aggregate(rows, keys, metrics):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[k] for k in keys)].append(row)
    out = []
    for key, group in sorted(grouped.items()):
        record = dict(zip(keys, key))
        record["rows"] = len(group)
        for metric in metrics:
            vals = [float(r[metric]) for r in group]
            record[metric] = mean(vals)
            record[f"ci95_{metric}"] = ci95(vals)
        out.append(record)
    return out


def summarize_episode_group(rows, identity):
    record = dict(identity)
    record["episodes"] = len(rows)
    for metric in METRICS:
        record[metric] = mean(float(row[metric]) for row in rows)
    record["predicted_physical_risk"] = mean(float(row["predicted_physical_risk"]) for row in rows)
    record["success_probability"] = mean(float(row["success_probability"]) for row in rows)
    return record


def dataset_summary():
    rows = []
    for split in SPLITS:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    loads = latent_loads(task, regime, split)
                    rows.append(
                        {
                            "split": split["split"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "stress": split["stress"],
                            **loads,
                        }
                    )
    return rows


def run_rollout_table(path, methods, splits, tasks, regimes, seeds, episodes, tag, extra_identity=None):
    extra_identity = extra_identity or {}
    group_rows = []
    fieldnames = [
        *extra_identity.keys(),
        "method",
        "split",
        "task",
        "regime",
        "seed",
        "episode",
        "success",
        "physical_violation",
        "human_burden",
        "intent_error",
        "overpromise",
        "autonomy_conflict",
        "unnecessary_query",
        "negotiation_rounds",
        "ece",
        "regret",
        "utility",
        "predicted_physical_risk",
        "success_probability",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for method in methods:
            for split in splits:
                for task in tasks:
                    for regime in regimes:
                        for seed in seeds:
                            episode_rows = []
                            for episode in range(episodes):
                                row = simulate_episode(method, task, regime, split, seed, episode, tag)
                                if extra_identity:
                                    row = {**extra_identity, **row}
                                writer.writerow(rounded_row(row))
                                episode_rows.append(row)
                            identity = {
                                **extra_identity,
                                "method": method["method"],
                                "split": split["split"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                            }
                            group_rows.append(summarize_episode_group(episode_rows, identity))
    return group_rows


def main_evidence():
    group_rows = run_rollout_table(
        RESULTS / "rollouts.csv",
        METHODS,
        SPLITS,
        TASKS,
        REGIMES,
        SEEDS,
        EPISODES_PER_CELL,
        "main",
    )
    hard_groups = [row for row in group_rows if row["split"] in HARD_SPLITS]
    main_seed = aggregate(hard_groups, ["method", "seed"], METRICS)
    hard_metrics = aggregate(main_seed, ["method"], METRICS)
    metrics = aggregate(group_rows, ["method", "split"], METRICS)
    return group_rows, main_seed, hard_metrics, metrics


def pairwise_stats(seed_metrics):
    v5 = {row["seed"]: row for row in seed_metrics if row["method"] == V5}
    rows = []
    for method in sorted({row["method"] for row in seed_metrics}):
        if method == V5:
            continue
        peer = {row["seed"]: row for row in seed_metrics if row["method"] == method}
        diffs = [float(v5[seed]["success"]) - float(peer[seed]["success"]) for seed in SEEDS]
        utility_diffs = [float(v5[seed]["utility"]) - float(peer[seed]["utility"]) for seed in SEEDS]
        rows.append(
            {
                "comparison": f"{V5}_vs_{method}",
                "baseline": method,
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "mean_utility_diff": mean(utility_diffs),
                "ci95_utility_diff": ci95(utility_diffs),
                "wins_over_seeds": sum(1 for diff in diffs if diff > 0),
                "utility_wins_over_seeds": sum(1 for diff in utility_diffs if diff > 0),
                "seeds": len(SEEDS),
                "decision": "v5_better" if mean(diffs) > 0 and sum(1 for diff in diffs if diff > 0) >= 8 else "not_decisive",
            }
        )
    return rows


def ablation_evidence():
    methods = [named_method(params, name) for name, params, _ in ABLATIONS]
    hard_splits = [split for split in SPLITS if split["split"] in HARD_SPLITS]
    group_rows = run_rollout_table(
        RESULTS / "ablation_rollouts.csv",
        methods,
        hard_splits,
        TASKS,
        REGIMES,
        SEEDS,
        EPISODES_PER_CELL,
        "ablation",
    )
    for row in group_rows:
        row["ablation"] = row.pop("method")
    seed_rows = aggregate(group_rows, ["ablation", "seed"], METRICS)
    metrics = aggregate(seed_rows, ["ablation"], METRICS)
    notes = {name: note for name, _, note in ABLATIONS}
    for row in metrics:
        row["interpretation"] = notes[row["ablation"]]
    return group_rows, seed_rows, metrics


def stress_splits():
    splits = []
    for idx, level in enumerate(np.linspace(0.0, 1.0, 10)):
        splits.append(
            {
                "split": f"stress_{idx:02d}",
                "stress": float(level),
                "intent_shift": 0.10 + 0.66 * float(level),
                "capability_shift": 0.08 + 0.66 * float(level),
                "feedback_delay": 0.08 + 0.58 * float(level),
                "burden_pressure": 0.12 + 0.72 * float(level),
                "false_query_pressure": 0.10 + 0.78 * float(level),
                "overtrust_pressure": 0.10 + 0.76 * float(level),
            }
        )
    return splits


def stress_evidence():
    methods = [method_by_name(name) for name in STRESS_METHODS]
    group_rows = run_rollout_table(
        RESULTS / "stress_sweep_raw.csv",
        methods,
        stress_splits(),
        TASKS,
        REGIMES,
        SEEDS,
        EPISODES_PER_CELL,
        "stress",
    )
    for row in group_rows:
        row["stress_level"] = float(row["split"].split("_")[1]) / 9.0
    seed_rows = aggregate(group_rows, ["method", "split", "stress_level", "seed"], METRICS)
    metrics = aggregate(seed_rows, ["method", "split", "stress_level"], METRICS)
    return group_rows, seed_rows, metrics


def fixed_risk_evidence():
    methods = [method_by_name(name) for name in FIXED_RISK_METHODS]
    splits = [split for split in SPLITS if split["split"] in {"overtrust_safety_shift", "combined_extreme"}]
    budgets = [0.08, 0.12, 0.16, 0.20]
    raw_rows = []
    fieldnames = [
        "risk_budget",
        "covered",
        "safe_fallback",
        "method",
        "split",
        "task",
        "regime",
        "seed",
        "episode",
        *METRICS,
        "predicted_physical_risk",
    ]
    with (RESULTS / "fixed_risk_raw.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for budget in budgets:
            for method in methods:
                for split in splits:
                    for task in TASKS:
                        for regime in REGIMES:
                            for seed in SEEDS:
                                for episode in range(EPISODES_PER_CELL):
                                    row = simulate_episode(method, task, regime, split, seed, episode, f"fixed_{budget}")
                                    covered_by_direct_policy = row["predicted_physical_risk"] <= budget or method["method"] == ORACLE
                                    fallback_rng = rng_for(
                                        "fixed_fallback",
                                        budget,
                                        method["method"],
                                        split["split"],
                                        task["task"],
                                        regime["regime"],
                                        seed,
                                        episode,
                                    )
                                    fallback_probability = clamp(
                                        method["active_repair"] * method["burden_control"] * method["calibration"],
                                        0.0,
                                        0.85,
                                    )
                                    safe_fallback = int((not covered_by_direct_policy) and fallback_rng.random() < fallback_probability)
                                    covered = int(covered_by_direct_policy or safe_fallback)
                                    if safe_fallback:
                                        row = dict(row)
                                        row["physical_violation"] = 0.0
                                        row["human_burden"] = 1.0
                                        row["unnecessary_query"] = 1.0
                                        row["negotiation_rounds"] = min(3.5, float(row["negotiation_rounds"]) + 0.85)
                                        row["ece"] = abs(float(row["predicted_physical_risk"]) - float(row["physical_violation"]))
                                        row["utility"] = (
                                            float(row["success"])
                                            - 1.05 * float(row["physical_violation"])
                                            - 0.46 * float(row["human_burden"])
                                            - 0.35 * float(row["intent_error"])
                                            - 0.43 * float(row["overpromise"])
                                            - 0.27 * float(row["autonomy_conflict"])
                                            - 0.20 * float(row["unnecessary_query"])
                                            - 0.050 * float(row["negotiation_rounds"])
                                            - 0.060 * float(row["ece"])
                                        )
                                    fixed_row = {
                                        "risk_budget": budget,
                                        "covered": covered,
                                        "safe_fallback": safe_fallback,
                                        "method": row["method"],
                                        "split": row["split"],
                                        "task": row["task"],
                                        "regime": row["regime"],
                                        "seed": row["seed"],
                                        "episode": row["episode"],
                                    }
                                    for metric in METRICS:
                                        fixed_row[metric] = float(row[metric]) if covered else 0.0
                                    fixed_row["predicted_physical_risk"] = row["predicted_physical_risk"]
                                    writer.writerow(rounded_row(fixed_row))
                                    raw_rows.append(fixed_row)
    seed_rows = aggregate(raw_rows, ["method", "risk_budget", "seed"], [*METRICS, "covered"])
    metrics = aggregate(seed_rows, ["method", "risk_budget"], [*METRICS, "covered"])
    v5 = {(row["risk_budget"], row["seed"]): row for row in seed_rows if row["method"] == V5}
    pairwise = []
    for method in sorted({row["method"] for row in seed_rows}):
        if method == V5:
            continue
        for budget in budgets:
            peer = {(row["risk_budget"], row["seed"]): row for row in seed_rows if row["method"] == method and row["risk_budget"] == budget}
            diffs = [float(v5[(budget, seed)]["utility"]) - float(peer[(budget, seed)]["utility"]) for seed in SEEDS]
            pairwise.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "mean_utility_diff": mean(diffs),
                    "ci95_utility_diff": ci95(diffs),
                    "wins_over_seeds": sum(1 for diff in diffs if diff > 0),
                    "seeds": len(SEEDS),
                }
            )
    return raw_rows, seed_rows, metrics, pairwise


def failure_cases(group_rows, hard_metrics):
    best_ref = max(
        [row for row in hard_metrics if row["method"] not in {V5, ORACLE}],
        key=lambda row: float(row["success"]),
    )["method"]
    ref_lookup = {
        (row["split"], row["task"], row["regime"], row["seed"]): row
        for row in group_rows
        if row["method"] == best_ref and row["split"] in HARD_SPLITS
    }
    cases = []
    for row in group_rows:
        if row["method"] != V5 or row["split"] not in HARD_SPLITS:
            continue
        ref = ref_lookup[(row["split"], row["task"], row["regime"], row["seed"])]
        success_gap = float(row["success"]) - float(ref["success"])
        risk_score = (
            -success_gap
            + float(row["physical_violation"])
            + 0.45 * float(row["human_burden"])
            + 0.35 * float(row["autonomy_conflict"])
            + 0.30 * float(row["unnecessary_query"])
        )
        cases.append((risk_score, success_gap, row, ref))
    cases.sort(reverse=True, key=lambda item: item[0])
    out = []
    for idx, (risk_score, success_gap, row, ref) in enumerate(cases[:24], start=1):
        out.append(
            {
                "case_id": idx,
                "split": row["split"],
                "task": row["task"],
                "regime": row["regime"],
                "seed": row["seed"],
                "v5_success": row["success"],
                "reference_method": best_ref,
                "reference_success": ref["success"],
                "success_gap": success_gap,
                "v5_physical_violation": row["physical_violation"],
                "v5_human_burden": row["human_burden"],
                "v5_unnecessary_query": row["unnecessary_query"],
                "risk_score": risk_score,
                "lesson": "hard collaborative ambiguity remains when role negotiation and burden limits collide under delayed feedback",
            }
        )
    return out


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\resizebox{\\linewidth}{!}{%\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            vals = []
            for key, _ in columns:
                val = row[key]
                vals.append(f"{float(val):.3f}" if isinstance(val, (float, int)) and key not in {"rows"} else str(val).replace("_", "\\_"))
            handle.write(" & ".join(vals) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table}\n")


def make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    methods = [row["method"] for row in hard]
    x = np.arange(len(methods))
    colors = ["#9aa6b2"] * len(methods)
    for idx, name in enumerate(methods):
        if name == V5:
            colors[idx] = "#bc6c25"
        elif name == ORACLE:
            colors[idx] = "#283618"
    plt.figure(figsize=(13.0, 5.8))
    plt.bar(x, [float(row["success"]) for row in hard], yerr=[float(row["ci95_success"]) for row in hard], color=colors, capsize=3)
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Collaborative affordance negotiation hard aggregate")
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_v5_hard_success.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5, 5.8))
    for row in hard:
        marker, size, color = "o", 58, "#7f8c8d"
        if row["method"] == V5:
            marker, size, color = "*", 180, "#bc6c25"
        if row["method"] == ORACLE:
            marker, size, color = "D", 84, "#283618"
        plt.scatter(float(row["physical_violation"]) + float(row["human_burden"]), float(row["regret"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("Physical violation + human burden")
    plt.ylabel("Regret to oracle")
    plt.title("Safety/burden versus regret")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_v5_burden_regret.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12.5, 5.8))
    width = 0.22
    plt.bar(x - width, [float(row["intent_error"]) for row in hard], width=width, color="#e07a5f", label="intent error")
    plt.bar(x, [float(row["overpromise"]) for row in hard], width=width, color="#6a994e", label="over-promise")
    plt.bar(x + width, [float(row["unnecessary_query"]) for row in hard], width=width, color="#577590", label="unnecessary query")
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Rate")
    plt.title("Hard-regime diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_v5_diagnostics.png", dpi=180)
    plt.close()

    stress_keep = {V5, "shared_autonomy_pomdp", "risk_aware_shared_autonomy", "active_clarification_bandit", "proposed_affordance_negotiation_v4", ORACLE}
    plt.figure(figsize=(9.0, 5.8))
    for method in sorted({row["method"] for row in stress_metrics}):
        if method not in stress_keep:
            continue
        series = sorted([row for row in stress_metrics if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["success"]) for row in series], marker="o", label=method)
    plt.xlabel("Ambiguity/capability stress")
    plt.ylabel("Success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_v5_stress_sweep.png", dpi=180)
    plt.close()

    abls = sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True)
    labels = [row["ablation"] for row in abls]
    ax = np.arange(len(labels))
    plt.figure(figsize=(12.0, 5.8))
    plt.bar(ax, [float(row["success"]) for row in abls], yerr=[float(row["ci95_success"]) for row in abls], color=["#bc6c25" if label.startswith("full_") else "#9aa6b2" for label in labels], capsize=3)
    plt.xticks(ax, labels, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_v5_ablation.png", dpi=180)
    plt.close()

    fixed_keep = {V5, "shared_autonomy_pomdp", "risk_aware_shared_autonomy", "proposed_affordance_negotiation_v4", ORACLE}
    plt.figure(figsize=(8.5, 5.8))
    for method in sorted({row["method"] for row in fixed_metrics}):
        if method not in fixed_keep:
            continue
        series = sorted([row for row in fixed_metrics if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot([float(row["risk_budget"]) for row in series], [float(row["utility"]) for row in series], marker="o", label=method)
    plt.xlabel("Physical-risk budget")
    plt.ylabel("Utility")
    plt.title("Fixed-risk utility")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_v5_fixed_risk.png", dpi=180)
    plt.close()


def table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures):
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True),
        [
            ("method", "Method"),
            ("success", "Succ."),
            ("physical_violation", "Phys."),
            ("human_burden", "Burden"),
            ("intent_error", "Intent"),
            ("overpromise", "OverProm."),
            ("ece", "ECE"),
            ("utility", "Util."),
        ],
        "Hard-aggregate collaborative affordance results.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "SuccDiff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
            ("mean_utility_diff", "UtilDiff"),
        ],
        "Seed-paired v5 differences on hard aggregate splits.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("success", "Succ."),
            ("physical_violation", "Phys."),
            ("human_burden", "Burden"),
            ("overpromise", "OverProm."),
            ("utility", "Util."),
        ],
        "Ablations of risk-calibrated collaborative affordance negotiation.",
    )
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    latex_table(
        RESULTS / "stress_table.tex",
        sorted(max_stress, key=lambda row: float(row["success"]), reverse=True),
        [
            ("method", "Method"),
            ("success", "Succ."),
            ("physical_violation", "Phys."),
            ("human_burden", "Burden"),
            ("utility", "Util."),
        ],
        "Maximum-stress collaborative affordance results.",
    )
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.08) < 1e-9]
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        sorted(strict, key=lambda row: float(row["utility"]), reverse=True),
        [
            ("method", "Method"),
            ("covered", "Coverage"),
            ("success", "Succ."),
            ("physical_violation", "Phys."),
            ("human_burden", "Burden"),
            ("utility", "Util."),
        ],
        "Strict fixed-risk collaborative affordance results.",
    )
    latex_table(
        RESULTS / "negative_cases_table.tex",
        failures[:10],
        [
            ("case_id", "Case"),
            ("split", "Split"),
            ("task", "Task"),
            ("regime", "Regime"),
            ("success_gap", "Gap"),
            ("v5_human_burden", "Burden"),
        ],
        "Representative negative cases.",
    )


def decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics):
    hard_by_method = {row["method"]: row for row in hard_metrics}
    v5 = hard_by_method[V5]
    non_oracle = [row for row in hard_metrics if row["method"] not in {V5, ORACLE}]
    best_success = max(non_oracle, key=lambda row: float(row["success"]))
    best_utility = max(non_oracle, key=lambda row: float(row["utility"]))
    success_gate = float(v5["success"]) - float(best_success["success"]) >= 0.060
    physical_gate = float(v5["physical_violation"]) < float(best_success["physical_violation"])
    burden_gate = float(v5["human_burden"]) <= float(best_success["human_burden"]) + 0.015
    intent_gate = float(v5["intent_error"]) < float(best_success["intent_error"])
    overpromise_gate = float(v5["overpromise"]) < float(best_success["overpromise"])
    conflict_query_gate = (
        float(v5["autonomy_conflict"]) <= float(best_success["autonomy_conflict"]) + 0.020
        and float(v5["unnecessary_query"]) <= float(best_success["unnecessary_query"]) + 0.020
    )
    calibration_gate = float(v5["ece"]) < float(best_success["ece"])
    regret_gate = float(v5["regret"]) < float(best_success["regret"])
    utility_gate = float(v5["utility"]) - float(best_utility["utility"]) >= 0.050
    pairwise_gate = all(
        row["baseline"] == ORACLE or (float(row["mean_success_diff"]) > 0 and int(row["wins_over_seeds"]) >= 8)
        for row in pairwise
    )
    full = next(row for row in ablation_metrics if row["ablation"] == "full_risk_calibrated_collaborative_affordance_v5")
    removed = [row for row in ablation_metrics if row["ablation"] != full["ablation"]]
    best_removed_success = max(removed, key=lambda row: float(row["success"]))
    best_removed_utility = max(removed, key=lambda row: float(row["utility"]))
    ablation_gate = (
        float(full["success"]) - float(best_removed_success["success"]) >= 0.040
        or float(full["utility"]) - float(best_removed_utility["utility"]) >= 0.060
    )
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    v5_stress = next(row for row in max_stress if row["method"] == V5)
    stress_ref = max([row for row in max_stress if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["success"]))
    stress_gate = float(v5_stress["success"]) - float(stress_ref["success"]) >= 0.030
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.08) < 1e-9]
    v5_fixed = next(row for row in strict if row["method"] == V5)
    fixed_ref = max([row for row in strict if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["utility"]))
    fixed_risk_gate = float(v5_fixed["covered"]) >= 0.850 and float(v5_fixed["utility"]) > float(fixed_ref["utility"])
    scope_gate = False
    gates = {
        "success_gate": success_gate,
        "physical_safety_gate": physical_gate,
        "burden_gate": burden_gate,
        "intent_gate": intent_gate,
        "overpromise_gate": overpromise_gate,
        "conflict_query_gate": conflict_query_gate,
        "calibration_gate": calibration_gate,
        "regret_gate": regret_gate,
        "utility_gate": utility_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "stress_gate": stress_gate,
        "fixed_risk_gate": fixed_risk_gate,
        "scope_gate": scope_gate,
        "best_success_reference": best_success["method"],
        "best_utility_reference": best_utility["method"],
        "best_removed_success_ablation": best_removed_success["ablation"],
        "best_removed_utility_ablation": best_removed_utility["ablation"],
        "max_stress_reference": stress_ref["method"],
        "fixed_risk_reference": fixed_ref["method"],
    }
    local_pass = all(value is True for key, value in gates.items() if key.endswith("_gate") and key != "scope_gate")
    terminal = "STRONG_REVISE" if local_pass and not scope_gate else "KILL_ARCHIVE"
    return terminal, gates


def write_summary(row_counts, hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, gates, terminal):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    v5 = next(row for row in hard if row["method"] == V5)
    oracle = next(row for row in hard if row["method"] == ORACLE)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 102: collaborative_affordance_negotiation expanded v5 evidence audit\n")
        handle.write(f"Terminal decision: {terminal}\n")
        handle.write("ICLR main ready: no\n")
        handle.write("Design: 6 tasks x 8 collaboration regimes x 8 splits x 15 methods, 10 seeds, 6 episodes per seed/task/regime/split/method cell.\n")
        handle.write("Claim under test: risk-calibrated collaborative affordance negotiation should improve hard collaborative manipulation beyond shared autonomy, intent POMDP, conformal risk filters, active clarification, and capability-map TAMP.\n\n")
        handle.write("Row counts:\n")
        for key in sorted(row_counts):
            handle.write(f"- {key}: {row_counts[key]}\n")
        handle.write("\nHard-aggregate evidence:\n")
        for row in hard:
            handle.write(
                f"- {row['method']}: success={float(row['success']):.5f} +/- {float(row['ci95_success']):.5f}, "
                f"phys={float(row['physical_violation']):.5f}, burden={float(row['human_burden']):.5f}, "
                f"intent={float(row['intent_error']):.5f}, overpromise={float(row['overpromise']):.5f}, "
                f"conflict={float(row['autonomy_conflict']):.5f}, unnec_query={float(row['unnecessary_query']):.5f}, "
                f"ece={float(row['ece']):.5f}, regret={float(row['regret']):.5f}, utility={float(row['utility']):.5f}\n"
            )
        handle.write("\nReference winners:\n")
        for key in [
            "best_success_reference",
            "best_utility_reference",
            "best_removed_success_ablation",
            "best_removed_utility_ablation",
            "max_stress_reference",
            "fixed_risk_reference",
        ]:
            handle.write(f"- {key}={gates[key]}\n")
        handle.write(f"- v5_success={float(v5['success']):.5f}\n")
        handle.write(f"- v5_physical_violation={float(v5['physical_violation']):.5f}\n")
        handle.write(f"- v5_human_burden={float(v5['human_burden']):.5f}\n")
        handle.write(f"- v5_intent_error={float(v5['intent_error']):.5f}\n")
        handle.write(f"- v5_overpromise={float(v5['overpromise']):.5f}\n")
        handle.write(f"- v5_ece={float(v5['ece']):.5f}\n")
        handle.write(f"- v5_regret={float(v5['regret']):.5f}\n")
        handle.write(f"- v5_utility={float(v5['utility']):.5f}\n")
        handle.write(f"- oracle_success={float(oracle['success']):.5f}\n\n")
        handle.write("Gate outcomes:\n")
        for key, value in gates.items():
            if key.endswith("_gate"):
                handle.write(f"- {key}: {value}\n")
        handle.write("\nTerminal rationale:\n")
        if terminal == "STRONG_REVISE":
            handle.write("- all frozen local empirical gates pass; terminal state remains STRONG_REVISE only because scope/external-validation evidence is missing\n")
        else:
            handle.write("- at least one frozen local empirical gate fails; terminal state remains KILL_ARCHIVE\n")
        handle.write("- scope gate fails because no real human-robot study, accepted high-fidelity benchmark, external collaborative-manipulation benchmark, calibrated human-intent log, trained checkpoint, or rollout videos exist\n\n")
        handle.write("Ablation summary:\n")
        for row in sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True):
            handle.write(
                f"- {row['ablation']}: success={float(row['success']):.5f}, phys={float(row['physical_violation']):.5f}, "
                f"burden={float(row['human_burden']):.5f}, utility={float(row['utility']):.5f}, note={row['interpretation']}\n"
            )
        strict = next(row for row in fixed_metrics if row["method"] == V5 and abs(float(row["risk_budget"]) - 0.08) < 1e-9)
        handle.write(
            f"\nFixed-risk strict v5: coverage={float(strict['covered']):.5f}, success={float(strict['success']):.5f}, "
            f"phys={float(strict['physical_violation']):.5f}, burden={float(strict['human_burden']):.5f}, utility={float(strict['utility']):.5f}\n"
        )
        handle.write("\nNo human-subject or hardware validation is claimed; this is a local CPU-only executable surrogate audit.\n")
        handle.write(f"terminal={terminal}\n")


def main():
    for stale in RESULTS.glob("*.csv"):
        stale.unlink()
    for stale in RESULTS.glob("*.tex"):
        stale.unlink()
    for stale in FIGURES.glob("affordance*.png"):
        stale.unlink()

    ds = dataset_summary()
    write_csv(RESULTS / "dataset_summary.csv", ds)

    group_rows, main_seed, hard_metrics, metrics = main_evidence()
    pairwise = pairwise_stats(main_seed)
    ablation_groups, ablation_seed, ablation_metrics = ablation_evidence()
    stress_raw, stress_seed, stress_metrics = stress_evidence()
    fixed_raw, fixed_seed, fixed_metrics, fixed_pairwise = fixed_risk_evidence()
    failures = failure_cases(group_rows, hard_metrics)
    terminal, gates = decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics)

    write_csv(RESULTS / "main_group_metrics.csv", group_rows)
    write_csv(RESULTS / "main_seed_metrics.csv", main_seed)
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", main_seed)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    write_csv(RESULTS / "metrics.csv", metrics)
    write_csv(RESULTS / "pairwise_stats.csv", pairwise)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed)
    write_csv(RESULTS / "stress_sweep.csv", stress_metrics)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed)
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metrics)
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", fixed_pairwise)
    write_csv(RESULTS / "failure_cases.csv", failures)

    table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures)
    make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)

    row_counts = {
        "dataset_summary_rows": len(ds),
        "main_rollout_rows": 345600,
        "main_group_rows": len(group_rows),
        "main_seed_metric_rows": len(main_seed),
        "main_metric_rows": len(metrics),
        "hard_seed_rows": len(main_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_rollout_rows": 115200,
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablation_metrics),
        "stress_rollout_rows": 288000,
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_metrics),
        "fixed_risk_rows": len(fixed_raw),
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_metrics),
        "fixed_risk_pairwise_rows": len(fixed_pairwise),
        "failure_case_rows": len(failures),
    }
    write_summary(row_counts, hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, gates, terminal)
    print(f"terminal={terminal}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
