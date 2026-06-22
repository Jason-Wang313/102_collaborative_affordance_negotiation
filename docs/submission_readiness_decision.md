# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v5 expanded rebuild executed a frozen, paper-specific collaborative-affordance benchmark. It includes strong baselines, ablations, stress tests, fixed-risk tests, seed uncertainty, pairwise comparisons, failure cases, generated figures, generated tables, a 27-page manuscript, and reproducible code. The local evidence supports the mechanism against every non-oracle baseline.

Reproduced local gates:

- Success gate: proposed v5 success `0.73038 +/- 0.00638` vs `0.63090 +/- 0.00787` for the strongest non-oracle success reference and `0.60503 +/- 0.00663` for shared-autonomy POMDP.
- Physical-safety gate: proposed physical violation `0.06693`, below the strongest success reference.
- Burden gate: proposed human burden `0.25547`, within the frozen burden margin.
- Diagnostic gates: intent error `0.24809`, over-promise `0.12101`, autonomy conflict `0.01589`, unnecessary query `0.00156`.
- Calibration gate: proposed ECE `0.09596`.
- Pairwise gate: proposed v5 beats all non-oracle baselines and trails only the oracle.
- Utility/regret gate: proposed utility `0.35244` and regret `0.07670`.
- Ablation gate: full v5 success `0.72023` vs best removed-component success `0.67856`.
- Fixed-risk gate: strict coverage `0.87101`, success `0.62309`, physical violation `0.04861`, human burden `0.34288`, utility `0.19317`.
- Scope gate: failed.

The paper is not submission-ready because validation remains local. It still lacks real HRI deployment, accepted external benchmark comparison, calibrated intent/burden logs, trained model checkpoints, videos, and a full manual related-work synthesis.

Honest terminal action: keep as STRONG_REVISE. Do not submit to ICLR main until external empirical validation exists.
