#!/usr/bin/env python3
"""Narration for spotlight: lines.json -> voice/<id>.wav (levelled) + durations.json, with Piper TTS run locally.

  voice.py <work/lines.json>

lines.json: [{"id": "s1", "text": "...", "lang": "en"}, ...]; a line may also set "voice" (a Piper voice name such as
"de_DE-mls-medium", or a path to a local .onnx with its .onnx.json beside it) and "speaker" (an id, for multi-speaker
voices). Output lands next to lines.json. Each line is levelled to -16 LUFS, so it sits clearly over the -23 LUFS
music bed that mix.py ducks under it. A re-run synthesises only the lines whose text or voice changed (voice/takes.json
remembers the rest); delete voice/<id>.wav for a new take of an unchanged line.

Piper is not bundled and runs as a separate program (piper-tts is GPL; nothing here imports it):
  uv tool install --python 3.12 "piper-tts>=1.3"
Voices download on first use into ~/.cache/spotlight/piper/ (SPOTLIGHT_PIPER_DIR overrides), pinned to one revision of
huggingface.co/rhasspy/piper-voices and checked against its md5 sums. The defaults below were picked for their
licences: a narrated promo is commercial use, and most Piper voices are fine-tuned from a research-only base.

Needs ffmpeg/ffprobe. Python stdlib only.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

INSTALL = 'uv tool install --python 3.12 "piper-tts>=1.3"'
REV = "c10ece1aade47bb51c153c893d14e5bf8e5b7117"  # rhasspy/piper-voices: voices get retrained and removed upstream
BASE = f"https://huggingface.co/rhasspy/piper-voices/resolve/{REV}/"
VOICE_LUFS = -16.0
# language -> (voice, speaker, licence). Only voices trained from scratch on public-domain/CC0 data, or on CC BY
# data (credit line printed). No default for ar (the one voice has no dataset licence) or for tr, es, pt, ru, pl, zh, hi
# (nothing clean); a line can still name any voice itself.
VOICES = {
    "en": ("en_US-ljspeech-high", None, "public domain (LJ Speech)"),
    "fa": ("fa_IR-gyro-medium", None, "CC0 dataset as declared; provenance thin"),
    "it": ("it_IT-serena-high", None, "CC BY 4.0"),
    "nl": ("nl_NL-alex-medium", None, "CC0"),
    "uk": ("uk_UA-ukrainian_tts-medium", 0, "CC0"),
}
CREDITS = {
    "it_IT-serena-high": "Voice: Piper serena, dataset committa/serena-synthetic-it-27h, CC BY 4.0 "
                         "(includes Tatoeba sentences, CC BY 2.0 FR)",
    "de_DE-mls-medium": "Voice: Piper MLS, trained on Multilingual LibriSpeech by Pratap et al. (Meta AI), CC BY 4.0, openslr.org/94",
    "fr_FR-mls-medium": "Voice: Piper MLS, trained on Multilingual LibriSpeech by Pratap et al. (Meta AI), CC BY 4.0, openslr.org/94",
    "en_US-libritts-high": "Voice: Piper libritts (high), trained on LibriTTS by Zen et al., CC BY 4.0, openslr.org/60",
}


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, **kw)
    if r.returncode:
        err = r.stderr if isinstance(r.stderr, str) else r.stderr.decode(errors="replace")
        raise RuntimeError(f"{Path(str(cmd[0])).name} failed: {err.strip()[-600:]}")
    return r.stdout


def cache():
    d = Path(os.environ.get("SPOTLIGHT_PIPER_DIR") or Path.home() / ".cache/spotlight/piper")
    d.mkdir(parents=True, exist_ok=True)
    return d


def fetch(rel, dst, size=None, md5=None):
    # download to a temp name and move into place only once it checks out: a broken download never sits in the cache
    tmp = dst.with_name(dst.name + ".part")
    with urllib.request.urlopen(BASE + rel, timeout=60) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)
    data = tmp.read_bytes()
    if (size is not None and len(data) != size) or (md5 and hashlib.md5(data).hexdigest() != md5):
        tmp.unlink()
        raise RuntimeError(f"download of {rel} is corrupt (size or md5 mismatch); run again")
    tmp.replace(dst)


def model(name):
    # a local .onnx is used as is; a voice name is downloaded once into the cache
    if name.endswith(".onnx"):
        p = Path(name).expanduser()
        if not p.exists():
            raise RuntimeError(f"voice model {p} not found")
        return p
    d = cache()
    index = d / f"voices-{REV[:8]}.json"
    if not index.exists():
        fetch("voices.json", index)
    entry = json.loads(index.read_text()).get(name)
    if not entry:
        raise RuntimeError(f"Piper has no voice named {name!r} (see huggingface.co/rhasspy/piper-voices)")
    for rel, meta in entry["files"].items():
        if rel.endswith((".onnx", ".onnx.json")):
            dst = d / Path(rel).name
            if not (dst.exists() and dst.stat().st_size == meta["size_bytes"]):
                print(f"downloading {Path(rel).name} ({meta['size_bytes'] / 1e6:.0f} MB)", file=sys.stderr)
                fetch(rel, dst, meta["size_bytes"], meta["md5_digest"])
    return d / f"{name}.onnx"


def lufs(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"I:\s+(-?[0-9.]+|-inf) LUFS", r.stderr[r.stderr.rfind("Summary:"):])
    return float(m.group(1)) if m and m.group(1) != "-inf" else None


def pick(line):
    lang = str(line.get("lang") or "").split("-")[0].split("_")[0].lower()
    name, speaker = line.get("voice"), line.get("speaker")
    if not name:
        if lang not in VOICES:
            raise RuntimeError(f"no default voice for {lang!r} (line {line['id']}): set \"voice\" to a Piper voice name "
                               f"whose licence you have checked, or leave narration off; defaults: {', '.join(VOICES)}")
        name, default_speaker, _ = VOICES[lang]
        speaker = default_speaker if speaker is None else speaker
    return name, speaker


def speak(line, name, speaker, outdir, tmp):
    onnx = model(name)
    raw = Path(tmp) / f"{line['id']}.raw.wav"
    # one line of text on stdin: the new CLI puts no pause between input lines, and both CLIs accept only these flags
    text = " ".join(str(line["text"]).split()) + "\n"
    cmd = ["piper", "-m", onnx, "-f", raw, "--sentence_silence", "0.25"] + (["-s", speaker] if speaker is not None else [])
    run(cmd, input=text.encode("utf-8"))
    if not raw.exists() or raw.stat().st_size < 100:
        raise RuntimeError(f"piper wrote no audio for line {line['id']}")
    measured = lufs(raw)
    gain = VOICE_LUFS - measured if measured is not None and measured > -60 else 0.0
    out = outdir / "voice" / f"{line['id']}.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", f"volume={gain:.2f}dB,aresample=48000",
         "-c:a", "pcm_f32le", out])
    dur = float(json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-show_format", out]))["format"]["duration"])
    return round(dur, 3)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lines_json", help="work/lines.json")
    a = ap.parse_args()
    if not shutil.which("piper"):
        print(f"voice.py: Piper isn't installed. Install it with:\n  {INSTALL}\nor render without narration.", file=sys.stderr)
        sys.exit(2)
    src = Path(a.lines_json)
    try:
        lines = json.loads(src.read_text(encoding="utf-8"))
        assert isinstance(lines, list) and all({"id", "text"} <= set(x) for x in lines)
    except (OSError, json.JSONDecodeError, AssertionError, TypeError) as e:
        raise SystemExit(f"voice.py: cannot read {src} as [{{id, text, lang}}, ...]: {e}")
    outdir = src.parent
    (outdir / "voice").mkdir(exist_ok=True)
    # Piper isn't deterministic: a second take of the same line differs by up to ~0.3 s, pauses included. So a line whose
    # text and voice haven't changed keeps its take, and the timing built on it stays true.
    made = outdir / "voice" / "takes.json"
    try:
        takes = json.loads(made.read_text())
    except (OSError, ValueError):
        takes = {}
    durations, used = {}, set()
    try:
        with tempfile.TemporaryDirectory(prefix="spotlight voice ") as tmp:
            for line in lines:
                lid = line["id"]
                name, speaker = pick(line)
                key = hashlib.sha1(json.dumps([" ".join(str(line["text"]).split()), name, speaker, VOICE_LUFS, REV]).encode()).hexdigest()
                kept = takes.get(lid, {}).get("key") == key and (outdir / "voice" / f"{lid}.wav").exists()
                durations[lid] = takes[lid]["dur"] if kept else speak(line, name, speaker, outdir, tmp)
                takes[lid] = {"key": key, "dur": durations[lid]}
                made.write_text(json.dumps(takes, indent=2) + "\n")
                used.add(name)
                print(f"{lid}: {durations[lid]:.2f}s ({Path(name).name}{', unchanged' if kept else ''})")
    except (RuntimeError, OSError) as e:
        raise SystemExit(f"voice.py: {e}")
    (outdir / "durations.json").write_text(json.dumps(durations, indent=2) + "\n")
    for name in sorted(used):
        if name in CREDITS:
            print(f"credit (put it in sources.md and caption.txt): {CREDITS[name]}")
    print(f"-> {outdir / 'voice'}/<id>.wav, {outdir / 'durations.json'}")


if __name__ == "__main__":
    main()
