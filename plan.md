# Plan

Paper 102 v5 expanded-submission rebuild executed from `docs/paper102_expanded_submission_plan_20260622.md`.

Terminal result: STRONG_REVISE.

Frozen local empirical gates passed: success, physical safety, burden, intent, over-promise, conflict/query, calibration, regret, utility, pairwise, ablation, stress, and fixed-risk.

Failed submission-readiness gate: scope. The artifact still lacks real human-robot validation, accepted high-fidelity benchmark evidence, external collaborative-manipulation benchmarks, calibrated human-intent logs, trained checkpoints, rollout videos, and deeper manual related-work synthesis.

Next revival work:

1. Evaluate the frozen method on real human-robot collaborative manipulation or accepted HRI benchmark tasks.
2. Calibrate intent, burden, and over-promise regimes from human-subject or robot logs rather than only executable surrogate distributions.
3. Replace the executable proxy with a trained graph/belief model and release checkpoints plus model cards.
4. Compare against deployed shared-autonomy, human-model MPC, and risk-aware HRI systems under the same fixed protocol.
5. Release per-episode traces, videos, and external failure audits.
