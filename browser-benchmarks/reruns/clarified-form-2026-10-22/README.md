# Clarified form experiment: TinyFish vs Claude — 22 October 2026

Six real executions: three fresh TinyFish hosted browser runs and three fresh Claude native Firefox/Linux runs. The exact clarified user prompt was submitted to both, with the original ten-field rubric and a maximum of 600 seconds each. The earlier ambiguous-prompt cohorts are preserved separately.

**Result:** Claude has three independently verified 10/10 completions. TinyFish has two partial results with nine correct visible fields and an unverified newsletter, plus one budget-stopped failed workflow. All three TinyFish runs entered the full message at least at an intermediate stage; the cancelled run did not preserve its completed fields to the end.

## All six new runs

| Agent / attempt | Independently verified final state | Outcome | Client/native time to stop | Cost / uncertainty |
|---|---|---|---:|---|
| TinyFish 1 | 9 correct, 0 incorrect, 1 unverified /10 | PARTIAL | 64.16 s | $0.208 observed debit / tariff |
| TinyFish 2 | 1 correct, 7 incorrect, 2 unverified /10 | FAIL, spending-watchdog cancellation | 253.40 s | $0 incremental debit observed; charge unresolved, $0.465 reserved |
| TinyFish 3 | 9 correct, 0 incorrect, 1 unverified /10 | PARTIAL | 127.14 s | $0.192 observed debit / tariff |
| Claude 1 | 10 correct /10 | PASS | 49.57 s | $0.142128 token estimate |
| Claude 2 | 10 correct /10 | PASS | 56.15 s | $0.203556 token estimate |
| Claude 3 | 10 correct /10 | PASS | 60.28 s | $0.238684 token estimate |

No new agent run was restarted. One optional TinyFish API field was rejected before agent creation; that setup rejection and subsequent supported submission are separately retained. A cancellation is not a free completed test. Costs are not reconciled invoices. [Full measurement and error table](RESULTS.md) explains the zero billing counter and post-run Claude capture errors.

## Earlier results — unchanged reference configuration

| Agent / original-prompt attempt | Strict verified state | Time | Cost |
|---|---|---:|---:|
| Claude original | PASS 10/10 | 66.75 s | $0.194282 estimate |
| TinyFish original | PARTIAL: 5 correct, 3 incorrect, 2 unverified /10 | 37.03 s | $0.112 estimate |
| TinyFish previous rerun 1 (attempt 2) | PARTIAL: 8 correct, 1 incorrect, 1 unverified /10 | 101.53 s | $0.224 |
| TinyFish previous rerun 2 (attempt 3) | PARTIAL: 8 correct, 1 incorrect, 1 unverified /10 | 71.44 s | $0.192 |
| TinyFish previous rerun 3 (attempt 4) | PARTIAL: 8 correct, 1 incorrect, 1 unverified /10 | 106.20 s | $0.208 |

The prior message had a reasonable alternative reading; prior sensitivity scores remain visible in the [earlier report](../tinyfish-form-2026-10-22/README.md). Do not pool these two prompt configurations into one pass rate.

## Evidence for each new attempt

| Attempt | Verification | Original response | Upper / last state | Lower checkbox evidence | Trace |
|---|---|---|---|---|---|
| TinyFish 1 | [grade](tinyfish/attempt-1/independent-verification.json) | [original](tinyfish/attempt-1/original-response.txt) | [image](tinyfish/attempt-1/screenshots/screenshot-011.jpg) | unavailable | [trace](tinyfish/attempt-1/provider-run.json) |
| TinyFish 2 | [grade](tinyfish/attempt-2/independent-verification.json) | [original null result](tinyfish/attempt-2/original-response.txt) | [last image](tinyfish/attempt-2/screenshots/screenshot-023.jpg), [earlier nine-field state](tinyfish/attempt-2/screenshots/screenshot-021.jpg) | unavailable | [trace](tinyfish/attempt-2/provider-run.json), [cost/stop audit](tinyfish/attempt-2/cost-and-stop-audit.json) |
| TinyFish 3 | [grade](tinyfish/attempt-3/independent-verification.json) | [original](tinyfish/attempt-3/original-response.txt) | [image](tinyfish/attempt-3/screenshots/screenshot-010.jpg) | unavailable | [trace](tinyfish/attempt-3/provider-run.json) |
| Claude 1 | [grade](claude/attempt-1/independent-verification.json) | [original](claude/attempt-1/original-response.txt) | [upper](claude/attempt-1/native-evidence/20261022T152051Z-b701f569/screenshots/independent-upper.png) | [lower](claude/attempt-1/native-evidence/20261022T152051Z-b701f569/screenshots/0031-screenshot.png) | [native trace](claude/attempt-1/native-evidence/20261022T152051Z-b701f569/events.jsonl) |
| Claude 2 | [grade](claude/attempt-2/independent-verification.json) | [original](claude/attempt-2/original-response.txt) | [upper](claude/attempt-2/native-evidence/20261022T152202Z-b7ce3a14/screenshots/independent-upper.png) | [lower](claude/attempt-2/native-evidence/20261022T152202Z-b7ce3a14/screenshots/0038-screenshot.png) | [native trace](claude/attempt-2/native-evidence/20261022T152202Z-b7ce3a14/events.jsonl) |
| Claude 3 | [grade](claude/attempt-3/independent-verification.json) | [original](claude/attempt-3/original-response.txt) | [upper](claude/attempt-3/native-evidence/20261022T152321Z-35d0c90f/screenshots/independent-upper.png) | [lower](claude/attempt-3/native-evidence/20261022T152321Z-35d0c90f/screenshots/0037-screenshot.png) | [native trace](claude/attempt-3/native-evidence/20261022T152321Z-35d0c90f/events.jsonl) |

[Comparison and plain-English answers](COMPARISON.md) · [Methodology and deviations](METHODOLOGY.md) · [Article-ready findings](ARTICLE-READY.md) · [Exact prompt](clarified-prompt.txt) · [Results JSON](results.json) · [CSV](results.csv) · [Budget audit](reconciled-budget.json) · [Raw-copy hashes](source-provenance.json)
