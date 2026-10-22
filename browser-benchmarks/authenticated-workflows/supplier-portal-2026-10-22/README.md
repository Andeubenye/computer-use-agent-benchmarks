# Repeated authenticated supplier workflows: TinyFish vs Claude

Six actual attempts per provider, in two phases on 22 October 2026. **The primary comparison is the three new attempts each without custom spending stops.** Preserve the original three pilots separately: two TinyFish pilots were interrupted by the harness's spending watchdog. This is a small controlled case study, not a population reliability estimate or general product ranking.

| Measurement | TinyFish | Claude native computer use |
|---|---:|---:|
| New attempts 4–6: complete verified workflows | 3/3 | 3/3 |
| New attempts: exact server-side saves | 3/3 | 3/3 |
| New attempts: authenticated session reused | 3/3 | 3/3 |
| New successful execution mean | 179.32 s | 67.39 s |
| New API estimate, all three attempts | $1.120000 | $0.746342 |
| New API cost per verified workflow, including unsuccessful new attempts | $0.373333 | $0.248781 |
| All six: complete workflows | 4/6, including two censored attempts | 6/6 |
| All six: correct server-side saves | 5/6 | 6/6 |
| All-six API accounting / verified workflow | $0.668000, including unresolved pilot reserves | $0.249695 |

| Agent | Attempt | Verified workflow | Correct save | Time | Actions / entries | Images | API estimate | Evidence |
|---|---:|---|---|---:|---|---:|---:|---|
| Tinyfish | 4 | PASS | Yes | 158.14 s | 26 provider steps | 25 | $0.416000 | [Original + audit](uncapped-followup/runs/tinyfish/attempt-04/server-verification.json) |
| Tinyfish | 5 | PASS | Yes | 253.20 s | 26 provider steps | 25 | $0.416000 | [Original + audit](uncapped-followup/runs/tinyfish/attempt-05/server-verification.json) |
| Tinyfish | 6 | PASS | Yes | 126.61 s | 18 provider steps | 17 | $0.288000 | [Original + audit](uncapped-followup/runs/tinyfish/attempt-06/server-verification.json) |
| Claude | 4 | PASS | Yes | 74.69 s | 30 native computer actions including screenshots/zoom | 11 | $0.260754 | [Original + audit](uncapped-followup/runs/claude/attempt-04/server-verification.json) |
| Claude | 5 | PASS | Yes | 59.67 s | 28 native computer actions including screenshots/zoom | 10 | $0.223442 | [Original + audit](uncapped-followup/runs/claude/attempt-05/server-verification.json) |
| Claude | 6 | PASS | Yes | 67.81 s | 31 native computer actions including screenshots/zoom | 11 | $0.262146 | [Original + audit](uncapped-followup/runs/claude/attempt-06/server-verification.json) |


[All twelve attempts](RESULTS.md) · [Comparison and interpretation](COMPARISON.md) · [Setup effort](SETUP.md) · [Methodology](METHODOLOGY.md) · [Costs and unexecuted projections](COSTS.md) · [Article-ready findings](ARTICLE-READY.md) · [Offline verification](verify_complete_experiment.py) · [Machine-readable combined results](combined-results.json)

Each attempt opens a specific synthetic supplier, changes Pending to Reviewed, enters an exact paired note, saves, checks the visible record and returns its generated confirmation. Independent owner-side audit and native database snapshots verify the saved data and final returned ID. No agent is given the verification data or API credentials in its prompt. No harness performs the evaluated supplier task.

**Watchdog correction:** [Original stop investigation](WATCHDOG-INVESTIGATION.md) and [amended protocol](uncapped-followup/AMENDMENT.md) retain the interrupted pilots. The old locally frozen plan remains historical evidence; the user's later authorization superseded its extension gate for exactly three additional attempts each. Pairs 7–10 were not run. No automatic benchmark restart, top-up, purchase, Vault login or agent session-recovery test occurred. Both test sessions were revoked and the owned desktop/VM stopped after execution.

TinyFish exposes a managed Web Agent and dedicated saved Browser Context Profile; its exact model revision and internal action/retry details were not exposed. Claude used `claude-sonnet-5-5`, native `computer_toolset_20260801`, and an owned local Linux/Firefox environment. These are materially different execution systems, not a comparison of the same model in two wrappers.
