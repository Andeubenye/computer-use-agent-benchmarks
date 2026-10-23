# What survived when I shut the browser down

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

[Results and original responses](RESULTS.md) · [Setup and ownership](SETUP.md) · [Costs](COSTS.md) · [Methodology and interruption records](METHODOLOGY.md).
