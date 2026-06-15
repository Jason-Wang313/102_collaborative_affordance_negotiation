# ICLR Main Gate

Paper: 102 collaborative_affordance_negotiation

Previous v3 decision: KILL_ARCHIVE

Current v4.1 gate verdict: KILL_ARCHIVE

## Gate Evidence

- Local benchmark: 5 tasks, 7 collaboration ambiguity families, 5 splits, 9 methods.
- Seeds: 7.
- Episodes: 84 per method/task/family/split/seed group.
- Strongest non-oracle baseline: `shared_autonomy_pomdp`.
- Proposed vs strongest baseline combined-stress success margin: `+0.0239`.
- Proposed vs strongest physical-violation delta: `-0.0304`.
- Proposed vs strongest human-burden delta: `+0.0102`.
- Full method vs best removed-component ablation margin: `+0.0196`.

## Passed Local Gates

- Safety/burden gate: passed.
- Diagnostic gate: passed.
- Pairwise seed gate: passed.
- Continuation rerun gate: passed.

## Failed Gates

- Success gate: failed.
- Ablation gate: failed.
- External validation gate: failed.

Conclusion: KILL_ARCHIVE. Do not submit.
