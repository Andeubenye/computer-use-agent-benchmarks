# Browser benchmarks

The original experiments included six agents. This public archive presents the five in scope; it does not imply TinyFish was tested in a separate later batch. TinyFish is a browser agent. The original four-task additional cohort had 20 runs across five agents; this scope retains 16 of those runs across four agents, without changing their grades. UI-TARS’s four matching tasks were unsubmitted. Its later five-prompt suite is separate.

- [GitHub bug research](tasks/github-issues.md)
- [Wikipedia research](tasks/wikipedia-research.md)
- [Form completion](tasks/form-completion.md)
- [GitHub enhancement navigation](tasks/github-navigation.md)
- [Popup error recovery](tasks/error-recovery.md)
- [Five later UI-TARS tasks](tasks/ui-tars-supplement.md)

[Per-attempt measurements](results/benchmark-results.csv) · [Screenshots](screenshots/README.md) · [Recorded verification and traces](evidence/) · [Recovered synthetic fixture](fixtures/)

## Dated follow-up

[Three TinyFish form reruns — 22 October 2026](reruns/tinyfish-form-2026-10-22/README.md), compared against the unchanged original Claude result. This is a separately reported browser cohort, not a desktop evaluation or a rewrite of the original additional-task totals.

## Clarified prompt follow-up

[Clarified form: TinyFish ×3 and Claude ×3](reruns/clarified-form-2026-10-22/README.md) is a separate configuration with an unchanged field rubric, an exact clarified shared prompt, 600-second ceilings and a below-$2 additional budget. Historical counts above remain unchanged.

## Authenticated supplier workflows — 22 October 2026

A separate twelve-attempt experiment retains three pilots and three additional uncapped attempts per provider. [Results, setup, costs and evidence](authenticated-workflows/supplier-portal-2026-10-22/README.md) · [Offline verifier](authenticated-workflows/supplier-portal-2026-10-22/verify_complete_experiment.py). Earlier benchmark evidence is unchanged.
