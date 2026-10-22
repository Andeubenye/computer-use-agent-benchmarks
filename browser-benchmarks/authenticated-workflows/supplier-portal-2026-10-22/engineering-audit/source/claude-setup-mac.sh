#!/bin/sh
# Installs only free tools. Does not load credentials or call Anthropic.
set -eu
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
python3.12 - <<'PY'
import shutil
free = shutil.disk_usage('.').free / 1024**3
if free < 12:
    raise SystemExit(f'Need at least 12 GiB free before Docker setup; currently {free:.1f} GiB. No installation started.')
PY
command -v brew >/dev/null
HOMEBREW_NO_AUTO_UPDATE=1 brew install docker colima
# Dedicated VM, native architecture, no host directory mounts or SSH agent forwarding.
# Sparse disk limits are virtual capacity, not an up-front allocation.
colima start --profile claude-benchmark --cpus 2 --memory 3 --disk 16 \
    --vm-type vz --mount none --ssh-agent=false --ssh-config=false --activate=false
export DOCKER_CONTEXT=colima-claude-benchmark
docker info --format '{{.ServerVersion}}'
uv sync --frozen
uv run --frozen python -m benchmark build
uv run --frozen python -m benchmark start
uv run --frozen python -m benchmark smoke
printf '%s\n' 'Free smoke test finished. Reset with stop/start before any paid run.'
