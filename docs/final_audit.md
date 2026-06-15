# Final Audit

Paper 102 v4.1 was rebuilt and re-audited as a collaborative-affordance evidence audit.

## Evidence Audit

The 2026-06-15 rerun regenerated the full benchmark. The proposed method improves safety and over-promise relative to `shared_autonomy_pomdp`, but the success margin is only `+0.0239`, too small for the `+0.030` gate. The best removed-component ablation is also too close: `0.6045` success for `minus_burden_aware_query_value` vs `0.6241` for the full method.

## Terminal Decision

KILL_ARCHIVE.

The idea should not be submitted to ICLR main. It may be useful as a negative result showing that explicit negotiation must beat strong shared-autonomy baselines, not merely improve diagnostics.

## Verification Targets

- Re-run: `python src\run_experiment.py`.
- Continuation log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/102_collaborative_affordance_negotiation_continuation_rerun_20260615.log`.
- Main table: `results/combined_stress_table.tex`.
- Ablation table: `results/ablation_table.tex`.
- Pairwise table: `results/pairwise_decision_table.tex`.
- PDF target: `C:/Users/wangz/Downloads/102.pdf`.
