# Preregistered scoring

Use one attempt per task/configuration. Provider completion is not independently verified success. No answer is not an answer with zero factual errors: record completion separately from accuracy. Mark unavailable observations explicitly. No aggregate reliability rate is justified by one attempt per task. The existing three Claude GitHub attempts remain visible and are not merged into a single first-attempt success.

## Test 2: Wikipedia, 15 factual checks

For each of the five specified people: one check for the full birth date, one for birthplace, and one for the matching English Wikipedia article URL. Accept equivalent date formats and unambiguous geographic aliases; a birthplace must include the named locality rather than only a country. Report omitted locality detail separately. Verify website visits from execution evidence; memorized facts alone do not establish computer-use completion. A different Margaret Hamilton is incorrect.

## Test 3: form, 10 state checks plus submission constraint

Ten checks cover the ten fields in FORM-RECONSTRUCTION.md, including the unchecked newsletter. Normalize punctuation in the fictional phone number without changing its digits; compare text exactly otherwise. Verify the visible final form or an independently collected post-run state snapshot. An agent's final claim alone is insufficient. Submission attempts fail the non-submission constraint even when intercepted by the fixture. Full success requires all ten values correct and no submission attempt. If final state is unavailable, mark verification unavailable rather than infer success.

## Test 4: GitHub enhancements, up to 20 field checks

Four checks per expected issue: number, title, canonical URL, exact calendar updated date/timestamp. Verify membership and descending update order separately. If fewer than five qualifying issues exist, use four checks per actual issue and require the correct count. Relative dates earn no exact-date point; preserve them in the original output. Confirm open status and enhancement label. Verify through GitHub's website, not its API. Save a timestamped reference near each run because issue order changes over time; do not feed it to agents. A snapshot captured during preparation is not automatically the reference for a later run.

## Test 5: popup, four workflow checks

1. Blocking modal dismissed through an intended dismissal control (Escape also allowed).
2. Standard review selected and Checklist reviewed checked.
3. Step two reached through Continue to step 2, with no disabled-control bypass or source inspection.
4. Correct visible confirmation code returned.

Use execution logs, screenshots, and browser-local inspection records where retrievable. Correct code without evidence of the required path does not establish full workflow success. Keep the confirmation-code reference outside agent inputs.

## Outcome labels and measurements

- Successful: independently verified full result and all mandatory workflow constraints.
- Partially successful: a genuine attempt with a verifiable subset or incomplete required precision.
- Failed: submitted run with error, deadline, prohibited workflow, or no usable completion; retain any partial observations.
- Blocked: known prerequisite prevents task submission.
- Not run: planned but never submitted, including pending spending authorization.

Record provider steps, browser tool calls, native actions and screenshots in their original units. Never rank providers by treating these units as equivalent. Report task-submission wall time, provider execution time, queue/setup time and cancellation acknowledgement separately where available. Cost tables distinguish provider billed usage, promotional-credit depletion, model-token estimates, invoices and unmeasured costs.
