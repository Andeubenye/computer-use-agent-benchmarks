# Setup and engineering effort

| Item | TinyFish | Claude |
|---|---|---|
| Existing integration reused | Hosted async Web Agent API client | Native Anthropic loop and Docker desktop controller |
| Runtime to maintain for this experiment | Provider-managed cloud browser; saved dedicated profile | Existing Colima VM, ARM64 container, Firefox and native action executor |
| Initial timed login/profile setup | 22.62 s | 21.94 s |
| Refresh before new three attempts | 21.96 s | 21.16 s |
| Login/controller method, outside scored tasks | Supported profile setup CDP session; existing Playwright installation logs in and saves | Native keyboard/mouse login; clipboard cleared afterward |
| Persistence during each batch | Same dedicated profile, `use_profile=true` | Same owned container/Firefox cookie context |
| Password in agent goal | No | No |
| Vault / actual agent reauthentication | NOT TESTED | NOT TESTED |

These short login timings are not from-scratch integration times. The first audit/fixture/deployment/integration work occupied about 31 minutes of wall-clock time before the first pilot submission (16:19:36–16:50:40 UTC), with existing SDKs, adapters, VM image and prior engineering reused. Implementing and validating the later spending-guard amendment took roughly three further minutes of wall-clock preparation before its first submission; this is elapsed preparation, not measured human labor. Human engineering hours, concurrent work and historical setup were not measured separately. Provider-specific bootstrap/setup sources and exact hashes are published; their size is not a measure of development effort.

Shared work built an isolated synthetic HTTPS portal with durable database records, session authentication, CSRF protection, optimistic versions, atomic save/audit operations, receipts, reset and expiry endpoints. Twelve unscored fixture QA checks passed; the QA record was removed from the active dashboard before scored attempts. No synthetic Save performed by QA counted as an agent success.

One initial deployment omitted the migration directory; QA seed failed. The supported archive field was corrected and migrations included in the next source version before any scored request. An unused synthetic admin value echoed in a connector schema error was discarded and replaced before deployment; no valid provider key appeared in evidence. The new batch initially used the wrong local Python interpreter for profile setup; it failed before any provider request, then used the already-installed Playwright environment. No dependency installation, app rebuild or benchmark retry resulted.

The original two sessions were revoked during cleanup before the user requested the additional batch. Both providers therefore received one refreshed synthetic login in setup, with new session aliases and no per-attempt login. This is an environment reset between phases and must be disclosed. The same TinyFish profile, Linux image and fixture deployment were retained; local desktop startup/teardown is infrastructure overhead outside model timing. No real account/password-manager connection was created.

TinyFish's observable operational advantage here is that I did not host its browser or native executor. Claude's local runtime gave me direct control over screenshots and action execution. This experiment does not quantify maintenance labor, availability SLAs, profile security, or production infrastructure costs. It does not show that either approach has lower total ownership cost.

[Pilot setup evidence](setup/) · [New setup evidence](uncapped-followup/) · [Deployed fixture source](fixture/) · [Executed pilot harness snapshots](harness/executed-source/) · [Executed new harness/core snapshots](uncapped-followup/harness/executed-source/)

After the final agent stopped, the first bulk collection pass exited 1 after fetching the audit; its wrapper suppressed stderr, so the precise cause is unavailable. One unchanged read-only collection retry succeeded. Both passes are recorded; no agent request or task was repeated. The independent native database read and per-run audits agree. [Collector failure](uncapped-followup/final-collection-status.json) · [Read-only retry](uncapped-followup/collection-retry.json).
