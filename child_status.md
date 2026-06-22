# Child Status

Paper: 102 collaborative_affordance_negotiation

Status: SUCCESS_STRONG_REVISE

Hardening version: v5 expanded

Last update: 2026-06-22

PDF: C:/Users/wangz/Downloads/102.pdf

PDF SHA256: C384D1E57B0C3F5C42B044027505CD847BBDFA1FD82FB513ABBCDDF0BEADC69E

Pages: 27

GitHub: https://github.com/Jason-Wang313/102_collaborative_affordance_negotiation

Evidence: v5 rerun with 345,600 main closed-loop rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, 24 negative cases, strong non-oracle baselines, oracle reference, calibration and fixed-risk tests, generated figures, generated tables, and a 27-page manuscript with boxed citation links. The proposed `risk_calibrated_collaborative_affordance_v5` reaches success 0.73038 versus 0.63090 for the strongest non-oracle success reference and 0.60503 for `shared_autonomy_pomdp`.

ICLR main ready: no. All local empirical gates pass, but the scope gate fails because human-robot validation, calibrated human-intent logs, accepted high-fidelity benchmark evidence, a trained deployable checkpoint, and rollout videos are still missing.
