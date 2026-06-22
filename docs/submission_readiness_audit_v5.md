# Submission Readiness Audit v5

Paper: 102 collaborative_affordance_negotiation

Terminal decision: STRONG_REVISE

ICLR-main readiness: no

Canonical PDF: `C:/Users/wangz/Downloads/102.pdf`

PDF SHA256: `C384D1E57B0C3F5C42B044027505CD847BBDFA1FD82FB513ABBCDDF0BEADC69E`

Page count: 27

## Frozen Protocol

- 6 tasks.
- 8 collaboration regimes.
- 8 splits.
- 15 methods.
- 10 seeds.
- 6 episodes per method/task/regime/split/seed cell.

## Produced Evidence

- Dataset summary rows: 3,840.
- Main rollout rows: 345,600.
- Main group rows: 57,600.
- Main seed rows: 150.
- Main metric rows: 120.
- Hard aggregate seed rows: 150.
- Hard aggregate metric rows: 15.
- Pairwise comparison rows: 14.
- Ablation rollout rows: 115,200.
- Stress rollout rows: 288,000.
- Fixed-risk rollout rows: 276,480.
- Negative cases: 24.

## Main Result

- v5 success: `0.73038 +/- 0.00638`.
- v5 physical violation: `0.06693`.
- v5 human burden: `0.25547`.
- v5 intent error: `0.24809`.
- v5 over-promise: `0.12101`.
- v5 ECE: `0.09596`.
- v5 regret: `0.07670`.
- v5 utility: `0.35244`.
- strongest non-oracle success: `0.63090 +/- 0.00787`.
- shared-autonomy POMDP success: `0.60503 +/- 0.00663`.
- oracle success: `0.79783 +/- 0.00834`.

## Gate Result

Passed local gates: success, physical safety, burden, intent, over-promise, conflict/query, calibration, regret, utility, pairwise, ablation, stress, fixed-risk.

Failed gate: scope.

## Required Before Submission

- Real human-robot validation or accepted high-fidelity benchmark validation.
- External benchmark comparison.
- Calibrated intent, burden, and over-promise logs.
- Trained checkpoint and model card.
- Rollout videos and per-episode traces.
- Full manual related-work synthesis.
