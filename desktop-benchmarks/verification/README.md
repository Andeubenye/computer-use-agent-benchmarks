# Independent verification

The original CSV rubric is unchanged in scripts/verify_result.py. The original fixture and expected file are inputs/orders_to_fix.csv and expected/orders_corrected.csv. Each GUI observation cites actual screenshots reviewed after its attempt stopped; the reviewer never finishes a task step.

Additional task prompts, fixture hashes and rubrics are in inputs/additional/tasks.json. verification/verify_additional.py checks exact file destinations/hashes, DOCX paragraphs/styles/tables, independently recomputed sales metrics, preserved originals and cited GUI evidence. It never edits an output. Expected files are grader-only. Provisional artifact audits do not imply workflow completion.

Offline commands:

```sh
python3 scripts/check_verifier.py
python3 verification/check_harness.py
python3 verification/check_additional.py
```

Use a Python runtime with python-docx for the added grader checks. These tests use disposable temporary files or simulated API envelopes, make no provider requests, and are not benchmark runs. Final per-run results are independent-verification.json; source screenshot observations are gui-observations.json. Rendered output pages are independent visual evidence and never shown to the task model.
