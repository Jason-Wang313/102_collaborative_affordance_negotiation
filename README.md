# 102 Collaborative Affordance Negotiation

Submission-hardening version: v5 expanded.

Terminal decision: STRONG_REVISE for an ICLR-main-target project, not submission-ready.

Paper 102 was rebuilt from the v4.1 negative audit into a CPU-only, RAM-light, hostile-review evidence package for risk-calibrated collaborative affordance negotiation. The v5 rebuild revives the local mechanism because every frozen local empirical gate passes, including fixed-risk non-abstention. It still refuses ICLR-main readiness because the scope gate fails.

Public repository: `https://github.com/Jason-Wang313/102_collaborative_affordance_negotiation`

Canonical local PDF: `C:/Users/wangz/Downloads/102.pdf`

PDF SHA256: `C384D1E57B0C3F5C42B044027505CD847BBDFA1FD82FB513ABBCDDF0BEADC69E`

Page count: 27.

## Key Evidence

- Frozen benchmark design: 6 tasks x 8 collaboration regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.
- Main evidence scale: 345,600 closed-loop rollout rows, 57,600 group rows, 150 hard seed rows, 120 method/split metric rows.
- Proposed v5 hard aggregate: success `0.73038 +/- 0.00638`, physical violation `0.06693`, human burden `0.25547`, intent error `0.24809`, over-promise `0.12101`, autonomy conflict `0.01589`, unnecessary query `0.00156`, ECE `0.09596`, regret `0.07670`, utility `0.35244`.
- Strongest non-oracle success reference: `proposed_affordance_negotiation_v4` success `0.63090 +/- 0.00787`, physical violation `0.11024`, human burden `0.28759`, utility `0.13749`.
- Strongest non-oracle utility reference: `risk_aware_shared_autonomy` utility `0.15211`.
- Shared-autonomy POMDP reference: success `0.60503 +/- 0.00663`, physical violation `0.13194`, burden `0.26285`, utility `0.07035`.
- Oracle reference: success `0.79783 +/- 0.00834`.
- Ablation scale: 115,200 rollout rows. Full v5 success `0.72023`; best removed-component success `0.67856`.
- Stress scale: 288,000 rollout rows. Fixed-risk scale: 276,480 rows.
- Strict fixed-risk v5: coverage `0.87101`, success `0.62309`, physical violation `0.04861`, burden `0.34288`, unnecessary query `0.15469`, utility `0.19317`.
- Negative-case ledger: 24 curated failure cases.
- Local gates passed: success, physical safety, burden, intent, over-promise, conflict/query, calibration, regret, utility, pairwise, ablation, stress, and fixed-risk.
- Scope gate failed: no real human-robot study, accepted high-fidelity benchmark, external collaborative-manipulation benchmark, calibrated human-intent logs, trained checkpoint, or rollout videos.

## Reproduce Evidence

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
python scripts\validate_submission_artifacts.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript uses boxed hyperlink citations so in-text citations route directly to the reference section.

## Honest Limitation

This is a rigorous local surrogate audit, not a submission-ready HRI deployment result. The paper should not be submitted to ICLR main until the same claims survive real human-robot validation, accepted external benchmarks, calibrated human-intent logs, trained-model release, videos, and deeper manual related-work synthesis.
