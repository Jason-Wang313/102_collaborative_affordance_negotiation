# Paper 102 Expanded Submission Plan 2026-06-22

Paper: 102 collaborative_affordance_negotiation

Target: rebuild into a 25+ page, CPU-only, RAM-light, hostile-review evidence package.

Terminal rule: optimize for a result that survives hostile review, not for a pretty result. Freeze this protocol before executing the v5 runner. Report every predefined gate honestly.

## Starting Point

The v4.1 continuation audit was `KILL_ARCHIVE`. The old proposed method improved safety and over-promise but only beat `shared_autonomy_pomdp` by `+0.0239` combined-stress success, below the declared `+0.030` practical gate. The old ablation gate also failed.

The v5 rebuild may revive the paper only if a substantially stronger mechanism clears all local gates. Otherwise the correct terminal state remains `KILL_ARCHIVE`.

## New Mechanism Under Test

Method name: `risk_calibrated_collaborative_affordance_v5`.

Mechanism claim: collaborative robot action selection improves when human intent, robot capability, role assignment, physical over-promise risk, query burden, and interaction calibration are represented jointly as a risk-calibrated negotiation state. The method should ask fewer unnecessary questions than clarification-only policies, avoid unsafe over-promising better than intent-only policies, and beat shared-autonomy baselines on closed-loop utility rather than only on diagnostics.

## Frozen Benchmark

Use a streaming CPU-only simulator that writes aggregate rows to disk instead of storing trajectories in memory.

Design:

- 6 tasks.
- 8 collaboration ambiguity regimes.
- 8 splits.
- 15 methods.
- 10 seeds.
- 6 episodes per method/task/regime/split/seed cell.

Expected main rollout rows: 345,600.

### Tasks

- `handover_grip_choice`
- `co_carry_doorway`
- `assisted_assembly`
- `collaborative_sorting`
- `tool_use_handoff`
- `shared_fixture_insertion`

### Ambiguity Regimes

- `ambiguous_intent`
- `asymmetric_reach`
- `load_sharing_mismatch`
- `occluded_human_goal`
- `ergonomic_constraint`
- `role_switch_request`
- `conflicting_safety_preference`
- `temporal_commitment_drift`

### Splits

- `nominal`
- `intent_ambiguity_shift`
- `capability_shift`
- `delayed_human_feedback`
- `burden_sensitive_shift`
- `false_clarification_shift`
- `overtrust_safety_shift`
- `combined_extreme`

### Methods

- `robot_capability_only_planner`
- `intent_only_follower`
- `language_affordance_planner`
- `static_role_policy`
- `uncertainty_clarification_policy`
- `shared_autonomy_pomdp`
- `capability_map_tamp`
- `human_model_mpc`
- `inverse_rl_intent_pomdp`
- `risk_aware_shared_autonomy`
- `conformal_intent_risk_filter`
- `active_clarification_bandit`
- `proposed_affordance_negotiation_v4`
- `risk_calibrated_collaborative_affordance_v5`
- `oracle_joint_intent_capability_planner`

## Metrics

Report all metrics by split/method, hard aggregate, seed, ablation, stress, and fixed-risk where applicable:

- task success
- physical violation
- human burden
- intent-alignment error
- over-promise rate
- autonomy conflict rate
- unnecessary query rate
- negotiation rounds
- expected calibration error
- regret to oracle
- utility

Utility must penalize physical violation, human burden, intent error, over-promise, conflict, unnecessary query, and excessive negotiation rounds.

## Required Evidence Outputs

- `results/dataset_summary.csv`
- `results/rollouts.csv`
- `results/main_group_metrics.csv`
- `results/main_seed_metrics.csv`
- `results/metrics.csv`
- `results/hard_aggregate_seed_metrics.csv`
- `results/hard_aggregate_metrics.csv`
- `results/pairwise_stats.csv`
- `results/ablation_rollouts.csv`
- `results/ablation_seed_metrics.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep_raw.csv`
- `results/stress_sweep_seed_metrics.csv`
- `results/stress_sweep.csv`
- `results/fixed_risk_raw.csv`
- `results/fixed_risk_seed_metrics.csv`
- `results/fixed_risk_metrics.csv`
- `results/fixed_risk_pairwise_stats.csv`
- `results/failure_cases.csv`
- generated tables and figures from those CSVs
- a 25+ page manuscript with visible boxed citation links
- canonical numbered PDF copied only to `C:/Users/wangz/Downloads/102.pdf`

## Frozen Local Gates

Mark `STRONG_REVISE` only if every local empirical gate below passes. Otherwise mark `KILL_ARCHIVE`.

- Success gate: v5 must beat the strongest non-oracle success reference on the hard aggregate.
- Physical-safety gate: v5 physical violation must be lower than the strongest non-oracle success reference.
- Burden gate: v5 human burden must not exceed the strongest non-oracle success reference by more than `0.015`.
- Intent gate: v5 intent error must be lower than the strongest non-oracle success reference.
- Over-promise gate: v5 over-promise must be lower than the strongest non-oracle success reference.
- Conflict/query gate: v5 must not win by spamming clarifications; unnecessary query and autonomy conflict rates must remain controlled.
- Calibration gate: v5 ECE must be lower than the strongest non-oracle success reference.
- Regret gate: v5 regret to oracle must be lower than the strongest non-oracle success reference.
- Utility gate: v5 utility must exceed the strongest non-oracle utility reference.
- Pairwise gate: v5 must beat every non-oracle baseline in seed-level success comparisons on the hard aggregate.
- Ablation gate: removing intent belief, capability map, burden-aware query value, role negotiation, over-promise risk, calibration, or active repair must reduce success or utility.
- Stress gate: v5 must remain ahead of the strongest non-oracle method at maximum ambiguity/capability stress.
- Fixed-risk gate: v5 must remain competitive under fixed physical-risk budgets and cannot win by abstaining.

## Scope Gate

The scope gate fails by default unless the repository contains real human-robot studies, accepted external collaborative-manipulation benchmarks, calibrated human-intent logs, a trained deployable model checkpoint, and rollout videos. A local CPU-only surrogate cannot be called ICLR-main ready.

## Expected Terminal Wording

- `STRONG_REVISE`: local mechanism is supported, but ICLR-main readiness is no because the scope gate fails.
- `KILL_ARCHIVE`: local mechanism does not survive the frozen empirical gates; do not submit.

## Execution Order

1. Replace `src/run_experiment.py` with the frozen v5 runner.
2. Run the full benchmark once.
3. Generate manuscript, bibliography, figures, tables, and validator.
4. Compile PDF to at least 25 pages with boxed citation links.
5. Validate row counts, finite metrics, py_compile, LaTeX logs, PDF page count, SHA256, no Desktop PDF, no repo-local numbered PDF, and no stale docs.
6. Commit and push to the public GitHub repository.
7. Update root ledgers only after the child repo is clean and pushed.
