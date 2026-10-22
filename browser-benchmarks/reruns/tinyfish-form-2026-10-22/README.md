# TinyFish form follow-up — 22 October 2026

Three actual, independent TinyFish hosted-agent runs, using the unchanged original form prompt and a 600-second limit each. No Claude rerun, manual field corrections, other benchmark or paid retry. This is a separate follow-up cohort; the original common-browser table and desktop results remain unchanged.

**Finding:** TinyFish improved from five to eight independently confirmed fields on each rerun. It did not match Claude's verified 10/10 under the original strict rubric. The short-message interpretation is ambiguous; the newsletter checkbox was not captured. These are partial verified results, not proof that TinyFish necessarily left that checkbox wrong.

| Configuration / attempt | Strict verified result | Comparison timer (s) | Cost (USD) | Recorded actions | Captured images |
|---|---|---:|---:|---|---:|
| Claude original | PASS 10/10 | 66.75 | 0.194282 estimated | 37 native actions, including screenshots/zoom | 7 reported |
| TinyFish original (1) | PARTIAL: 5 correct, 3 incorrect, 2 unverified /10 | 37.03 | 0.112 estimated | 7 provider steps | 6 |
| TinyFish rerun 1 (2) | PARTIAL: 8 correct, 1 incorrect, 1 unverified /10 | 101.53 | 0.224 | 14 provider steps | 13 |
| TinyFish rerun 2 (3) | PARTIAL: 8 correct, 1 incorrect, 1 unverified /10 | 71.44 | 0.192 | 12 provider steps | 11 |
| TinyFish rerun 3 (4) | PARTIAL: 8 correct, 1 incorrect, 1 unverified /10 | 106.20 | 0.208 | 13 provider steps | 12 |

New TinyFish costs are steps × $0.016, matching observed account-balance decreases; they are not invoices. Claude's cost is a token estimate. Timers and action units differ; see [methodology](METHODOLOGY.md). All new primary times exceeded Claude's recorded time, although these measurements do not isolate model speed.

## Inspect the evidence

| Attempt | Independent verification | Original response | Final image | Full trace and images |
|---|---|---|---|---|
| Claude original | [verification](../../evidence/additional-tasks/runs/claude/test-3-form/verification.json) | [response](../../evidence/additional-tasks/runs/claude/test-3-form/original-response.txt) | [lower controls](../../evidence/additional-tasks/runs/claude/test-3-form/native-evidence/20261017T182319Z-148ad151/screenshots/independent-final.png), [recovered upper names](original-claude-reference/0023-screenshot.png) | [original evidence](../../evidence/additional-tasks/runs/claude/test-3-form/) |
| TinyFish original | [verification](../../evidence/additional-tasks/runs/tinyfish/test-3-form/verification.json) | [response](../../evidence/additional-tasks/runs/tinyfish/test-3-form/original-response.txt) | [image](../../evidence/additional-tasks/runs/tinyfish/test-3-form/screenshots/screenshot-005.jpg) | [original evidence](../../evidence/additional-tasks/runs/tinyfish/test-3-form/) |
| TinyFish 2 | [verification](attempt-2/independent-verification.json) | [response](attempt-2/original-response.txt) | [image](attempt-2/screenshots/screenshot-012.jpg) | [trace](attempt-2/provider-run.json), [images](attempt-2/screenshots/), [HTML](attempt-2/html-captures/) |
| TinyFish 3 | [verification](attempt-3/independent-verification.json) | [response](attempt-3/original-response.txt) | [image](attempt-3/screenshots/screenshot-010.jpg) | [trace](attempt-3/provider-run.json), [images](attempt-3/screenshots/), [HTML](attempt-3/html-captures/) |
| TinyFish 4 | [verification](attempt-4/independent-verification.json) | [response](attempt-4/original-response.txt) | [image](attempt-4/screenshots/screenshot-011.jpg) | [trace](attempt-4/provider-run.json), [images](attempt-4/screenshots/), [HTML](attempt-4/html-captures/) |

[Detailed results](RESULTS.md) · [Comparison](COMPARISON.md) · [Article-ready paragraph](ARTICLE-READY.md) · [Machine-readable results](results.json) · [CSV](results.csv) · [Copy provenance](source-provenance.json) · [Unchanged prompt](../../prompts/exact/test-3-form.txt)
