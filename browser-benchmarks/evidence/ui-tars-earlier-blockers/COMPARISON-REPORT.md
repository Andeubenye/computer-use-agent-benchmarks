# UI-TARS benchmark comparison — 17 October 2026

> **Final authorized Test A attempt: unsuccessful before agent execution.** The working Terminal-launched development app was not running, and Terminal access remained blocked by the computer-use tool. Per the user’s final stop instruction, no further troubleshooting, rebuild, retry, or setup request was made. Test B was not attempted again. No prompt, endpoint wake, or paid inference was initiated. No new accuracy, time, action, screenshot, or response metrics exist. See final-attempt record (original local source) and article-ready limitation (original local source). Earlier results are preserved below and copied into the final-attempt folder.

Both configurations stopped before agent execution. Neither produced an issue list. This is a record of setup and access failures, not a completed model-performance comparison. No substitute agent performed the task, no benchmark was restarted, and no paid inference or Hugging Face wake was initiated.

**Endpoint status:** the dashboard showed **Scaled to Zero** immediately before the final Scale Endpoint to Zero button action. Subsequent normal and hard refreshes showed a blank dashboard, so fresh post-action verification is unavailable. The user was alerted. No wake/resume was issued. Please check the existing dashboard manually if it remains blank.

## Actual results

| Metric | Test A — Hugging Face | Test B — Volcano Engine |
|---|---|---|
| Outcome | Blocked before agent start | Blocked before agent start |
| Completed / independently verified | No / no | No / no |
| Accuracy | Unavailable: no issue list | Unavailable: no issue list |
| Agent wall-clock duration | Not measured: never started | Not measured: never started |
| Agent actions / screenshots | Unavailable / unavailable | Unavailable / unavailable |
| Setup screenshots in run folder | 1 | 2 |
| Original agent response | None produced | None produced |
| Prompt submitted / inference requests | No / 0 | No / 0 |
| Automatic benchmark restarts | 0 | 0 |
| HF cold start / billed GPU time | Not initiated / not measured | Not initiated / not measured |
| Estimated incremental service cost from actions taken | $0: no wake or inference | $0: no trial allocation or purchase |
| Actual invoice cost | Not inspected | Not inspected |
| Blocker | Final app reported Accessibility denied | Official trial entry required account login and additional terms |

Unavailable metrics were not converted into zero-performance scores. Setup screenshots and offline application launches are separate from agent screenshots and benchmark attempts.

## Test A: permission and credential evidence

The existing patched prebuilt development application was used without rebuilding. Source: official v0.2.4 tag, commit `0ee87301a6db754c5f67909e5fbbcf05233abad9`; its internal app manifest is 0.2.3. Electron: 34.1.1 arm64. Configuration: Hugging Face for UI-TARS-1.5, `ByteDance-Seed/UI-TARS-1.5-7B`, Chat Completions, output 2048, existing endpoint context 32768, Local Browser Operator. No model, hardware, context, or API-mode change was made.

After the approved normal System Settings grants, a user-run Terminal session with placeholder credentials passed native Accessibility and Screen Recording checks; Electron Accessibility was true. Structured and serialized fixture values were redacted in console and file logs. Evidence remains in `offline-validation/terminal-native-permissions.json` and `terminal-offline-readiness-passed.json`.

Existing credentials were then staged in a separate private profile, directory mode 0700 and settings mode 0600. Credentials were never put in output artifacts, command arguments or environment variables. Settings and availability-check screens were not opened with real credentials: the original renderer can log settings there, and its availability check can itself make inference requests.

The user reported the prepared application open, but the expected Test A log, permission result and running process were not observed at that point. A direct launch of the existing prebuilt launcher then opened Home but reported:

```json
{"accessibility":"denied","screen":"authorized","electronAccessibility":false,"electronVersion":"34.1.1","logHookInstalled":true}
```

The difference between manual Terminal and direct execution is observed. Launch-context attribution is a possible explanation, not a proven diagnosis. The required Accessibility check was not overridden. The app was stopped before endpoint wake or task submission. A nonfatal startup error, `TypeError: installExtension is not a function`, is also retained; the window nevertheless opened.

The computer-use tool refused Terminal access: “Computer Use is not allowed to use the app 'com.apple.Terminal' for safety reasons.” Terminal was not operated through another automation route. The direct launch executed Electron itself.

Copied credentials were removed from the stopped benchmark profile. The original installed credential settings were untouched. Final text-artifact scans found no existing API key or private endpoint URL. The external runtime filter affects logging only, in memory; it does not change networking, model behavior, parsing or operators.

Evidence: run record (original local source), native check (original local source), filtered log (original local source), Home screenshot (original local source), credential cleanup (original local source).

## Test B: official service access limitation

The unchanged installed official Desktop 0.2.4 client was launched with an isolated credential-free profile. Its Browser Operator entry opened Volcano Engine's application-create flow, then redirected to account/phone login requiring credentials and additional service terms. No anonymous 30-minute trial entry was exposed in this client.

No credentials were entered, no agreement accepted, no account created, no resource allocated, and no prompt submitted. The provider tab and isolated client were closed. No alternative entry or second trial attempt was made. The exact remote model/service version and browser configuration were not exposed.

The previously disclosed development-client notice states that data is transmitted to servers and all records used for academic research; visible text did not specify retention/deletion terms. User approval covered that disclosed free trial under the no-personal-credentials/no-additional-account-commitments conditions. It did not supply login credentials or authorize a new account commitment. The older development client's private trial signer was unavailable; no vendor key was extracted or spoofed.

The installed client's background updater attempted GitHub release metadata and received HTTP 404. No update was installed. This was not a GitHub issues API lookup to solve the benchmark.

Evidence: run record (original local source), official entry (original local source), account requirement (original local source), startup log (original local source).

## Task, environments and measurement limits

Both run folders retain identical prepared prompts, SHA256 `40ea2777b2d6d330d275ded4e42757c23c975c4beaf84d314f2dd40a0feced4e`. The task requires GitHub's website interface to find the five most recently updated open issues labeled bug in `browser-use/browser-use`, returning number, title, URL and update date newest first. No GitHub API, login or repository changes are allowed.

The approved agent maximum was 600 seconds per test, excluding cold start. An identity-checking watchdog was validated offline against an isolated placeholder Electron process with a one-second deadline; it sent its stop signal at approximately 1.016 seconds. Neither benchmark started, so no agent timer ran and no timeout was reached.

Test A's unmodified Local Browser Operator launches a separate browser with a temporary profile and default 1280×800 viewport. It did not reach browser launch here. Test B's planned remote browser was never allocated. Client versions, browser location and exposed service metadata differ, so speed and accuracy cannot be compared.

No independent issue verification was performed because neither agent returned a list. Codex did not solve the GitHub task as a substitute. Historical screenshots of the installed application's original 65535-token error remain separately labeled in `offline-validation/`; they are not newly executed Test A results.

## Costs, shutdown and cleanup

The user supplied $1.80/hour for one NVIDIA L40S replica, autoscaling 0–1: $0.03 per billed minute, approximately $0.30 for ten billed minutes, plus billable initialization and idle time. This is an estimate, not an enforced cap. No cold start occurred; billed GPU duration and actual invoice cost were not measured.

The existing inference token returned HTTP 403 for management discovery. No token was created or widened. The signed-in dashboard showed Scaled to Zero before B, after B's blocker, and before the final scale-to-zero action. A fresh final refresh went blank; status was not inferred from a blank page. See `hf-lifecycle/events.jsonl` and `final-dashboard-refresh-unavailable.png`.

Both isolated clients and the standalone renderer server stopped. Terminal's approved Accessibility and Screen Recording permissions remain enabled; disable them in System Settings > Privacy & Security when no longer needed.

## Source and earlier evidence

The installed application's Info.plist, executable and app.asar still match their original SHA256 values. The project diff exactly matches the original token patch. No rebuild occurred in this workflow. Only the previously patched `packages/ui-tars/sdk/src/Model.ts` and `packages/ui-tars/sdk/tests/Model.test.ts` remain changed; previous regression and type-check results are preserved.

Twenty-five of 26 original evidence files remain byte-for-byte unchanged. The original live `dev-startup.log` appended 85 shutdown bytes when its process stopped; its full original 6684-byte prefix remains intact. No earlier evidence was truncated or replaced. Preparation records remain separate.

See `offline-validation/final-unchanged-app-and-source.json`, `earlier-evidence-recheck.json` and `final-artifact-credential-scan.json`. The execution-folder manifest records file sizes and SHA256 values.
