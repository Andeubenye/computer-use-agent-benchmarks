# OpenAI Computer Use

The original response remains untouched. All five issue identities, titles, links and ordering are correct. Relative dates do not meet the common calendar rubric, although the original prompt explicitly allowed them. No new OpenAI inference request was sent.

| Agent | Model/configuration | Result | Verified required fields | Recorded time | Actions (different units) | Visual evidence | Cost and basis |
|---|---|---|---|---|---|---|---|
| OpenAI Computer Use | gpt-6.1-sol / computer | Partially successful under calendar rubric | 15/20; five correct, ordered; relative dates | 97.55 s | 27 native actions | 11 images | $0.0731802 token estimate |

- [run-record.json](run-record.json)
- [verification.json](verification.json)
- [original-response.txt](original-response.txt)
- [Preserved earlier evidence](preserved)

## Recorded metrics

```json
{
  "run_id": "openai_run_1",
  "status": "partially_successful",
  "model": "gpt-6.1-sol",
  "native_tool": "computer",
  "native_computer_call_observed": true,
  "wall_clock_seconds": 97.546,
  "api_request_attempts": 11,
  "computer_tool_calls": 10,
  "computer_actions": 27,
  "retries": 0,
  "errors": [],
  "issue_fields_correct": 15,
  "issue_fields_total": 20,
  "issue_identity_and_order_correct": true,
  "calendar_dates_returned": false,
  "prompt_explicitly_permitted_relative_dates": true,
  "model_screenshot_count": 11,
  "cost_estimate_usd": 0.0731802,
  "cost_kind": "Token-derived model estimate; arithmetic and rate source checked, invoice not checked",
  "no_new_run_submitted_by_this_audit": true,
  "original_response_file": "original-response.txt"
}
```


Complete comparison (not included in this scoped archive; private original retained) · Methodology (not included in this scoped archive; private original retained)
