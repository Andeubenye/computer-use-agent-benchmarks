# Every actual attempt

| Agent | Attempt | Verified workflow | Correct save | Time | Actions / entries | Images | API estimate | Evidence |
|---|---:|---|---|---:|---|---:|---:|---|
| Tinyfish | 1 | PARTIAL; budget-censored | No | 285.25 s | 27 recorded activity entries (billing counter 0 is unreliable) | 27 | Unresolved + $0.60 unresolved reserve | [Original + audit](runs/tinyfish/attempt-01/server-verification.json) |
| Claude | 1 | PASS | Yes | 47.62 s | 24 native computer actions including screenshots/zoom | 9 | $0.188832 | [Original + audit](runs/claude/attempt-01/server-verification.json) |
| Claude | 2 | PASS | Yes | 82.39 s | 33 native computer actions including screenshots/zoom | 12 | $0.300618 | [Original + audit](runs/claude/attempt-02/server-verification.json) |
| Tinyfish | 2 | PASS | Yes | 251.33 s | 22 billed provider steps | 21 | $0.352000 | [Original + audit](runs/tinyfish/attempt-02/server-verification.json) |
| Tinyfish | 3 | PARTIAL; budget-censored | Yes | 188.63 s | 27 recorded activity entries (billing counter 0 is unreliable) | 27 | Unresolved + $0.60 unresolved reserve | [Original + audit](runs/tinyfish/attempt-03/server-verification.json) |
| Claude | 3 | PASS | Yes | 54.90 s | 30 native computer actions including screenshots/zoom | 11 | $0.262380 | [Original + audit](runs/claude/attempt-03/server-verification.json) |
| Tinyfish | 4 | PASS | Yes | 158.14 s | 26 provider steps | 25 | $0.416000 | [Original + audit](uncapped-followup/runs/tinyfish/attempt-04/server-verification.json) |
| Tinyfish | 5 | PASS | Yes | 253.20 s | 26 provider steps | 25 | $0.416000 | [Original + audit](uncapped-followup/runs/tinyfish/attempt-05/server-verification.json) |
| Tinyfish | 6 | PASS | Yes | 126.61 s | 18 provider steps | 17 | $0.288000 | [Original + audit](uncapped-followup/runs/tinyfish/attempt-06/server-verification.json) |
| Claude | 4 | PASS | Yes | 74.69 s | 30 native computer actions including screenshots/zoom | 11 | $0.260754 | [Original + audit](uncapped-followup/runs/claude/attempt-04/server-verification.json) |
| Claude | 5 | PASS | Yes | 59.67 s | 28 native computer actions including screenshots/zoom | 10 | $0.223442 | [Original + audit](uncapped-followup/runs/claude/attempt-05/server-verification.json) |
| Claude | 6 | PASS | Yes | 67.81 s | 31 native computer actions including screenshots/zoom | 11 | $0.262146 | [Original + audit](uncapped-followup/runs/claude/attempt-06/server-verification.json) |

Workflow completion requires the exact saved values, a valid matching receipt in the agent's original response, the correct target record, no saves to another supplier, terminal completion within limits and retained GUI evidence. Session reuse is measured separately. A correct saved file/record alone does not complete the reporting workflow.

The cancelled TinyFish pilot 1 typed values but never saved them. Pilot 3 correctly saved twice but was stopped before returning its response. Pilot 2 also saved twice and returned the latest receipt correctly. These repeated Save actions are agent behavior, not benchmark restarts; every generated receipt is retained in the audit. No extra charge is inferred solely from a Save click.

The original Claude summaries say `needs_review`/`success:false` because their generic manual-grading placeholder did not evaluate this portal. They are preserved unchanged; independent server grading determines the reported results. The legacy TinyFish record's `fresh_profile_requested:true` and pre-override `submitted-once.json` are adapter defaults; actual payloads, `profile_attached`, and session audit prove saved-profile use.

[All original pilot records](results.json) · [New records](uncapped-followup/results.json) · [Complete results CSV](combined-results.csv) · [Final independent verification](verification-complete.json)
