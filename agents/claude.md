# Claude Computer Use

**Classification:** Native API computer-use agent; browser and desktop evidence.

Browser: all four additional tasks pass; original GitHub pass only after two failures. Desktop: CSV 4/5; organization 2/5 with executor error; document and sales 5/5; recovery 5/5 on labeled retry, first attempt 4/5.

[Browser task definitions](../browser-benchmarks/README.md) · [Browser measurements](../browser-benchmarks/results/benchmark-results.csv) · [Desktop comparison](../desktop-benchmarks/COMPARISON.md) · [Costs](../COSTS.md)

Original responses, configuration, screenshots, failed attempts and verification remain under the agent-owned evidence folders. Model aliases are recorded, not inferred as immutable snapshots.

## Clarified form — separate browser configuration

[Three new native runs](../browser-benchmarks/reruns/clarified-form-2026-10-22/README.md) each verified 10/10, including exact message and visibly unchecked newsletter. Mean native time 55.33 s; mean token estimate $0.194789. Two runs corrected an initial entry mistake. Post-model collection timed out in all three; original error records and sufficient retained upper/lower screenshots remain visible. No task was rerun or manually repaired. Browser and desktop outcomes remain separate.

## Authenticated supplier workflows — 22 October 2026

A separate twelve-attempt experiment retains three pilots and three additional uncapped attempts per provider. [Results, setup, costs and evidence](../browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/README.md) · [Offline verifier](../browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/verify_complete_experiment.py). Earlier benchmark evidence is unchanged.

## Session durability without Vault — 22–23 October 2026

One new diagnostic per configuration: TinyFish saved Profile **restored** authentication, Claude original disposable container **lost** it, and Claude with a separate persistent Firefox volume **restored** it. All three agents/configurations correctly reported the observed page. New total API usage value **$0.165142**, with no cost watchdog or prior benchmark rerun. One unsubmitted infrastructure failure and its repair are retained. [Experiment, original outputs and independent server checks](../browser-benchmarks/session-durability/supplier-portal-2026-10-22/README.md). Vault and expired-session reauthentication remain NOT TESTED. [Final article benchmark update](../article/FINAL-BENCHMARK-UPDATE.md).
