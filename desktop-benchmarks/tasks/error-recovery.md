# Desktop error recovery

## Objective and provenance

Reconstructed under explicit authorization from the stated task objective, then frozen before execution. This is the actual submitted frozen prompt, not a claim that missing older specifications were recovered.

## Environment and starting state

Isolated Linux desktop, Xvfb 1024×768, Openbox and LibreOffice 7.4.7.2. Containers have no network, host mounts or credentials. CSV begins with blank Calc; organization uses PCManFM at Inbox; document work requests blank Writer; reporting begins with Calc. Recovery’s actual initial screenshots show blank Calc behind the same synthetic warning, despite the launcher requesting Writer. Inputs and expected outputs are [separate](../inputs/); expected data were never staged in the model environment.

## Exact submitted prompt

SHA-256 `f7c88f57a71dadec9c89b969d1c1eb1706f1e24800a57b7ee5e8b78f71a60d23`.

```text
A single synthetic interruption notice is on screen. Dismiss it and continue using desktop GUI controls. Among the similarly named dispatch_plan documents in /home/agent/Desktop/benchmark, inspect the contents to find the one with Document ID REC-204 and Approval APPROVED. Do not edit a draft or rely on the filename alone. In that approved document, change the dispatch handoff time from 16:00 to 16:30, preserving every other paragraph. Save a separate recovery_plan_corrected.docx in the same folder without changing any of the four source documents. Close and reopen the corrected document to verify its ID, approval, and corrected time. Use only desktop graphical applications, mouse and keyboard. Do not use a browser, terminal, scripts, macros, programmatic file tools, or the network. Spreadsheet formulas entered through the GUI are allowed for calculations. Report what you changed, the output location, and any incomplete steps.
```

## Execution and time limit

Claude Messages native computer toolset or OpenAI Responses native computer tool. The model decides every GUI action. The executor applies it, captures screenshots and collects files after stopping; it never chooses edits or supplies answers. Maximum 600 seconds per attempt. Historical CSV uses its recorded remaining-time allocation; every observed wall interval was below 600 seconds.

## Five-point rubric

1. Identified REC-204 approved source by contents — 1 point.
2. Dismissed the controlled interruption through GUI — 1 point.
3. Corrected time and preserved all other text — 1 point.
4. Separate valid output and all four source documents unchanged — 1 point.
5. Reopened corrected document and verified ID approval and time — 1 point.

## Independent verification and results

Read-only checks compare originals byte-for-byte, saved outputs against expected content, and cited GUI screenshots/actions for workflow completion. A correct file alone cannot earn the reopening check. See [verifier](../verification/README.md), [all scored attempts](../RESULTS.md) and [comparison](../COMPARISON.md). The interruption is a controlled warning, not a real crash. Its exit code and model-requested dismissal are retained. The first Claude attempt remains 4/5; one labeled local-budget repair retry passes 5/5. 

[Fixtures](../inputs/) · [Expected outputs](../expected/) · [Actual artifacts](../outputs/) · [Traces](../logs/) · [Screenshots](../screenshots/)
