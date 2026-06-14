# Claims

## Supported Local Claim

Collaborative affordance negotiation can reduce physical violations and over-promise relative to shared-autonomy baselines in the local benchmark.

## Unsupported Main Claim

The method does not decisively improve closed-loop task success over the strongest non-oracle baseline. The combined-stress success margin over `shared_autonomy_pomdp` is only `+0.024`, below the required `+0.030` gate.

## Evidence

- Proposed combined-stress success: `0.629 +/- 0.004`.
- `shared_autonomy_pomdp` combined-stress success: `0.605 +/- 0.005`.
- Proposed physical violation: `0.109`; shared-autonomy baseline: `0.140`.
- Proposed human burden: `0.208`; shared-autonomy baseline: `0.197`.
- Best removed-component ablation, `minus_burden_aware_query_value`, nearly matches full success.

## Terminal Claim

KILL_ARCHIVE. The mechanism is not strong enough for an ICLR-main-target paper without a substantially new empirical project.
