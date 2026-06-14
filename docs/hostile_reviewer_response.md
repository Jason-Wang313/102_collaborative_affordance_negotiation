# Hostile Reviewer Response

## Attack: The method does not beat shared autonomy decisively.

Response: Correct. The strongest non-oracle baseline is `shared_autonomy_pomdp`. The proposed method improves success by only `0.024`, below the `0.030` gate. This is the main reason for KILL_ARCHIVE.

## Attack: The method wins by asking more or shifting burden.

Response: The burden delta is small (`+0.010`) and the safety/burden gate passes, but the success gain is still too small.

## Attack: The ablation story is weak.

Response: Correct. `minus_burden_aware_query_value` nearly matches full success, so the ablation gate fails.

## Attack: There is no real HRI validation.

Response: Correct. The benchmark is local and synthetic-HRI. A revival would need real human-robot experiments or accepted high-fidelity collaborative benchmarks.
