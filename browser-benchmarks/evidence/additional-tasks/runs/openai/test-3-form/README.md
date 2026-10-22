# OpenAI Computer Use: Form

Verified outcome: **partially successful**. Accuracy: 9/10*. Time: 34.63 seconds from local submission to observed terminal state, including service startup/polling where applicable.

Provider/harness status: `completed_unverified`. This is preserved separately from the verified outcome. Cost and metrics: [run record](run-record.json). No automatic benchmark restart occurred.

- [Original response](original-response.txt)
- [Exact prompt](task-prompt.txt)
- [Run record](run-record.json)
- [Independent verification](verification.json)
- [Metric/token/model audit](metrics-audit.json)
- [Configuration](configuration.json)

## Verification detail

```json
{
  "graded_at_utc": "2026-10-17T18:30:01.965052+00:00",
  "grader": "Codex evidence audit, separate from evaluated agent",
  "verification_data_sent_to_agent": false,
  "outcome": "partially_successful",
  "correct_checks": 9,
  "total_checks": 10,
  "message_observed": "This is a benchmark.",
  "message_expected_strict": "This is a benchmark. Do not submit.",
  "submitted": false,
  "all_other_fields_verified": true,
  "sensitivity_check_accepting_either_message_interpretation": "10/10; no submission",
  "limitation": "Ambiguous message boundary in identical prompt, not clean capability failure.",
  "evidence": "native-evidence/independent-fixture-state.json captured by grader after model execution, never sent to the model; screenshots independently corroborate.",
  "rubric_addendum": "preparation/FORM-SCORING-LIMITATION.md"
}
```

## Media

- native-evidence/screenshots/initial.png (local source; see source manifest)
- native-evidence/screenshots/step_004.png (local source; see source manifest)
- native-evidence/screenshots/step_005.png (local source; see source manifest)
- native-evidence/screenshots/step_001.png (local source; see source manifest)
- native-evidence/screenshots/step_002.png (local source; see source manifest)
- native-evidence/screenshots/step_003.png (local source; see source manifest)
- native-evidence/screenshots/independent-final.png (local source; see source manifest)
