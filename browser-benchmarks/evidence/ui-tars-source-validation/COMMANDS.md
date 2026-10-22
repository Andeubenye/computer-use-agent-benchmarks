# Commands — 20 October 2026

Working directory is the original project root unless specified.

## Inspect only

```sh
uname -m
sw_vers
sysctl -n hw.memsize
node --version
pnpm --version
corepack pnpm@9.10.0 --version
git --version
```

Repository instructions: `CONTRIBUTING.md`, `docs/quick-start.md`, `package.json`, `.node-version`, `.npmrc`. Previous source/launch reports were read, not edited. Original installed app baseline is in `installed-app-before.json`.

## Fresh source

```sh
git clone --branch v0.2.4 --single-branch --depth 1 https://github.com/bytedance/UI-TARS-desktop.git work/UI-TARS-desktop-v0.2.4-2026-10-20
cd work/UI-TARS-desktop-v0.2.4-2026-10-20
git rev-parse HEAD
git switch -c codex/ui-tars-2048-2026-10-20
git apply --check ../../outputs/ui-tars-v0.2.4-token-fix.patch
git apply ../../outputs/ui-tars-v0.2.4-token-fix.patch
git diff --check
```

## Install and offline validation (from fresh checkout)

```sh
env -u VLM_PROVIDER -u VLM_BASE_URL -u VLM_API_KEY -u VLM_MODEL_NAME -u UI_TARS_APP_PRIVATE_KEY_BASE64 corepack pnpm@9.10.0 install --frozen-lockfile --child-concurrency=1 --network-concurrency=8
corepack pnpm@9.10.0 exec vitest run --config ../../outputs/ui-tars-revalidation-2026-10-20/vitest.offline.config.mjs
corepack pnpm@9.10.0 exec tsc --noEmit -p packages/ui-tars/sdk/tsconfig.json
corepack pnpm@9.10.0 --filter ui-tars-desktop run typecheck
node ../../outputs/ui-tars-revalidation-2026-10-20/verify-built-sdk.mjs
```

See the separate logs for actual exit codes/results; listing a command here does not imply success.

## Development startup

```sh
bash outputs/ui-tars-revalidation-2026-10-20/launch-dev.sh
```

This uses the official `pnpm run dev:ui-tars`, a local Corepack shim for Turbo children, and `ELECTRON_EXEC_PATH` to pass the isolated user-data directory. It clears VLM environment variables and refuses a credential-bearing profile. It does not run inference or manage Hugging Face. Stop with Ctrl-C in the owning terminal.

No installed ASAR was unpacked, patched, resigned, or replaced. No macOS protections/permissions or Hugging Face endpoint settings were changed.
