# TinyFish Agent API

Recovered the completed historical run without launching another. All twenty issue fields and ordering pass. Model version, internal retry count and charge were not exposed.

| Agent | Model/configuration | Result | Verified required fields | Recorded time | Actions (different units) | Visual evidence | Cost and basis |
|---|---|---|---|---|---|---|---|
| TinyFish Agent API | Revision not exposed | Successful | 20/20; five correct, ordered | 198.0 s | 8 reported steps | 7 images | Unavailable |

- [run-record.json](run-record.json)
- [verification.json](verification.json)
- [original-response.txt](original-response.txt)
- [provider-run.json](provider-run.json)

## Recorded metrics

```json
{
  "status": "successful",
  "run_id": "id-6b46a07ff490",
  "existing_run_retrieved_not_repeated": true,
  "model_version": null,
  "model_version_limitation": "Exact model revision not exposed by run endpoint",
  "agent_duration_seconds": 198.0,
  "request_to_finish_seconds": 201.0,
  "duration_method": "Provider started_at to finished_at; created_at-to-finish also supplied",
  "provider_reported_steps": 8,
  "raw_step_records": 9,
  "screenshots_retrieved": 7,
  "api_run_error": null,
  "failed_step_records": 0,
  "internal_retries": null,
  "automatic_benchmark_restarts_by_this_audit": 0,
  "cost_usd": null,
  "cost_limitation": "Run endpoint does not expose cost; no invoice retrieved",
  "fresh_profile": true,
  "browser_configuration": {
    "proxy_enabled": true,
    "proxy_country_code": "US"
  },
  "original_response_file": "original-response.txt",
  "verification_file": "verification.json"
}
```


Complete comparison (not included in this scoped archive; private original retained) · Methodology (not included in this scoped archive; private original retained)
