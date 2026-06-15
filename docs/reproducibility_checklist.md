# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`.
- Dependencies: `numpy`, `matplotlib`.
- Deterministic base seed: `102_2026`.
- Seeds: `0..6`.
- Results directory: `results/`.
- Figures directory: `figures/`.
- Tables are generated from CSV outputs.
- PDF can be rebuilt with two `pdflatex` passes in `paper/`.
- 2026-06-15 continuation rerun passed `python -m py_compile src/run_experiment.py`.
- 2026-06-15 continuation rerun regenerated all result CSVs, figures, and LaTeX tables from `src/run_experiment.py`.
- Continuation log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/102_collaborative_affordance_negotiation_continuation_rerun_20260615.log`.

## Known Limits

- The benchmark is local and synthetic-HRI, not human-subject validation.
- No external benchmark data is consumed.
- Full trajectories are not stored to keep RAM and disk usage light.
- No trained policy checkpoint is released.
