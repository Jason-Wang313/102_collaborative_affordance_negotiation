import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 102_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


TASKS = [
    {"task": "handover_grip_choice", "difficulty": 0.055, "intent_need": 0.86, "capability_need": 0.72, "burden_sensitivity": 0.48},
    {"task": "co_carry_doorway", "difficulty": 0.076, "intent_need": 0.80, "capability_need": 0.92, "burden_sensitivity": 0.65},
    {"task": "assisted_assembly", "difficulty": 0.068, "intent_need": 0.90, "capability_need": 0.78, "burden_sensitivity": 0.58},
    {"task": "collaborative_sorting", "difficulty": 0.050, "intent_need": 0.82, "capability_need": 0.60, "burden_sensitivity": 0.42},
    {"task": "tool_use_handoff", "difficulty": 0.071, "intent_need": 0.87, "capability_need": 0.84, "burden_sensitivity": 0.62},
]

FAMILIES = [
    {"family": "ambiguous_intent", "intent_ambiguity": 0.86, "capability_mismatch": 0.24, "safety_pressure": 0.28},
    {"family": "asymmetric_reach", "intent_ambiguity": 0.42, "capability_mismatch": 0.80, "safety_pressure": 0.50},
    {"family": "load_sharing_mismatch", "intent_ambiguity": 0.50, "capability_mismatch": 0.84, "safety_pressure": 0.72},
    {"family": "occluded_human_goal", "intent_ambiguity": 0.78, "capability_mismatch": 0.42, "safety_pressure": 0.38},
    {"family": "ergonomic_constraint", "intent_ambiguity": 0.48, "capability_mismatch": 0.70, "safety_pressure": 0.66},
    {"family": "role_switch_request", "intent_ambiguity": 0.74, "capability_mismatch": 0.56, "safety_pressure": 0.44},
    {"family": "conflicting_safety_preference", "intent_ambiguity": 0.68, "capability_mismatch": 0.72, "safety_pressure": 0.82},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "intent_shift": 0.08, "capability_shift": 0.04, "feedback_delay": 0.00},
    {"split": "intent_ambiguity_shift", "stress": 0.52, "intent_shift": 0.66, "capability_shift": 0.12, "feedback_delay": 0.12},
    {"split": "capability_shift", "stress": 0.50, "intent_shift": 0.24, "capability_shift": 0.68, "feedback_delay": 0.10},
    {"split": "delayed_human_feedback", "stress": 0.48, "intent_shift": 0.46, "capability_shift": 0.28, "feedback_delay": 0.66},
    {"split": "combined_stress", "stress": 0.80, "intent_shift": 0.68, "capability_shift": 0.64, "feedback_delay": 0.58},
]

METHODS = [
    {"method": "robot_capability_only_planner", "base": 0.650, "intent": 0.08, "capability": 0.60, "query": 0.03, "role": 0.10, "risk": 0.42, "burden": 0.04, "overpromise": 0.17},
    {"method": "intent_only_follower", "base": 0.670, "intent": 0.62, "capability": 0.12, "query": 0.04, "role": 0.18, "risk": 0.14, "burden": 0.03, "overpromise": 0.42},
    {"method": "language_affordance_planner", "base": 0.684, "intent": 0.52, "capability": 0.36, "query": 0.12, "role": 0.24, "risk": 0.24, "burden": 0.08, "overpromise": 0.30},
    {"method": "static_role_policy", "base": 0.664, "intent": 0.28, "capability": 0.44, "query": 0.08, "role": 0.20, "risk": 0.34, "burden": 0.06, "overpromise": 0.22},
    {"method": "uncertainty_clarification_policy", "base": 0.700, "intent": 0.70, "capability": 0.50, "query": 0.74, "role": 0.34, "risk": 0.52, "burden": 0.42, "overpromise": 0.13},
    {"method": "shared_autonomy_pomdp", "base": 0.716, "intent": 0.66, "capability": 0.58, "query": 0.42, "role": 0.52, "risk": 0.48, "burden": 0.24, "overpromise": 0.16},
    {"method": "capability_map_tamp", "base": 0.688, "intent": 0.34, "capability": 0.74, "query": 0.20, "role": 0.42, "risk": 0.62, "burden": 0.16, "overpromise": 0.10},
    {"method": "proposed_affordance_negotiation", "base": 0.708, "intent": 0.70, "capability": 0.66, "query": 0.48, "role": 0.66, "risk": 0.54, "burden": 0.25, "overpromise": 0.12},
    {"method": "oracle_joint_intent_capability_planner", "base": 0.765, "intent": 0.95, "capability": 0.92, "query": 0.68, "role": 0.90, "risk": 0.76, "burden": 0.18, "overpromise": 0.04},
]

ABLATIONS = [
    ("full_affordance_negotiation", {"base": 0.708, "intent": 0.70, "capability": 0.66, "query": 0.48, "role": 0.66, "risk": 0.54, "burden": 0.25, "overpromise": 0.12}, "all components"),
    ("minus_intent_belief", {"base": 0.690, "intent": 0.36, "capability": 0.64, "query": 0.42, "role": 0.56, "risk": 0.52, "burden": 0.21, "overpromise": 0.14}, "removes human-intent belief update"),
    ("minus_capability_map", {"base": 0.692, "intent": 0.68, "capability": 0.34, "query": 0.44, "role": 0.54, "risk": 0.39, "burden": 0.22, "overpromise": 0.24}, "removes robot capability map"),
    ("minus_burden_aware_query_value", {"base": 0.704, "intent": 0.72, "capability": 0.64, "query": 0.78, "role": 0.60, "risk": 0.52, "burden": 0.46, "overpromise": 0.11}, "asks whenever uncertain without burden modeling"),
    ("minus_role_negotiation", {"base": 0.691, "intent": 0.64, "capability": 0.62, "query": 0.44, "role": 0.24, "risk": 0.50, "burden": 0.22, "overpromise": 0.16}, "uses fixed role assignments"),
    ("minus_overpromise_risk", {"base": 0.706, "intent": 0.70, "capability": 0.61, "query": 0.42, "role": 0.62, "risk": 0.24, "burden": 0.20, "overpromise": 0.30}, "does not penalize infeasible promises"),
    ("clarification_only", {"base": 0.702, "intent": 0.72, "capability": 0.52, "query": 0.80, "role": 0.32, "risk": 0.50, "burden": 0.47, "overpromise": 0.12}, "clarifies ambiguity but does not negotiate capability/roles"),
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probabilities(method, task, family, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    intent_shift = split["intent_shift"]
    capability_shift = split["capability_shift"]
    feedback_delay = split["feedback_delay"]
    intent_load = task["intent_need"] * family["intent_ambiguity"] * (0.72 + 0.40 * stress + 0.20 * feedback_delay)
    capability_load = task["capability_need"] * family["capability_mismatch"] * (0.70 + 0.45 * stress + 0.18 * capability_shift)
    safety_load = task["capability_need"] * family["safety_pressure"] * (0.66 + 0.48 * stress)

    rng = rng_for(method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    noise = rng.normal(0.0, 0.012)

    intent_error = clamp(
        0.315
        + 0.145 * intent_load
        + 0.095 * intent_shift
        + 0.070 * feedback_delay
        - 0.170 * method["intent"]
        - 0.080 * method["query"]
        - 0.045 * method["role"]
        + 0.040 * method["burden"] * feedback_delay
        + rng.normal(0.0, 0.007),
        0.02,
        0.78,
    )
    overpromise = clamp(
        method["overpromise"]
        + 0.165 * capability_load
        + 0.060 * capability_shift
        - 0.150 * method["capability"]
        - 0.068 * method["risk"]
        - 0.030 * method["role"]
        + rng.normal(0.0, 0.007),
        0.01,
        0.72,
    )
    physical_violation = clamp(
        0.065
        + 0.355 * overpromise
        + 0.090 * safety_load
        + 0.035 * stress
        - 0.070 * method["risk"]
        - 0.030 * method["capability"]
        + rng.normal(0.0, 0.006),
        0.004,
        0.62,
    )
    human_burden = clamp(
        0.040
        + 0.430 * method["burden"]
        + 0.115 * method["query"] * (intent_load + feedback_delay)
        + 0.065 * task["burden_sensitivity"] * method["query"]
        - 0.040 * method["role"]
        + rng.normal(0.0, 0.006),
        0.01,
        0.85,
    )
    negotiation_rounds = clamp(
        0.18
        + 1.25 * method["query"] * (0.45 + intent_load)
        + 0.55 * method["role"] * capability_load
        + 0.25 * feedback_delay
        + rng.normal(0.0, 0.035),
        0.0,
        3.5,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.052 * stress
        - 0.054 * intent_shift
        - 0.050 * capability_shift
        - 0.045 * feedback_delay
        + 0.123 * method["intent"] * intent_load
        + 0.125 * method["capability"] * capability_load
        + 0.075 * method["role"] * (intent_load + capability_load)
        + 0.058 * method["risk"] * safety_load
        + 0.048 * method["query"] * intent_load
        - 0.118 * intent_error
        - 0.110 * physical_violation
        - 0.090 * human_burden
        - 0.030 * max(0.0, negotiation_rounds - 1.25)
        + noise,
        0.03,
        0.97,
    )
    total_cost = clamp(
        0.52 * physical_violation
        + 0.36 * human_burden
        + 0.30 * intent_error
        + 0.30 * overpromise
        + 0.055 * negotiation_rounds,
        0.0,
        2.0,
    )
    return success, physical_violation, human_burden, intent_error, overpromise, negotiation_rounds, total_cost


def simulate_group(method, task, family, split, seed, stress_override=None):
    p_success, p_violation, p_burden, p_intent_error, p_overpromise, rounds, total_cost = probabilities(
        method, task, family, split, seed, stress_override
    )
    rng = rng_for("episodes", method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    n = EPISODES_PER_GROUP
    return {
        "method": method["method"],
        "split": split["split"],
        "task": task["task"],
        "family": family["family"],
        "seed": seed,
        "episodes": n,
        "success": rng.binomial(n, p_success) / n,
        "physical_violation": rng.binomial(n, p_violation) / n,
        "human_burden": rng.binomial(n, p_burden) / n,
        "intent_error": rng.binomial(n, p_intent_error) / n,
        "overpromise": rng.binomial(n, p_overpromise) / n,
        "negotiation_rounds": rounds,
        "total_cost": total_cost,
    }


def mean(values):
    return float(np.mean(values))


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / math.sqrt(len(arr)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        grouped.setdefault(key, []).append(row)
    out = []
    for key, group in sorted(grouped.items()):
        record = dict(zip(keys, key))
        for metric in metrics:
            vals = [float(r[metric]) for r in group]
            record[f"mean_{metric}"] = mean(vals)
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group)
        out.append(record)
    return out


def rounded(rows):
    clean_rows = []
    for row in rows:
        clean = {}
        for key, value in row.items():
            clean[key] = f"{value:.4f}" if isinstance(value, float) else value
        clean_rows.append(clean)
    return clean_rows


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_main():
    seed_rows = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for family in FAMILIES:
                    for seed in SEEDS:
                        seed_rows.append(simulate_group(method, task, family, split, seed))
    metrics = [
        "success",
        "physical_violation",
        "human_burden",
        "intent_error",
        "overpromise",
        "negotiation_rounds",
        "total_cost",
    ]
    per_task_family = aggregate(seed_rows, ["method", "split", "task", "family"], metrics)
    seed_split = aggregate(seed_rows, ["method", "split", "seed"], metrics)
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in metrics])

    oracle_lookup = {}
    for row in per_task_family:
        if row["method"] == "oracle_joint_intent_capability_planner":
            oracle_lookup[(row["split"], row["task"], row["family"])] = float(row["mean_success"])
    for row in per_task_family:
        row["mean_regret_to_oracle"] = clamp(
            oracle_lookup[(row["split"], row["task"], row["family"])] - float(row["mean_success"]),
            -0.2,
            1.0,
        )
    for row in summary:
        vals = [
            r["mean_regret_to_oracle"]
            for r in per_task_family
            if r["method"] == row["method"] and r["split"] == row["split"]
        ]
        row["mean_regret_to_oracle"] = mean(vals)
        row["ci95_regret_to_oracle"] = ci95(vals)
    return seed_rows, per_task_family, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    strongest = max(
        [
            r
            for r in combined.values()
            if r["method"] not in {"proposed_affordance_negotiation", "oracle_joint_intent_capability_planner"}
        ],
        key=lambda r: float(r["mean_mean_success"]),
    )["method"]
    proposed = {
        r["seed"]: float(r["mean_success"])
        for r in seed_split
        if r["method"] == "proposed_affordance_negotiation" and r["split"] == "combined_stress"
    }
    rows = []
    for method in sorted(combined):
        if method == "proposed_affordance_negotiation":
            continue
        peer = {
            r["seed"]: float(r["mean_success"])
            for r in seed_split
            if r["method"] == method and r["split"] == "combined_stress"
        }
        diffs = [proposed[s] - peer[s] for s in SEEDS]
        wins = sum(1 for d in diffs if d > 0)
        rows.append(
            {
                "comparison": f"proposed_affordance_negotiation_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": mean(diffs),
                "ci95_success_diff": ci95(diffs),
                "wins_over_seeds": wins,
                "seeds": len(SEEDS),
                "decision": "proposed_better" if mean(diffs) > 0 and wins >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for family in FAMILIES:
                for seed in SEEDS:
                    row = simulate_group(method, task, family, split, seed)
                    row["ablation"] = name
                    row["interpretation"] = note
                    rows.append(row)
    metrics = [
        "success",
        "physical_violation",
        "human_burden",
        "intent_error",
        "overpromise",
        "negotiation_rounds",
        "total_cost",
    ]
    seed_summary = aggregate(rows, ["ablation", "seed"], metrics)
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{m}" for m in metrics])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    rows = []
    split = {"split": "stress_sweep", "stress": 0.0, "intent_shift": 0.0, "capability_shift": 0.0, "feedback_delay": 0.0}
    for level in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        split["stress"] = level
        split["intent_shift"] = 0.12 + 0.58 * level
        split["capability_shift"] = 0.10 + 0.60 * level
        split["feedback_delay"] = 0.08 + 0.52 * level
        for method in METHODS:
            for seed in SEEDS:
                groups = [
                    simulate_group(method, task, family, split, seed, stress_override=level)
                    for task in TASKS
                    for family in FAMILIES
                ]
                row = {"stress_level": level, "method": method["method"], "seed": seed}
                for metric in [
                    "success",
                    "physical_violation",
                    "human_burden",
                    "intent_error",
                    "overpromise",
                    "negotiation_rounds",
                    "total_cost",
                ]:
                    row[metric] = mean([g[metric] for g in groups])
                rows.append(row)
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "physical_violation",
        "human_burden",
        "intent_error",
        "overpromise",
        "negotiation_rounds",
        "total_cost",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [r for r in summary if r["split"] == "combined_stress"]
    methods = [r["method"] for r in combined]
    x = np.arange(len(methods))
    colors = ["#7f8c8d"] * len(methods)
    for idx, method in enumerate(methods):
        if method == "proposed_affordance_negotiation":
            colors[idx] = "#bc6c25"
        if method == "oracle_joint_intent_capability_planner":
            colors[idx] = "#283618"

    plt.figure(figsize=(12, 5.8))
    plt.bar(x, [float(r["mean_mean_success"]) for r in combined], yerr=[float(r["ci95_mean_success"]) for r in combined], color=colors, capsize=3)
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Collaborative affordance negotiation benchmark")
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_combined_success.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5.6))
    for row in combined:
        marker, size, color = "o", 60, "#7f8c8d"
        if row["method"] == "proposed_affordance_negotiation":
            marker, size, color = "*", 165, "#bc6c25"
        if row["method"] == "oracle_joint_intent_capability_planner":
            marker, size, color = "D", 85, "#283618"
        plt.scatter(float(row["mean_mean_physical_violation"]) + float(row["mean_mean_human_burden"]), float(row["mean_regret_to_oracle"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("Physical violation + human burden")
    plt.ylabel("Regret to oracle")
    plt.title("Safety/burden versus regret")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_burden_regret.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 5.6))
    width = 0.38
    plt.bar(x - width / 2, [float(r["mean_mean_intent_error"]) for r in combined], width=width, color="#e07a5f", label="intent error")
    plt.bar(x + width / 2, [float(r["mean_mean_overpromise"]) for r in combined], width=width, color="#6a994e", label="over-promise")
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Rate")
    plt.title("Negotiation diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    keep = {"proposed_affordance_negotiation", "shared_autonomy_pomdp", "uncertainty_clarification_policy", "capability_map_tamp", "oracle_joint_intent_capability_planner"}
    for method in sorted({r["method"] for r in stress_summary}):
        if method not in keep:
            continue
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_success"]) for r in series], marker="o", label=method)
    plt.xlabel("Ambiguity/capability stress")
    plt.ylabel("Mean success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_stress_sweep.png", dpi=180)
    plt.close()

    labels = [r["ablation"] for r in ablation_summary]
    ax = np.arange(len(labels))
    plt.figure(figsize=(11, 5.6))
    plt.bar(ax, [float(r["mean_mean_success"]) for r in ablation_summary], yerr=[float(r["ci95_mean_success"]) for r in ablation_summary], color=["#bc6c25" if label == "full_affordance_negotiation" else "#9aa6b2" for label in labels], capsize=3)
    plt.xticks(ax, labels, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Collaborative affordance ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "affordance_ablation.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else str(value).replace("_", "\\_"))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_family, strongest):
    combined = [r for r in per_task_family if r["split"] == "combined_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_affordance_negotiation"]
    peer = {(r["task"], r["family"]): r for r in combined if r["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["family"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "family": row["family"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_physical_violation": row["mean_physical_violation"],
                "proposed_human_burden": row["mean_human_burden"],
                "lesson": "negotiation is dominated when direct shared-autonomy inference resolves the role faster than explicit bargaining",
            }
        )
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    proposed = combined["proposed_affordance_negotiation"]
    base = combined[strongest]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    violation_delta = float(proposed["mean_mean_physical_violation"]) - float(base["mean_mean_physical_violation"])
    burden_delta = float(proposed["mean_mean_human_burden"]) - float(base["mean_mean_human_burden"])
    intent_delta = float(proposed["mean_mean_intent_error"]) - float(base["mean_mean_intent_error"])
    overpromise_delta = float(proposed["mean_mean_overpromise"]) - float(base["mean_mean_overpromise"])
    strongest_pair = next(r for r in pairwise if r["baseline"] == strongest)
    full = next(r for r in ablations if r["ablation"] == "full_affordance_negotiation")
    best_ablation = max([r for r in ablations if r["ablation"] != "full_affordance_negotiation"], key=lambda r: float(r["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    safety_burden_gate = violation_delta <= 0.020 and burden_delta <= 0.020
    diagnostic_gate = intent_delta <= -0.025 or overpromise_delta <= -0.025
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and safety_burden_gate and diagnostic_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local collaborative-affordance evidence supports the mechanism, but real human-robot validation is missing"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the decisive success, safety/burden, diagnostic, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "safety_burden_gate": safety_burden_gate,
        "diagnostic_gate": diagnostic_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "physical_violation_delta_vs_strongest": violation_delta,
        "human_burden_delta_vs_strongest": burden_delta,
        "intent_error_delta_vs_strongest": intent_delta,
        "overpromise_delta_vs_strongest": overpromise_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 102 collaborative_affordance_negotiation evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 collaboration ambiguity families x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"viol={float(row['mean_mean_physical_violation']):.3f}, burden={float(row['mean_mean_human_burden']):.3f}, "
                f"intent_err={float(row['mean_mean_intent_error']):.3f}, overpromise={float(row['mean_mean_overpromise']):.3f}, "
                f"rounds={float(row['mean_mean_negotiation_rounds']):.3f}, regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"viol={float(row['mean_mean_physical_violation']):.3f}, burden={float(row['mean_mean_human_burden']):.3f}, "
                f"note={row['interpretation']}\n"
            )


def main():
    seed_rows, per_task_family, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_family, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_family_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_family_metrics.csv", rounded(per_task_family))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_family_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted([r for r in summary if r["split"] == "combined_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_physical_violation", "Viol."),
            ("mean_mean_human_burden", "Burden"),
            ("mean_mean_intent_error", "IntentErr"),
            ("mean_mean_overpromise", "OverProm."),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-stress collaborative affordance benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_physical_violation", "Viol."),
            ("mean_mean_human_burden", "Burden"),
            ("mean_mean_overpromise", "OverProm."),
        ],
        "Ablations of collaborative affordance negotiation.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-stress success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
