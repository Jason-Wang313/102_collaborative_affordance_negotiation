# ICLR Main Gate

Paper: 102 collaborative_affordance_negotiation

Previous v3 decision: KILL_ARCHIVE

Current v4 gate verdict: KILL_ARCHIVE

## Gate Evidence

- Local benchmark: 5 tasks, 7 collaboration ambiguity families, 5 splits, 9 methods.
- Seeds: 7.
- Episodes: 84 per method/task/family/split/seed group.
- Strongest non-oracle baseline: `shared_autonomy_pomdp`.
- Proposed vs strongest baseline combined-stress success margin: `+0.024`.
- Proposed vs strongest physical-violation delta: `-0.030`.
- Proposed vs strongest human-burden delta: `+0.010`.
- Full method vs best removed-component ablation margin: `+0.020` before stricter unrounded gate precision.

## Passed Local Gates

- Safety/burden gate: passed.
- Diagnostic gate: passed.
- Pairwise seed gate: passed.

## Failed Gates

- Success gate: failed.
- Ablation gate: failed.
- External validation gate: failed.

Conclusion: KILL_ARCHIVE. Do not submit.
