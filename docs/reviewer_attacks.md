# Reviewer Attacks

1. The proposed method does not decisively beat `shared_autonomy_pomdp`: v4.1 margin is `+0.0239`, below the `+0.030` gate.
2. The ablation removing burden-aware query value remains too close to the full method: `0.6045` vs `0.6241` success.
3. The benchmark uses simulated human intent and burden rather than human-subject data.
4. Real collaborative robotics needs timing, trust, ergonomics, and adaptation evidence.
5. The oracle gap remains large: `0.6288` proposed success versus `0.7602` oracle success.
6. Human burden is abstract and not validated with participant measures.
7. Related work still needs a full manual synthesis.
