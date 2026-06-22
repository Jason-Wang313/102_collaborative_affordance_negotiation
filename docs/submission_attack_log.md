# Submission Attack Log

Paper: 102 collaborative_affordance_negotiation

## Attack 1: No real human-robot validation

Verdict: still valid. This blocks ICLR-main readiness.

Action: mark STRONG_REVISE, not ready.

## Attack 2: No external benchmark

Verdict: still valid. The v5 local benchmark is large and targeted, but local evidence is not enough.

Action: require external collaborative-manipulation validation before submission.

## Attack 3: Shared-autonomy baselines are weak

Verdict: materially improved. v5 includes shared-autonomy POMDP, risk-aware shared autonomy, human-model MPC, inverse-RL intent POMDP, active clarification, conformal intent-risk filtering, capability-map TAMP, v4 detector, and oracle.

Action: keep as STRONG_REVISE because baselines are stronger, but most remain executable proxies rather than deployed systems.

## Attack 4: The method wins by burdening the human

Verdict: addressed locally. Burden, unnecessary query, negotiation rounds, and fixed-risk safe-repair cost are reported explicitly.

Action: keep burden and query metrics central in the manuscript.

## Attack 5: Fixed-risk could be abstention

Verdict: addressed locally. Fixed-risk uses a safe-repair fallback with visible burden/query cost. Strict v5 coverage is `0.87101`, not near-zero abstention.

Action: report fixed-risk coverage and still list real-time HRI validation as missing.

## Attack 6: Ablations may not isolate affordance negotiation

Verdict: addressed locally. Removing intent belief, capability map, burden-aware query value, role negotiation, over-promise risk, calibration, or active repair reduces success or utility.

Action: preserve ablation table and avoid overstating causality beyond the local benchmark.

## Attack 7: Related work is incomplete

Verdict: still valid.

Action: require manual survey before submission.

## Terminal Action

STRONG_REVISE. Continue only with external experiments; do not submit this version to ICLR main.
