# Additional setup and operational ownership

I reused the portal, provider adapters, synthetic account, action executor, local Linux image and previous engineering audit. No dependencies were installed and no image/portal source was rebuilt.

| Responsibility | TinyFish saved context | Claude original | Claude persistent configuration |
|---|---|---|---|
| Browser host/lifecycle | Provider | Existing developer VM/container | Same developer VM/container |
| Saved session state across execution removal | Provider Profile API | No external storage configured | Dedicated Docker volume mounted at Firefox profile path |
| Initial login and authorization | My setup client | My setup routine | My setup routine |
| Action decisions | Provider Web Agent | Claude native computer tool | Same Claude tool |
| Action execution/screenshots | Provider | Reused developer executor | Same executor |
| Profile permissions and mount | Provider implementation uninspected | N/A | My bounded initialization and mount |
| Profile backup, encryption, isolation, rotation, concurrency | Provider internals not audited; application policy remains mine | Not configured | My production responsibility; not implemented or priced here |
| Correctness/timeout/API keys/audit | My shared application/harness | My shared application/harness | Same |
| Cleanup | Close setup clients; revoke test session | Remove container, stop VM | Remove container, separately remove experiment volume, stop VM |

## What changed for Claude

A separate [runtime helper](harness/executed-source/persistent_runtime.py#L5) added **24 physical lines / 23 code-bearing lines / 32 Python AST statements**. It covers volume creation/ownership, container start with mount, controlled stop/remove and label-checked volume deletion. This is the measured helper scope, not all test-harness additions, a minimum production implementation or developer hours. The original implementation stayed unchanged. [Prior full audit](../../authenticated-workflows/supplier-portal-2026-10-22/ENGINEERING-EFFORT-AUDIT.md).

Representative source excerpts (full source and provenance are retained):

```python
VOLUME='manicule-durability-firefox-20261022'
# Existing image and executor; add persistent storage outside container filesystem.
'--mount', f'type=volume,source={VOLUME},target=/home/agent/profile'
```

[Initializer and mount, lines 5–11](harness/executed-source/persistent_runtime.py#L5); [shutdown and cleanup, lines 12–24](harness/executed-source/persistent_runtime.py#L12). The one-time volume initializer used a network-disabled helper with only CHOWN capability; running desktops remained non-root with dropped capabilities and no-new-privileges. I managed profile ownership, shutdown/flush attempt, attachment to the next container and eventual volume deletion. No browser cookie/profile database was exported or published.

TinyFish's actual new-run options were:

```python
use_profile=True
profile_id=setup['profile_id']
use_vault=False
```

That removed my need to mount/store/reattach its browser profile on my execution host. I still had to create and save the profile, establish authorized access, select the correct profile, protect provider keys, monitor the run and independently verify the result. TinyFish did not remove application-level responsibility.

## Timings and manual work

The automated TinyFish login/save routine took 20.46 seconds plus 0.97 seconds for Profile creation. Claude's login routines took 15.15 seconds (original) and 13.82 seconds (persistent). Persistent initial runtime setup/start took 3.40 seconds; subsequent new-container browser readiness took 2.29 seconds. The completed persistent lifecycle, including login, stop, restart, agent and collection, took 71.99 seconds, **excluding** earlier interrupted/failed setup, VM boot, credential configuration/deployments and authoring.

Source files and recorded timestamps show that profile configuration was written before Claude execution, and the successful persistent pass occurred at 23:24:42–23:25:54 UTC. They do not measure focused human labor. Controller/RAM interruption, restoring runtime access, a failed setup, password-hash deployments and offline investigation added elapsed operational work; they cannot be attributed solely to Claude or counted as invented developer hours. Full development time: **UNKNOWN**. No human GUI intervention was needed during any of the three model diagnostics; programmatic unscored login and operator preparation were required before them.

The former engineering audit only established Claude's live-container reuse. This separate experiment extends the evidence to restoration after container removal. It does not make TinyFish uniquely capable of persistent sessions, or require every Claude application to use this architecture. Anthropic's separate [Browser Use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool), [SDK drivers](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk) and [managed integrations](https://platform.claude.com/docs/en/managed-agents/overview) have different ownership boundaries; they were not benchmarked.
