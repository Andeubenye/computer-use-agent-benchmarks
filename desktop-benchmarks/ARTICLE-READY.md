# What I learned from testing Claude and OpenAI on desktop work

I wanted to know whether a computer-use agent could finish the whole job: open a file, make the right changes, save a separate copy, and reopen it to check the result. A correct-looking final message was not enough. I checked the saved files against an answer key and reviewed the screenshots and action traces separately.

I used five small desktop tasks: correcting two CSV typos, organizing 20 files, editing and formatting a document, turning 30 sales records into a written report, and continuing after a controlled interruption. Claude and OpenAI made their own mouse and keyboard decisions through their native computer tools. They worked in isolated Linux desktops with LibreOffice, not directly in my everyday Mac applications. The harness executed their requested actions; it did not complete the tasks for them.

| Desktop task | Claude | OpenAI |
|---|---|---|
| CSV corrections | Partial, 4/5 | Pass, 5/5 |
| File organization and batch renaming | Partial, 2/5; executor error | Pass, 5/5 |
| Document editing and formatting | Pass, 5/5 | Pass, 5/5 |
| Cross-application sales report | Pass, 5/5 | Pass, 5/5 |
| Controlled error recovery | First attempt partial, 4/5; labeled retry pass, 5/5 | Pass, 5/5 |

The document and reporting tasks gave me the clearest examples of completed work. Both agents fixed the document’s spelling and table entry, applied the required heading style, preserved the source and reopened the new file. Both also moved between Calc and Writer to produce a correct sales summary: 1,780.00 in revenue, 90 units, an average order value of 59.33, and South as the highest-revenue region. I recomputed those figures independently from the original 30 rows. OpenAI’s report took about 146 seconds and Claude’s about 193 seconds, but these single observations are not a reliable speed ranking.

Claude’s CSV result shows why I separate file editing from workflow completion. Its corrected file matched the expected CSV exactly, and the original was untouched. But it stopped at the reopening dialog after a token-count request timed out. I kept that result at 4/5. Its file-organization attempt was also interrupted by the desktop executor during a drag. It created the four folders and preserved all 20 files, but did not finish moving or renaming them. That is a limitation of the observed run, not proof that Claude cannot organize files.

Recovery needed another qualification. The interruption was a synthetic warning, not an actual crash or lost document. Claude’s first attempt saved the right approved document and reopened it, but my local request-budget guard stopped the next model response before it could review the reopened image. I preserved that 4/5 attempt, then made one clearly labeled retry with more of the existing allowance allocated to it. The retry completed all five checks in about 204 seconds. OpenAI completed its recovery workflow in about 97 seconds without a benchmark restart. The different retry history and local allowances matter when interpreting those results.

Across this desktop batch, OpenAI completed all five task checklists. Claude completed three, including recovery on its retry, and had two partial results. I would not turn that into a claim that one agent is generally better. There was one task instance per category, the added fixtures were reconstructed from my task descriptions and then frozen, and infrastructure affected several runs. OpenAI’s first two runs also preceded a click-modifier translation fix. Their saved results still passed, but their timings and action counts carry that caveat. Claude’s older CSV timing overlapped host sleep, so I exclude it from speed comparisons.

My estimated API spending was **$3.67 in total**, including failed and interrupted attempts: **$3.20 for Claude and $0.47 for OpenAI**. The full-precision estimate is $3.6676817, leaving $3.3323183 of the original $7 cap. These figures come from returned token usage and recorded prices, not reconciled invoices. OpenAI reported automatic cached input; Claude reported no cache reads. Tokenization, caching, tool behavior and retries all affect the totals. Raw action and screenshot counts are available in the evidence, but the providers do not count identical units.

Sai remains **not tested** for these added desktop tasks because its authorized control route returned HTTP 403. I did not bypass that restriction. UI-TARS was not part of this desktop batch. My TinyFish recommendation for managed web research, navigation and extraction belongs to the separate browser section; I have kept the browser results and desktop results separate.

For me, the useful distinction is between producing a correct file and completing the requested workflow. Both deserve to be recorded, and neither should be inferred from an agent saying “done.”

[Full results and every attempt](RESULTS.md) · [Methodology and limitations](METHODOLOGY.md) · [Costs](COST-COMPARISON.md) · [Independent audit](logs/usage-reconciliation.json)
