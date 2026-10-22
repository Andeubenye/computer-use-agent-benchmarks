# OpenAI Computer Use: Wikipedia

Verified outcome: **successful**. Accuracy: 15/15. Time: 54.70 seconds from local submission to observed terminal state, including service startup/polling where applicable.

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
  "graded_at_utc": "2026-10-17T18:30:01.964931+00:00",
  "grader": "Codex evidence audit, separate from evaluated agent",
  "verification_data_sent_to_agent": false,
  "outcome": "successful",
  "correct_checks": 15,
  "total_checks": 15,
  "order_correct": true,
  "reference": "verification/wikipedia-reference.json",
  "evidence": "Original response matches every reference field; native computer action/screenshot trace records article navigation. Only the computer tool was exposed; no DOM or HTTP tool."
}
```

## Media

- native-evidence/screenshots/initial.png (local source; see source manifest)
- native-evidence/screenshots/step_007.png (local source; see source manifest)
- native-evidence/screenshots/step_006.png (local source; see source manifest)
- native-evidence/screenshots/step_004.png (local source; see source manifest)
- native-evidence/screenshots/step_005.png (local source; see source manifest)
- native-evidence/screenshots/step_001.png (local source; see source manifest)
- native-evidence/screenshots/step_002.png (local source; see source manifest)
- native-evidence/screenshots/step_003.png (local source; see source manifest)
- native-evidence/screenshots/independent-final.png (local source; see source manifest)
