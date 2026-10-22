# Verified results

Read the [five-attempt comparison table](README.md). Claude's original 10/10 and TinyFish's original five confirmed fields were checked against their archived verifier and screenshots. The original TinyFish image visibly shows a blank job title, unchanged country and unselected contact method. Its message and newsletter were outside the captured viewport. Its original full-success claim was contradicted by those visible omissions.

## Three new attempts

Each final screenshot confirms **Alex; Morgan; alex.morgan@example.com; +1 202-555-0147; Northstar Labs; Product Manager; United States; Email**. All three originally omitted controls are now correct. The message reads **“This is a benchmark.”** in every rerun. The unchanged reference requires **“This is a benchmark. Do not submit.”** Strict result per attempt: **eight correct, one message mismatch, one newsletter state unverified, out of ten**. All three are PARTIAL.

The prompt's message boundary admits a reasonable shorter reading. Under the already documented sensitivity reading, each rerun earns **nine confirmed fields with one still unverified**. This is not a confirmed 10/10 under either interpretation. Unverified checkbox state is not evidence that it was checked.

All 36 screenshots were visually reviewed, including each blank initial viewport and each filled final viewport. None shows the newsletter. All 36 HTML captures were retained. They serialize DOM attributes, not the current form properties: visibly filled text fields have no value attributes, and the visibly selected Email radio lacks checked. The checkbox's missing checked attribute cannot prove its state. Requested snapshot/element capture flags were accepted, but no retrievable live-property state was exposed in the returned run schema. The agent's unchecked claim was not used as independent evidence.

Each final HTML capture displays **“Not submitted.”** The complete recorded action sequence shows no Submit action, submission or reload afterward. Together these support the non-submission constraint; the final agent assertion alone would not. No prohibited submission is evident.

All three provider statuses were COMPLETED, with no reported provider error, client error, timeout, benchmark restart or capture-submission repair. Internal provider retries were not exposed. Attempt 2 contains two country-selection steps; this is retained as recorded behavior, not an invented API retry. TinyFish's full-success claims are not substantiated by strict independent grading. Unlike the original attempt, the new evidence does not show those three controls left blank; the remaining message discrepancy is ambiguous and the checkbox claim is unverified.

## Aggregates, without selecting the fastest run

| Cohort | Observed strict full passes | Confirmed field points | Unverified field points | Mean client time | Total / mean cost |
|---|---:|---:|---:|---:|---:|
| Three new TinyFish reruns | 0/3 | 24/30 | 3/30 | 93.05 s | $0.624 / $0.208 |
| All four TinyFish form attempts | 0/4 | 29/40 | 5/40 | 79.05 s | $0.736 / $0.184 |
| Original Claude reference | 1/1 | 10/10 | 0/10 | 66.75 s | $0.194282 estimated |

The new-run median is 101.53 seconds, with a range of 71.44–106.20 seconds. New-run cost range is $0.192–$0.224. The 39 provider steps produced 36 images and 36 HTML captures. The four-attempt mean combines different dates and capture settings; the three-rerun mean is the primary follow-up summary. These are case counts and confirmed evidence coverage, not population reliability estimates. Cost per verified TinyFish full completion cannot be calculated because none was independently established; it is not $0. Claude's one verified completion cost an estimated $0.194282.

Follow-up debit: $0.624. The existing browser ledger baseline was $2.1059203; committed estimate after follow-up is $2.7299203, leaving $7.2700797 under that $10 cap. No purchase, top-up or billing setting change was made. This does not change the separate desktop ledger.
