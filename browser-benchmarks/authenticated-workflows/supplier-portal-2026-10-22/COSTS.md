# Measured costs and unexecuted scale scenarios

| Scope | TinyFish | Claude |
|---|---:|---:|
| New three attempts, known API estimate | $1.120000 | $0.746342 |
| New cost per fully verified workflow, includes all new attempts | $0.373333 | $0.248781 |
| All six, known estimate | $1.472000 | $1.498172 |
| Unresolved old cancelled-run accounting reserve | $1.200000 | $0 |
| All-six API accounting including old reserve | $2.672000 | $1.498172 |
| All-six accounted cost / full workflow | $0.668000 | $0.249695 |

TinyFish completed-run estimates use its exposed $0.016 per billed step and wallet debit observations. Cancelled pilots report zero steps despite 27 trace entries each; cost is unresolved, not zero. The $1.20 reserve is an accounting allowance, **not an invoice, verified charge or hard upper bound**. The earlier experiment's separate $0.465 unresolved reservation is preserved elsewhere and is not released or double-counted here. The new batch has no spending cap; a reserve in the old ledger does not restrict new execution.

Claude costs are recomputed from raw SDK responses using the unchanged saved tariff: uncached input $2/M, output $10/M, cache-read $0.10/M, cache-write $2.50/M (5 min) or $4/M (1 hour). These are estimates using the benchmark's saved pricing schedule, not a current-invoice claim. Token-count calls are logged separately from generation. No invoice or account-wide Anthropic spending statement was available.

Profile setup wallet changes were observed as zero at the saved check times. The exposed browser tariff is $0.002/minute; a zero observed balance change does not prove that setup or cancelled activity is free. Preserve $0.02 initial setup uncertainty separately; refresh setup has its own timings/observations. This allowance is not a verified upper bound on later reconciled billing. Hosting was deployed through the existing authorized Sites environment without a new purchase; its allocation is not itemized. Local hardware, electricity, engineering labor and earlier integration costs are unpriced. Thus these numbers are **API accounting**, not all-in costs.

## Projections, not additional benchmark runs

| Volume of attempted workflows (not executed) | TinyFish API scenario | Claude API scenario |
|---|---:|---:|
| 10 | $3.733333 | $2.487807 |
| 50 | $18.666667 | $12.439033 |
| 100 | $37.333333 | $24.878067 |


Each scenario multiplies the empirical mean API estimate of the **three new attempts only** by 10, 50 or 100. It assumes the same tasks, step/token distribution and tariff. This is a plug-in scenario from a tiny sample, not a statistical forecast or promise of 100 successes. It excludes one-time setup, unresolved old pilot charges, site hosting, local runtime, human intervention and future maintenance. It does not assume TinyFish's interrupted-pilot behavior will recur or that either observed completion rate generalizes. No 10-, 50- or 100-run sequence was executed. If a new run has unresolved cost, its known-only scenario understates total cost and must not be treated as a complete estimate.

[Original pilot ledger](evidence/budget-ledger.json) · [New usage ledger](uncapped-followup/budget-ledger.json) · [Pilot wallet observations](evidence/wallet-reconciliation.json) · [New wallet observations](uncapped-followup/wallet-reconciliation.json) · [Exact per-run API estimates](combined-results.csv)
