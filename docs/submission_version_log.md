# Submission Version Log

## v1

Generated draft and repository scaffold.

## v2

Initial hardening pass.

## v3

ICLR-main gate archive. Decision: KILL_ARCHIVE because evidence was synthetic/template-only.

## v4

Paper-specific collaborative-affordance evidence rebuild. Decision remained KILL_ARCHIVE because the proposed method improved safety and over-promise but did not clear the practical success or ablation gates against shared-autonomy baselines.

## v4.1

Added a pre-execution ICLR-main submission-readiness plan for Paper 102, reran the local benchmark on 2026-06-15, and reconfirmed KILL_ARCHIVE.

## v5 expanded

- Added a frozen hostile-review plan for a 25+ page submission artifact.
- Expanded the benchmark to 6 tasks x 8 collaboration regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.
- Produced 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, and 24 negative cases.
- Added v5 method `risk_calibrated_collaborative_affordance_v5` with calibration, active safe repair, burden-aware query value, role negotiation, intent belief, capability maps, and over-promise risk.
- Added strong baselines including risk-aware shared autonomy, human-model MPC, inverse-RL intent POMDP, conformal intent-risk filtering, active clarification bandit, v4 detector, and oracle.
- Generated a 27-page PDF at `C:/Users/wangz/Downloads/102.pdf` with SHA256 `C384D1E57B0C3F5C42B044027505CD847BBDFA1FD82FB513ABBCDDF0BEADC69E`.
- Added bright boxed citation hyperlinks and 230 bibliography entries selected from the local deep-read pool.
- Terminal decision changed to STRONG_REVISE, still not ICLR-main ready without external HRI or accepted benchmark validation.
