# Desktop benchmark methodology

## Task provenance and scope

This package contains five desktop tasks for Claude and OpenAI, plus four additional Sai eligibility records. The original CSV task, data, expected CSV and five-point rubric are unchanged. Claude's existing CSV repair attempt counts as its CSV evaluation; it was not repeated to improve the score. Its earlier paid protocol failure remains a separate attempt and cost.

The user later authorized reconstructing four additional tasks from stated objectives: organize 20 files and rename eight PDFs; edit and format a document; report four metrics from 30 sales records; recover from an interruption while selecting and editing the correct document. Complete historical specifications were not recovered from the accessible project/conversation. The added prompts, synthetic data and five-point rubrics are explicitly reconstructed, not claimed to match unknown earlier files exactly. TASKS.md and inputs/additional/tasks.json freeze the same versions for every agent. Expected values and hashes remain grader-only and are never staged in agent desktops.

## Native tools and role separation

Claude uses Anthropic Messages with computer_toolset_20260801. Its tool results carry the paired computer toolset name. OpenAI uses Responses with type computer, executes returned computer_call actions in order, and returns computer_call_output screenshots paired by call_id and previous_response_id. Provider-returned model aliases are recorded; no immutable model snapshot is inferred when only an alias is exposed.

The model chooses every task action. The harness translates requested keyboard/mouse actions, captures screenshots, stages original inputs before the timer, manages isolated applications, and retrieves artifacts only after the agent loop has stopped. It never chooses an edit, supplies calculated answers, completes a stalled Open dialog, rewrites an agent result, or substitutes scripted task completion. GUI typing uses an isolated clipboard. Spreadsheet formulas are allowed through the Calc GUI for the added calculation task; scripts and macros are prohibited. Source- and expected-file preparation and read-only post-run verification use code outside the agent environment.

Official references: [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use), [OpenAI token counting](https://developers.openai.com/api/docs/guides/token-counting), [Anthropic computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), and [Sai control API](https://platform.simular.ai/documentation/api-reference/control). Archived documentation is in docs/.

## Environment and starting state

Host: Apple M1 Mac, 8 GB RAM. Execution: existing local Colima profile, 2 CPUs and 3 GB VM memory. Each attempt uses its own Linux container with 2 CPU/2 GB limits, Xvfb 1024×768, Openbox, dropped capabilities, no host mounts and no network. No API credentials enter the container. LibreOffice 7.4.7.2 performs spreadsheet/document work.

The original CSV image is desktop-csv-benchmark:2026-10-21. Additional tasks use desktop-additional-benchmark:2026-10-21, a derivative adding LibreOffice Writer, PCManFM and Zenity. Both agents use the same added image. The initial application is blank Calc, blank Writer, or PCManFM at Inbox; no task document is pre-opened. Existing blank Calc can remain behind another initial application. In task 5 the same single synthetic modal warning is present at the initial screenshot. Although the launcher requested a Writer recovery start, the actual initial screenshots show blank Calc behind the modal for both agents and the retry; those screenshots describe the observed starting state. This tests dismissal and continuation, not recovery from a real crash or data loss.

Original macOS applications, UI-TARS copies and Hugging Face configuration/state are outside this batch and were not operated. Earlier browser evidence and success counts remain separate. Fixture rendering and offline review sometimes overlapped remote-agent runs on the host; contention was not measured. These are single observations rather than controlled speed trials.

## Evidence and scoring

After the agent loop stops, a read-only final screenshot and the benchmark directory are collected before the container is stopped. Saved provider responses, native action events, token usage, interim/final text, errors, input hashes and output files are retained per attempt. An original response claiming completion is never sufficient proof.

The original CSV verifier checks parsed values, row order, both corrections and a byte-identical original. New DOCX checks read paragraphs, table cells and heading styles; source documents must remain byte-identical. The sales grader independently computes the four expected metrics. File organization checks the exact 20 destination paths, eight names and unchanged binary hashes, excluding application metadata/lock files. GUI workflow checks require post-run visual review of cited screenshots and action traces. No reviewer controls the live task desktop to finish a missing step.

PASS requires all five task-specific checks. PARTIAL records completed requirements with an unfinished task. FAIL identifies a valid attempt without meaningful required work. NOT TESTED/BLOCKED carries no zero score when access or setup prevents submission. Infrastructure interruptions are separately described even when some artifact requirements earned points. A 4/5 checklist score is not a general 80% accuracy estimate. Provisional artifact-verification.json files deliberately leave GUI checks unverified; independent-verification.json holds the final audit.

## Timing and actions

Each attempt has a maximum 600-second agent execution allowance. Setup, artifact collection and independent verification are excluded; initial screenshot/count overhead is included by the runner's timer. A watchdog and per-action/request checks stop execution. New runs use the stricter elapsed value from wall and monotonic clocks and a temporary process-scoped idle-sleep inhibitor.

The historical Claude CSV attempt recorded 183.18 stopwatch seconds and a 397.54-second UTC event span. Filtered Mac power logs show sleep/wake events during the stalled request and strongly support host sleep as the cause of most of the discrepancy. Exact reconciliation is not established. Both values remain unchanged; exclude this attempt from speed claims.

Counts are raw provider-native actions, including model-requested screenshots/waits. OpenAI adds harness screenshots after computer calls; those are images, not extra model actions. A native drag can translate to multiple low-level mouse operations. Tool bundling and screenshot policies differ, so raw counts are not a normalized efficiency ranking. Returned model aliases and timing methods are available in the traces.

## Repairs and attempt policy

Claude CSV attempt 1 failed because the adapter omitted toolset_name on tool results; one explicitly announced repair attempt followed and remains 4/5. The first added Claude organization setup failed before any generation because the staging directory was not ready; one announced repair created it explicitly, then a separate retry ran. That retry later stopped on a drag executor error. No third attempt was made and its exact low-level cause was not captured in the old error event.

OpenAI CSV and organization ran before a click-modifier adapter fix: optional SHIFT/CTRL click modifiers were being dropped. OpenAI recovered in organization using other graphical actions, and its outputs/workflow were verified, but the defect confounds its action count and duration. Subsequent runs preserve supported click modifiers and reject unsupported modified drags rather than silently discarding them. New executor errors also retain their sanitized category. On resume, the completed OpenAI reporting and recovery runs were verified rather than repeated. Claude recovery attempt 1 had produced the correct file but hit a local $1 reservation guard before the model reviewed its reopened image. One explicitly announced repair raised that task’s local allowance to $1.75 within the unchanged cumulative $7 cap; a separate attempt reused the frozen fixtures and existing image. Its prior stopped container could not resume a live GUI conversation. Both attempts and their full costs remain visible. No completed benchmark was repeated to improve a score. Offline protocol checks simulate envelopes/guards only; they are not provider runs or capability results.

## Budget, credentials and access

The original $7 total cap includes all historical and new attempts. Before each generation, token counting and a conservative reservation check the local run cap and cumulative recorded costs/reservations. Uncertain generation charges remain reserved. The assistant made no purchases or top-ups and provisioned no paid GPUs, subscriptions or paid infrastructure. The user’s external credit top-up did not reset the $7 cap. Per-task caps can use released allowance from earlier runs; the initial task 4 and task 5 attempts had matched caps of $1.25 and $1.00 for both agents. Claude’s labeled recovery retry used $1.75; all remain under the same cumulative $7 limit. This allocation difference prevents treating the recovery comparison as matched first-attempt reliability.

Estimates use provider-returned input/output/cache token usage and recorded Standard prices. OpenAI returned automatic cache reads; Claude's recorded defaults did not explicitly enable caching. Cost differences therefore include provider tokenization and caching behavior. Estimates are not invoices; reconciliation, taxes, electricity and labor are not measured. Cost per verified PASS includes unsuccessful attempts for that provider and is descriptive of this batch only.

Execution was initially paused because replacement keys were not discoverable. The user then explicitly authorized retrieving and using earlier exposed keys and rotating them after testing. Keys were recovered without printing their values and supplied by a mode-0600 Unix socket broker holding them in RAM. They were not put into source, logs, screenshots, containers or commits. This authorization does not mean they were rotated. The broker must be stopped after the batch and the owner should rotate exposed credentials afterward.

Sai's authorized recheck returned HTTP 403 forbidden, Not authorized for this machine. The tested direct-control route could not stage/retrieve desktop fixtures, so no added Sai task was submitted. This does not establish that every Sai API route or desktop feature is unavailable; it is an observed access restriction. No bypass, lease takeover or account change was attempted.

## Reproducibility checks

The original grader has six offline failure-case checks; the native adapter has six offline plumbing/guard checks; the added graders have nine disposable artifact checks. Test cases never populate agent output directories. Fixtures and generated DOCX artifacts are rendered for visual audit without altering agent files. Final secret scanning and integrity manifests preserve unsuccessful attempts and make evidence changes detectable. See verification/README.md and the per-run audit files.
