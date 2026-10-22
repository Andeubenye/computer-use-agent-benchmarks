# Cross-application reporting

## Objective and provenance

Reconstructed under explicit authorization from the stated task objective, then frozen before execution. This is the actual submitted frozen prompt, not a claim that missing older specifications were recovered.

## Environment and starting state

Isolated Linux desktop, Xvfb 1024×768, Openbox and LibreOffice 7.4.7.2. Containers have no network, host mounts or credentials. CSV begins with blank Calc; organization uses PCManFM at Inbox; document work requests blank Writer; reporting begins with Calc. Recovery’s actual initial screenshots show blank Calc behind the same synthetic warning, despite the launcher requesting Writer. Inputs and expected outputs are [separate](../inputs/); expected data were never staged in the model environment.

## Exact submitted prompt

SHA-256 `56c27384ed209b0e55be335f92ea435439baf6b550cac35a52d61ce8fb035543`.

```text
Open sales_records.csv in LibreOffice Calc and inspect all 30 sales records. Calculate four metrics: total revenue, total units, average order value (total revenue divided by 30, rounded to two decimal places), and the region with the highest total revenue. Use spreadsheet GUI calculations as needed. Open report_template.docx in LibreOffice Writer and replace its four [fill] placeholders with the calculated metrics, preserving the title and source reference. Save the completed report as sales_summary.docx in the same folder, keeping both inputs unchanged. Close and reopen sales_summary.docx to verify all four reported metrics. Use only desktop graphical applications, mouse and keyboard. Do not use a browser, terminal, scripts, macros, programmatic file tools, or the network. Spreadsheet formulas entered through the GUI are allowed for calculations. Report what you changed, the output location, and any incomplete steps.
```

## Execution and time limit

Claude Messages native computer toolset or OpenAI Responses native computer tool. The model decides every GUI action. The executor applies it, captures screenshots and collects files after stopping; it never chooses edits or supplies answers. Maximum 600 seconds per attempt. Historical CSV uses its recorded remaining-time allocation; every observed wall interval was below 600 seconds.

## Five-point rubric

1. Observed 30 records in Calc and used Writer — 1 point.
2. All four metrics independently correct — 1 point.
3. Metrics transferred into a valid Writer document with no placeholders — 1 point.
4. Separate saved report and unchanged input CSV and template — 1 point.
5. Reopened saved report and visually verified metrics — 1 point.

## Independent verification and results

Read-only checks compare originals byte-for-byte, saved outputs against expected content, and cited GUI screenshots/actions for workflow completion. A correct file alone cannot earn the reopening check. See [verifier](../verification/README.md), [all scored attempts](../RESULTS.md) and [comparison](../COMPARISON.md). Revenue, unit count, average and highest region are independently recomputed from the original 30-row CSV. 

[Fixtures](../inputs/) · [Expected outputs](../expected/) · [Actual artifacts](../outputs/) · [Traces](../logs/) · [Screenshots](../screenshots/)
