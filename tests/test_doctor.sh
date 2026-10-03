#!/usr/bin/env bash
# Self-check for doctor.sh: passes here, and names ffmpeg when it isn't on PATH.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
D="$ROOT/skills/spotlight/scripts/doctor.sh"
out=$(bash "$D"); grep -q "^ready" <<< "$out" || { echo "FAIL: doctor not ready here"; echo "$out"; exit 1; }
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
for b in bash env node python3 grep ls test sed head; do ln -s "$(command -v $b)" "$t/$b"; done
if out=$(PATH="$t" bash "$D" 2>&1); then echo "FAIL: doctor passed without ffmpeg"; exit 1; fi
grep -q "MISS.*ffmpeg" <<< "$out" || { echo "FAIL: ffmpeg not named"; echo "$out"; exit 1; }
echo "doctor: ok"
