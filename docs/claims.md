# Claims

## Supported Local Claim

Risk-calibrated collaborative affordance negotiation improves closed-loop collaborative manipulation in a local CPU-only benchmark. The claim covers human intent, robot capability, role assignment, burden-aware queries, physical over-promise risk, active safe repair, and fixed-risk deployment.

## Evidence

- Benchmark: 6 tasks x 8 collaboration regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.
- Main rollouts: 345,600.
- Proposed v5 hard-aggregate success: `0.73038 +/- 0.00638`.
- Strongest non-oracle success reference, `proposed_affordance_negotiation_v4`: `0.63090 +/- 0.00787`.
- Shared-autonomy POMDP success: `0.60503 +/- 0.00663`.
- Oracle reference: `0.79783 +/- 0.00834`.
- Safety and burden: v5 physical violation `0.06693`, human burden `0.25547`.
- Diagnostics: v5 intent error `0.24809`, over-promise `0.12101`, autonomy conflict `0.01589`, unnecessary query `0.00156`, ECE `0.09596`.
- Utility/regret: v5 utility `0.35244`, regret `0.07670`.
- Ablation: full v5 success `0.72023`; best removed-component success `0.67856`.
- Fixed-risk strict v5: coverage `0.87101`, success `0.62309`, physical violation `0.04861`, human burden `0.34288`, unnecessary query `0.15469`, utility `0.19317`.

## Scope

The claim is local. It does not prove real HRI performance, external benchmark superiority, deployable model performance, or broad dominance over all shared-autonomy and collaborative manipulation systems.
