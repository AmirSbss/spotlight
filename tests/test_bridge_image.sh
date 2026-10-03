#!/usr/bin/env bash
# Self-check for gpt-image-2 --image passthrough using a fake codex (spends no ChatGPT quota).
set -euo pipefail
W=~/.claude/skills/gpt-image-bridge/bin/gpt-image-2
# the official bridge has no --image yet; this checks the patched one when it's installed
if [[ ! -x $W ]] || ! grep -q -- '--image' "$W"; then echo "bridge --image: skipped (no bridge with --image installed)"; exit 0; fi
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir "$t/bin"
cat >"$t/bin/codex" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" >"$ARGS_LOG"
while [[ $# -gt 0 ]]; do [[ "$1" == -C ]] && cd "$2"; shift; done
printf 'PNG' >out.png
EOF
chmod +x "$t/bin/codex"
printf 'x' >"$t/photo one.jpg"
export ARGS_LOG="$t/args" PATH="$t/bin:$PATH"

( cd "$t" && "$W" "remove the cup" "$t/o1.png" --image "photo one.jpg" >/dev/null )
grep -qx -- '-i' "$t/args"
grep -qx -- "$t/photo one.jpg" "$t/args"
grep -qx -- '--' "$t/args"
grep -q 'INPUT IMAGE' "$t/args"

"$W" "a sunset" "$t/o2.png" >/dev/null
# `! cmd` never trips set -e, so negative checks need an explicit exit
if grep -qx -- '-i' "$t/args"; then echo "FAIL: -i passed without --image"; exit 1; fi
if grep -q 'INPUT IMAGE' "$t/args"; then echo "FAIL: edit wording without --image"; exit 1; fi

if "$W" "x" "$t/o3.png" --image "$t/missing.jpg" 2>/dev/null; then echo "FAIL: missing image accepted"; exit 1; fi
echo "bridge --image: ok"
