# TinyFish: Form

Verified outcome: **partially successful**. Accuracy: 5 confirmed / 10; 2 unverified. Time: 37.03 seconds from local submission to observed terminal state, including service startup/polling where applicable.

Provider/harness status: `COMPLETED`. This is preserved separately from the verified outcome. Cost and metrics: [run record](run-record.json). No automatic benchmark restart occurred.

- [Original response](original-response.txt)
- [Exact prompt](task-prompt.txt)
- [Run record](run-record.json)
- [Independent verification](verification.json)
- [Metric/token/model audit](metrics-audit.json)
- [Configuration](configuration.json)

## Verification detail

```json
{
  "graded_at_utc": "2026-10-17T18:57:08.860390+00:00",
  "grader": "Codex evidence audit, separate from evaluated agent",
  "verification_data_sent_to_agent": false,
  "outcome": "partially_successful",
  "correct_checks_confirmed": 5,
  "total_checks": 10,
  "correct_fields_confirmed": [
    "firstName",
    "lastName",
    "email",
    "phone",
    "company"
  ],
  "incorrect_fields_confirmed": [
    "jobTitle",
    "country",
    "contactMethod"
  ],
  "unverified_fields": [
    "message",
    "newsletter"
  ],
  "submission_observation": "No submission action appears in the captured seven-step trace; lower final status not visible in last screenshot.",
  "false_completion_claim": true,
  "claim": "The original structured final answer says Form Filled Successfully and reports values for controls still visibly blank.",
  "evidence": "screenshots/screenshot-005.jpg: job title empty, country Select a country, contact radios unselected; provider-run.json steps stop after five text entries and report incomplete form.",
  "scoring_note": "Report five confirmed correct fields, three confirmed incorrect fields and two unverified; do not infer 10/10 from the final response. Message ambiguity is separate from the visible omissions."
}
```

## Media

- screenshots/screenshot-005.jpg (local source; see source manifest)
- screenshots/screenshot-004.jpg (local source; see source manifest)
- screenshots/screenshot-000.jpg (local source; see source manifest)
- screenshots/screenshot-001.jpg (local source; see source manifest)
- screenshots/screenshot-003.jpg (local source; see source manifest)
- screenshots/screenshot-002.jpg (local source; see source manifest)
