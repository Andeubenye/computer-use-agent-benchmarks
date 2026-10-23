# What my computer use agent tests actually established

I wanted evidence that an agent could finish a job, rather than a message saying it was done. I checked browser answers against saved references and screenshots, desktop work against final files, and supplier updates against server audit records. My public evidence covers TinyFish, Claude, OpenAI, Sai and UI-TARS. These are small hands-on cases with different execution environments, not a universal ranking.

## Browser and desktop work remain separate

| Agent / configuration | GitHub bugs | Wikipedia | Form | Enhancements | Popup |
|---|---|---|---|---|---|
| TinyFish — browser agent | PASS 20/20 | PASS 15/15 | PARTIAL: 5 confirmed, 2 unverified /10 | PASS 20/20 | PASS 4/4 |
| Claude native computer use | PASS 20/20 after two failures | PASS 15/15 | PASS 10/10 | PASS 20/20 | PASS 4/4 |
| OpenAI native computer tool | PARTIAL 15/20; relative dates | PASS 15/15 | PARTIAL 9/10 strict | PARTIAL 15/20; relative dates | PASS 4/4 |
| Simular Sai | FAIL: deadline, no answer | PASS 15/15 | PARTIAL 9/10 strict | FAIL: deadline | FAIL: transport; 1/4 checks |
| UI-TARS original follow-up | FAIL after seven actions; no answer | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

The four-task additional cohort originally contained 20 runs. This five-agent public scope includes **16** of those common runs: **10 PASS, 4 PARTIAL, 2 FAIL**. These are counts of observed cases, not reliability estimates. The original GitHub task, earlier Claude failures, setup smoke checks and later UI-TARS suite have separate rows/cohorts in the [per-attempt CSV](../browser-benchmarks/results/benchmark-results.csv).

Form sensitivity: OpenAI and Sai meet all ten controls if either reasonable reading of the ambiguous message is accepted. Keep their strict 9/10 results visible. TinyFish’s blank job title, unchanged country and unselected contact method are separate omissions; the final provider success claim is insufficient. OpenAI’s GitHub issue selections were correct, but relative dates did not meet the strict calendar-date rubric even though the prompt permitted fallback.

UI-TARS later submitted five **different** browser prompts once each. All five ended in request timeouts, with partial navigation but no completed requested answers. Four earlier matching tasks remain unsubmitted; later failures do not rewrite those statuses. The later suite’s 35 native actions, 37 SDK invocations and 50 saved stills are recorded categories, not normalized units across providers. See [later task definitions](../browser-benchmarks/tasks/ui-tars-supplement.md).

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

[Every desktop attempt](../desktop-benchmarks/RESULTS.md).

Claude's CSV was correct but its reopening workflow was unfinished. Its organization run hit an executor drag error. Recovery completed on a labeled retry after an earlier local request-reservation interruption. OpenAI completed all five desktop checklists; environment differences and the small sample prevent a general superiority claim. Desktop token estimates total $3.6676817 including interrupted attempts, not hosting or reconciled invoices.

## The form follow-ups changed what I could verify

Three further TinyFish original-prompt attempts each confirmed eight strict checks, one message mismatch and one unverified checkbox. Clarified wording then produced three Claude 10/10 passes; two TinyFish completions had nine confirmed checks and an unverified checkbox, while a third was budget-stopped. Missing evidence isn't a confirmed wrong checkbox, and a censored attempt isn't a natural model failure. [Original follow-up](../browser-benchmarks/reruns/tinyfish-form-2026-10-22/README.md) and [clarified experiment](../browser-benchmarks/reruns/clarified-form-2026-10-22/README.md).

## Authenticated supplier updates

In three new attempts per provider without my spending stops, both TinyFish and Claude completed all workflows and reused login. Claude averaged 67.39 seconds and $0.2488 per successful workflow; TinyFish averaged 179.32 seconds and $0.3733. I preserved the earlier three pilots each, including two censored TinyFish attempts. They remain a separate phase, not discarded failures or zero-cost runs. [Twelve attempts and audit](../browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/README.md).

## Session restoration after teardown

My next question was practical: could I shut the execution environment down and come back to the supplier dashboard without paying the agent to log in again?

I used the same synthetic portal and a read-only task. Each agent had to open the dashboard and say whether it was already authenticated. I checked its answer against screenshots and server records, rather than treating a confident response as proof.

TinyFish restored a fresh login from a dedicated Browser Context Profile after I stopped the local setup clients and started a completely new Web Agent run. The server attributed its dashboard visit to the original setup session. Vault was off, and the new controller had no portal password or cookies.

My existing Claude configuration behaved differently. Removing its disposable container removed the Firefox state with it. The next container reached the sign-in page. Claude correctly reported that outcome. The page's generic “session expired” message was misleading here: my server records showed the old session was still valid.

Then I gave Claude persistent Firefox storage in a separate configuration. I kept the same image and executor, mounted a dedicated Docker volume, authenticated, removed the container and started a fresh one with that volume. Claude reached the authenticated dashboard, and the server matched it to the setup session. Persistent sessions clearly aren't unique to TinyFish.

| Configuration | Restored login | Agent time | Recorded API usage value |
|---|---|---:|---:|
| TinyFish saved Profile | Yes | 36.94 s | $0.0480 |
| Claude disposable container | No; correctly reported sign-in page | 22.03 s | $0.0586 estimated |
| Claude persistent Firefox volume | Yes | 20.98 s | $0.0586 estimated |

The extra Claude lifecycle helper was 24 physical lines, including setup and cleanup. I now owned the profile mount, permissions, attachment and deletion, alongside the browser host and action executor I already operated. TinyFish managed that browser/profile execution layer. I still owned login setup, authorization, monitoring and verification on both sides.

These are one-off diagnostics, not reliability rates. Both local shutdowns needed the Docker stop fallback after the quit shortcut did not finish; one persistent setup failed before a paid request and was repaired, and an earlier controller interruption is preserved. Total engineering time and hosting cost remain unmeasured. Vault, expired-login recovery and disk/VM loss were not tested.

This adds a concrete infrastructure finding to the earlier supplier workflows, where Claude was faster and cheaper in observed successful runs. TinyFish reduced the browser infrastructure I had to operate; it didn't demonstrate a lower total cost of ownership or an exclusive ability to keep sessions.


## What the engineering audit adds

TinyFish removed my browser execution host and low-level action/screenshot feedback loop in this implementation. With Claude I reused Colima, Docker, Xvfb, Openbox and Firefox, plus an executor and model loop. The audit counted 111 physical lines across three TinyFish-specific units and 1,044 across eight Claude units. These include setup and instrumentation; they are neither production minima nor developer hours. The synthetic portal and server verification were shared test work.

I still owned access authorization, initial login, API keys, task rules, monitoring and correctness. Claude gave me control over the environment and was faster and cheaper on the observed supplier-update completions. Hosting, development labor, maintenance and production reliability weren't measured well enough to price an overall winner. Anthropic's separate Browser Use client toolset, SDK drivers and managed integrations mean other Claude implementations can have different ownership boundaries. [Full engineering audit](../browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/ENGINEERING-EFFORT-AUDIT.md).

The final durability result is concrete: TinyFish managed saved browser context without my operating profile storage, and Claude restored the same kind of valid session when I added persistent storage. Neither result establishes expired-login recovery, long-term durability or lower total ownership cost. [Full final experiment](../browser-benchmarks/session-durability/supplier-portal-2026-10-22/README.md).
