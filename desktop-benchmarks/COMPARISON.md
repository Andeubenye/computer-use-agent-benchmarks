# Matched desktop task comparison

| Task | Claude | OpenAI | Sai |
|---|---|---|---|
| Desktop CSV editing | PARTIAL 4/5 | PASS 5/5 | Earlier access-blocked; no new CSV run |
| File organization | PARTIAL 2/5; executor interrupted retry | PASS 5/5 | NOT TESTED / BLOCKED |
| Document editing | PASS 5/5 | PASS 5/5 | NOT TESTED / BLOCKED |
| Cross-application reporting | PASS 5/5 | PASS 5/5 | NOT TESTED / BLOCKED |
| Desktop error recovery | PASS 5/5 on labeled retry; first attempt PARTIAL 4/5 | PASS 5/5 | NOT TESTED / BLOCKED |

Scores describe five task-specific requirements, not general agent accuracy. A correct file can coexist with an unfinished GUI workflow. Access-blocked runs have no score. Infrastructure-interrupted attempts are explicitly identified in RESULTS.md and must not be treated as clean model capability failures.

| Configuration | Requested and returned model alias | Native interface |
|---|---|---|
| Claude | claude-sonnet-5-5 | Messages, computer_toolset_20260801 |
| OpenAI | gpt-6.1-sol | Responses, computer tool |
| Sai | No model task submitted or version exposed | Control route rejected authorization |

These are provider-returned aliases, not independently identified immutable weight snapshots. Per-attempt wall time, raw action counts, screenshots and estimated costs are in RESULTS.md; response counts and token totals are independently reconciled in logs/usage-reconciliation.json.

Both models used Linux Xvfb at 1024×768, Openbox, network-isolated containers, and LibreOffice. The original CSV used the original Calc image; tasks 2–5 used a derivative adding Writer, PCManFM and Zenity. Matched additional tasks used identical frozen inputs and prompts. Recovery screenshots show the same synthetic warning over blank Calc, despite the launcher's requested Writer state. The historical Claude CSV run predates the sleep-inclusive timer repair. OpenAI CSV/organization precede a click-modifier correction. Claude recovery required one separately retained retry with a larger local allowance; this is not a first-attempt pass. This small set cannot establish general superiority, reliability, or stable speed rankings.
