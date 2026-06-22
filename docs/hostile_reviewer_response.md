# Hostile Reviewer Response

## Attack: This is not real HRI evidence.

Response: Correct. The terminal result is STRONG_REVISE, not ready. The benchmark is much stronger than v4.1, but it does not replace human-subject studies, robot hardware, accepted high-fidelity simulation, or accepted external benchmarks.

## Attack: Shared autonomy is the real baseline.

Response: v5 includes `shared_autonomy_pomdp`, `risk_aware_shared_autonomy`, `human_model_mpc`, and `inverse_rl_intent_pomdp`. V5 reaches success `0.73038` versus `0.60503` for shared-autonomy POMDP and `0.61858` for risk-aware shared autonomy.

## Attack: The method may win by asking too many questions.

Response: The hard aggregate reports human burden `0.25547` and unnecessary query `0.00156`; active clarification baselines have much higher burden or unnecessary query. In fixed-risk mode, v5 safe repair visibly increases burden and unnecessary query, so the cost is not hidden.

## Attack: The result could be a diagnostic-only win.

Response: The local evidence includes closed-loop success, physical violation, burden, regret, fixed-risk behavior, and utility, not only intent or over-promise diagnostics.

## Attack: What is missing for submission?

Response: Real human-robot validation, accepted external benchmark validation, calibrated intent/burden logs, trained checkpoint release, rollout videos, and deeper manual related-work synthesis.
