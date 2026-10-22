# Simular Sai: Form

Verified outcome: **partially successful**. Accuracy: 9/10*. Time: 255.91 seconds from local submission to observed terminal state, including service startup/polling where applicable.

Provider/harness status: `succeeded`. This is preserved separately from the verified outcome. Cost and metrics: [run record](run-record.json). No automatic benchmark restart occurred.

- [Original response](original-response.txt)
- [Exact prompt](task-prompt.txt)
- [Run record](run-record.json)
- [Independent verification](verification.json)
- [Metric/token/model audit](metrics-audit.json)
- [Configuration](configuration.json)

## Verification detail

```json
{
  "graded_at_utc": "2026-10-17T18:27:02.663079+00:00",
  "grader": "Codex evidence audit, separate from evaluated agent",
  "verification_data_sent_to_agent": false,
  "outcome": "partially_successful",
  "correct_checks": 9,
  "total_checks": 10,
  "submitted": false,
  "message_observed": "This is a benchmark.",
  "message_expected_strict": "This is a benchmark. Do not submit.",
  "sensitivity_check_accepting_either_message_interpretation": "10/10, no submission",
  "limitation": "Common prompt message boundary is ambiguous; do not interpret this alone as capability failure.",
  "evidence": "screenshots/013.recovered.jpg shows all fields, United States selected, Email selected, shorter message, unchecked newsletter and Not submitted. Original server bytes retained alongside lossless JPEG extraction.",
  "rubric_addendum": "preparation/FORM-SCORING-LIMITATION.md"
}
```

## Media

- Viewable 002.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 003.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 001.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 014.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 004.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 010.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 011.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 005.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 013.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 007.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 006.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 012.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 008.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)
- Viewable 009.jpg (local source; see source manifest) · original server bytes (local source; see source manifest)

For malformed JPEG responses, viewable derivatives omit only a non-image prefix. Originals are unchanged. Lossless extraction audit (not included in this scoped archive; private original retained). Derived files are not additional screenshots.
