# Reproducing and inspecting the experiments

## Inspect without making provider calls

Python 3.12 was used. Offline CSV verification uses the standard library. DOCX grading needs python-docx; optional fixture/render tooling also uses Pillow/reportlab and LibreOffice. Install dependencies in a separate environment, for example:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install python-docx Pillow reportlab
python verification/scripts/validate_package.py
python desktop-benchmarks/scripts/check_verifier.py
python desktop-benchmarks/verification/check_harness.py
python desktop-benchmarks/verification/check_additional.py
python desktop-benchmarks/scripts/verify_result.py desktop-benchmarks/outputs/openai --observations desktop-benchmarks/logs/openai/gui-observations.json
```

These commands do not call providers or perform agent task work. They inspect saved artifacts or disposable test cases. PASS means all task-specific requirements, including cited GUI workflow evidence. PARTIAL preserves correct subsets; NOT TESTED has no artificial zero score. Read each saved independent-verification.json and its cited screenshots; file parsing alone cannot verify GUI reopening.

For added DOCX/file tasks, for example:

```sh
python desktop-benchmarks/verification/verify_additional.py 4 desktop-benchmarks/outputs/openai/task-4 --observations desktop-benchmarks/logs/openai/task-4/gui-observations.json
```

Do not run the historical final_audit.py to overwrite reports in this archive. Its old 43-file integrity manifest describes the preserved source set, while the public manifest accounts for publication redactions and omitted documentation. The public package validator verifies current bytes and grades without rewriting them.

## A new, explicitly authorized agent experiment

This publication task did not run any of the commands below. Use a **separate experiment directory** and a fresh budget. Do not clear historical start markers, replace outputs, regenerate frozen fixtures or reuse this archive as a writable run directory.

Supply your own keys outside source control through OPENAI_API_KEY and ANTHROPIC_API_KEY. Managed providers use TINYFISH_API_KEY and SAI_API_KEY (or the recorded supported alias); confirm the retained adapter’s environment lookup before any separately approved execution. Do not put values into commands, logs, screenshots, commits or the shared task desktop. No provider key is required to read this repository.

Actual desktop execution used macOS/Apple M1 as host and an existing Colima Docker context named colima-claude-benchmark. Models interacted with Linux/Xvfb/Openbox at 1024×768. LibreOffice 7.4.7.2 Calc/Writer, PCManFM and Zenity are required for the added suite. Containers were network-isolated and credential-free. Other host operating systems were not tested. Windows/macOS-native application behavior cannot be inferred from these Linux runs.

The custom desktop-csv-benchmark:2026-10-21 base image was pre-existing locally and is not a public registry dependency. Dockerfile.additional is a derivative, not a complete portable base build. Match its recorded software, layout and native action translator before executing a new trial. Do not claim equivalent conditions from a different image without disclosing them. Historical adapters require manual setup; installation and full execution have not been verified on a fresh machine.

Copy the **already frozen inputs** from inputs/ and preserve their hashes. Keep expected/ outside the task container. Source preparation scripts are provenance, not instructions to recreate successful outputs. In a separately configured run directory, the historical interfaces are:

```sh
# Requires a new authorized budget, working custom image/context and reviewed pause/start guards.
python scripts/run_native.py openai --seconds 600 --budget YOUR_APPROVED_LOCAL_CAP
python scripts/run_additional.py claude 4 --budget YOUR_APPROVED_LOCAL_CAP
```

They are interface examples, not one-command reproduction. The retained completion pause and submitted-once guards intentionally prevent rerunning this published evidence. In a new harness configuration review cumulative reservations, hard deadlines, toolset pairing, native call ordering and modifier translation **offline** before paid execution. Every model decision must remain native; the harness may only set up, execute requested actions, capture observations and verify afterward.

## Browser trials

Choose one [exact task and prompt variant](browser-benchmarks/README.md), provider and cohort. Browser orchestration sources are retained under the relevant evidence audit/orchestration directory; some shared outside-scope wrappers were not republished. They are archival sources, not a verified installable SDK package. Configure a managed TinyFish browser, Sai account with permitted computer access, or the recorded native Claude/OpenAI environment using that provider’s official setup. Paid access and current model availability are external prerequisites. A new conversation may not reset a managed desktop.

Use fresh sessions where supported; retain failures and explicitly label any repair attempt. Apply the actual task deadline and an approved cumulative spend cap. Independently capture fresh website reference state near each new run without giving it to the evaluated agent. Do not use GitHub’s API for the issue task. Do not log in or modify the tested repository.

The recovered synthetic HTML is [here](browser-benchmarks/fixtures/index.html). A local preview can use `python -m http.server --directory browser-benchmarks/fixtures 8000`. Managed agents may need a separately hosted copy. Any new hosting URL substitution must be disclosed; preserve original historical prompt bytes. The form’s message ambiguity must remain visible if comparing against this strict rubric.

UI-TARS is archived evidence, not an instruction to restart the original endpoint. Source patch validation is retained, but no guaranteed launch/control recipe or counterfactual successful run is claimed. Sai’s tested direct-control route returned HTTP 403; do not bypass provider authorization, assume frontend access solves API restrictions, or treat unavailable access as a task failure.

After any separately approved new experiment, stop the agent, independently inspect artifacts and screenshots, preserve original text/usage/errors, stop billable infrastructure and verify shutdown. Keep new results outside this historical publication.

## TinyFish form follow-up evidence

The [22 October follow-up](browser-benchmarks/reruns/tinyfish-form-2026-10-22/README.md) contains three completed runs, actual submission payloads, unchanged prompts, original responses, all returned images/HTML, independent observations and value-free cost deltas. The [executed source archive](browser-benchmarks/reruns/tinyfish-form-2026-10-22/execution-source/source-hashes.json) records exact source provenance; it is not standalone without the private original helper. Use the offline grader below, which reads already saved observations and HTML and makes no requests:

```sh
python3 browser-benchmarks/reruns/tinyfish-form-2026-10-22/verify_followup.py
```

No rerun is needed to inspect these results. Provider access and new spending authorization would be needed for further paid execution.

## Clarified form configuration

[Six completed/stopped agent attempts](browser-benchmarks/reruns/clarified-form-2026-10-22/README.md), their exact shared prompt, all returned images/HTML, original responses, native token usage and infrastructure errors are separately retained. Regrade saved independent observations and integrity/cost checks offline:

```sh
python3 browser-benchmarks/reruns/clarified-form-2026-10-22/verify_clarified.py
```

The executed-source archive records private original-adapter dependencies and is not presented as a standalone turnkey runner. Inspection/regrading makes no provider requests and requires no keys. Further paid execution needs its own authorization.
