# Evidence and offline validation

[Current public-file manifest](public-manifest.json) describes the bytes actually included here. [Source provenance](source-provenance.json) maps copied files to the existing reviewed archive, with source and publication hashes. Historical source manifests remain evidence of their earlier scope, not a claim every private file is published. [Prompt integrity](prompt-integrity.json) records original file hashes and reconstructed/frozen desktop prompt sources. [Runtime variants](runtime-prompt-variants.json) expose detailed original GitHub instructions rather than assuming one shared short prompt.

Run `python verification/scripts/validate_package.py` from the repository root for offline checks of links, public manifest, prompt files, provider scope, declared desktop grades, raw usage/cost totals and credential/private-path patterns. No model request or live website benchmark is made. Stored browser grades remain evidence-reviewed historical results, not newly regraded live pages. Recovered website target names and issue titles are task data, not evaluated-agent entries.

Desktop graders and 21 disposable/mock cases remain in desktop-benchmarks/scripts and desktop-benchmarks/verification. They do not perform the evaluated task. The saved screenshots and GUI observations support required workflow checks; a model’s own completion claim alone does not.

Sanitized logs, original responses and configurations stay adjacent within agent-owned browser evidence directories or desktop logs. Full local raw sources, private account/control metadata and omitted bulk documentation remain outside this publication. No real keys, cookies, browser profiles, account dumps or private endpoint addresses should be included. The publication safety scan also checks Git-history blob contents before any push.

## TinyFish form follow-up — 22 October 2026

[Offline follow-up grader](../browser-benchmarks/reruns/tinyfish-form-2026-10-22/verify_followup.py) checks three separate attempts, exact prompts, independent observations, retained captures and cost deltas without provider requests. It regrades manually reviewed screenshot observations; it is not automated image recognition. [Current-key exact-value audit](tinyfish-followup-safety.json) and [visual review](tinyfish-followup-review.json) supplement the preserved earlier audits. Package validation now includes this separate cohort while retaining historical browser and desktop checks.

## Clarified form configuration

[Six-run audit](../browser-benchmarks/reruns/clarified-form-2026-10-22/verify_clarified.py) checks exact shared prompts, independently reviewed final observations, 26 raw Claude generations, TinyFish cancelled-counter discrepancies, uncertainty-adjusted spending, and copied artifacts. It does not execute agents or recognize image content automatically. [Visual review](clarified-form-review.json) and [credential-value scan](clarified-form-safety.json) document publication checks. Earlier ambiguous-prompt records and desktop checks remain separate and unchanged.

## Authenticated supplier workflows — 22 October 2026

A separate twelve-attempt experiment retains three pilots and three additional uncapped attempts per provider. [Results, setup, costs and evidence](../browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/README.md) · [Offline verifier](../browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/verify_complete_experiment.py). Earlier benchmark evidence is unchanged.
