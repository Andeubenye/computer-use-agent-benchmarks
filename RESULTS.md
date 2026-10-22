# Recorded benchmark results

## Browser tasks

| Agent / configuration | GitHub bugs | Wikipedia | Form | Enhancements | Popup |
|---|---|---|---|---|---|
| TinyFish — browser agent | PASS 20/20 | PASS 15/15 | PARTIAL: 5 confirmed, 2 unverified /10 | PASS 20/20 | PASS 4/4 |
| Claude native computer use | PASS 20/20 after two failures | PASS 15/15 | PASS 10/10 | PASS 20/20 | PASS 4/4 |
| OpenAI native computer tool | PARTIAL 15/20; relative dates | PASS 15/15 | PARTIAL 9/10 strict | PARTIAL 15/20; relative dates | PASS 4/4 |
| Simular Sai | FAIL: deadline, no answer | PASS 15/15 | PARTIAL 9/10 strict | FAIL: deadline | FAIL: transport; 1/4 checks |
| UI-TARS original follow-up | FAIL after seven actions; no answer | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

The four-task additional cohort originally contained 20 runs. This five-agent public scope includes **16** of those common runs: **10 PASS, 4 PARTIAL, 2 FAIL**. These are counts of observed cases, not reliability estimates. The original GitHub task, earlier Claude failures, setup smoke checks and later UI-TARS suite have separate rows/cohorts in the [per-attempt CSV](browser-benchmarks/results/benchmark-results.csv).

Form sensitivity: OpenAI and Sai meet all ten controls if either reasonable reading of the ambiguous message is accepted. Keep their strict 9/10 results visible. TinyFish’s blank job title, unchanged country and unselected contact method are separate omissions; the final provider success claim is insufficient. OpenAI’s GitHub issue selections were correct, but relative dates did not meet the strict calendar-date rubric even though the prompt permitted fallback.

UI-TARS later submitted five **different** browser prompts once each. All five ended in request timeouts, with partial navigation but no completed requested answers. Four earlier matching tasks remain unsubmitted; later failures do not rewrite those statuses. The later suite’s 35 native actions, 37 SDK invocations and 50 saved stills are recorded categories, not normalized units across providers. See [later task definitions](browser-benchmarks/tasks/ui-tars-supplement.md).

## Desktop tasks

| Task | Claude | OpenAI |
|---|---|---|
| CSV editing | PARTIAL 4/5 | PASS 5/5 |
| File organization | PARTIAL 2/5; executor interruption | PASS 5/5 |
| Document editing | PASS 5/5 | PASS 5/5 |
| Cross-application reporting | PASS 5/5 | PASS 5/5 |
| Desktop error recovery | PASS 5/5 on labeled retry; first attempt PARTIAL 4/5 | PASS 5/5 |

Every requirement was independently checked against saved files and cited GUI observations. Claude’s CSV matched the expected file exactly, but reopening was unfinished. Its organization retry stopped on an executor drag error after making folders. Its first recovery file was correct, but a local request-reservation guard stopped the model’s final review; the separately labeled retry completed it. Original partials and both costs remain visible.

Sai’s original CSV/API eligibility record and four further desktop slots are NOT TESTED after HTTP 403, not scored failures. A request references separate frontend desktop attempts, but no independently scoreable frontend artifacts/traces were recovered; those are missing evidence, not inferred API runs. TinyFish had no desktop test. UI-TARS’s planned desktop evaluation was not completed.

[Every desktop attempt](desktop-benchmarks/RESULTS.md) · [Independent token/artifact audit](desktop-benchmarks/logs/usage-reconciliation.json) · [Browser per-attempt measurements](browser-benchmarks/results/benchmark-results.csv)
