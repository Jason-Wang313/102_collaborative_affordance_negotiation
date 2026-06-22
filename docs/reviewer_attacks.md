# Reviewer Attacks

1. The collaboration regimes are hand-designed and not calibrated from human-subject logs.
2. The proposed detector is still an executable proxy, not a trained human-robot model with released checkpoints.
3. Shared-autonomy and human-model MPC systems may close the gap under real interaction data.
4. Intent and over-promise diagnostics are useful, but reviewers will demand real closed-loop HRI rollouts.
5. The oracle gap remains material: `0.73038` proposed success versus `0.79783` oracle success.
6. Fixed-risk safe repair increases human burden and needs human-subject validation.
7. The paper still needs a full manual related-work synthesis.
8. The benchmark is large, but still local; reviewers can attack domain transfer.
9. The fixed-risk audit is local and does not certify safety on hardware or with human participants.

Response after v5: keep the paper as STRONG_REVISE because the local collaborative-affordance mechanism survives a stronger audit, but do not submit it without external validation.
