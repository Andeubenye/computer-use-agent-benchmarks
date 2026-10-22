# CSV editing

## Objective and provenance

Original unchanged CSV task and five-point rubric.

## Environment and starting state

Isolated Linux desktop, Xvfb 1024×768, Openbox and LibreOffice 7.4.7.2. Containers have no network, host mounts or credentials. CSV begins with blank Calc; organization uses PCManFM at Inbox; document work requests blank Writer; reporting begins with Calc. Recovery’s actual initial screenshots show blank Calc behind the same synthetic warning, despite the launcher requesting Writer. Inputs and expected outputs are [separate](../inputs/); expected data were never staged in the model environment.

## Exact submitted prompt

SHA-256 `409633c43e51d6dec788410a90874c4375246d32e41548c56e8af7fa731bf439`.

```text
Open orders_to_fix.csv in a desktop spreadsheet application. Find and correct both instances of 'Pendng' to 'Pending'. Do not change any other values or the order of the rows. Save the corrected file as orders_corrected.csv in the same folder, preserving the original file. Reopen the saved file to verify both corrections, then report what you changed and where you saved it. Do not use a web browser, terminal, scripts, or programmatic file-editing tools to complete the task.
```

## Execution and time limit

Claude Messages native computer toolset or OpenAI Responses native computer tool. The model decides every GUI action. The executor applies it, captures screenshots and collects files after stopping; it never chooses edits or supplies answers. Maximum 600 seconds per attempt. Historical CSV uses its recorded remaining-time allocation; every observed wall interval was below 600 seconds.

## Five-point rubric

1. Opened CSV in spreadsheet — 1 point.
2. Corrected both Pendng statuses to Pending — 1 point.
3. Preserved all other values and row order — 1 point.
4. Saved separate correct CSV and preserved original bytes — 1 point.
5. Reopened saved CSV and verified both corrections — 1 point.

## Independent verification and results

Read-only checks compare originals byte-for-byte, saved outputs against expected content, and cited GUI screenshots/actions for workflow completion. A correct file alone cannot earn the reopening check. See [verifier](../verification/README.md), [all scored attempts](../RESULTS.md) and [comparison](../COMPARISON.md). 

[Fixtures](../inputs/) · [Expected outputs](../expected/) · [Actual artifacts](../outputs/) · [Traces](../logs/) · [Screenshots](../screenshots/)
