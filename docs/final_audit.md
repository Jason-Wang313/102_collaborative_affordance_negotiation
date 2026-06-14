# Final Audit

Paper 102 v4 was rebuilt as a collaborative-affordance evidence audit.

## Evidence Audit

The proposed method improves safety and over-promise relative to `shared_autonomy_pomdp`, but the success margin is too small for the required gate. The best ablation nearly matches the full method.

## Terminal Decision

KILL_ARCHIVE.

The idea should not be submitted to ICLR main. It may be useful as a negative result showing that explicit negotiation must beat strong shared-autonomy baselines, not merely improve diagnostics.

## Verification Targets

- Re-run: `python src\run_experiment.py`.
- Main table: `results/combined_stress_table.tex`.
- Ablation table: `results/ablation_table.tex`.
- Pairwise table: `results/pairwise_decision_table.tex`.
- PDF target: `C:/Users/wangz/Downloads/102.pdf`.
