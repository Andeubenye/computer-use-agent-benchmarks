# Methodology

Evaluation date: October 21, 2026, Africa/Lagos (UTC+01:00). Machine-readable evidence retains UTC timestamps; application logs use WAT.

## Configuration held fixed

The evaluator used the existing patched UI-TARS Desktop development application through Electron, not the broken Desktop packaged testing copy. Source: official v0.2.4 tag, commit `0ee87301a6db754c5f67909e5fbbcf05233abad9`, checkout `work/UI-TARS-desktop-v0.2.4-2026-10-20`. The upstream internal package version was not relabeled. Existing main/preload bundles and the renderer-only development server were reused; no rebuild, reinstall, source change, model switch or new permission grant was performed for this suite.

Host: Apple M1, 8 GB RAM, macOS 15.4.1. Electron: 34.1.1. The 7B model runs remotely, not in the Mac's RAM. The saved provider is Hugging Face for UI-TARS-1.5, model `ByteDance-Seed/UI-TARS-1.5-7B`, Chat Completions, Local Browser Operator, validated output limit 2048 and user-reported model context 32768. Maximum loop count is 100 and the loop interval is one second. The Chat Completions implementation supplies a 30-second request timeout. The evaluation did not change that timeout or retry behavior.

Earlier dashboard evidence exposed revision `683d002dd99d8f95104d31e70391a39348857f4e`, container `vllm/vllm-openai:v0.29.0`, Nvidia L40S and $1.80/hour. Those are previously observed configuration values, not a fresh deployment audit. A new authenticated, read-only model-list request returned HTTP 200 and the expected model. Actual current hardware changes, provider-side latency causes and invoice costs were not measured. The endpoint was not resumed, restarted, paused, reconfigured or redeployed by this suite.

Accessibility and Screen Recording were already authorized for the exact development Electron binary. Chrome was available. Existing Local Browser code denies downloads and launches a temporary Chrome with flags including `--no-sandbox` and `--disable-web-security`. These flags were not changed. Only the public benchmark sites and the browser's built-in Google starting page were used; no personal browser profile or account was used by the agent. No additional system or browser permission was granted.

## Protocol

The five new prompts were copied exactly from the user's October 21 attachment, omitting only the surrounding quotation marks used to delimit each prompt. `tasks.json` and each `prompt.txt` retain the text and SHA-256 digest. This is a new protocol: it changes the people, requested facts, target GitHub repository, issue count, form and recovery fixture from the older comparison. Earlier other-agent scores therefore are not directly comparable to this suite.

Each task uses one new UI-TARS conversation and a new Chrome temporary profile. Before the next task, after terminal-state verification, the harness closes only the Chrome process whose parent is this development Electron and whose command line identifies a Puppeteer temporary profile. It leaves the personal Chrome process and profiles untouched. The next run lets UI-TARS itself launch the fresh browser; the harness does not navigate it to the task site. Profile names and browser versions are recorded by the screenshot logger. Chrome observed by that logger: 155.0.8059.85, retina screenshots 2560×1600 from a 1280×800 CSS viewport.

The harness sets the exact prompt in the application's visible task field, verifies the text, and clicks Send once. Timing begins immediately before that native submission. A maximum of 600 seconds includes browser initialization, navigation, inference, retries and waits. The emergency process-identity watchdog is armed shortly before submission, so its fallback cutoff is slightly conservative; actual runs finishing earlier are unaffected. There are no automatic benchmark reruns. Same-run retries performed by UI-TARS are retained and counted separately. The suite has a conservative 55-minute execution envelope.

UI-TARS performs all task navigation, clicks, typing, scrolling and reasoning. The harness sends no corrective follow-up instructions and does not fill fields or provide answers. The public demo login credentials and synthetic form values appear only as supplied in the original task prompts. No personal account login is required. The model's own use of Google before the requested website is preserved as observed behavior.

## Evidence and independent verification

The original application log is sliced by each saved submission byte offset and the next submission or terminal run marker. Saved copies mask the existing API key and private inference hostname/URL. The full model responses, parsed action inputs, retry/error stacks and terminal status are retained. `final-response.txt` is the last original model response; it is not a harness-written substitute answer. A terminal error response that merely describes the next action is not counted as a completed answer.

The screenshot-only recorder attaches to the identified agent-owned local browser. During execution it uses only browser metadata, target attachment, screenshot capture and detach messages. It sends no navigation, input, DOM evaluation or answer-extraction commands. It records a screenshot near each observed action-count change and at termination; this does not guarantee every exact pre-action image sent to the model. Test 1 recording began after its initial actions, and its first image had an incorrect step count before a logger correction. The capture gaps and corrections are recorded in EXECUTION-LOG.md. Later tests start their recorder immediately after submission. Native UI screenshots preserve the app's final response/error state.

Only after an application terminal marker does the independent verifier inspect the final page's rendered text, URL, title and actual input/select/textarea values, and capture an additional screenshot. It refuses to inspect an active task. This read-only verification is separate from the agent and its data is never sent back to UI-TARS. It does not click, navigate, type or change page state. GitHub verification uses the website, not GitHub's API. If no issue list is returned, there are no issue identities/dates to score; the harness does not solve the task to manufacture a result.

A screenshot matching a pre-existing form default is not evidence that UI-TARS filled it. State agreement and changes actually completed are reported separately. No submission is inferred from a completion claim: the visible state, URL and complete observed action trace are checked. Network-level proof of every absent request was not measured.

## Scoring

- **PASS:** All essential success criteria verified, including website/workflow requirements.
- **PARTIAL:** Meaningful verified completion with missing, incorrect or unverifiable required information.
- **FAIL:** No meaningful completion, a critical terminal error, or timeout. Verified partial progress is still retained.
- **NOT RUN:** No prompt submitted; never counted as a model failure or zero-accuracy answer.

People research requires the five requested years and article URLs, with relevant identities and no fabrication. The new phrase “Margaret Hamilton (computer scientist)” is preserved exactly; it must not silently be replaced with a different Hamilton from an older task. The form has 14 requested state checks, including five states that can already match without changes, nine requested changes, and a no-submission gate. VS Code research requires three eligible open bug issues, descending update ordering, and four returned fields each. Login recovery requires evidence of intentional failure, recognition, successful recovery and final-state reporting. Language research requires five verified year/creator/URL sets and a structured table. The exact original success criteria remain in `preflight/user-instructions.txt`.

Task completion, partial observed progress and factual accuracy remain separate. Missing final answers do not earn fabricated factual scores. One attempt per task measures this particular Desktop/Hugging Face stack and session; it does not establish general model reliability or the cause of remote inference latency.

## Metrics and costs

Submission-to-terminal wall time is calculated from the controller timestamp and application terminal timestamp. App-reported agent-loop time is separate and may omit browser setup or callback overhead. Native action count includes logged click/type/hotkey/wait etc.; it is not directly comparable to other providers' bundled browser calls. Model invocation count is from the SDK log, not an invoice-confirmed HTTP total. Aggregate token counts come from application telemetry; input/output splits are Not measured unless explicitly exposed.

Per-request inference price, actual hosting billed to each run, invoice totals and per-token cost are **Not measured**. The previously observed hourly rate is retained as context, not converted into an asserted inference charge. No invented cost is assigned to incomplete tasks. The endpoint remains in the user's chosen state, so stopping benchmark execution is not a claim that hosting billing has stopped.
