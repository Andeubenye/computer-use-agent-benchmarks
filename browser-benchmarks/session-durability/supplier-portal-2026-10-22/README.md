# Session durability without Vault

One new read-only diagnostic in each of three configurations. Agent execution occurred on 22 October UTC; final cleanup and publication preparation crossed into 23 October in Africa/Lagos. Earlier benchmarks and the engineering audit remain unchanged.

| Configuration | Authentication restored after teardown | Agent diagnosis | Agent time | API usage value |
|---|---|---|---:|---:|
| TinyFish saved Browser Context Profile, new controller/run | Yes | Correct authenticated dashboard | 36.94 s | $0.048000 |
| Claude original disposable container, new container | No | Correct sign-in page | 22.03 s | $0.058582 estimated |
| Claude separate persistent Firefox volume, new container | Yes | Correct authenticated dashboard | 20.98 s | $0.058560 estimated |

TinyFish managed saved state and remote browser execution. Claude also retained authentication once I explicitly kept its Firefox profile outside the disposable container. This compares storage configurations, not unique model capabilities. Three diagnostic tasks completed correctly; two configurations restored authentication. One observation per configuration is not a reliability rate.

[Detailed results](RESULTS.md) · [Frozen task](task-prompt.txt) · [Methodology](METHODOLOGY.md) · [Costs](COSTS.md) · [Setup and ownership](SETUP.md) · [Article-ready summary](ARTICLE-READY.md) · [Offline verifier](verify_durability.py) · [Verification output](verification.json)

Vault, expired-session reauthentication, MFA, CAPTCHA, VM/disk loss, multi-tenant scaling and long-term retention: **NOT TESTED**. No artificial spending watchdogs, previous benchmark reruns, provider-credit purchases, new model/image builds or portal source rebuilds. A pre-submission infrastructure failure and its targeted repair are retained separately.
