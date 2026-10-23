# New experiment costs

| Case | Evidence | Usage value USD |
|---|---|---:|
| TinyFish | 3 reported steps × saved $0.016 rate; dedicated before/after wallet decrease agrees | 0.048000 |
| Claude original | 26,991 input +460 output, no cache, at saved $2/$10 per million rates | 0.058582 |
| Claude persistent | 26,985 input +459 output, no cache, same rates | 0.058560 |
| Three new agent diagnostics | Sum of categories above | **0.165142** |

[Wallet reconciliation](evidence/wallet-reconciliation.json) and each native run's raw usage responses support these amounts. TinyFish setup's immediate observed wallet change was $0.000; this is not proof that setup/hosting is free, because delayed or unitemized charges cannot be excluded. No invoice reconciliation or itemized host charge was obtained. Claude estimates exclude the local Mac/Colima/Docker/browser host, electricity, integration and maintenance. No provider-credit purchases/top-ups were made, and no funding error occurred. These are usage values, not necessarily cash out of pocket.

There were four generation requests plus four token-count calls per Claude case, zero SDK retries, zero uncertain billed failures and no paid persistent-case submission during its infrastructure failure. Exactly one actual diagnostic per configuration was paid. Provider-internal TinyFish retries are not exposed. No artificial spending watchdog interrupted the runs.

TinyFish's diagnostic usage was lower than either Claude diagnostic here. In the earlier three uncapped supplier-update workflows, Claude was faster and cheaper in recorded API usage. These are different tasks/cohorts; do not reverse or merge those findings. Hosting, setup labor and maintenance remain UNKNOWN in money terms. Do not claim TinyFish is cheaper overall or that these three observations measure production ownership costs.
