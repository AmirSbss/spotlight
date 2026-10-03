#!/usr/bin/env bash
# What spotlight needs. Required tools missing -> exit 1.
set -u
ok=1
have() { eval "$1" >/dev/null 2>&1; }
req() { if have "$2"; then printf '  ok    %s\n' "$1"; else printf '  MISS  %s: %s\n' "$1" "$3"; ok=0; fi; }
opt() { if have "$2"; then printf '  ok    %s (optional)\n' "$1"; else printf '  --    %s (optional): %s\n' "$1" "$3"; fi; }
echo "spotlight doctor"
req "ffmpeg + ffprobe" "command -v ffmpeg && command -v ffprobe" "install ffmpeg 4.4+ (apt install ffmpeg / brew install ffmpeg)"
req "ffmpeg zscale filter (HDR tone-mapping)" "ffmpeg -hide_banner -filters | grep -q ' zscale '" "use an ffmpeg build with libzimg"
req "ImageMagick" "command -v magick || command -v convert" "apt install imagemagick / brew install imagemagick"
req "Python 3.8+" "python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))'" "install python3"
req "Node.js 18+" "node -e 'process.exit(+(+process.versions.node.split(\".\")[0] < 18))'" "install Node.js 18+"
req "Chromium" "test -n \"\${CHROMIUM:-}\" || command -v chromium || command -v chromium-browser || command -v google-chrome || test -d '/Applications/Google Chrome.app' || ls -d ~/.cache/ms-playwright/chromium-* ~/Library/Caches/ms-playwright/chromium-*" "install Chromium or Chrome, run 'npx playwright install chromium', or set CHROMIUM=/path/to/chrome"
opt "uv (music tempo and cues)" "command -v uv" "https://docs.astral.sh/uv/"
opt "piper (narration, phase 2)" "command -v piper" "uv tool install piper-tts"
opt "codex + gpt-image-bridge (AI images)" "command -v codex && test -x ~/.claude/skills/gpt-image-bridge/bin/gpt-image-2" "https://github.com/oakplank/gpt-image-bridge"
if [[ $ok == 1 ]]; then echo "ready"; else echo "missing required tools"; exit 1; fi
