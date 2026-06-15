# 102 Collaborative Affordance Negotiation

Submission-hardening version: v4.1

Terminal decision: KILL_ARCHIVE for ICLR main.

Paper 102 was rebuilt from a template archive into a paper-specific collaborative-affordance benchmark and re-audited on 2026-06-15. The evidence is useful but negative: explicit affordance negotiation improves over simple capability-only, intent-only, language-affordance, clarification-only, and capability-map baselines, but it does not clear the decisive gate against the strongest non-oracle baseline, `shared_autonomy_pomdp`.

## Key Evidence

- Benchmark design: 5 tasks x 7 collaboration ambiguity families x 5 splits x 9 methods.
- Seeds: 7 independent seeds, 84 episodes per method/task/family/split/seed group.
- Strongest non-oracle baseline: `shared_autonomy_pomdp`.
- Continuation rerun: `python -m py_compile src/run_experiment.py` and `python src/run_experiment.py` passed on 2026-06-15.
- Combined stress: proposed success `0.6288 +/- 0.0042`; strongest baseline success `0.6049 +/- 0.0054`.
- Success margin: `+0.0239`, below the required `+0.030` practical margin.
- Ablation gate failed: full method success `0.6241`; `minus_burden_aware_query_value` success `0.6045`, margin `+0.0196`.
- Proposed reduces violations and over-promise, but the task-success gain is not decisive enough for a main-conference trajectory.

## Reproduce Evidence

```powershell
python -m py_compile src\run_experiment.py
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/102.pdf`

## Honest Limitation

This repo should be retained as a negative empirical audit. Reviving the idea would require real human-robot studies or high-fidelity collaborative manipulation benchmarks and a method that decisively beats shared-autonomy baselines.
