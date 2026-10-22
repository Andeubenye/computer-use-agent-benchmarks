# Desktop benchmark results

All task decisions came from the providers' native computer tools. Expected artifacts stayed outside the agent desktops. Independent artifact checks and cited GUI observations determine outcomes; agent claims alone do not count.

| Task | Claude | OpenAI | Sai |
|---|---|---|---|
| Desktop CSV editing | PARTIAL 4/5 | PASS 5/5 | Earlier access-blocked; no new CSV run |
| File organization | PARTIAL 2/5; executor interrupted retry | PASS 5/5 | NOT TESTED / BLOCKED |
| Document editing | PASS 5/5 | PASS 5/5 | NOT TESTED / BLOCKED |
| Cross-application reporting | PASS 5/5 | PASS 5/5 | NOT TESTED / BLOCKED |
| Desktop error recovery | PASS 5/5 on labeled retry; first attempt PARTIAL 4/5 | PASS 5/5 | NOT TESTED / BLOCKED |

## Every attempt and its cost

| Attempt | Outcome / stop reason | Time seconds | Actions | Images | Estimated API cost |
|---|---|---:|---:|---:|---:|
| [claude](logs/claude/run-record.json) | BLOCKED — harness protocol failure; execution_error | 12.71 | 5 | 3 | $0.013434 |
| [claude-attempt-2](logs/claude-attempt-2/run-record.json) | PARTIAL; execution_error | 397.54 UTC / 183.18 stopwatch | 49 | 13 | $0.273314 |
| [openai](logs/openai/run-record.json) | PASS; model_finished | 128.71 | 34 | 25 | $0.0801494 |
| [claude/task-2](logs/claude/task-2/run-record.json) | NOT TESTED; infrastructure_or_protocol_error | 0.00 | 0 | 0 | $0 |
| [claude/task-2/attempt-2](logs/claude/task-2/attempt-2/run-record.json) | PARTIAL; execution_error | 106.13 | 49 | 10 | $0.22361 |
| [openai/task-2](logs/openai/task-2/run-record.json) | PASS; model_finished | 292.04 | 95 | 38 | $0.1791222 |
| [claude/task-3](logs/claude/task-3/run-record.json) | PASS; model_finished | 104.52 | 45 | 13 | $0.335324 |
| [openai/task-3](logs/openai/task-3/run-record.json) | PASS; model_finished | 112.36 | 34 | 19 | $0.0668268 |
| [claude/task-4](logs/claude/task-4/run-record.json) | PASS; model_finished | 193.29 | 102 | 20 | $0.715518 |
| [openai/task-4](logs/openai/task-4/run-record.json) | PASS; model_finished | 146.06 | 54 | 27 | $0.0896323 |
| [claude/task-5](logs/claude/task-5/run-record.json) | PARTIAL; execution_error | 223.24 | 100 | 25 | $0.885828 |
| [claude/task-5/attempt-2](logs/claude/task-5/attempt-2/run-record.json) | PASS; model_finished | 204.41 | 74 | 21 | $0.750362 |
| [openai/task-5](logs/openai/task-5/run-record.json) | PASS; model_finished | 96.94 | 31 | 16 | $0.054561 |

Estimated cumulative spending: **$3.6676817 of $7**. Uncertain request reservations: **$0**. Remaining conservative allowance: **$3.3323183**. These are token-usage estimates, not reconciled invoices. No paid infrastructure was provisioned.

## Evidence and interpretation

- Original responses, native actions, provider usage, errors and screenshots remain under each attempt folder. `independent-verification.json` contains the scored checks and cited GUI evidence. `artifact-verification.json` is a provisional read-only audit and does not replace the final GUI review.
- OpenAI's CSV run is PASS, 5/5: both edits, unchanged original, separate correct CSV, and reopened-file verification. Its actual output is `outputs/openai/orders_corrected.csv`; its parsed values and byte hash match the expected CSV.
- Claude's historical CSV repair attempt remains PARTIAL, 4/5. It saved an exactly correct file but stopped on a token-count timeout at the reopening dialog. Its interim last text is not a completed final response. The earlier HTTP 400 harness failure is retained and charged in the total.
- Mac power logs show sleep/wake events during the historical Claude CSV timeout. They strongly support host sleep as the explanation for most of its 214.36-second clock discrepancy. Preserve both clocks; exclude that run from comparative speed claims. New runs use both clocks and a temporary process-scoped idle-sleep inhibitor.
- The first additional Claude file-organization setup failed before generation due to a staging-directory readiness race. A single announced repair explicitly created the folder; its retry is retained separately. That retry later stopped on an executor drag error. No third attempt was made. Its files and partial work remain in the evidence.
- Claude's first error-recovery attempt saved the correct document and reopened it, but the local $1 request-reservation guard stopped the next generation before the model could review that screenshot. Its workflow remains PARTIAL, 4/5. On resume, one explicitly labeled infrastructure retry used a $1.75 local allowance from the unchanged $7 balance. It completed all five requirements. Both attempts and both costs remain in the tables; the original artifact was not regenerated or replaced.
- OpenAI's cross-application report had already finished when this resume began. Its retained artifact and GUI trace pass all five requirements. It was verified, not rerun. OpenAI's error-recovery run also finished in the previous queue and was verified without rerunning it.
- OpenAI's CSV and organization runs preceded the click-modifier adapter correction. Their outputs and required GUI workflows pass, but optional SHIFT/CTRL clicks were dropped, confounding action counts and duration. Subsequent tasks use the corrected translation. The two early passes were not repeated.
- Sai's authorized direct-control recheck returned HTTP 403, `forbidden`, “Not authorized for this machine.” No additional Sai task was submitted. This is an account/credential access limitation on the tested route, not a measured failure to perform the desktop tasks. No bypass or ownership takeover was attempted.
- Tasks 2–5 were reconstructed and frozen under the user's latest authorization because complete historical definitions were not recovered. Their prompts, fixture hashes and five-point criteria are in TASKS.md. They are not claimed to reproduce unknown earlier files exactly.
- UI-TARS was not operated. Earlier browser evidence and counts are separate and unchanged.

See [methodology](METHODOLOGY.md), [comparison](COMPARISON.md), [cost analysis](COST-COMPARISON.md), [article section](ARTICLE-READY.md), and `logs/final-evaluations.json` for machine-readable results.
