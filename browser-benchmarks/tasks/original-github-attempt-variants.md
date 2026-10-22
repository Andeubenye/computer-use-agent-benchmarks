# Original GitHub runtime prompt variants

The per-agent root prompt files recover the orchestration request. Native attempt configurations also preserve more detailed runtime instructions. They are reproduced below rather than silently treated as identical to the short request. Each source is linked; a source configuration is evidence of that attempt’s instructions, not proof that every historical attempt used the same text. System messages remain in the linked configurations where recovered.

## claude — `3ff5a35b7468`

SHA-256 `3ff5a35b7468f6594d685c938ca2eefc4a5cc495d0ea168672e16ab4515c57fa`. Sources: [task.json](../../browser-benchmarks/evidence/original-github/agents/claude/preserved/20261017T004821Z-eba39479/task.json), [task.json](../../browser-benchmarks/evidence/original-github/agents/claude/preserved/20261017T005847Z-7cbd2a64/task.json)

```text
Open https://github.com/browser-use/browser-use/issues. Using GitHub's website interface, find the five most recently updated open issues labeled bug. Return each issue's number, title, URL, and last updated date, ordered from most recently updated to least recently updated. Do not use GitHub's API. If fewer than five issues exist, report the number found. Do not log in or make any changes to the repository.
```

## claude — `5c281596758a`

SHA-256 `5c281596758a95d83eb871bc44ab5bed440a96f5d22ba18797ceb0971ae1afc9`. Sources: [reproducibility.json](../../browser-benchmarks/evidence/original-github/agents/claude/preserved/20261017T001240Z-00ae9af7/reproducibility.json)

```text
Open https://github.com/browser-use/browser-use/issues. Using GitHub's website interface, find the five most recently updated open issues labeled bug. Return each issue's number, title, URL, and last updated date, ordered from most recently updated to least recently updated. Do not use GitHub's API, Playwright, Selenium, DOM inspection, or direct HTTP requests to retrieve issue data. Do not log in or make any changes to the repository. Use only the native computer toolset and visible GitHub website. Hovering visible relative update dates may reveal exact dates in tooltips; do not confuse issue creation dates with update dates. Return exact dates if visible. If only a relative update date is available, preserve it verbatim and state that limitation rather than inventing a date. Return a final JSON object with keys issues, count_found, notes. Each issue must include number (integer), title, url, last_updated, and last_updated_precision (exact_timestamp, calendar_date, or relative).
```

