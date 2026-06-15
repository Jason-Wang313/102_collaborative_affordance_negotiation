# Submission Version Log

## v1

Generated draft and repository scaffold.

## v2

Initial hardening pass.

## v3

ICLR-main gate archive. Decision: KILL_ARCHIVE because evidence was synthetic/template-only.

## v4

Paper-specific collaborative-affordance evidence rebuild. Added deterministic NumPy benchmark, strong baselines, ablations, stress sweep, pairwise seed tests, generated figures, LaTeX tables, failure cases, rewritten docs, and a new manuscript. Decision remains KILL_ARCHIVE because the proposed method does not decisively beat `shared_autonomy_pomdp` and fails the ablation gate.

## v4.1

Continuation rerun on 2026-06-15. Recompiled `src/run_experiment.py`, regenerated the benchmark, verified CSV coverage, pairwise statistics, ablations, stress sweep, and failure cases, and kept KILL_ARCHIVE because the success margin over `shared_autonomy_pomdp` is only `+0.0239` and the best removed-component ablation margin is only `+0.0196`.
