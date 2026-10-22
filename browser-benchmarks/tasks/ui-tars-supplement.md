# UI-TARS: five later browser tasks (separate suite)

These are five different prompts, not reruns of the common browser batch and not desktop-application tasks. Each was submitted once. All ended with model-request timeouts and no complete answer. Partial navigation evidence is preserved without inventing factual accuracy scores. The 2048-token patch was already in place; these failures do not reproduce the earlier 65535-token error.

## test-1-wikipedia-people

**Objective and start:** follow the task-specific target and instructions below in the patched macOS Browser Operator. **Deadline:** 600 seconds maximum; the model request timeout ended each run earlier.

```text
Open Wikipedia and find the birth years of the following five people:

1. Alan Turing
2. Ada Lovelace
3. Grace Hopper
4. Tim Berners-Lee
5. Margaret Hamilton (computer scientist)

For each person, provide their full name, birth year, and the direct URL to the Wikipedia article you used.

Use Wikipedia itself to verify your answers. Do not invent missing information.
```

SHA-256 `e64e2e4338c4ac0b112b8ee0c96d978dade4ce6b5267024e98208ee4528a078f`.

**Scoring:** the exact task-specific rubric, independent observations and partial states are in [verification](../evidence/ui-tars-oct21/test-1-wikipedia-people/verification.json). **Execution:** UI-TARS selected actual browser actions; the verifier observed only after stopping. **Outcome:** FAIL, interrupted by request timeout; no completed structured answer. [Original responses and trace](../evidence/ui-tars-oct21/test-1-wikipedia-people/) · [record](../evidence/ui-tars-oct21/test-1-wikipedia-people/record.json).

## test-2-selenium-form

**Objective and start:** follow the task-specific target and instructions below in the patched macOS Browser Operator. **Deadline:** 600 seconds maximum; the model request timeout ended each run earlier.

```text
Open https://www.selenium.dev/selenium/web/web-form.html

Complete the form using the following information:

- Text input: Vera Agiang
- Password: Benchmark2026!
- Textarea: Testing UI-TARS computer-use capabilities.
- Disabled input: Leave unchanged
- Read-only input: Leave unchanged
- Dropdown select: Two
- Dropdown datalist: New York
- Checked checkbox: Keep checked
- Default checkbox: Check it
- Checked radio button: Keep selected
- Default radio button: Leave unselected
- Color picker: #ff0000
- Date picker: 10/21/2026
- Range slider: 7

Do not submit the form. Stop when all editable fields have been completed.
```

SHA-256 `ef227524c59a9622a777b7ee596bcbb76d83b638067c21991a8aa77915fd6bfc`.

**Scoring:** the exact task-specific rubric, independent observations and partial states are in [verification](../evidence/ui-tars-oct21/test-2-selenium-form/verification.json). **Execution:** UI-TARS selected actual browser actions; the verifier observed only after stopping. **Outcome:** FAIL, interrupted by request timeout; no completed structured answer. [Original responses and trace](../evidence/ui-tars-oct21/test-2-selenium-form/) · [record](../evidence/ui-tars-oct21/test-2-selenium-form/record.json).

## test-3-vscode-issues

**Objective and start:** follow the task-specific target and instructions below in the patched macOS Browser Operator. **Deadline:** 600 seconds maximum; the model request timeout ended each run earlier.

```text
Open https://github.com/microsoft/vscode

Navigate through the website's interface to the Issues section.

Find open issues labeled `bug`.

Sort the issues by most recently updated.

Identify the three most recently updated issues.

For each issue, report:
1. Issue number
2. Exact issue title
3. Direct GitHub URL
4. Last updated date

Use the GitHub interface to complete the task. Do not invent issue details.
```

SHA-256 `ba03728944aa40cbb15f0d7ffd36f717b9c9cb9d27a34b5f0bf051c0ab3c2862`.

**Scoring:** the exact task-specific rubric, independent observations and partial states are in [verification](../evidence/ui-tars-oct21/test-3-vscode-issues/verification.json). **Execution:** UI-TARS selected actual browser actions; the verifier observed only after stopping. **Outcome:** FAIL, interrupted by request timeout; no completed structured answer. [Original responses and trace](../evidence/ui-tars-oct21/test-3-vscode-issues/) · [record](../evidence/ui-tars-oct21/test-3-vscode-issues/record.json).

## test-4-login-recovery

**Objective and start:** follow the task-specific target and instructions below in the patched macOS Browser Operator. **Deadline:** 600 seconds maximum; the model request timeout ended each run earlier.

```text
Open https://the-internet.herokuapp.com/login

Attempt to log in using these incorrect credentials:

Username: incorrect_user
Password: wrong_password

Observe the error message.

Then recover by using the correct demo credentials:

Username: tomsmith
Password: SuperSecretPassword!

Verify that login succeeds and report the final result.
```

SHA-256 `5fe9ea639842724cba8ccc63d292b0be9b536be4ec1d1aa16a0eca5b26dc70b2`.

**Scoring:** the exact task-specific rubric, independent observations and partial states are in [verification](../evidence/ui-tars-oct21/test-4-login-recovery/verification.json). **Execution:** UI-TARS selected actual browser actions; the verifier observed only after stopping. **Outcome:** FAIL, interrupted by request timeout; no completed structured answer. [Original responses and trace](../evidence/ui-tars-oct21/test-4-login-recovery/) · [record](../evidence/ui-tars-oct21/test-4-login-recovery/record.json).

## test-5-programming-languages

**Objective and start:** follow the task-specific target and instructions below in the patched macOS Browser Operator. **Deadline:** 600 seconds maximum; the model request timeout ended each run earlier.

```text
Open https://en.wikipedia.org/wiki/List_of_programming_languages

Find these five programming languages:

1. Python
2. Java
3. Rust
4. Go
5. Ruby

For each language, navigate to its Wikipedia article and collect:

- Programming language name
- Year it first appeared
- Original designer or creator
- Direct Wikipedia URL

Return the information in a structured table.

Verify the information against each Wikipedia article. Do not invent missing details.
```

SHA-256 `9ba091e33abdd8d8c00c59f9f73e8eee5a72cfc530c0c1218e07eb9c27efec65`.

**Scoring:** the exact task-specific rubric, independent observations and partial states are in [verification](../evidence/ui-tars-oct21/test-5-programming-languages/verification.json). **Execution:** UI-TARS selected actual browser actions; the verifier observed only after stopping. **Outcome:** FAIL, interrupted by request timeout; no completed structured answer. [Original responses and trace](../evidence/ui-tars-oct21/test-5-programming-languages/) · [record](../evidence/ui-tars-oct21/test-5-programming-languages/record.json).


## Recorded criteria and point-allocation limits

- **Wikipedia people:** ten factual checks were recorded (five birth years and five article URLs); identity follows the named people. A complete final-answer score was unavailable. The Alan Turing trace observation is partial progress, not a fabricated full-answer score.
- **Selenium form:** fourteen equally counted state checks: text, password, textarea, disabled unchanged, read-only unchanged, select Two, datalist New York, checked checkbox retained, default checkbox checked, checked radio retained, default radio unselected, red color, requested date and range 7. There were nine required changes. The five matching defaults were unchanged; zero required changes completed. No submission was observed.
- **VS Code issues:** correct repository, open/bug filter, newest-updated order, a complete three-issue list and the four requested fields per issue. The recorded audit is boolean/workflow-based; no original numerical point allocation was recovered, so no retrospective twelve-point score is invented. Repository/filter navigation is separate from the missing answer.
- **Demo login recovery:** four counted workflow checks: requested initial failed demo login; recognition of error; successful recovery using the public demo credentials; final success report. Zero were verified because the fixture was never reached. This is not an isolated test of authentication recovery ability.
- **Programming languages:** visit the five articles, collect first-appearance year, original creator and article URL, and return the structured table. No original numeric point allocation was recovered. Factual accuracy remains Not measured because no complete result was returned.

These are the saved criteria, not a new rubric applied to improve outcomes. Each linked verification JSON preserves the actual observations and limitations.
