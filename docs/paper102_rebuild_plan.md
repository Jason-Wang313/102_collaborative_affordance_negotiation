# Paper 102 Rebuild Plan: Collaborative Affordance Negotiation

Started: 2026-06-14 23:18:00 +0100

## Goal

Rebuild Paper 102 from a template archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that modeling affordances as negotiated between human intent and robot physical capability improves collaborative robot task success without excessive human burden or unsafe over-promising.

## Claimed Mechanism

The proposed method, `proposed_affordance_negotiation`, maintains a joint belief over:

- human intent;
- robot reach/force/collision capability;
- shared object affordances;
- role assignment;
- clarification value;
- physical over-promise risk;
- human burden from asking too many questions.

It should negotiate a feasible collaborative action before execution rather than either blindly following inferred intent or conservatively asking the human for every ambiguous choice.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than full trajectory storage. The benchmark will cover:

- 5 collaborative tasks: handover with grip choice, co-carry through a doorway, assisted assembly, collaborative sorting, and tool-use handoff.
- 7 ambiguity/failure families: ambiguous intent, asymmetric reach, load-sharing mismatch, occluded human goal, ergonomic constraint, role-switch request, and conflicting safety/preference constraints.
- 5 splits: nominal, intent ambiguity shift, capability shift, delayed human feedback, and combined stress.
- 9 methods: robot-capability-only planner, intent-only follower, language-affordance planner, static role policy, uncertainty clarification policy, shared-autonomy POMDP, capability-map TAMP, proposed affordance negotiation, and oracle joint intent/capability planner.
- 7 random seeds with independent task/family episodes.

## Evidence Requirements

The rebuild must produce:

- Task success, physical violation, human burden, intent-alignment error, over-promise rate, negotiation rounds, regret, and total cost.
- Per-task/per-family breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over ambiguity/capability mismatch.
- Ablations for intent belief, capability map, burden-aware query value, role negotiation, and over-promise risk.
- Failure cases explaining when negotiation is unnecessary, too slow, or dominated by simple clarification.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined-stress success by a meaningful margin.
- Does not increase physical violations or human burden relative to the strongest baseline.
- Improves intent alignment or over-promise rate relative to non-negotiating baselines.
- Wins paired seed comparisons against the strongest baseline.
- Survives core ablations: removing intent belief, capability maps, query-value/burden modeling, role negotiation, or over-promise risk must not match the full method.
- States clearly that real human-subject/robot validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared probability script with a paper-specific collaborative-affordance benchmark.
2. Generate metrics, seed metrics, per-task/per-family tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `102.pdf` to `C:/Users/wangz/Downloads/102.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, families, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.

## Execution Result

Completed: 2026-06-14 23:21:13 +0100

The benchmark was implemented and run. Terminal gate result: KILL_ARCHIVE. The proposed method improved safety/over-promise but did not clear the practical success margin against `shared_autonomy_pomdp`, and the best removed-component ablation nearly matched the full method.

## Continuation Result

Re-audited: 2026-06-15 15:49:54 +0100

The v4.1 continuation rerun recompiled and regenerated the benchmark from source. Terminal gate result remains KILL_ARCHIVE: combined-stress success margin over `shared_autonomy_pomdp` is `+0.0239`, below the `+0.030` practical gate, and the best removed-component ablation margin is only `+0.0196`.
