# What TinyFish took off my plate—and what I still had to build

My developer job was straightforward: update a supplier record in a logged-in portal, save the exact note and bring back a confirmation I could verify. After running the workflow with TinyFish and Claude Computer Use, I wanted to look beyond whether the agents finished. What did I actually have to build and keep running for each one?

The execution results matter here. In the three new attempts without my custom spending stops, both completed every workflow. Claude averaged about **67 seconds**, compared with **179 seconds** for TinyFish. Estimated API cost per completed workflow was about **$0.25 for Claude and $0.37 for TinyFish**. TinyFish didn't win this test on speed or measured API cost. [Results and cost evidence](combined-results.json).

What it changed was the execution stack I owned.

## With TinyFish, I called a service. With Claude, I operated the hands.

My TinyFish integration submitted the goal, URL and saved profile ID, polled the run and collected the result and screenshots. TinyFish operated the browser and the agent's action loop behind that API. I still wrote timeout, error-handling and evidence-collection code, but I didn't implement a mouse driver or send each screenshot back into its model conversation. [Submission/polling source](harness/executed-source/tinyfish-adapter-original.py#L14), [profile override](uncapped-followup/harness/executed-source/run_workflows.py#L71).

My Claude implementation had more moving parts under my control. The model ran through Anthropic's API, but the browser ran in my existing Linux desktop environment: Colima, Docker, Xvfb, Openbox and Firefox. My code translated Claude's tool calls into keyboard and mouse actions, captured screenshots, formatted the tool results and continued the conversation. I also owned container startup, readiness checks and shutdown. [Desktop lifecycle](harness/executed-source/claude/desktop.py#L103), [native executor](harness/executed-source/claude/native-action.py#L69), [feedback loop](uncapped-followup/harness/executed-source/uncapped_core.py#L466).

That is the clearest infrastructure difference I can support: **TinyFish removed my browser execution host and low-level action loop from this implementation.** It didn't remove my application.

| What I owned | TinyFish implementation | Claude implementation |
|---|---|---|
| Browser execution host | Provider-managed | My reused VM/container and Firefox environment |
| Low-level GUI actions and image feedback | Provider-managed | My bridge, native executor and model loop |
| Initial authenticated access | My setup script and TinyFish profile API | My native login script and persistent Firefox context |
| Task policy, verification and evidence | My code | My code |
| Production maintenance cost | Not measured | Not measured |

## The login setup was less different than I expected

TinyFish's saved Browser Context Profile was useful: I established a synthetic login once and selected that profile for later runs. But getting it ready still used my own setup script and an existing Playwright installation connected to the hosted browser. “Managed” didn't mean there was no integration work. [Profile setup source](uncapped-followup/harness/executed-source/setup_tinyfish_profile.py#L20).

I gave Claude equivalent access. It kept the same Firefox session across its three attempts. Both reused their logins, so this experiment did not show that authentication persistence was unique to TinyFish. TinyFish restored saved state into separate remote runs; my Claude setup kept a live container rather than implementing durable restore after shutdown. I didn't test expired-login recovery for either, and TinyFish Vault wasn't configured. [Session evidence and limits](METHODOLOGY.md).

The recorded initial setup routines took roughly 23 seconds for TinyFish and 22 seconds for Claude. Those are automated setup timings, not the time it took me to design, integrate and debug everything. Both reused earlier work. I can't turn them into a claim about developer hours.

## I counted code, but I wouldn't count hours that way

The audit found **111 physical lines across three TinyFish-specific source units**, compared with **1,044 across eight Claude units** in the selected effective implementation. Those totals include setup, error handling and benchmark instrumentation; Claude's total also includes reusable grading and recording code. TinyFish's Python is much more compressed: its 109 code-bearing lines contain 212 Python statements. The comparison is not a production minimum, and it certainly doesn't mean nine times less engineering. [Reproducible inventory and counting rules](ENGINEERING-EFFORT-AUDIT.md#1-source-scope-and-measurement-rules).

The useful finding is which code wasn't needed on the TinyFish side: my Docker desktop recipe, local action executor and custom model-to-desktop feedback loop. I still needed credentials handling, an authorized task, run monitoring, result parsing and an independent way to know the save really happened.

I also built a synthetic portal, paired records and server-side audit checks for the experiment. That was shared benchmark work, not an integration cost I can assign to either provider. In a real application I wouldn't rebuild that test portal, but I would still need business rules, authorization and trustworthy completion checks. [Shared implementation and responsibilities](ENGINEERING-EFFORT-AUDIT.md#3-component-and-dependency-inventory).

## This isn't the only way to build with Claude

My comparison needs that qualification. Anthropic now documents a Browser Use tool that works inside webpages without a full desktop. Its SDK can run the tool loop with a supplied driver, including partner drivers. Developers don't all need my custom native executor. [Browser Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool), [SDK toolsets](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk).

There are managed options too. Claude Managed Agents supplies a hosted harness/runtime, and Browserbase and Kernel document browser integrations with it. Those integrations differ from simply enabling the native client toolset. I didn't benchmark them, price them or test their authentication behavior, so I can't assign them my local implementation's overhead. [Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview), [Browserbase](https://docs.browserbase.com/integrations/anthropic/managed-agents/introduction), [Kernel](https://www.kernel.sh/blog/claude-managed-agents).

For my implementation, TinyFish reduced the browser infrastructure and execution code I had to operate. Claude gave me direct control over that environment and performed the successful runs faster and at a lower estimated API cost. I haven't measured whether the infrastructure TinyFish took off my hands outweighs that API difference in money, maintenance time or production reliability. That is the boundary of the evidence—not a reason to invent a winner.

[Full engineering audit, architecture, source counts, responsibility matrix and ownership-cost framework](ENGINEERING-EFFORT-AUDIT.md).
