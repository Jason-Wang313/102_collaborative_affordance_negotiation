# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

The v4 rebuild adds a paper-specific collaborative-affordance benchmark with strong baselines, ablations, uncertainty intervals, stress tests, failure cases, generated figures, generated tables, and reproducible code. The evidence is not strong enough to revive the paper.

Fatal evidence:

- Success gate failed: proposed gain over `shared_autonomy_pomdp` is `+0.024`, below the `+0.030` practical margin.
- Ablation gate failed: removing burden-aware query value nearly matches the full method.
- Real human-robot validation is absent.

Honest terminal action: archive/kill for ICLR main.
