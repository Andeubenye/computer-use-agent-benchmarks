# UI-TARS source validation — 20 October 2026

**Outcome: source patch validated offline; development startup blocked. No browser-control success is claimed. Work stopped after one failed development launch.**

## What was preserved

- `/Applications/UI TARS.app` was not modified. Info.plist, executable and app.asar SHA-256 checks match both this attempt's initial baseline and the earlier original-app baseline.
- Desktop application copies/backups were not opened or modified.
- Earlier development checkout, patch, reports and benchmark results were preserved. The sampled earlier source/evidence hashes still match.
- Existing Hugging Face connection/settings were not read, copied or reconfigured. No availability check, inference request, endpoint wake, scaling or billing change was performed. The endpoint's current state was not queried.
- No macOS security protections, permission databases, signing settings or system-wide preferences were changed.

## Source and requirements

Fresh official clone: `work/UI-TARS-desktop-v0.2.4-2026-10-20`, branch `codex/ui-tars-2048-2026-10-20`, tag `v0.2.4`, commit `0ee87301a6db754c5f67909e5fbbcf05233abad9`.

This tag internally labels its Desktop package `0.2.3`; the installed app reports `0.2.4`. The upstream label was preserved. Host is Apple ARM64, 8 GiB RAM, macOS 15.4.1. Node v24.16.0 satisfies the documented >=20 requirement. Default pnpm is 11.25.0; commands used the exact packageManager version 9.10.0 through Corepack, without global changes. Chrome is installed. The remote model was not loaded onto the Mac. Upstream documents single-monitor use; no minimum development RAM was found in the inspected instructions.

## Exact tracked changes

1. `packages/ui-tars/sdk/src/Model.ts`, starting at line 110: UI-TARS 1.5 Chat Completions defaults to `max_tokens: 2048` instead of `65535`. Other versions retain `1000`; explicitly selected Responses behavior remains unchanged. Explicit SDK caller overrides remain possible.
2. `packages/ui-tars/sdk/tests/Model.test.ts`: regression tests cover omitted/false `useResponsesApi`, serialized request arguments, model identity, 2048 output tokens, context arithmetic, action parsing, unchanged other-provider defaults and explicitly selected Responses behavior.

No prompt, action parser, model identity, operator, coordinate handling, screenshot handling or API mode was changed. Local Browser and Local Computer share the SDK configuration; Desktop supplies no completion-token override. Availability checks and remote provider routing were inspected, not exercised or modified.

2048 output tokens leave at most 30720 input tokens in a 32768-token context. Text, images and overhead must still fit; this is not automatic history truncation.

The complete reversible patch is `source.patch`. The lockfile is unchanged.

## Actual checks

| Check | Result |
|---|---|
| Locked dependency installation, pnpm 9.10.0 | Exit 0, 1m 29.9s |
| SDK/parser unit tests | 80 passed in 6 files, 4.70s |
| SDK TypeScript | Passed, exit 0 |
| Desktop main and renderer TypeScript | Passed, exit 0 |
| Compiled SDK request, fetch completely mocked | Passed: Chat Completions, original model name, max_tokens=2048, finished action parsed; no network I/O |
| Source whitespace check / lockfile | Passed / unchanged |
| Official development workflow | Failed, exit 1; one attempt |
| Native development window / permissions | Not verified; Electron did not start |
| UI-TARS controls example.com | Not run |
| Five benchmark tasks | Not run |

Passing negative unit tests emit expected invalid-image/parser diagnostics. An optional `macos-alias` native build failed during installation, but pnpm completed. Its verbose build-environment dump was removed from the saved install log. The separate Electron runtime was missing despite installation success; this report does not establish why its installer failed to leave the executable.

## Startup blocker and stopping point

`launch-dev.sh` called official `pnpm run dev:ui-tars` with pinned pnpm for Turbo's children and an isolated user-data directory. Main/preload bundles built, and Vite started its local renderer at `http://localhost:5173/`. Electron startup then failed:

```text
node_modules/electron/dist/Electron.app/Contents/MacOS/Electron: No such file or directory
ELIFECYCLE Command failed with exit code 1.
```

The workflow exited after approximately 7.35 seconds. No development application reached a native window. No processes belonging to the fresh checkout remained in the final process check. There was no Electron extraction repair, dependency reinstall, second launch, packaged-app modification or security workaround after this failure, following the user's stop condition.

## Credentials, permissions and paid testing

The launcher clears VLM credential/configuration environment variables and uses a new profile. It refuses to launch a profile containing an API key because upstream logs complete settings objects. A full real-credential logging safeguard has not been activated in this fresh checkout. Existing credentials remain untouched; no live connection was claimed.

Accessibility permits keyboard/mouse control; Screen Recording permits screenshots. The repository also notes that development permissions can attach to the launcher (Terminal/iTerm) rather than the installed app. Browser Automation permission may be relevant only if macOS separately requests it. Current permissions for this new executable were not verified because it never launched. No permissions were granted or bypassed.

No request for paid testing approval is made while startup is blocked. A future approved continuation must first resolve reliable development startup, verify credential-safe logs and actual macOS permissions, and then obtain approval before waking the existing endpoint or running a bounded example.com smoke test. Browser-control evidence must come from UI-TARS itself, not a replacement agent. The five tasks remain gated on that real interaction succeeding.

## Reproduce or reverse the source change

Commands and launch script are retained for reproducibility, not a claim that startup currently works. See `COMMANDS.md`, `PLAN.md` and the individual logs.

To reverse only the patch in this new checkout:

```sh
cd work/UI-TARS-desktop-v0.2.4-2026-10-20
git apply --reverse ../../outputs/ui-tars-revalidation-2026-10-20/source.patch
```

This does not affect the original installation or earlier project.

## Sources

- [Official v0.2.4 source](https://github.com/bytedance/UI-TARS-desktop/tree/v0.2.4)
- [Development instructions](https://github.com/bytedance/UI-TARS-desktop/blob/v0.2.4/CONTRIBUTING.md)
- [Browser/macOS prerequisites](https://github.com/bytedance/UI-TARS-desktop/blob/v0.2.4/docs/quick-start.md)
- [Token-limit issue 587](https://github.com/bytedance/UI-TARS-desktop/issues/587): same 65535 completion versus 32768 context problem; original report concerns UI-TARS-2B-SFT/v0.1.1, rather than this exact model/app combination.
