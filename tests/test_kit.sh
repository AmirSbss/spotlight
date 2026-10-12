#!/usr/bin/env bash
# Self-check for skills/spotlight/kit: frame lookup, panel shots and the end card, vertical and landscape.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
IM=$(command -v magick >/dev/null && echo "magick" || echo "convert")
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
npm i --silent --prefer-offline --prefix "$t" playwright-core >/dev/null 2>&1
px() { $IM "$1" -format "%[fx:int(255*p{$2,$3}.r)] %[fx:int(255*p{$2,$3}.g)] %[fx:int(255*p{$2,$3}.b)]" info:; }
for fmt in 320x568 568x320; do
  W=${fmt%x*}; H=${fmt#*x}; w="$t/$fmt"
  mkdir -p "$w/frames/a"
  cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$w/"
  : > "$w/fonts.css"
  $IM -size 60x60 xc:white "$w/logo.png"
  # clip frames colored by index, so a wrong frame lookup is visible
  for i in $(seq 1 30); do $IM -size 64x64 "xc:rgb($(( (i-1)*8 )),0,$(( 255-(i-1)*8 )))" "$w/frames/a/$(printf '%05d' $i).jpg"; done
  # other-aspect media for this format: a wide still in vertical, a tall one in landscape
  if (( W < H )); then $IM -size 640x360 xc:red "$w/wide.png"; else $IM -size 360x640 xc:red "$w/wide.png"; fi
  cat > "$w/timeline.js" <<JS
window.SPOTLIGHT = { width: $W, height: $H, duration: 2.0, end: 1.5,
  shots: [ { a: 0, b: 1, clip: "frames/a", n: 30, push: [1, 1] },
           { a: 1, b: 1.5, still: "wide.png", panel: true, push: [1, 1] } ] };
JS
  (cd "$w" && node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null)
  n=$(ls "$w"/out/*.jpg | wc -l); [[ $n -eq 60 ]] || { echo "FAIL $fmt: $n frames"; exit 1; }
  for i in $(seq 0 29); do  # frame i at t=i/30 must show clip frame i+1 (the 1e-6 floor fix)
    read -r r g b <<< "$(px "$w/out/$(printf '%05d' $i).jpg" $((W/2)) $((H/2)))"
    (( r - i*8 < 10 && i*8 - r < 10 && b - (255-i*8) < 10 && (255-i*8) - b < 10 )) || { echo "FAIL $fmt: frame $i shows r=$r b=$b"; exit 1; }
  done
  read -r r g b <<< "$(px "$w/out/00036.jpg" $((W/2)) $((H/2)))"
  (( r > 200 && g < 60 )) || { echo "FAIL $fmt: panel not shown ($r $g $b)"; exit 1; }
  read -r r g b <<< "$(px "$w/out/00036.jpg" 3 3)"
  (( r < 170 )) || { echo "FAIL $fmt: panel background not dimmed ($r)"; exit 1; }
  read -r r g b <<< "$(px "$w/out/00055.jpg" $((W/2)) $((H-4)))"
  (( r > 220 && g > 220 )) || { echo "FAIL $fmt: end card not in ($r $g $b)"; exit 1; }
done
# a gap in the timeline is a readable error, not a stack trace
g="$t/gap"; mkdir -p "$g"
cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$g/"; : > "$g/fonts.css"; cp "$t/320x568/wide.png" "$g/"
echo 'window.SPOTLIGHT = { width: 320, height: 568, duration: 2, shots: [ { a: 0, b: 1, still: "wide.png" }, { a: 1.5, b: 2, still: "wide.png" } ] };' > "$g/timeline.js"
ln -s "$t/node_modules" "$g/node_modules"
if out=$(cd "$g" && node "$ROOT/skills/spotlight/scripts/capture.mjs" stills 0 2>&1); then echo "FAIL: gap accepted"; exit 1; fi
grep -q "gap" <<< "$out" || { echo "FAIL: gap error unclear: $out"; exit 1; }
# web shot: a tall page scrolls from y0 to y1 at the output width
k="$t/web"; mkdir -p "$k"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$k/"; : > "$k/fonts.css"
ln -s "$t/node_modules" "$k/node_modules"
$IM -size 320x500 xc:red -size 320x1000 xc:gray50 -size 320x500 xc:blue -append "$k/full.png"
echo 'window.SPOTLIGHT = { width: 320, height: 568, duration: 1, shots: [ { a: 0, b: 1, web: "full.png", scroll: [0, 1432] } ] };' > "$k/timeline.js"
(cd "$k" && node "$ROOT/skills/spotlight/scripts/capture.mjs" stills 0 0.99 >/dev/null)
read -r r g b <<< "$(px "$k/check/t0.00.png" 160 100)"; (( r > 200 && b < 60 )) || { echo "FAIL: web shot top not red ($r $g $b)"; exit 1; }
read -r r g b <<< "$(px "$k/check/t0.99.png" 160 500)"; (( b > 200 && r < 60 )) || { echo "FAIL: web shot not scrolled to the bottom ($r $g $b)"; exit 1; }

# a long text card over a blurred still: never reads as frozen (no hold > 0.6 s), with grain off so it can't cheat;
# 8 s, because a fixed push/drift spread over a long card slows into holds
c="$t/card"; mkdir -p "$c"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$c/"; : > "$c/fonts.css"
ln -s "$t/node_modules" "$c/node_modules"
ffmpeg -v error -y -f lavfi -i "testsrc2=size=640x1136" -frames:v 1 "$c/bg.jpg"
cat > "$c/timeline.js" <<'JS'
window.SPOTLIGHT = { width: 320, height: 568, duration: 8, grain: 0,
  shots: [ { a: 0, b: 8, still: "bg.jpg", filter: "blur(16px) brightness(.42)" } ] };
JS
python3 - "$c/scene.html" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
card = '<div class="cap mid" data-a="0.2" data-b="7.9"><div class="rule"></div><div class="row" data-at="0.3"><span class="n">01</span><span class="t">First</span></div><div class="row" data-at="0.5"><span class="n">02</span><span class="t">Second</span></div></div>'
open(p, "w").write(s.replace('<div id="end">', card + '\n  <div id="end">'))
PY
(cd "$c" && node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && python3 "$ROOT/skills/spotlight/scripts/footage.py" encode out none card.mp4 >/dev/null)
python3 "$ROOT/skills/spotlight/scripts/footage.py" check "$c/card.mp4" --out "$c/chk" >/dev/null || true
python3 -c "import json,sys; r=json.load(open('$c/chk/check.json')); h=r['frozen']['long_holds']; sys.exit(0 if not h else print('FAIL: card holds', h) or 1)"
# a natural-looking backdrop (seeded plasma, made here: no image is committed): a plain still, then a text card over its
# blurred copy (blur(5px) at 320 px wide is blur(16px) at 1080). Stills move at a constant speed, so neither the still's
# ends nor the card read as frozen; the high-contrast testsrc2 above would pass with far less motion
n="$t/natural"; mkdir -p "$n"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$n/"; : > "$n/fonts.css"
ln -s "$t/node_modules" "$n/node_modules"
$IM -seed 3 -size 640x1136 plasma:fractal "$n/bg.jpg"
cat > "$n/timeline.js" <<'JS'
window.SPOTLIGHT = { width: 320, height: 568, duration: 7, grain: 0,
  shots: [ { a: 0, b: 3, still: "bg.jpg" }, { a: 3, b: 7, still: "bg.jpg", filter: "blur(5px) brightness(.42)" } ] };
JS
python3 - "$n/scene.html" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
card = '<div class="cap mid" data-a="3.2" data-b="6.9"><div class="rule"></div><div class="row" data-at="3.3"><span class="n">01</span><span class="t">First</span></div><div class="row" data-at="3.5"><span class="n">02</span><span class="t">Second</span></div></div>'
open(p, "w").write(s.replace('<div id="end">', card + '\n  <div id="end">'))
PY
(cd "$n" && node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && python3 "$ROOT/skills/spotlight/scripts/footage.py" encode out none n.mp4 >/dev/null)
python3 "$ROOT/skills/spotlight/scripts/footage.py" check "$n/n.mp4" --out "$n/chk" >/dev/null || true
python3 -c "import json,sys; f=json.load(open('$n/chk/check.json'))['frozen']; sys.exit(0 if not f['long_holds'] and f['total'] < 0.3 else print('FAIL: natural backdrop frozen', f['total'], 's, holds', f['holds']) or 1)"
# parallel capture changes no pixel, even when only some workers ever render a web shot
q="$t/purity"; mkdir -p "$q"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$q/"; : > "$q/fonts.css"
ln -s "$t/node_modules" "$q/node_modules"; cp "$k/full.png" "$t/card/bg.jpg" "$q/"; $IM -size 640x360 xc:red "$q/wide.png"
echo 'window.SPOTLIGHT = { width: 540, height: 960, duration: 3, shots: [ { a: 0, b: 1, still: "bg.jpg", filter: "blur(8px) brightness(.42)" }, { a: 1, b: 2, web: "full.png", scroll: [0, 600] }, { a: 2, b: 3, still: "wide.png", panel: true } ] };' > "$q/timeline.js"
(cd "$q" && CAPTURE_WORKERS=1 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && (cd out && md5sum *.jpg) > serial.md5 \
  && CAPTURE_WORKERS=7 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && (cd out && md5sum -c --quiet ../serial.md5)) \
  || { echo "FAIL: parallel capture changed pixels"; exit 1; }
# a slow web scroll (44 px over 4.4 s, like 150 px at 1080 wide) keeps moving: web shots scroll at a constant speed,
# where an eased scroll stalls at both ends and reads as frozen
v="$t/webslow"; mkdir -p "$v"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$v/"; : > "$v/fonts.css"
ln -s "$t/node_modules" "$v/node_modules"
$IM -seed 5 -size 320x2400 plasma:fractal "$v/page.png"
echo 'window.SPOTLIGHT = { width: 320, height: 568, duration: 4.4, grain: 0, shots: [ { a: 0, b: 4.4, web: "page.png", scroll: [0, 44] } ] };' > "$v/timeline.js"
(cd "$v" && node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && python3 "$ROOT/skills/spotlight/scripts/footage.py" encode out none v.mp4 >/dev/null)
python3 "$ROOT/skills/spotlight/scripts/footage.py" check "$v/v.mp4" --out "$v/chk" >/dev/null || true
python3 -c "import json,sys; f=json.load(open('$v/chk/check.json'))['frozen']; sys.exit(0 if not f['long_holds'] and f['total'] < 0.3 else print('FAIL: slow web scroll frozen', f['total'], 's, holds', f['holds']) or 1)"
# a web shot honours push and filter like any other shot: held on one spot it zooms, and brightness(.6) darkens it
u="$t/webpush"; mkdir -p "$u"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$u/"; : > "$u/fonts.css"
ln -s "$t/node_modules" "$u/node_modules"
$IM -seed 7 -size 320x1200 plasma:fractal "$u/page.png"
echo 'window.SPOTLIGHT = { width: 320, height: 568, duration: 1, grain: 0, shots: [ { a: 0, b: 1, web: "page.png", scroll: [100, 100], push: [1, 1.3], filter: "brightness(.6)" } ] };' > "$u/timeline.js"
(cd "$u" && node "$ROOT/skills/spotlight/scripts/capture.mjs" stills 0 0.99 >/dev/null)
CMP=$(command -v magick >/dev/null && echo "magick compare" || echo compare)
ae=$($CMP -metric AE -fuzz 5% "$u/check/t0.00.png" "$u/check/t0.99.png" null: 2>&1 | cut -d' ' -f1) || true
(( ${ae%.*} > 1000 )) || { echo "FAIL: web shot ignored push ($ae px changed)"; exit 1; }
lum() { $IM "$@" -colorspace gray -format '%[fx:mean]' info:; }
python3 -c "import sys; r = $(lum "$u/check/t0.00.png") / $(lum "$u/page.png" -crop 320x568+0+100); sys.exit(0 if 0.45 < r < 0.75 else print('FAIL: web shot ignored filter, luma ratio', r) or 1)"
# charts: bars settle at heights in the data's ratio, a number settles on its exact source string (Persian digits and
# separator kept) and counts up in the same digits, a donut's arcs follow the data, every chart stays inside the side
# margins in both formats, and parallel capture changes no pixel
CHARTS=$(cat <<'HTML'
<div class="cap mid" data-a="0.1" data-b="2.9"><div class="chart" data-kind="bar" data-values='[10, 20, "40"]' data-labels='["A", "B", "C"]' data-at="0.2" data-dur="1"></div>
  <div class="chart" data-kind="number" data-value="۱۲٬۴۰۰" data-at="0.2" data-dur="1" lang="fa"></div>
  <div class="chart" data-kind="donut" data-values='["25%", "75%"]' data-labels='["x", "y"]' data-at="0.2" data-dur="1"></div>
  <div class="chart" data-kind="line" data-values='[3, 1, 4, 1, 5]' data-labels='["1", "2", "3", "4", "5"]' data-at="0.2" data-dur="1"></div></div>
HTML
)
for fmt in 320x568 568x320; do
  W=${fmt%x*}; H=${fmt#*x}; c="$t/chart$fmt"; mkdir -p "$c"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$c/"; : > "$c/fonts.css"
  ln -s "$t/node_modules" "$c/node_modules"; $IM -size 64x64 xc:gray20 "$c/bg.png"
  echo "window.SPOTLIGHT = { width: $W, height: $H, duration: 3, grain: 0, shots: [ { a: 0, b: 3, still: \"bg.png\" } ] };" > "$c/timeline.js"
  python3 - "$c/scene.html" "$CHARTS" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read(); open(p, "w").write(s.replace('<div id="end">', sys.argv[2] + '\n  <div id="end">'))
PY
  out=$(cd "$c" && node --input-type=module -e "
    import { launch } from '$ROOT/skills/spotlight/scripts/browser.mjs';
    import { pathToFileURL } from 'node:url';
    const b = await launch(), p = await b.newPage({ viewport: { width: $W, height: $H } });
    p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
    await p.goto(pathToFileURL(process.cwd() + '/scene.html').href); await p.evaluate(() => window.ready);
    const at = (t) => p.evaluate(async (t) => { await window.render(t);
      const q = (s) => [...document.querySelectorAll(s)];
      const side = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--side'));
      return { bars: q('.chart .bar').map((e) => e.getBoundingClientRect().height),
               num: q('.chart[data-kind=number]')[0].textContent,
               arcs: q('.chart[data-kind=donut] .seg').map((e) => parseFloat(e.getAttribute('stroke-dasharray'))),
               line: +q('.chart[data-kind=line] .ln')[0].style.strokeDashoffset,
               inside: q('.chart').every((e) => { const r = e.getBoundingClientRect(); return r.width > 10 && r.left >= side - 1 && r.right <= innerWidth - side + 1; }) }; }, t);
    console.log(JSON.stringify({ mid: await at(0.7), end: await at(1.8) }));
    await b.close();")
  python3 - "$out" "$fmt" <<'PY' || { echo "FAIL $fmt: charts"; echo "$out"; exit 1; }
import json, sys
r = json.loads(sys.argv[1].splitlines()[-1]); e, m = r["end"], r["mid"]
b = e["bars"]; assert len(b) == 3 and b[0] > 4 and abs(b[1] / b[0] - 2) < 0.04 and abs(b[2] / b[0] - 4) < 0.08, b
assert e["num"] == "۱۲٬۴۰۰", e["num"]
assert set(m["num"]) <= set("۰۱۲۳۴۵۶۷۸۹٬") and 0 < int(m["num"].replace("٬", "").translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))) < 12400, m["num"]
a = e["arcs"]; assert len(a) == 2 and abs(a[1] / a[0] - 3) < 0.05, a
assert e["line"] < 0.001 and m["line"] > 0.01, (m["line"], e["line"])
assert e["inside"] and m["inside"], "a chart crosses the side margins"
PY
done
q="$t/chart320x568"; (cd "$q" && CAPTURE_WORKERS=1 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && (cd out && md5sum *.jpg) > serial.md5 \
  && CAPTURE_WORKERS=4 node "$ROOT/skills/spotlight/scripts/capture.mjs" frames >/dev/null && (cd out && md5sum -c --quiet ../serial.md5)) \
  || { echo "FAIL: parallel capture changed chart pixels"; exit 1; }
# diagrams: a path draws in from its data-at over data-dur (hidden before, partly drawn mid-way, whole after);
# other diagram elements fade in like caption lines
dg="$t/diagram"; mkdir -p "$dg"; cp "$ROOT/skills/spotlight/kit/scene.html" "$ROOT/skills/spotlight/kit/kit.js" "$dg/"; : > "$dg/fonts.css"
ln -s "$t/node_modules" "$dg/node_modules"; $IM -size 64x64 xc:gray20 "$dg/bg.png"
echo 'window.SPOTLIGHT = { width: 320, height: 568, duration: 2, grain: 0, shots: [ { a: 0, b: 2, still: "bg.png" } ] };' > "$dg/timeline.js"
python3 - "$dg/scene.html" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
d = '<div class="cap mid" data-a="0" data-b="2"><svg class="diagram" viewBox="0 0 300 100"><path id="p" d="M10 50 H290" data-at="0.5" data-dur="0.6"/><circle id="c" cx="290" cy="50" r="8" data-at="0.5"/></svg></div>'
open(p, "w").write(s.replace('<div id="end">', d + '\n  <div id="end">'))
PY
out=$(cd "$dg" && node --input-type=module -e "
  import { launch } from '$ROOT/skills/spotlight/scripts/browser.mjs';
  import { pathToFileURL } from 'node:url';
  const b = await launch(), p = await b.newPage({ viewport: { width: 320, height: 568 } });
  await p.goto(pathToFileURL(process.cwd() + '/scene.html').href); await p.evaluate(() => window.ready);
  const r = [];
  for (const t of [0.4, 0.8, 1.2]) r.push(await p.evaluate(async (t) => { await window.render(t); const s = (id) => getComputedStyle(document.getElementById(id));
    return [+s('p').opacity, parseFloat(s('p').strokeDashoffset), +s('c').opacity]; }, t));
  console.log(JSON.stringify(r)); await b.close();")
python3 - "$out" <<'PY' || { echo "FAIL: diagram draw-in $out"; exit 1; }
import json, sys
(o0, d0, c0), (o1, d1, c1), (o2, d2, c2) = json.loads(sys.argv[1].splitlines()[-1])
assert o0 == 0 and c0 == 0, "visible before data-at"
assert o1 == 1 and 0.01 < d1 < 0.99, ("not drawing mid-way", o1, d1)
assert abs(d2) < 1e-3 and c2 == 1, ("not whole after", d2, c2)
PY
echo "kit: ok"
