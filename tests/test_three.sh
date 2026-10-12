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

# routes: a globe with two routes. Accent pixels (points, routes) are absent before anything pops in, present after
ROUTES='points: [ { id: "dxb", lat: 25.25, lon: 55.36, at: 0.2 }, { id: "lhr", lat: 51.47, lon: -0.45, at: 0.3 }, { id: "ika", lat: 35.42, lon: 51.15, at: 0.4 } ],
  routes: [ { from: "dxb", to: "lhr", at: 0.8, dur: 1.4 }, { from: "dxb", to: "ika", at: 1.4, dur: 1.0 } ]'
g="$t/routes"
page "$g" "window.SPOTLIGHT = { width: 320, height: 568, duration: 3, grain: 0, shots: [ { a: 0, b: 3, three: \"three/routes.js\", params: { $ROUTES } } ] };"
(cd "$g" && CAPTURE_WORKERS=1 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null) || fail "routes capture failed"
accent() { $IM "$1" -fx '(r>0.78 && g>0.55 && b<0.4) ? 1 : 0' -format '%[fx:int(mean*w*h)]' info:; }
a0=$(accent "$g/out/00003.jpg"); a1=$(accent "$g/out/00087.jpg")
(( a0 < 5 && a1 > 60 )) || fail "routes don't draw in (accent pixels $a0 at 0.1 s, $a1 at 2.9 s)"
(cd "$g/out" && md5sum *.jpg) > "$t/routes.md5"
(cd "$g" && CAPTURE_WORKERS=3 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null)
(cd "$g/out" && md5sum -c --quiet "$t/routes.md5") || fail "parallel routes capture changed pixels"
# anchors: centred on London, London's label sits at the frame centre; centred on its antipode, it hides
probe() {  # probe <dir> <t> <anchor id> -> "left top opacity" of that anchor's element after render(t)
  (cd "$1" && node --input-type=module -e "
    import { launch } from '$ROOT/skills/spotlight/scripts/browser.mjs';
    import { pathToFileURL } from 'node:url';
    const b = await launch(), p = await b.newPage({ viewport: { width: 320, height: 568 } });
    await p.goto(pathToFileURL(process.cwd() + '/scene.html').href); await p.evaluate(() => window.ready);
    console.log(await p.evaluate(async ([t, id]) => { await window.render(t); const s = document.querySelector('[data-anchor=' + id + ']').style;
      return [parseFloat(s.left), parseFloat(s.top), +s.opacity].join(' '); }, [$2, '$3']));
    await b.close();")
}
for c in "51.47, -0.45" "-51.47, 179.55"; do
  d="$t/anchor$RANDOM"
  page "$d" "window.SPOTLIGHT = { width: 320, height: 568, duration: 3, grain: 0, shots: [ { a: 0, b: 3, three: \"three/routes.js\", params: { $ROUTES, center: { from: [$c], to: [$c] } } } ] };" \
    '<div data-anchor="lhr"></div>'
  read -r x y o <<< "$(probe "$d" 1.5 lhr)"
  if [[ $c == 51* ]]; then
    python3 -c "import sys; sys.exit(not (abs($x - 160) < 2 and abs($y - 284) < 2 and $o > 0.95))" || fail "London's anchor at $x,$y ($o), want 160,284"
  else
    python3 -c "import sys; sys.exit(not ($o < 0.01))" || fail "London's label shows ($o) with London on the far side"
  fi
done

# extrude: the fixture logo (an amber circle) fills the centre from the first frame, turns, and captures identically
e="$t/extrude"
page "$e" 'window.SPOTLIGHT = { width: 320, height: 568, duration: 2, grain: 0, shots: [ { a: 0, b: 2, three: "three/extrude.js", params: { svg: "logo.svg" } } ] };'
cp "$ROOT/tests/fixtures/site/logo.svg" "$e/"
(cd "$e" && CAPTURE_WORKERS=1 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null) || fail "extrude capture failed"
read -r r g b <<< "$(px "$e/out/00000.jpg" 160 284)"; (( r > 150 && g > 90 && b < 90 )) || fail "extruded logo not in the centre at frame 0 ($r $g $b)"
ae=$($CMP -metric AE -fuzz 3% "$e/out/00000.jpg" "$e/out/00059.jpg" null: 2>&1 | cut -d' ' -f1) || true
(( ${ae%.*} > 300 )) || fail "the extruded logo doesn't move ($ae px changed)"
(cd "$e/out" && md5sum *.jpg) > "$t/extrude.md5"
(cd "$e" && CAPTURE_WORKERS=3 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null)
(cd "$e/out" && md5sum -c --quiet "$t/extrude.md5") || fail "parallel extrude capture changed pixels"

# a bad module path is a loud error naming the path
x="$t/bad"
page "$x" 'window.SPOTLIGHT = { width: 320, height: 568, duration: 1, shots: [ { a: 0, b: 1, three: "three/nope.js" } ] };'
if out=$(cd "$x" && node "$ROOT/skills/spotlight/scripts/capture.mjs" stills 0 2>&1); then fail "bad module path accepted"; fi
grep -q "three/nope.js" <<< "$out" || fail "error doesn't name the module: $out"
echo "three: ok"
