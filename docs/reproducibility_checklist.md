# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`.
- Manuscript generator: `scripts/generate_manuscript.py`.
- Artifact validator: `scripts/validate_submission_artifacts.py`.
- Dependencies: `numpy`, `matplotlib`, LaTeX, BibTeX.
- Deterministic base seed: `102_2026`.
- Seeds: `0..9`.
- Results directory: `results/`.
- Figures directory: `figures/`.
- Tables are generated from CSV outputs.
- Canonical PDF path: `C:/Users/wangz/Downloads/102.pdf`.
- PDF SHA256: `C384D1E57B0C3F5C42B044027505CD847BBDFA1FD82FB513ABBCDDF0BEADC69E`.
- PDF page count: 27.
- PDF can be rebuilt with `pdflatex`, `bibtex`, and two final `pdflatex` passes in `paper/`.

## Known Limits

- The benchmark is local rather than human-subject or hardware-calibrated.
- Full trajectories are not stored to keep RAM and disk use light.
- No external benchmark data is consumed.
- No trained model checkpoint is released.
- Videos are not released.
