# Paper 102 ICLR Submission-Readiness Execution Plan

Started: 2026-06-15 15:37:49 +0100

## Objective

Re-audit Paper 102 end to end under the continuation standard before moving to Paper 103. The paper can only move from `KILL_ARCHIVE` to `STRONG_REVISE` if the rerun evidence actually clears the pre-declared ICLR-main gates. No metric tuning, baseline weakening, or cosmetic upgrade is allowed.

## Current State

- Repo: `102_collaborative_affordance_negotiation`
- Prior terminal decision: `KILL_ARCHIVE`
- Prior hardening version: `v4`
- Canonical PDF target: `C:/Users/wangz/Downloads/102.pdf`
- GitHub: `https://github.com/Jason-Wang313/102_collaborative_affordance_negotiation`
- Known prior fatal issues:
  - Proposed method only beat `shared_autonomy_pomdp` by about `+0.024` combined-stress success, below the `+0.030` practical margin.
  - The best removed-component ablation nearly matched the full method.
  - No real human-robot or external collaborative manipulation validation exists.

## Evidence Gates

Keep `KILL_ARCHIVE` unless all of the following are true on a clean rerun:

1. `python -m py_compile src/run_experiment.py` succeeds.
2. `python src/run_experiment.py` regenerates all result CSVs, tables, and figures without repair-only shortcuts.
3. CSV outputs are finite, nonempty, and cover the declared design: 5 tasks, 7 families, 5 splits, 9 methods, 7 seeds, stress sweep, ablations, and failure cases.
4. `proposed_affordance_negotiation` beats the strongest non-oracle baseline, expected to remain `shared_autonomy_pomdp`, by at least the practical success margin on combined stress.
5. The proposed method does not hide gains behind worse physical violation or excessive human burden.
6. Paired seed statistics support the claim against the strongest baseline.
7. All core ablations remain clearly below the full method.
8. The paper, README, and audit docs state the actual decision honestly, including the lack of real human-robot/external validation.
9. The PDF builds cleanly and is copied only to `C:/Users/wangz/Downloads/102.pdf`.
10. No `102.pdf` is placed on the visible Desktop.
11. The child repo is committed, pushed, clean, and public.
12. Root ledgers are updated only after the child repo and PDF checks pass.

## Execution Steps

1. Re-run the Paper 102 benchmark from source with controlled thread env vars.
2. Audit result coverage, strongest baseline, paired statistics, ablations, stress sweep, and failure cases directly from regenerated CSVs.
3. Decide honestly:
   - `STRONG_REVISE` only if the success, safety/burden, paired-seed, stress, and ablation gates all pass.
   - `KILL_ARCHIVE` if the prior narrow-margin and ablation failures reproduce.
4. Update child docs to v4.1 with exact rerun evidence.
5. Update `paper/main.tex` only to make the manuscript match the verified evidence; do not inflate claims.
6. Rebuild LaTeX, scan logs, copy `102.pdf` to Downloads, hash it, and verify Desktop exclusion.
7. Commit and push the child repo; verify local/remote SHA match and public GitHub visibility.
8. Update the root reports through Paper 102.

## Expected Outcome Before Rerun

The expected outcome is likely `KILL_ARCHIVE`, because the existing evidence says the method narrowly improves safety/over-promise but fails the practical success and ablation gates. That expectation is not a conclusion; the rerun decides.
