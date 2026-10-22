# File organization

## Objective and provenance

Reconstructed under explicit authorization from the stated task objective, then frozen before execution. This is the actual submitted frozen prompt, not a claim that missing older specifications were recovered.

## Environment and starting state

Isolated Linux desktop, Xvfb 1024×768, Openbox and LibreOffice 7.4.7.2. Containers have no network, host mounts or credentials. CSV begins with blank Calc; organization uses PCManFM at Inbox; document work requests blank Writer; reporting begins with Calc. Recovery’s actual initial screenshots show blank Calc behind the same synthetic warning, despite the launcher requesting Writer. Inputs and expected outputs are [separate](../inputs/); expected data were never staged in the model environment.

## Exact submitted prompt

SHA-256 `bbd0c4794d7c45f0c7ff1768f79ea3558675dcec93234d9126528d35e59a4008`.

```text
In /home/agent/Desktop/benchmark/Inbox, organize all 20 files into exactly four subfolders named PDFs, Images, Notes, and Spreadsheets, according to their file types. Move the eight PDFs into PDFs and rename them using this mapping: scan_01.pdf to 2026-01-INV-1001.pdf; scan_02.pdf to 2026-01-INV-1002.pdf; scan_03.pdf to 2026-01-INV-1003.pdf; scan_04.pdf to 2026-01-INV-1004.pdf; scan_05.pdf to 2026-01-INV-1005.pdf; scan_06.pdf to 2026-01-INV-1006.pdf; scan_07.pdf to 2026-01-INV-1007.pdf; scan_08.pdf to 2026-01-INV-1008.pdf. Move all PNGs to Images, TXT files to Notes, and CSV files to Spreadsheets, keeping those filenames. Do not change any file contents. Verify that exactly 20 files remain, with none missing, duplicated, or left loose in Inbox, and verify the eight PDF names. Use only desktop graphical applications, mouse and keyboard. Do not use a browser, terminal, scripts, macros, programmatic file tools, or the network. Spreadsheet formulas entered through the GUI are allowed for calculations. Report what you changed, the output location, and any incomplete steps.
```

## Execution and time limit

Claude Messages native computer toolset or OpenAI Responses native computer tool. The model decides every GUI action. The executor applies it, captures screenshots and collects files after stopping; it never chooses edits or supplies answers. Maximum 600 seconds per attempt. Historical CSV uses its recorded remaining-time allocation; every observed wall interval was below 600 seconds.

## Five-point rubric

1. All 20 files retained exactly once — 1 point.
2. All four type folders correct and no loose files — 1 point.
3. All eight PDF renames correct — 1 point.
4. Every file byte-identical to its input — 1 point.
5. GUI verification of final folders and filenames — 1 point.

## Independent verification and results

Read-only checks compare originals byte-for-byte, saved outputs against expected content, and cited GUI screenshots/actions for workflow completion. A correct file alone cannot earn the reopening check. See [verifier](../verification/README.md), [all scored attempts](../RESULTS.md) and [comparison](../COMPARISON.md). 

[Fixtures](../inputs/) · [Expected outputs](../expected/) · [Actual artifacts](../outputs/) · [Traces](../logs/) · [Screenshots](../screenshots/)
