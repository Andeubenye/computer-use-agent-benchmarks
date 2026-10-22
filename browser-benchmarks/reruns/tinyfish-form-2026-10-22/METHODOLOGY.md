# Follow-up methodology and limitations

## Frozen task and separation

Executed on 22 October 2026: exactly three additional TinyFish runs, numbered 2–4 after the original attempt. The original [prompt bytes](../../prompts/exact/test-3-form.txt) have SHA-256 `1b237d3e106992c3cdc5e1e866b19f7e2d873d04937f6cbd2d58649a67d2f155`. Each actual submission payload and retained prompt match this hash. The original [scoring rules](../../evidence/additional-tasks/preparation/SCORING.md) and [field reference](../../evidence/additional-tasks/preparation/FORM-RECONSTRUCTION.md) remain unchanged. That field specification was reconstructed before the original batch, a historical limitation already disclosed; this follow-up did not invent new values.

The existing hosted V1 form URL was reused, without redeployment or source changes. Fresh TinyFish sessions were requested through separate asynchronous runs, use_profile=false, use_vault=false, lite browser profile, proxy disabled. Each returned profile_attached=false; the initial visible controls were blank/default. Provider isolation internals and the off-screen checkbox's initial state are not independently observable. No profile or personal account was provided.

TinyFish made all task decisions in its hosted browser. The existing adapter submitted the exact prompt, polled status, enforced a 600-second watchdog, saved provider output and downloaded evidence. No Codex field edits, DOM manipulation, Playwright task script or injected expected-answer state was used. Independent inspection occurred after terminal status and was not given to TinyFish. No Claude rerun, unrelated test or automatic benchmark restart took place.

## Capture differences and verification

Original TinyFish used default captures. The follow-up added read-only capture flags screenshots, html, snapshots and elements, accepted without a rejected submission or repair. Extra capture may affect run overhead; it does not change the task prompt. The returned run schema exposed images and HTML, not live-value snapshot/element artifacts. Every available artifact was preserved. The 36 provider images were visually inspected; private contact sheets aided review but are not published as agent screenshots. No agent screenshot was edited or replaced.

Filled text values and radio checked properties are absent from serialized HTML. HTML is therefore used for its visible status text and trace corroboration, not as proof of input property values. The independent [observations](attempt-2/gui-observations.json) distinguish visible state from the model's assertions. The original strict comparison requires exact text except phone punctuation. The existing shorter-message sensitivity is reported separately. Neither the model's claim nor default-checkbox inference earns a newsletter point. No submission action, final Not submitted status, and no post-submission reload in the captured trace support the mandatory non-submission constraint.

## Timing, action units, models and costs

| Attempt | Primary client/native timer | Provider started→finished | Provider created→started | Steps / native actions |
|---|---:|---:|---:|---|
| Claude original | 66.749507 s | unavailable | unavailable | 37 native computer actions including images/zoom |
| TinyFish original | 37.03136050000103 s | not used in this comparison | not used | 7 provider steps |
| TinyFish 2 | 101.52620445899811 s | 71 s | 4 s | 14 provider steps |
| TinyFish 3 | 71.4355691669989 s | 47 s | 4 s | 12 provider steps |
| TinyFish 4 | 106.1973695839988 s | 79 s | 3 s | 13 provider steps |

TinyFish's original adapter stopwatch starts immediately before submission and ends when a terminal status is observed. It includes submission, queue/transport and polling overhead, but excludes subsequent evidence retrieval. wrapper-timing.json includes artifact collection and is not the comparison timer. Created/started/finished timestamps are provider-reported whole seconds. The difference between client and provider intervals cannot be assigned entirely to queueing or polling. Claude's original primary stopwatch is its native runner time, with 66.749573 seconds recorded for the wider wrapper. Neither model-only latency nor perfectly identical timer boundaries are available. No timeout fired.

TinyFish uses the provider's hosted browser; immutable model revision and exact browser build/OS were not exposed. lite is a browser profile, not a model identity. Claude used the earlier Firefox/Linux native computer environment, alias claude-sonnet-5-5 and computer_toolset_20260801. The runs occurred on different dates. They are browser-task comparisons, not TinyFish desktop tests. No normalization of native actions into provider steps is justified.

The account's returned tariff was $0.016 per Agent step. Steps × tariff equaled each observed wallet decrease ($0.224, $0.192, $0.208), total $0.624. This supports run attribution but is not an invoice reconciliation; concurrent external account activity cannot be conclusively ruled out. Absolute balances and account links are excluded. Auto-reload was unconfigured, with no pending top-up. No purchase or settings change was made. Claude's original cost is a token estimate; infrastructure, labor and electricity are unpriced. No TinyFish cost per verified full completion is calculable with zero verified full completions.

## Preservation and audit

Original files and grades remain unchanged. New attempts are separate directories. Raw new evidence remains private; public copies retain synthetic task data and original response text, redact capability URLs and pseudonymize opaque run/step/DOM IDs. Images are byte-identical. [Copy hashes](source-provenance.json) document transformations. The recovered Claude name-field image is historical evidence already cited by its verifier, not a fresh Claude attempt. [Executed source archive](execution-source/source-hashes.json) records the wrapper and exact TinyFish function excerpt; private multi-provider dependencies are not republished, and the archive is not represented as standalone runnable code. Offline verification makes no provider calls.

Operational references: [TinyFish API reference](https://docs.tinyfish.ai/agent-api/reference), [run lifecycle and captures](https://docs.tinyfish.ai/key-concepts/runs), [async submission schema](https://docs.tinyfish.ai/api-reference/automation/start-automation-asynchronously), [run retrieval schema](https://docs.tinyfish.ai/api-reference/runs/get-run-by-id). These describe API operation, not independent proof of benchmark success. A raw HTTP preflight received 403/error 1010; the normal browser and all three TinyFish runs could open the original fixture. No security bypass was used.
