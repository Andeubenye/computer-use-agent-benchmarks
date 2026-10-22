# Cost comparison

Original cumulative cap: **$7**. Estimated spent: **$3.6676817**. Uncertain reserved: **$0**. Remaining conservative allowance: **$3.3323183**.

| Agent | Estimated total, including unsuccessful attempts | Verified PASS tasks | Estimated spend per verified PASS |
|---|---:|---:|---:|
| claude | $3.19739 | 3 | $1.0657967 |
| openai | $0.4702917 | 5 | $0.0940583 |
| sai | $0 | 0 | Not calculable; no verified PASS |

## Per-attempt usage

| Attempt | Outcome / stop reason | Time seconds | Actions | Images | Estimated API cost |
|---|---|---:|---:|---:|---:|
| [claude](logs/claude/run-record.json) | BLOCKED — harness protocol failure; execution_error | 12.71 | 5 | 3 | $0.013434 |
| [claude-attempt-2](logs/claude-attempt-2/run-record.json) | PARTIAL; execution_error | 397.54 UTC / 183.18 stopwatch | 49 | 13 | $0.273314 |
| [openai](logs/openai/run-record.json) | PASS; model_finished | 128.71 | 34 | 25 | $0.0801494 |
| [claude/task-2](logs/claude/task-2/run-record.json) | NOT TESTED; infrastructure_or_protocol_error | 0.00 | 0 | 0 | $0 |
| [claude/task-2/attempt-2](logs/claude/task-2/attempt-2/run-record.json) | PARTIAL; execution_error | 106.13 | 49 | 10 | $0.22361 |
| [openai/task-2](logs/openai/task-2/run-record.json) | PASS; model_finished | 292.04 | 95 | 38 | $0.1791222 |
| [claude/task-3](logs/claude/task-3/run-record.json) | PASS; model_finished | 104.52 | 45 | 13 | $0.335324 |
| [openai/task-3](logs/openai/task-3/run-record.json) | PASS; model_finished | 112.36 | 34 | 19 | $0.0668268 |
| [claude/task-4](logs/claude/task-4/run-record.json) | PASS; model_finished | 193.29 | 102 | 20 | $0.715518 |
| [openai/task-4](logs/openai/task-4/run-record.json) | PASS; model_finished | 146.06 | 54 | 27 | $0.0896323 |
| [claude/task-5](logs/claude/task-5/run-record.json) | PARTIAL; execution_error | 223.24 | 100 | 25 | $0.885828 |
| [claude/task-5/attempt-2](logs/claude/task-5/attempt-2/run-record.json) | PASS; model_finished | 204.41 | 74 | 21 | $0.750362 |
| [openai/task-5](logs/openai/task-5/run-record.json) | PASS; model_finished | 96.94 | 31 | 16 | $0.054561 |

OpenAI estimates use returned input/output/cache usage at Standard rates of $2/M uncached input, $0.10/M cached input, $2.50/M cache write, and $10/M output for the requested model. Anthropic estimates use the recorded Sonnet rates and returned usage. No cache tokens were reported for the historical Claude CSV attempts. See the [official OpenAI pricing](https://developers.openai.com/api/docs/pricing) and saved provider usage. Invoice reconciliation, taxes and unrelated earlier browser hosting costs are unavailable or outside this budget scope.

Cost per verified PASS includes unsuccessful attempts for the same provider and is descriptive of this small batch. It is not an estimate of production reliability or a matched cost ranking. Sai's denial produced no agent task charge. Local environment preparation used existing hardware and no paid cloud infrastructure; electricity and labor are not measured.
