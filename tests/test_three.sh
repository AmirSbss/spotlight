#!/usr/bin/env bash
# Self-check for three shots: WebGL frames are drawn (not blank), move with t, are identical in serial and parallel
# capture, DOM labels follow module anchors, and a bad module path stops the capture with the path in the error.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
K="$ROOT/skills/spotlight/kit"
IM=$(command -v magick >/dev/null && echo "magick" || echo "convert")
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
npm i --silent --prefer-offline --prefix "$t" playwright-core >/dev/null 2>&1
fail() { echo "FAIL: $*"; exit 1; }
px() { $IM "$1" -format "%[fx:int(255*p{$2,$3}.r)] %[fx:int(255*p{$2,$3}.g)] %[fx:int(255*p{$2,$3}.b)]" info:; }
# page <dir> <timeline js> [extra html before #end]: a work folder with the kit, three/ and node_modules
page() {
  mkdir -p "$1/three"; cp "$K/scene.html" "$K/kit.js" "$1/"; cp "$K"/three/*.js "$ROOT/tests/fixtures/three-spin.js" "$1/three/"
  : > "$1/fonts.css"; ln -sfn "$t/node_modules" "$1/node_modules"; echo "$2" > "$1/timeline.js"
  python3 - "$1/scene.html" "${3:-}" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
open(p, "w").write(s.replace('<div id="end">', sys.argv[2] + '\n  <div id="end">'))
PY
}

s="$t/spin"
page "$s" 'window.SPOTLIGHT = { width: 320, height: 568, duration: 2, grain: 0, shots: [ { a: 0, b: 2, three: "three/three-spin.js" } ] };' \
  '<div data-anchor="top" style="background:#0f0;width:20px;height:20px"></div>'
(cd "$s" && CAPTURE_WORKERS=1 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames 2>&1 >/dev/null | tail -5) || fail "spin capture failed"
read -r r g b <<< "$(px "$s/out/00030.jpg" 160 284)"
(( r > 120 && b < 120 )) || fail "three frame is blank or not the accent cube ($r $g $b)"
CMP=$(command -v magick >/dev/null && echo "magick compare" || echo compare)
ae=$($CMP -metric AE -fuzz 3% "$s/out/00000.jpg" "$s/out/00059.jpg" null: 2>&1 | cut -d' ' -f1) || true
(( ${ae%.*} > 500 )) || fail "the cube doesn't move ($ae px changed)"
(cd "$s/out" && md5sum *.jpg) > "$t/serial.md5"
(cd "$s" && CAPTURE_WORKERS=3 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null)
(cd "$s/out" && md5sum -c --quiet "$t/serial.md5") || fail "parallel three capture changed pixels"
# an anchored element is centred on its anchor: (0, 1.2, 0) projects to x 160, y ~104 at 320x568 (fov 35, z 6)
read -r r g b <<< "$(px "$s/out/00030.jpg" 160 104)"; (( g > 200 && r < 80 )) || fail "anchored label not on its anchor ($r $g $b)"
read -r r g b <<< "$(px "$s/out/00030.jpg" 160 128)"; (( g < 200 || r > 80 )) || fail "anchored label too big or too low"

# a bad module path is a loud error naming the path
x="$t/bad"
page "$x" 'window.SPOTLIGHT = { width: 320, height: 568, duration: 1, shots: [ { a: 0, b: 1, three: "three/nope.js" } ] };'
if out=$(cd "$x" && node "$ROOT/skills/spotlight/scripts/capture.mjs" stills 0 2>&1); then fail "bad module path accepted"; fi
grep -q "three/nope.js" <<< "$out" || fail "error doesn't name the module: $out"
echo "three: ok"
