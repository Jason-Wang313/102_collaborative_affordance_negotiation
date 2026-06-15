# Claims

## Supported Local Claim

Collaborative affordance negotiation can reduce physical violations and over-promise relative to shared-autonomy baselines in the local benchmark. The 2026-06-15 continuation rerun reproduced this local diagnostic claim.

## Unsupported Main Claim

The method does not decisively improve closed-loop task success over the strongest non-oracle baseline. The combined-stress success margin over `shared_autonomy_pomdp` is only `+0.0239`, below the required `+0.030` gate.

## Evidence

- Proposed combined-stress success: `0.6288 +/- 0.0042`.
- `shared_autonomy_pomdp` combined-stress success: `0.6049 +/- 0.0054`.
- Proposed physical violation: `0.1091`; shared-autonomy baseline: `0.1396`.
- Proposed human burden: `0.2076`; shared-autonomy baseline: `0.1975`.
- Best removed-component ablation, `minus_burden_aware_query_value`, reaches `0.6045` success vs `0.6241` for full.

## Terminal Claim

KILL_ARCHIVE. The mechanism is not strong enough for an ICLR-main-target paper without a substantially new empirical project.
