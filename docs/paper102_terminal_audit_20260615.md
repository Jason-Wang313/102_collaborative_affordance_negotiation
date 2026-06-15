# Paper 102 Terminal Audit

Date: 2026-06-15 15:49:54 +0100

Terminal decision: KILL_ARCHIVE

## Verification Summary

The continuation rerun regenerated the full Paper 102 benchmark from source. The run completed with `terminal_decision=KILL_ARCHIVE` and `strongest_non_oracle_baseline=shared_autonomy_pomdp`.

The regenerated evidence again shows a useful but non-decisive method:

- Success gate failed: `proposed_affordance_negotiation` reached `0.6288 +/- 0.0042` combined-stress success vs `0.6049 +/- 0.0054` for `shared_autonomy_pomdp`, a `+0.0239` margin below the `+0.030` practical gate.
- Safety/burden gate passed: physical violation improved from `0.1396` to `0.1091`, and human burden increased only from `0.1975` to `0.2076`.
- Diagnostic gate passed: over-promise improved from `0.1610` to `0.0929`.
- Pairwise seed gate passed: `+0.0239 +/- 0.0086` with `7/7` seed wins over the strongest baseline.
- Ablation gate failed: `minus_burden_aware_query_value` reached `0.6045 +/- 0.0110` vs `0.6241 +/- 0.0058` for full, leaving only `+0.0196` separation.
- External validation gate failed: no real human-subject, robot, or external collaborative manipulation benchmark evidence is present.

## Artifact Rules

- Canonical PDF target: `C:/Users/wangz/Downloads/102.pdf`.
- Final PDF SHA256: `C59626EBAC3DCECF972EC578641B398A80CEE497CAAE6FF3B7D77665D71A39B8`.
- No visible Desktop PDF is permitted.
- Root ledgers must not claim ICLR-main readiness.

## Final Action

Retain as a negative empirical audit. Do not submit this version to ICLR main.
