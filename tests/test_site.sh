#!/usr/bin/env bash
# Self-check for site.mjs: copy, brand, screens, full page, assets; RTL text; endless pages finish.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
IM=$(command -v magick >/dev/null && echo "magick" || echo "convert")
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
w="$t/work dir ٪ 50%"   # spaces, '%' and non-Latin in the work path
mkdir -p "$w"
npm i --silent --prefer-offline --prefix "$w" playwright-core >/dev/null 2>&1
cd "$w"
S="$ROOT/skills/spotlight/scripts/site.mjs"
node "$S" "file://$ROOT/tests/fixtures/site/index.html" . --size 1080x1920 >/dev/null
python3 - <<'PY'
import json
c = json.load(open("site/copy.json")); b = json.load(open("site/brand.json"))
assert c["title"].startswith("Fixture Co"), c["title"]
assert c["description"] == "Fixture Co builds small boats for cats.", c
assert [h["text"] for h in c["headings"]][:3] == ["Boats for cats", "How it works", "Pricing"], c["headings"]
assert {"Get a boat", "Order now"} <= {x["text"] for x in c["ctas"]}, c["ctas"]
assert b["background"].lower() == "#0f172a" and b["accent"].lower() == "#f59e0b", b
assert any("Fixture Sans" in f for f in b["fonts"]), b["fonts"]
assert b["logo"] and b["logo"].startswith("site/assets/"), b
PY
n=$(ls site/screens/*.png | wc -l); (( n >= 2 && n <= 12 )) || { echo "FAIL: $n screens"; exit 1; }
read -r W H <<< "$($IM site/screens/01.png -format '%w %h' info:)"
[[ "$W $H" == "1080 1920" ]] || { echo "FAIL: screen size $W x $H"; exit 1; }
read -r fh <<< "$($IM site/full.png -format '%h' info:)"; (( fh > 1920 )) || { echo "FAIL: full page height $fh"; exit 1; }
# the cookie banner (pure magenta) must be gone from the screens
read -r r g b <<< "$($IM site/screens/01.png -format '%[fx:int(255*p{540,1850}.r)] %[fx:int(255*p{540,1850}.g)] %[fx:int(255*p{540,1850}.b)]' info:)"
(( !(r > 240 && g < 20 && b > 240) )) || { echo "FAIL: cookie banner still on screen"; exit 1; }
# right-to-left page: exact strings, direction recorded
rm -rf site && node "$S" "file://$ROOT/tests/fixtures/site/fa.html" . >/dev/null
python3 -c "import json; c=json.load(open('site/copy.json')); assert c['dir']=='rtl' and c['lang']=='fa' and c['headings'][0]['text']=='یک نماینده برای همه کارها', c"
# colours written as oklch() (Tailwind v4) come out as real sRGB hex: a dark navy page, an amber button
rm -rf site && node "$S" "file://$ROOT/tests/fixtures/site/oklch.html" . >/dev/null
python3 -c "
import json; b = json.load(open('site/brand.json')); rgb = lambda h: [int(h[i:i + 2], 16) for i in (1, 3, 5)]
bg, ac = rgb(b['background']), rgb(b['accent'] or '#000000')
assert max(bg) < 60 and bg[2] > bg[0], b
assert ac[0] > 220 and 120 < ac[1] < 190 and ac[2] < 60, b"
# an endless page still finishes, within the caps
rm -rf site && timeout 150 node "$S" "file://$ROOT/tests/fixtures/site/infinite.html" . >/dev/null
n=$(ls site/screens/*.png | wc -l); (( n <= 12 )) || { echo "FAIL: endless page gave $n screens"; exit 1; }
read -r fh <<< "$($IM site/full.png -format '%h' info:)"; (( fh <= 12000 )) || { echo "FAIL: full page $fh px"; exit 1; }
# over HTTP: a font that never arrives, a consent "Accept" that is a navigating link, a bare path, a dead address
python3 "$ROOT/tests/site_server.py" > "$t/port" & srv=$!; trap 'kill $srv 2>/dev/null; rm -rf "$t"' EXIT
for _ in $(seq 50); do [[ -s "$t/port" ]] && break; sleep 0.1; done; P="http://127.0.0.1:$(cat "$t/port")"
rm -rf site; s0=$SECONDS
node "$S" "$P/hang.html" . >/dev/null 2>&1 || { echo "FAIL: stalled font: site.mjs exited non-zero"; exit 1; }
(( SECONDS - s0 <= 95 )) || { echo "FAIL: stalled font took $((SECONDS - s0)) s (cap 90)"; exit 1; }
ls site/screens/01.png site/full.png >/dev/null 2>&1 || { echo "FAIL: stalled font: no screens or full.png"; exit 1; }
rm -rf site; node "$S" "$P/consent-link.html" . >/dev/null 2>&1 || { echo "FAIL: consent link crashed site.mjs"; exit 1; }
python3 -c "import json; c=json.load(open('site/copy.json')); assert c['title'] == 'Consent link', c"
read -r r g b <<< "$($IM site/screens/01.png -format '%[fx:int(255*p{540,1850}.r)] %[fx:int(255*p{540,1850}.g)] %[fx:int(255*p{540,1850}.b)]' info:)"
(( !(r > 240 && g < 20 && b > 240) )) || { echo "FAIL: consent banner still on screen"; exit 1; }
rm -rf site; node "$S" "$ROOT/tests/fixtures/site/index.html" . >/dev/null 2>&1 || { echo "FAIL: a bare path failed"; exit 1; }
python3 -c "import json; c=json.load(open('site/copy.json')); assert c['title'].startswith('Fixture Co'), c"
if out=$(node "$S" "http://127.0.0.1:1/" . 2>&1); then echo "FAIL: a dead address exited 0"; exit 1; fi
[[ $(wc -l <<< "$out") -le 2 ]] && grep -q "can't open" <<< "$out" || { echo "FAIL: dead address message: $out"; exit 1; }
echo "site.mjs: ok"
