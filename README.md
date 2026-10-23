# Computer-use agent benchmarks

Supporting evidence for Vera Agiang’s Manicule article, **“Best Computer Use Agents in 2026: Tested and Compared by Use Case.”** This is a small hands-on case study, not a general agent ranking.

I began with website tasks, then tested native desktop file and application workflows. The original experiment covered six agents. This public edition presents five in scope from that existing work; TinyFish was part of the original browser batch, not a separately conducted replacement test. **TinyFish is a browser agent.**

| Start here | What you can inspect |
|---|---|
| [Results](RESULTS.md) | Separate browser and desktop tables; retries and blocks |
| [Browser tasks](browser-benchmarks/README.md) | Five common tasks, exact prompt variants, scoring, logs and screenshots |
| [Desktop tasks](desktop-benchmarks/tasks/README.md) | Five tasks, frozen fixtures, expected files, actual artifacts and GUI evidence |
| [Later UI-TARS suite](browser-benchmarks/tasks/ui-tars-supplement.md) | Five different browser tasks, all interrupted by timeouts |
| [Methodology](METHODOLOGY.md) | Environment differences and independent verification |
| [Costs](COSTS.md) | Per-attempt measurements, estimate categories and missing costs |
| [Limitations](LIMITATIONS.md) | Missing evidence, reconstruction and infrastructure confounds |
| [Reproducing](REPRODUCING.md) | Offline grading and honest execution prerequisites |
| [Evidence checks](verification/README.md) | Hashes, prompt integrity, scope, secrets and links |

## Direct task links

| Browser tasks | Desktop tasks |
|---|---|
| [GitHub bugs](browser-benchmarks/tasks/github-issues.md) | [CSV editing](desktop-benchmarks/tasks/csv-editing.md) |
| [Wikipedia](browser-benchmarks/tasks/wikipedia-research.md) | [File organization](desktop-benchmarks/tasks/file-organization.md) |
| [Form completion](browser-benchmarks/tasks/form-completion.md) | [Document editing](desktop-benchmarks/tasks/document-editing.md) |
| [GitHub enhancements](browser-benchmarks/tasks/github-navigation.md) | [Sales report](desktop-benchmarks/tasks/cross-application-reporting.md) |
| [Popup recovery](browser-benchmarks/tasks/error-recovery.md) | [Desktop recovery](desktop-benchmarks/tasks/error-recovery.md) |

## Agents

[Claude](agents/claude.md) · [OpenAI](agents/openai.md) · [Simular Sai](agents/simular-sai.md) · [UI-TARS](agents/ui-tars.md) · [TinyFish — browser only](agents/tinyfish.md)

## What the desktop artifacts establish

| Task | Claude | OpenAI |
|---|---|---|
| CSV editing | PARTIAL 4/5 | PASS 5/5 |
| File organization | PARTIAL 2/5; executor interruption | PASS 5/5 |
| Document editing | PASS 5/5 | PASS 5/5 |
| Cross-application reporting | PASS 5/5 | PASS 5/5 |
| Desktop error recovery | PASS 5/5 on labeled retry; first attempt PARTIAL 4/5 | PASS 5/5 |

OpenAI completed all five desktop checklists. Claude completed document editing, reporting and recovery on a labeled retry; CSV and organization remain partial. These observations include harness interruptions and do not establish general model superiority. Sai’s desktop API route was authorization-blocked; its separate frontend evidence could not be independently recovered. UI-TARS has browser interactions and failures, not a completed desktop workflow.

**The initial repository package was assembled without rerunning experiments.** The authorized TinyFish follow-up below is a later, separate execution. Earlier private repositories, raw logs and backups remain unchanged. Public copies retain failed attempts and explicitly describe redactions and missing material. No keys, browser profiles or private endpoint URLs are needed to inspect the results.

## Form follow-up — 22 October 2026

[Three TinyFish reruns against the original Claude form result](browser-benchmarks/reruns/tinyfish-form-2026-10-22/README.md): eight confirmed correct fields per rerun, one strict message mismatch, one unverified checkbox. The original packaging statement above refers to repository assembly; these are explicitly authorized later executions, not replacement results.

## Clarified form experiment — 22 October 2026

[Three fresh TinyFish and three fresh Claude runs](browser-benchmarks/reruns/clarified-form-2026-10-22/README.md) use the exact clarified prompt and unchanged ten-field rubric. Claude: three verified 10/10; TinyFish: two partial nine-confirmed results and one budget-stopped failure. Earlier prompt configurations remain separate. [Article-ready interpretation](browser-benchmarks/reruns/clarified-form-2026-10-22/ARTICLE-READY.md).

## Authenticated supplier workflows — 22 October 2026

New uncapped supplier workflows: TinyFish **3/3**, Claude **3/3**; both reused login. Earlier three pilots each remain separate, including two TinyFish budget-censored attempts. [Twelve attempts and verification](browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/README.md) · [Article-ready findings](browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/ARTICLE-READY.md). This is a new authenticated browser cohort, not a replacement for earlier browser or desktop results.

## Session durability without Vault — 22–23 October 2026

One new diagnostic per configuration: TinyFish saved Profile **restored** authentication, Claude original disposable container **lost** it, and Claude with a separate persistent Firefox volume **restored** it. All three agents/configurations correctly reported the observed page. New total API usage value **$0.165142**, with no cost watchdog or prior benchmark rerun. One unsubmitted infrastructure failure and its repair are retained. [Experiment, original outputs and independent server checks](browser-benchmarks/session-durability/supplier-portal-2026-10-22/README.md). Vault and expired-session reauthentication remain NOT TESTED. [Final article benchmark update](article/FINAL-BENCHMARK-UPDATE.md).
