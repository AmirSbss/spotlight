#!/usr/bin/env bash
# Self-check for voice.py: exit 2 and the install command without piper; the text reaches piper byte-exact (a fake
# piper records its stdin); an unknown language is a clear error; with a real piper, en and fa lines come out levelled.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
V="$ROOT/skills/spotlight/scripts/voice.py"
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
fail() { echo "FAIL: $*"; exit 1; }
lufs() { ffmpeg -hide_banner -nostats -i "$1" -af ebur128 -f null - 2>&1 | sed -n '/Summary:/,$p' | sed -n 's/^ *I: *\(-*[0-9.]*\) LUFS/\1/p'; }

# no piper on PATH: exit 2, and the message says how to install it
mkdir "$t/bare"; for b in python3 ffmpeg ffprobe; do ln -s "$(command -v $b)" "$t/bare/$b"; done
echo '[{"id": "a", "text": "Hello.", "lang": "en"}]' > "$t/l.json"
set +e; out=$(PATH="$t/bare" python3 "$V" "$t/l.json" 2>&1); rc=$?; set -e
[[ $rc == 2 ]] || fail "no piper: exit $rc, want 2 ($out)"
grep -q "uv tool install" <<< "$out" || fail "no install command: $out"

# a fake piper: records the model, speaker and stdin, writes a 1.2 s tone as the "speech"
mkdir "$t/fake"; for b in bash cat python3 ffmpeg ffprobe; do ln -s "$(command -v $b)" "$t/fake/$b"; done
cat > "$t/fake/piper" <<'SH'
#!/usr/bin/env bash
out=""; while (( $# )); do case "$1" in -f) out=$2; shift;; -m) echo "$2" > "$FAKE_LOG.model";; -s) echo "$2" > "$FAKE_LOG.speaker";; esac; shift; done
cat > "$FAKE_LOG.stdin"; echo x >> "$FAKE_LOG.calls"
ffmpeg -v error -y -f lavfi -i "sine=f=220:sample_rate=22050:duration=1.2" -af volume=-3dB "$out"
SH
chmod +x "$t/fake/piper"; : > "$t/model.onnx"
w="$t/w dir 50% ٪"; mkdir -p "$w"
# a ZWNJ (U+200C), a Latin name and a newline: one line reaches piper, every other byte unchanged
python3 - "$w/lines.json" "$t/model.onnx" <<'PY'
import json, sys
json.dump([{"id": "s1", "text": "اسپات‌لایت\nبا Spotlight", "lang": "fa", "voice": sys.argv[2], "speaker": 3}],
          open(sys.argv[1], "w"), ensure_ascii=False)
PY
FAKE_LOG="$t/log" PATH="$t/fake" python3 "$V" "$w/lines.json" >/dev/null || fail "fake piper run failed"
python3 - "$t/log.stdin" <<'PY' || fail "text changed on its way to piper"
import sys; got = open(sys.argv[1], encoding="utf-8").read()
assert got == "اسپات‌لایت با Spotlight\n", repr(got)
PY
[[ $(cat "$t/log.model") == "$t/model.onnx" && $(cat "$t/log.speaker") == 3 ]] || fail "model or speaker not passed"
python3 - "$w" <<'PY' || fail "durations.json wrong"
import json, sys; d = json.load(open(sys.argv[1] + "/durations.json"))
assert set(d) == {"s1"} and abs(d["s1"] - 1.2) < 0.05, d
PY
l=$(lufs "$w/voice/s1.wav"); python3 -c "import sys; sys.exit(abs($l + 16) > 1)" || fail "line not levelled to -16 LUFS ($l)"

# a re-run keeps unchanged takes (Piper's second take of a line differs, so timing built on the first would drift);
# a changed line, and only that line, is spoken again
python3 - "$w/lines.json" "$t/model.onnx" <<'PY'
import json, sys
json.dump([{"id": "s1", "text": "اسپات‌لایت\nبا Spotlight", "lang": "fa", "voice": sys.argv[2], "speaker": 3},
           {"id": "s2", "text": "Two.", "lang": "fa", "voice": sys.argv[2]}], open(sys.argv[1], "w"), ensure_ascii=False)
PY
: > "$t/log.calls"
FAKE_LOG="$t/log" PATH="$t/fake" python3 "$V" "$w/lines.json" > "$t/run2" || fail "second run failed"
[[ $(wc -l < "$t/log.calls") == 1 ]] && grep -q "s1: .*unchanged" "$t/run2" || fail "unchanged s1 was spoken again: $(cat "$t/run2")"
sed -i 's/Two\./Two, again./' "$w/lines.json"; : > "$t/log.calls"
FAKE_LOG="$t/log" PATH="$t/fake" python3 "$V" "$w/lines.json" > "$t/run3" || fail "third run failed"
[[ $(wc -l < "$t/log.calls") == 1 && $(cat "$t/log.stdin") == "Two, again." ]] || fail "edited s2 not respoken alone: $(cat "$t/run3")"
python3 - "$w" <<'PY' || fail "durations.json lost the kept line"
import json, sys; d = json.load(open(sys.argv[1] + "/durations.json"))
assert set(d) == {"s1", "s2"} and abs(d["s1"] - 1.2) < 0.05, d
PY

# a language with no default voice is a clear error that names it
echo '[{"id": "a", "text": "x", "lang": "xx"}]' > "$t/x.json"
set +e; out=$(FAKE_LOG="$t/log" PATH="$t/fake" python3 "$V" "$t/x.json" 2>&1); rc=$?; set -e
[[ $rc == 1 ]] && grep -q "no default voice for 'xx'" <<< "$out" || fail "unknown language: exit $rc: $out"

if ! command -v piper >/dev/null; then echo "voice: ok (real piper skipped: not installed)"; exit 0; fi
# the real thing: default voices download (once, into the cache), speak, and land at the level mix.py expects
r="$t/real"; mkdir -p "$r"
cat > "$r/lines.json" <<'JSON'
[{"id": "en1", "text": "Spotlight checks its own videos before you see them.", "lang": "en"},
 {"id": "fa1", "text": "اسپات‌لایت ویدیوهای خودش را پیش از شما بررسی می‌کند.", "lang": "fa"}]
JSON
python3 "$V" "$r/lines.json" >/dev/null || fail "real piper run failed"
python3 - "$r" <<'PY' || fail "real durations wrong"
import json, sys; d = json.load(open(sys.argv[1] + "/durations.json"))
assert set(d) == {"en1", "fa1"} and all(1.0 < v < 12 for v in d.values()), d
PY
for id in en1 fa1; do l=$(lufs "$r/voice/$id.wav"); python3 -c "import sys; sys.exit(abs($l + 16) > 1)" || fail "$id at $l LUFS"; done
echo "voice: ok"
