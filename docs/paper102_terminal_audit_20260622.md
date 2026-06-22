# Paper 102 Terminal Audit 2026-06-22

Paper: 102 collaborative_affordance_negotiation

Version: v5 expanded

Terminal decision: STRONG_REVISE

ICLR-main readiness: no

GitHub: `https://github.com/Jason-Wang313/102_collaborative_affordance_negotiation`

Canonical PDF: `C:/Users/wangz/Downloads/102.pdf`

PDF SHA256: `C384D1E57B0C3F5C42B044027505CD847BBDFA1FD82FB513ABBCDDF0BEADC69E`

Pages: 27

## Verification Summary

- The v5 runner completed and wrote all expected CSV, table, figure, and manuscript artifacts.
- The manuscript compiled to a 27-page PDF.
- Citation links use visible boxed borders and route to the reference section.
- The canonical numbered PDF is in Downloads only.
- No Desktop PDF is part of the artifact.
- No repo-local `102.pdf` is required or retained.

## Evidence Summary

- Main closed-loop rollouts: 345,600.
- Ablation rollouts: 115,200.
- Stress-sweep rollouts: 288,000.
- Fixed-risk rollouts: 276,480.
- Negative cases: 24.
- v5 hard success: `0.73038`.
- strongest non-oracle hard success: `0.63090`.
- shared-autonomy POMDP hard success: `0.60503`.
- oracle hard success: `0.79783`.
- v5 fixed-risk strict coverage: `0.87101`.

## Honest Scope Decision

The artifact is a strong local submission package, not a main-conference-ready HRI paper. The scope gate fails because the repository contains no real human-robot validation, accepted external benchmark validation, calibrated human-intent logs, trained checkpoint, videos, or complete manual related-work synthesis.
