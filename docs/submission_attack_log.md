# Submission Attack Log

Paper: 102 collaborative_affordance_negotiation

## Attack 1: No real human-robot validation

Verdict: valid and fatal for submission readiness.

Action: keep as KILL_ARCHIVE.

## Attack 2: No decisive gain over shared autonomy

Verdict: valid. The proposed method beats `shared_autonomy_pomdp` by only `0.0239` success under combined stress in the v4.1 rerun.

Action: fail the success gate.

## Attack 3: Negotiation may just be expensive clarification

Verdict: partly valid. The ablation removing burden-aware query value reaches `0.6045` success vs `0.6241` for full.

Action: fail the ablation gate.

## Attack 4: Safety gains are not enough

Verdict: valid. Proposed violations and over-promise are lower, but ICLR-main revival needs decisive task success and ablation evidence.

Action: report as useful negative evidence.

## Attack 5: Human burden is synthetic

Verdict: valid. No participant study or workload measure exists.

Action: do not claim HRI readiness.

## Terminal Action

KILL_ARCHIVE. Do not submit to ICLR main.
