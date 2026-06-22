# ICLR Main Gate

Paper: 102 collaborative_affordance_negotiation

Previous v4.1 decision: KILL_ARCHIVE

Current v5 gate verdict: STRONG_REVISE

ICLR-main readiness: no

## Gate Evidence

- Local benchmark: 6 tasks, 8 collaboration regimes, 8 splits, 15 methods.
- Seeds: 10.
- Episodes: 6 per method/task/regime/split/seed cell.
- Main rollouts: 345,600.
- Strongest non-oracle success reference: `proposed_affordance_negotiation_v4`.
- Proposed v5 versus strongest non-oracle success margin: `+0.09948`.
- Proposed v5 versus shared-autonomy POMDP success margin: `+0.12535`.
- Proposed v5 versus oracle success margin: `-0.06745`.
- Proposed v5 physical violation: `0.06693`.
- Proposed v5 human burden: `0.25547`.
- Proposed v5 intent error: `0.24809`.
- Proposed v5 over-promise: `0.12101`.
- Proposed v5 ECE: `0.09596`.
- Proposed v5 utility: `0.35244`.
- Strict fixed-risk v5 coverage: `0.87101`.

## Passed Local Gates

- Success gate: passed.
- Physical-safety gate: passed.
- Burden gate: passed.
- Intent gate: passed.
- Over-promise gate: passed.
- Conflict/query gate: passed.
- Calibration gate: passed.
- Regret gate: passed.
- Utility gate: passed.
- Pairwise gate: passed.
- Ablation gate: passed.
- Stress gate: passed.
- Fixed-risk gate: passed.

## Failed Submission-Ready Gates

- No real human-robot validation.
- No accepted high-fidelity collaborative-manipulation benchmark validation.
- No accepted external benchmark validation.
- No calibrated external human-intent or burden logs.
- No trained checkpoint or deployable model card.
- No rollout videos.
- Related-work synthesis is still not enough for a main-conference submission.

Conclusion: viable STRONG_REVISE project, not ICLR-main ready.
