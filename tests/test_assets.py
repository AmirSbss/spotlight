#!/usr/bin/env python3
"""The bundled library: every file licensed CC0/PD (or CC BY 4.0, credited) with its own source, real audio, within the size budget.

Run: python3 tests/test_assets.py
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "skills/spotlight/assets"
AUDIO = {".mp3", ".ogg", ".wav"}
MOODS = {"calm", "warm-acoustic", "upbeat", "minimal-tech", "cinematic"}
KINDS = {"whoosh", "click", "pop", "chime"}  # the effects sound.md promises; more kinds may exist


def probe(f):
    out = json.loads(subprocess.run(["ffprobe", "-v", "error", "-of", "json", "-show_streams", "-show_format", str(f)],
                                    capture_output=True, text=True, check=True).stdout)
    return out["streams"], float(out["format"]["duration"])


def main():
    for kind, budget in (("music", 30e6), ("sfx", 1.5e6)):
        d = A / kind
        files = sorted(p for p in d.iterdir() if p.suffix in AUDIO)
        lic = (d / "LICENSES.md").read_text()
        rows = {m[0]: m[1] for m in re.findall(r"^\|\s*`([\w.-]+\.(?:mp3|ogg|wav))`\s*\|(.+)$", lic, re.M)}
        assert set(rows) == {p.name for p in files}, (kind, sorted(set(rows) ^ {p.name for p in files}))
        for name, row in rows.items():
            assert re.search(r"\bCC0\b|[Pp]ublic [Dd]omain" + (r"|\bCC BY 4\.0\b" if kind == "music" else ""), row), f"{name}: no CC0/PD licence in its row"
            assert "https://" in row, f"{name}: no source page"
        assert sum(p.stat().st_size for p in files) <= budget, f"{kind} over {budget / 1e6:.1f} MB"
        for p in files:
            streams, dur = probe(p)
            assert [s["codec_type"] for s in streams] == ["audio"], f"{p.name}: not a single audio stream (cover art?)"
            assert dur > 0.04, p.name
            if kind == "music":
                assert 60 <= dur <= 240, f"{p.name}: {dur:.0f}s"
                cue = json.loads((d / "cues" / f"{p.stem}.json").read_text())
                assert abs(cue["duration"] - dur) < 0.5 and len(cue["per_second"]) >= dur - 2, p.name
                assert cue.get("tempo"), f"{p.name}: cue preset has no tempo (run footage.py track with uv on PATH)"
            else:
                assert dur <= 3.0, f"{p.name}: {dur:.1f}s is long for an effect"
        if kind == "music":
            # one track per mood under the mood's name, plus optional alternatives named <mood>-<n>
            stems = {p.stem for p in files}
            assert MOODS <= stems and all(re.fullmatch(r"(%s)(-\d+)?" % "|".join(MOODS), st) for st in stems), sorted(stems)
            # an explainer runs up to 180 s: at least one track must cover it from its start
            assert max(probe(p)[1] for p in files) >= 180, "no track long enough for a 180 s explainer"
        else:
            assert KINDS <= {p.stem.rsplit("-", 1)[0] for p in files}, sorted(p.stem for p in files)
    print("assets: all checks passed")


if __name__ == "__main__":
    main()
