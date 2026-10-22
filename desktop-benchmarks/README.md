# Desktop computer use benchmark

Five synthetic desktop tasks compare Claude Computer Use and OpenAI's native Responses computer tool. Four additional Sai task slots document an authorization blocker. Earlier browser benchmarks are separate; UI-TARS is outside this desktop batch.

Read [RESULTS.md](RESULTS.md) for each attempt, [COMPARISON.md](COMPARISON.md) for matched outcomes, [COST-COMPARISON.md](COST-COMPARISON.md) for spending, and [ARTICLE-READY.md](ARTICLE-READY.md) for the desktop findings section. The machine-readable final audit is logs/final-evaluations.json. Historical pre-authorization status files remain as evidence of earlier blockers; the final audit supersedes them.

## Tasks and provenance

The original CSV prompt, fixtures and five requirements are unchanged. Claude's earlier 4/5 CSV attempt remains its evaluation. Tasks 2–5 were reconstructed from the user's stated objectives under explicit authorization, then frozen identically for every agent: 20-file organization with eight PDF renames; Writer editing/formatting; four metrics from 30 sales rows; and correct-document selection with a synthetic interruption. These are not claimed to reproduce unavailable historical fixtures exactly. See [TASKS.md](TASKS.md) for full prompts, hashes, rubrics and limitations.

## Execution environment

The actual runs use an existing Apple M1 host and local Colima Linux desktop. Containers have no network, no host mounts and no credentials. Xvfb is 1024×768; applications are LibreOffice 7.4.7.2, Openbox and, for added tasks, PCManFM/Zenity. The original image is desktop-csv-benchmark:2026-10-21. A derivative, desktop-additional-benchmark:2026-10-21, adds the required desktop applications through scripts/Dockerfile.additional. The original signed UI-TARS application and Hugging Face endpoint were not operated.

Python 3.12 runs the harness. Fixture preparation and independent document checks require python-docx, Pillow and reportlab; these were resolved from the Codex bundled runtime for this experiment. Document rendering uses the bundled renderer and LibreOffice. Existing Docker images and their provenance are recorded in preflight/. The base image is a pre-existing local dependency, not downloaded from a public registry under that custom name.

## Native tools and reproduction

scripts/run_native.py executes provider-returned actions, preserves traces, and never decides task edits. scripts/run_additional.py stages immutable inputs and chooses the initial blank application/file manager. scripts/run_remaining_batch.py is a one-attempt sequential queue with a persistent start marker. It does not retry or restart failed benchmarks automatically. Original Responses/API envelopes and errors are retained for audit.

The model chooses all task GUI actions. Source preparation and grading scripts must never be used to create a substitute result in an agent output directory. Expected outputs remain outside every container. The CSV rubric stays in scripts/verify_result.py; added artifact checks and manual GUI observations are in verification/.

For an explicitly authorized new experiment, configure credentials through environment variables ANTHROPIC_API_KEY and OPENAI_API_KEY or an owner-only protected credential mechanism. Never place values in tracked files, terminal output, screenshots or chat. This batch's user-authorized recovery from previous chat used an ephemeral RAM-only broker; that is not a recommendation to keep using exposed keys. Rotate exposed credentials after testing. No key values are included in this package.

Run existing offline checks without provider calls:

```sh
python3 scripts/check_verifier.py
python3 verification/check_harness.py
python3 verification/check_additional.py
python3 scripts/verify_result.py outputs/openai --observations logs/openai/gui-observations.json
```

The document checker needs the dependency-equipped Python runtime. Completed runs and start markers intentionally refuse restart. Reproduction requires a separate, explicitly authorized experiment directory; do not remove markers or overwrite this evidence to repeat a result. The original $7 cap is cumulative across historical and new attempts and does not reset with a new process or chat.

## Evidence and interpretation

logs/ retains every attempt's provider responses, errors, usage and native actions. screenshots/ contains the desktop states. outputs/ contains actual collected artifacts, including incomplete work. expected/ contains grader-only truth. verification/ contains read-only checks and visual renders. preflight/batch-audit/ documents repairs, authorization/access checks and historical report snapshots.

A final model message saying done is not proof. PASS requires all five requirements, including required GUI verification. Correct files with unfinished workflows remain PARTIAL. Setup/access blocks are not zero-accuracy model failures. Timings, raw action counts, caching behavior and adapter changes carry limitations detailed in [METHODOLOGY.md](METHODOLOGY.md). This small batch does not establish universal superiority or production reliability.

The public preparation copy may omit account/resource metadata while preserving all local evidence. Publishing status and commit information are in preflight/batch-audit/publication.json when available. No new GitHub repository should be created or unrelated history overwritten to publish these results.
