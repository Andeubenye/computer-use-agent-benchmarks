# Why the earlier TinyFish pilots stopped

This was an intervention by our harness, not an established provider failure or a 600-second timeout. The user authorized existing-credit usage broadly. The harness nevertheless chose a $0.60 per-run reserve and $10 operational guard. Those were not user-imposed ceilings. The frozen pilot source documents both choices.

The TinyFish API returned a null aggregate step count while running. The wrapper calculated `max(num_of_steps or 0, len(steps))`; if status was RUNNING/PENDING and this count reached 26, it submitted `/cancel` once. The idea was to leave room for delayed progress at the observed $0.016/step tariff. In both cancelled attempts the poll already showed 27 trace entries. Trace entries are not necessarily billable steps, so this heuristic could censor useful work prematurely.

| Pilot | Cancel request UTC | Elapsed client time | Server outcome | Why incomplete |
|---|---|---:|---|---|
| TinyFish 1 | 16:55:01.946 | 285.25 s | Pending; note empty; no receipt | Stopped after typing fields, before a save |
| TinyFish 3 | 17:05:35.057 | 188.63 s | Reviewed; exact note; two unique receipts | Stopped after saving, before returning final response |

Both cancellation requests returned HTTP 200 and provider CANCELLED. Original provider `result` is null. Each run has 27 retained trace entries/images but reports zero aggregate billing steps. Observed wallet debit was zero at the recorded times; that does not establish free execution. Keep $0.60 uncertainty for each in the old ledger until billing is resolved. The cumulative guard did not cause these stops. There was no observed loss of authentication, and no provider safety restriction caused them.

The screenshots show repeated dashboard/link activity before editing, but the private managed controller did not expose enough detail to establish why navigation repeated. Do not invent a root cause or claim that the runs would or would not have completed within 600 seconds.

For the new three attempts each, the user explicitly removed custom spending stops. The wrapper's cancellation branch and cumulative/per-run admission checks were removed; Claude's three cost-stop checks were removed in a separate core copy. Costs continued to be measured. The real deadline, provider restrictions and native tool safeguards remain. The original core and pilot evidence were not edited. See the [exact core diff](uncapped-followup/core-spending-guard-removal.diff), [source audit](uncapped-followup/core-change-audit.json) and [preflight checks](uncapped-followup/preflight-checks.json).
