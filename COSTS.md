# Costs and attempt measurements

Costs below describe recorded evidence, not current prices or reconciled invoices. Browser and desktop budgets are separate. Unknown costs are not zero. Do not sum overlapping hosting intervals, alternative Sai usage figures or setup smoke checks into task totals.

## Browser usage

| Provider | Original task / attempts | Four additional tasks | Measurement basis |
|---|---:|---:|---|
| TinyFish — browser only | $0.128 attributed | $0.736 estimated | Original amount matched user billing text by minute/eight steps; no transaction run ID. Later 46 reported steps × saved $0.016 tariff. Five-run $0.864 is attributed/tariff usage, not five reconciled wallet transactions. |
| Claude | $0.761936 including two failures; successful run $0.222 | $0.979244 | Returned tokens × saved model rates; separate $0.077040 setup smoke excluded |
| OpenAI | $0.0731802 | $0.2178473 | Returned tokens including caching categories × saved rates; five-task $0.2910275; separate $0.00218 capability check excluded |
| Sai | $0.07 promotional-credit decrease; alternative provider usage $0.02 | $0.09 credit decrease | Immediate four-run deltas sum to $0.08; $0.01 unallocated. Do not add provider usage to credit delta. |
| UI-TARS | $0.24406 session hosting estimate | Four matching tasks unsubmitted | User-reported $1.80/hour × 488.120-second session-to-pause interval; includes setup/idle. Original submission interval $0.082303 is contained within it, not additional. Later different suite’s task hosting cost is unavailable. |

Supported task-cohort totals, including failed task attempts but excluding the separately listed setup checks: TinyFish **$0.864** attributed/tariff usage; Claude **$1.741180** token estimate; OpenAI **$0.2910275** token estimate. Sai’s two recorded credit-decrease windows total **$0.16**, including the unallocated cent; this is not an invoice total. UI-TARS has only the **$0.24406** known session estimate here, not a complete all-testing total.

The user-reported $10.05 HF account-period figure lacks a matching recovered dashboard snapshot. It is not a verified task charge or a UI-TARS-only amount. No cross-provider total is calculated from these incompatible categories. No current pricing recommendation or fastest/cheapest ranking is inferred.

[Browser per-attempt time, actions, images, model, errors and costs](browser-benchmarks/results/benchmark-results.csv) · [Scoped original cost rows](browser-benchmarks/results/cost-breakdown.csv)

## Desktop usage

Verified cumulative token estimate: **$3.6676817**, including all unsuccessful attempts and retries. Original cap: **$7**. Remaining allowance: **$3.3323183**. Uncertain generation reservations: **$0**. No invoice reconciliation is available.

| Provider | All retained desktop attempts | Verified PASS task definitions |
|---|---:|---:|
| Claude | $3.1973900 | 3, including recovery on retry |
| OpenAI | $0.4702917 | 5 |
| Sai | $0 agent generation; authorization-blocked | No task submitted |

[Every desktop attempt](desktop-benchmarks/RESULTS.md) retains exact time, actions, images, cost and stop reason. [Independent reconciliation](desktop-benchmarks/logs/usage-reconciliation.json) recalculates every estimate from saved raw responses and checks record totals. OpenAI reported automatic cached input; Claude reported no cache reads. Tool tokenization, request counts, screenshot policies, caching and retry history differ. These totals are descriptive, not a general cost-efficiency ranking.

Local hardware, electricity, labor and setup effort are unpriced. The assistant purchased no infrastructure or credits. The user’s external top-up did not reset the desktop cap. No paid execution took place during repository packaging.

## TinyFish form follow-up — separate browser cohort, 22 October 2026

Three new attempts cost **$0.224, $0.192 and $0.208**, totaling **$0.624** (39 steps × returned $0.016 tariff; matching observed account decreases, not invoices). Mean **$0.208**. Original form plus three reruns totals **$0.736 across four form attempts**. Original five-task TinyFish $0.864 plus this separate follow-up is **$1.488 attributed/tariff browser usage**; no earlier task cost was replaced. No verified full TinyFish form completion was established, so cost per verified full completion is unavailable. Claude's original verified form completion remains a $0.194282 token estimate. Measurement categories differ. Follow-up browser cap ledger: $2.1059203 baseline + $0.624 = $2.7299203, $7.2700797 remaining under $10. Desktop's $3.6676817 ledger is unchanged. [Details and caveats](browser-benchmarks/reruns/tinyfish-form-2026-10-22/RESULTS.md).

## Clarified form configuration — additional $2 cap

[Three Claude and three TinyFish runs](browser-benchmarks/reruns/clarified-form-2026-10-22/RESULTS.md) added **$0.584368** in recorded Claude token estimates and **$0.400** in observed TinyFish debits for the two completed partials. The cancelled TinyFish run reports a zero billing counter/current incremental debit despite 24 recorded activity entries; invoice cost remains unresolved and **$0.465** is conservatively reserved. Known mixed-basis amount **$0.984368**; budget accounting including uncertainty **$1.449368**, below the new $2 cap. Claude averaged $0.194789 per verified completion; TinyFish cost per verified full completion is unavailable. No desktop ledger, historical task amount or prior follow-up amount was overwritten. [Value-free billing audit](browser-benchmarks/reruns/clarified-form-2026-10-22/reconciled-budget.json).

## Authenticated supplier workflows — 22 October 2026

New uncapped supplier workflows: TinyFish **3/3**, Claude **3/3**; both reused login. Earlier three pilots each remain separate, including two TinyFish budget-censored attempts. [Twelve attempts and verification](browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/README.md) · [Article-ready findings](browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/ARTICLE-READY.md). This is a new authenticated browser cohort, not a replacement for earlier browser or desktop results. New API estimates: TinyFish $1.120000; Claude $0.746342. Old cancelled-pilot charges remain unresolved ($1.20 accounting reserve), separate from prior experiments. Hosting, hardware and engineering costs are not fully priced. [Costs/projections](browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/COSTS.md).
