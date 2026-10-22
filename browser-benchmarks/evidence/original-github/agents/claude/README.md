# Claude Computer Use

The preserved original successful-run summary says needs_review. A separate new verification now confirms all twenty fields and ordering. Both earlier GitHub failures remain preserved. No new Anthropic inference request was sent.

| Agent | Model/configuration | Result | Verified required fields | Recorded time | Actions (different units) | Visual evidence | Cost and basis |
|---|---|---|---|---|---|---|---|
| Claude Computer Use | claude-sonnet-5-5 / computer_toolset_20260801 | Successful rerun; 2 prior failures | 20/20; five correct, ordered | 116.31 s (successful run) | 61 native actions | 17 images/crops | $0.222 successful run; $0.761936 incl. GitHub failures (token-derived) |

- [run-record.json](run-record.json)
- [verification.json](verification.json)
- [Preserved earlier evidence](preserved/20261017T000017Z-7972f15e)

## Recorded metrics

```json
{
  "status": "successful",
  "representative_run_id": "20261017T005847Z-7cbd2a64",
  "original_summary_status_preserved": "needs_review",
  "independent_audit_now_complete": true,
  "model": "claude-sonnet-5-5",
  "native_toolset": "computer_toolset_20260801",
  "agent_seconds": 116.31301,
  "benchmark_wall_seconds": 116.313339,
  "native_computer_actions": 61,
  "failed_actions": 0,
  "screenshots": 17,
  "generation_requests": 9,
  "token_count_requests": 9,
  "api_requests": 18,
  "api_retries": 0,
  "errors": 0,
  "cost_usd_successful_run": "0.222000",
  "total_github_cost_usd_including_failures": "0.761936",
  "cost_kind": "Provider usage \u00d7 verified public standard token rates; no invoice verification",
  "prior_runs": [
    {
      "run_id": "20261017T000017Z-7972f15e",
      "task": "Wikipedia smoke test",
      "original_status": "success",
      "agent_seconds": 29.558108,
      "computer_actions": 14,
      "screenshots": 4,
      "api_cost_usd": "0.077040",
      "max_tokens": 1024,
      "max_seconds": 300,
      "final_answer_present": true
    },
    {
      "run_id": "20261017T001240Z-00ae9af7",
      "task": "GitHub issues benchmark",
      "original_status": "incomplete_max_tokens",
      "agent_seconds": 63.311159,
      "computer_actions": 28,
      "screenshots": 9,
      "api_cost_usd": "0.120910",
      "max_tokens": 1024,
      "max_seconds": 300,
      "final_answer_present": false
    },
    {
      "run_id": "20261017T004821Z-eba39479",
      "task": "GitHub issues benchmark",
      "original_status": "budget_limit",
      "agent_seconds": 167.296774,
      "computer_actions": 68,
      "screenshots": 16,
      "api_cost_usd": "0.419026",
      "max_tokens": 4096,
      "max_seconds": 300,
      "final_answer_present": false
    },
    {
      "run_id": "20261017T005847Z-7cbd2a64",
      "task": "GitHub issues benchmark",
      "original_status": "needs_review",
      "agent_seconds": 116.31301,
      "computer_actions": 61,
      "screenshots": 17,
      "api_cost_usd": "0.222000",
      "max_tokens": 4096,
      "max_seconds": 300,
      "final_answer_present": true
    }
  ],
  "no_new_run_submitted_by_this_audit": true,
  "original_response_file": "preserved/20261017T005847Z-7cbd2a64/final-answer.txt",
  "verification_file": "verification.json"
}
```


Complete comparison (not included in this scoped archive; private original retained) · Methodology (not included in this scoped archive; private original retained)
