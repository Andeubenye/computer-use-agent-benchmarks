# Claude GitHub benchmark rerun — budget-limit failure

Run **`20261017T004821Z-eba39479`**, 17 October 2026. The explicitly approved prepared launcher ran **exactly once** with the unchanged model, native toolset and limits. **Task success: false. Final answer: none.** No additional paid trial or retry was launched.

## Exact termination reason

The agent stopped as **`budget_limit`** before generation request 16. Known provider-reported usage cost was **$0.419026**. The free token-count preflight counted 22,094 input tokens for the next request. The unchanged conservative guard reserved **$0.102178**, including input allowance and all 4096 possible output tokens. Known spend plus reservation was **$0.521204**, exceeding the configured **$0.50** guard. The next generation request was **not sent**.

The last provider response ended with `tool_use`; `budget_limit` is the runner's termination status, not an Anthropic response stop reason. All 15 responses ended normally for a tool turn; none hit `max_tokens`. The largest response used 527 output tokens. The configured 300 seconds, 20 turns and 80 actions were not exhausted. A higher response allowance increases the conservative output reservation even when the model uses fewer tokens. No limit was increased to obtain another response.

## Final answer and independent grading

Claude returned **no final issue list, titles, URLs or calendar dates**. Its last retained text was progress commentary: “The Enter seems not processed; press again.” This is partial output, not an answer. The grader marked strict task success false. The result-field checks are unmet because the final answer is absent, not because the grader found incorrect returned values.

The saved screenshots show the correct filtered list (`is:issue is:open label:bug sort:updated-desc`, 48 matches). Claude visually opened issue pages #6068, #4579 and #6065 and attempted date hovers. It stopped while viewing #6065. Only native screenshot/mouse/keyboard actions were exposed. No GitHub API, DOM, direct issue-data HTTP retrieval, browser automation API, login or repository changes were used.

After the agent stopped, the grader independently inspected the current filtered list, hovered each title to observe its URL in Firefox's status bar, and hovered each update label to reveal the date tooltip. The following are **grader observations, not Claude's final answer**. They were never fed back to Claude.

| Issue / URL | Title | Last updated (UTC) |
| --- | --- | --- |
| [6068](https://github.com/browser-use/browser-use/issues/6068) | Bug: agent enables a disabled button with evaluate, places the order, and often reports a plain success | 2026-10-16 08:59 UTC |
| [4579](https://github.com/browser-use/browser-use/issues/4579) | Bug: CDP connection instability causing indefinite hangs with remote browsers | 2026-10-15 06:31 UTC |
| [6065](https://github.com/browser-use/browser-use/issues/6065) | Bug: Browser parameter accept_downloads is nonfunctional when running Browser-use locally | 2026-10-14 15:44 UTC |
| [4877](https://github.com/browser-use/browser-use/issues/4877) | Bug: ...pip dependency conflicts due to strict exact-pins (==) in pyproject.toml | 2026-10-14 06:18 UTC |
| [5633](https://github.com/browser-use/browser-use/issues/5633) | Bug: AnthropicMessageSerializer drops earlier system messages | 2026-10-10 05:54 UTC |

Dates have visible minute precision, not inferred seconds. Each number/title/link/date has screenshot evidence mapped in `grading/observed-issues.json` and `.csv`; the matching list is `grading/002-filtered-list.png`. The grader observed the same five entries as in the agent list. There was no visible list change between those observations; unobserved intermediate changes cannot be excluded. The calendar-date rubric remains exclusively in evaluation guidance, not the shared task prompt.

## Observed metrics

| Metric | Value |
| --- | ---: |
| Evaluated success | **False** |
| Agent execution termination | `budget_limit` |
| Final answer / returned issue count | None / 0 |
| Agent wall time | **167.296774 s** |
| Benchmark wall time | 167.296774 s |
| Generation request time | 45.898278 s |
| Token-count request time | 24.198048 s |
| Computer action time | 96.821664 s |
| Agent actions attempted / successful / failed | **68 / 68 / 0** |
| Agent screenshot images | **16**: 11 full screenshots + 5 zoom crops |
| Completed model turns / generation requests | **15 / 15** |
| Free token-count requests | **16**, including the blocking preflight |
| Total Anthropic API requests | **31** |
| Provider-reported input / output tokens | **193,673 / 3,168** |
| Cache write / cache read tokens | 0 / 0 |
| Usage-derived API cost | **$0.419026** |
| API / executor errors | 0 / 0 |
| Automatic API retries / instrumented tool-error recovery attempts | 0 / 0 |

Generation request time is client-observed API latency including transport; server-only inference time is unavailable. All 15 serialized response bodies and usage records were saved, with recognizable credential patterns redacted. There is no missing-usage cost reservation or billing uncertainty flag. Cost is `193,673 × $2/1M + 3,168 × $10/1M = $0.419026` using the existing [Anthropic standard pricing](https://platform.claude.com/docs/en/about-claude/pricing), verified 2026-10-17. This is actual reported usage multiplied by published rates, not an invoice; credits, taxes and account adjustments were not inspected. No provider-side account spending limit was changed or verified. The $0.50 guard remains local, not a guaranteed Anthropic billing cap.

## Errors and recovery behavior

No API request or desktop action reported an error. However, screenshots and action arguments show that Claude typed three URLs with trailing newlines (turns 1, 11 and 14) without an explicit Return key. Firefox remained at its address bar; subsequent turns 2, 12 and 15 pressed Return and completed navigation. This was agent correction within the same run, not an API retry. The formal recovery counter stays zero because it counts replanning after executor-reported failures, and none occurred. These navigation corrections added actions and growing conversation context. The complete action breakdown is in `action-breakdown.json`; raw native arguments are in `responses/`.

## Separate grading time and counts

| Metric | Value |
| --- | ---: |
| Grader elapsed time | **109.562569 s** |
| Grader computer actions | **39** |
| Grader screenshots | **12** |
| Grader clipboard metadata reads | 1 |
| Grader errors / API calls | 0 / 0 |
| Agent + grader measured intervals | 276.859343 s |
| Total graded wall time | **287.179649 s** |

Total graded wall time spans benchmark-loop start through grading completion and includes the inter-phase gap. Grading time includes human/model-assisted screenshot review and orchestration. It excludes container reset/setup, earlier offline validation, later report writing and packaging. None of the grader's actions or screenshots are included in the agent counts. The configured 300-second limit applies to the agent run, not subsequent independent grading. Original agent `summary.json` remains unchanged; `graded-summary.json`, `graded-results.csv` and `evaluation.json` contain the separate reviewed result.

## Environment, task and limits

Requested and returned model: **`claude-sonnet-5-5`**; native toolset **`computer_toolset_20260801`**; SDK method `client.messages.create()`, API version `2023-06-01`, no beta header. Reused Python 3.12.4, uv 0.5.3, Anthropic SDK 1.15.0, Docker/Colima and existing Firefox ESR 153.5.0 Linux ARM64 image. The prepared launcher stopped/started the benchmark container, producing a fresh profile without rebuilding or reinstalling. Resolution stayed **1024 × 768**. Claude changed browser zoom from 100% to 60%; the grader retained that final zoom.

Limits remained **$0.50 / 300 seconds / 20 model turns / 80 computer actions / 4096 output tokens per response / zero SDK retries**. The exact shared prompt and separate rubric are saved in `task.json`, and the actual tool/model/system/limits in `configuration.json`. Task ID: `github-browser-use-recent-open-bugs-v2`; task SHA-256 `d1ad105ba840e0b3bfe512beb0af50808ad308672525204bafffcfa351e9f120`. Image ID: `sha256:195fda83d17d253dbb5d122583fd7d58cdfb13971e16f6fd7c1f73840b07f55d`. Source hashes matched the approved preparation. Authentication succeeded; credentials and authentication headers are absent from retained artifacts.

Before execution, **54 offline tests and lint passed** using the existing environment. Those checks did not establish live task success; the live and independently graded result is failure.

## Comparison with existing results

| Metric | Original Claude GitHub | This approved rerun | Existing OpenAI |
| --- | ---: | ---: | ---: |
| Result | No final answer; `incomplete_max_tokens` | No final answer; `budget_limit` | Partial: five issues, relative dates |
| Strict success | False | False | False |
| Recorded benchmark wall time | 63.311995 s | 167.296774 s | 97.546 s |
| Model actions | 28 | 68 | 27 |
| Screenshot images | 9 | 16 | 11 |
| Generation requests | 6 | 15 | 11 |
| Input / output tokens | 49,585 / 2,174 | 193,673 / 3,168 | 132,467 / 955 |
| Recorded usage-derived / estimated USD cost | $0.120910 | $0.419026 | $0.07318020 |
| Output cap per response | 1024 | 4096 | 4096 |

OpenAI values come from the existing `openai_run_1.json` (model `gpt-6.1-sol`), not a new trial. Its input included 111,467 cached tokens; Claude had none. Its cost is retained as originally estimated, excludes a separate $0.002176 capability probe, and is not an invoice. OpenAI's extra model-access check is outside its 11 generation requests. The comparison is not controlled: different browser/desktop isolation, viewport, starting navigation, screenshot/action definitions, timer boundaries, output-format guidance and overall action/time limits apply. The output allowance now matches, but failure times are not successful task completion speeds. `comparison.json` records these limitations and source provenance.

## Saved records and preservation

This new directory contains the original agent summary/CSV entry, JSONL events, **15 redacted SDK response bodies**, task/configuration, **16 agent images**, independent evaluation, grader review/state/events, **12 grader images**, grader-observed issue CSV/JSON, separate graded JSON/CSV, budget explanation and reproducibility metadata. `github-rerun-results.zip` includes all of this directory and the updated paid CSV containing all three runs.

The previous Wikipedia and failed GitHub run files are byte-for-byte unchanged. The existing result archives and previous reports are unchanged. The paid CSV was appended with one new row; both historical rows match their original values. The original failed run has not been overwritten or reclassified. No further paid trial is authorized.
