# Methodology and limits

The identical UTF-8 task prompt was frozen before paid execution. All three stored prompt copies and the TinyFish submission goal match its bytes. Claude's task JSON also matches; its summary `task_sha256` hashes the task object, not just the prompt, and must not be compared to the text-file digest. Each actual agent diagnostic had 600 seconds, no custom cost watchdog and no benchmark restart. No previous task was rerun.

The task was to navigate to the same synthetic supplier dashboard, report whether already authenticated, and supply visible evidence. If redirected to sign in, the agent had to stop. It could not enter credentials, log in, submit forms, edit suppliers, execute code, or use direct website APIs. The agents alone chose diagnostic interactions. Unscored setup used the supported TinyFish setup CDP interface or the existing Claude native keyboard executor to establish login; owner-only APIs were used only for independent verification and post-test cleanup.

## Teardown boundaries

TinyFish: create a dedicated non-default Browser Context Profile; open setup browser; log into the existing account; save; disconnect/close setup clients; stop setup Python/children and credential broker. Local Colima was stopped. A separate Python controller then submitted a new remote Web Agent run, passing only the profile handle, provider key and owner verification credentials. The task received no login secret. Provider-internal browser process identities and teardown timing were not exposed. This tests independence from local setup clients, not independently audited physical destruction of every provider process.

Claude original: start the unchanged original no-mount execution configuration and authenticate; request Firefox quit, then stop/remove the container; launch a new container from the same existing image. Claude persistent: separate named container configuration using the same image plus a dedicated named volume at the actual Firefox profile path. Authenticate; request quit; stop/remove; start a fresh container with the same volume. In **both** cases the Firefox quit shortcut did not terminate the container within 25 seconds, so the documented Docker stop fallback was used before removal. There was no live predecessor container during the diagnostic. Do not describe these as clean Firefox exits or a crash-resilience test.

Both Claude cases used ARM64 Linux, Firefox 153.5.0esr, 1024×768, the existing Colima VM, image sha256:195fda83d17d253dbb5d122583fd7d58cdfb13971e16f6fd7c1f73840b07f55d, claude-sonnet-5-5 and computer_toolset_20260801. Each used a fresh model conversation. TinyFish used managed lite browser execution; its exact model/build/browser revision and internal retries were unavailable. Different viewports, hosting, action units, startup visibility and polling prevent a normalized speed or action-efficiency ranking.

## Independent rubric

1. Read the original agent response, final screenshot and server audit independently of model assertions.
2. For restoration, require authenticated dashboard requests attributed to that configuration's fresh setup session, with no intervening login. For the negative diagnosis, require the sign-in screenshot, no authenticated dashboard event, and an unrevoked/unexpired setup session immediately before the run.
3. Require correct visible heading and, for authenticated cases, account label and a real supplier ID. Never feed server verification data or expected outcomes to the model.
4. Require no agent logins or supplier saves; compare all supplier record fields with the latest recovered pre-experiment native database snapshot.
5. Check fresh execution boundaries: exited local setup/controller for TinyFish; different container IDs and intended mounts for Claude.

Authentication restoration is a configuration outcome, separate from diagnostic task accuracy. One observation each cannot establish reliability, production security, performance distributions or lower ownership cost.

## Interruptions and setup changes

The execution environment interrupted the sequential controller after Claude original completed and before a persistent-case paid submission. Its process/RAM became unavailable and Colima was observed stopped; exact cause UNKNOWN. The empty checkpoint was preserved. On continuation the persistent setup raised CalledProcessError before model submission; its owned container was removed, and a bounded volume permission helper succeeded in isolation. A stale container-name conflict is probable from the immediate failure/cleanup evidence, but stderr was not retained, so the exact cause remains UNKNOWN. One targeted clean-runtime repair then completed the persistent case. No TinyFish or Claude-original diagnostic was repeated; exactly three paid diagnostic runs exist. [Interruption record](evidence/interruption-record.json), [failed setup](infrastructure/claude-persistent-infrastructure-attempt-1/), [repair record](evidence/targeted-repair-record.json) and [clarification of inherited fields](evidence/targeted-repair-record-addendum.json).

The prior plaintext synthetic account password had been discarded. Setup temporarily changed only its runtime password hash, deploying the same previously saved portal version, without rebuilding or resetting data. Memory loss required further temporary password setup; three temporary hash configurations were applied in total. The original hash and secret metadata were restored and verified afterward. No personal account or Vault was used. The preserved original benchmark implementation was not edited.

**NOT TESTED:** expired-session reauthentication, Vault, MFA, CAPTCHA, prolonged inactivity, VM/disk loss, remote worker migration, concurrent profile writers, backup restoration, production monitoring or long-term maintenance.
