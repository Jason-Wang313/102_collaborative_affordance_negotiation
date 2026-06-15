# Submission Readiness Audit v4.1

Audit date: 2026-06-15 15:49:54 +0100

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

## Commands Executed

- `python -m py_compile src/run_experiment.py`
- `python src/run_experiment.py`

Continuation rerun log:

- `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/102_collaborative_affordance_negotiation_continuation_rerun_20260615.log`

## Regenerated Evidence Coverage

- `metrics.csv`: 45 rows.
- `per_task_family_metrics.csv`: 1575 rows.
- `seed_task_family_metrics.csv`: 11025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_family_seed_metrics.csv`: 1715 rows.
- `stress_sweep.csv`: 54 rows.
- `stress_sweep_seed_metrics.csv`: 378 rows.
- `failure_cases.csv`: 8 rows.

Coverage remained the declared design: 5 tasks, 7 collaboration ambiguity families, 5 splits, 9 methods, and 7 seeds.

## Main Gate Evidence

Strongest non-oracle baseline: `shared_autonomy_pomdp`.

Combined-stress metrics:

- Proposed success: `0.6288 +/- 0.0042`.
- Strongest baseline success: `0.6049 +/- 0.0054`.
- Success margin: `+0.0239`, below the `+0.030` practical gate.
- Proposed physical violation: `0.1091` vs `0.1396` baseline.
- Proposed human burden: `0.2076` vs `0.1975` baseline.
- Proposed intent error: `0.3300` vs `0.3435` baseline.
- Proposed over-promise: `0.0929` vs `0.1610` baseline.
- Proposed regret to oracle: `0.1314` vs `0.1553` baseline.

Paired seed comparison against `shared_autonomy_pomdp`:

- Success difference: `0.0239 +/- 0.0086`.
- Wins: `7/7`.

The pairwise result is positive, but it does not override the pre-declared practical success gate.

## Ablation Gate

- Full method success: `0.6241 +/- 0.0058`.
- Best removed-component ablation: `minus_burden_aware_query_value`.
- Best removed-component success: `0.6045 +/- 0.0110`.
- Ablation margin: `+0.0196`, below the required core-component separation.

The method therefore cannot claim that burden-aware negotiation is the decisive ingredient.

## Stress Sweep

The proposed method remains competitive across stress levels but does not establish decisive separation from `shared_autonomy_pomdp`. At maximum stress level `1.0`, proposed success is `0.6197 +/- 0.0078` vs `0.6009 +/- 0.0069` for `shared_autonomy_pomdp`.

## Terminal Decision

Keep `KILL_ARCHIVE`. The paper has useful negative evidence: explicit collaborative affordance negotiation reduces violation and over-promise, but the practical task-success gain and ablation evidence are too weak for an ICLR-main submission.

## PDF Verification

- Canonical PDF: `C:/Users/wangz/Downloads/102.pdf`.
- SHA256: `C59626EBAC3DCECF972EC578641B398A80CEE497CAAE6FF3B7D77665D71A39B8`.
- Size: `638649` bytes.
- Desktop copy: absent.
- LaTeX/BibTeX scan: no actionable warnings after regenerating tables with width-bounded tabular output; only harmless `rerunfilecheck` package text and BibTeX built-in statistics appeared.
