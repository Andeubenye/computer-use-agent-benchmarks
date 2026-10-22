# What this experiment establishes

In the new batch without spending stops, TinyFish completed 3/3 and Claude completed 3/3 fully verified workflows. Their successful-run means were 179.32 s and 67.39 s; their API costs per verified workflow were $0.373333 and $0.248781, respectively. These are observed cases on one fixture, not general rankings.

Both providers reused authenticated sessions in their original pilots and the new batch. TinyFish's managed profile therefore did not demonstrate a unique session-reuse capability over this persistent Claude baseline. I did not require Claude to log in every time.

The architectural distinction is concrete: TinyFish hosted its browser and persisted its profile; Claude needed the existing local VM/container, native action executor and Firefox context. That removes one component I would otherwise operate for TinyFish, but it did not remove the shared work of creating the portal, test data, prompts, verification, evidence collection and secure setup. This study did not measure ongoing maintenance hours or infrastructure SLAs, so it cannot turn that distinction into a proven total-cost advantage.

Across all six attempts, TinyFish completed 4/6, with two earlier censored attempts retained, while Claude completed 6/6. Treat that as a history of what happened under two protocols. The two watchdog interruptions cannot fairly be counted as evidence that TinyFish's uncapped agent would have failed. One interrupted run had already saved correctly, which is why server-side accuracy and full workflow completion are separate columns.

No Vault connection, MFA, password rotation, captcha or agent session-expiration recovery was evaluated. The user authorized existing API usage, not new account commitments or purchases; no automatic top-up occurred. More independent tasks, many more uncapped runs and a measured operations-cost study would be needed to establish repeated production reliability or total ownership cost.
