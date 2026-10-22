# Document editing

## Objective and provenance

Reconstructed under explicit authorization from the stated task objective, then frozen before execution. This is the actual submitted frozen prompt, not a claim that missing older specifications were recovered.

## Environment and starting state

Isolated Linux desktop, Xvfb 1024×768, Openbox and LibreOffice 7.4.7.2. Containers have no network, host mounts or credentials. CSV begins with blank Calc; organization uses PCManFM at Inbox; document work requests blank Writer; reporting begins with Calc. Recovery’s actual initial screenshots show blank Calc behind the same synthetic warning, despite the launcher requesting Writer. Inputs and expected outputs are [separate](../inputs/); expected data were never staged in the model environment.

## Exact submitted prompt

SHA-256 `f749dfee9d8adde4fc822584d8149c5a5b68808258f727232757e9cfaeec049b`.

```text
Open dispatch_original.docx in LibreOffice Writer. Correct 'shippment' to 'shipment' and 'recieve' to 'receive'. Apply the built-in Heading 1 paragraph style to the paragraph 'Next steps'. In the table, change the Training status from 'Pendng' to 'Pending'. Preserve all other text and the table structure. Save a separate dispatch_revised.docx in the same folder, keeping the original unchanged. Close and reopen the revised document to verify the text, heading style, and table correction. Use only desktop graphical applications, mouse and keyboard. Do not use a browser, terminal, scripts, macros, programmatic file tools, or the network. Spreadsheet formulas entered through the GUI are allowed for calculations. Report what you changed, the output location, and any incomplete steps.
```

## Execution and time limit

Claude Messages native computer toolset or OpenAI Responses native computer tool. The model decides every GUI action. The executor applies it, captures screenshots and collects files after stopping; it never chooses edits or supplies answers. Maximum 600 seconds per attempt. Historical CSV uses its recorded remaining-time allocation; every observed wall interval was below 600 seconds.

## Five-point rubric

1. Both spelling corrections and all other text preserved — 1 point.
2. Next steps uses Heading 1 — 1 point.
3. Training table cell is Pending and table structure preserved — 1 point.
4. Separate valid revised DOCX and unchanged original — 1 point.
5. Reopened revised document and visually verified requested changes — 1 point.

## Independent verification and results

Read-only checks compare originals byte-for-byte, saved outputs against expected content, and cited GUI screenshots/actions for workflow completion. A correct file alone cannot earn the reopening check. See [verifier](../verification/README.md), [all scored attempts](../RESULTS.md) and [comparison](../COMPARISON.md). 

[Fixtures](../inputs/) · [Expected outputs](../expected/) · [Actual artifacts](../outputs/) · [Traces](../logs/) · [Screenshots](../screenshots/)
