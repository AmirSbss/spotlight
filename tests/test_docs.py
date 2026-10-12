#!/usr/bin/env python3
"""The skill text is the product: every command, shot field and file it names must exist.

Run: python3 tests/test_docs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / "skills/spotlight"


def main():
    skill = (SK / "SKILL.md").read_text()
    refs = {p.name: p.read_text() for p in (SK / "references").glob("*.md")}
    every = skill + "\n".join(refs.values())
    fm = re.match(r"---\nname: (\S+)\ndescription: (.+?)\n---\n", skill, re.S)
    assert fm and fm.group(1) == "spotlight", "frontmatter name"
    for word in ("brag", "promo", "explain"):
        assert word in fm.group(2).lower(), f"description should mention {word}"
    for name in re.findall(r"references/([a-z-]+\.md)", every):
        assert (SK / "references" / name).exists(), f"missing references/{name}"
    assert {"brag.md", "promo.md", "explain.md", "critic.md", "quality-bar.md"} <= set(refs), sorted(refs)
    footage = (SK / "scripts/footage.py").read_text()
    for cmd in set(re.findall(r"\$F (\w+)", every)):
        assert f'add_parser("{cmd}"' in footage, f"SKILL names footage.py {cmd}, which doesn't exist"
    for script in set(re.findall(r"scripts/([a-z]+\.(?:mjs|py|sh))", every)):
        assert (SK / "scripts" / script).exists(), f"missing scripts/{script}"
    kit = (SK / "kit/kit.js").read_text()
    for field in ("clip", "still", "web", "scroll", "panel", "push", "origin", "filter", "drift", "grade", "grain", "dip", "draw"):
        assert re.search(rf"\b{field}\b", kit), f"kit.js doesn't document {field}"
        assert f"`{field}`" in every or f"{field}:" in every, f"the skill never explains {field}"
    for out in ("video.mp4", "poster.jpg", "caption.txt", "plan.md", "sources.md", "spotlight-output"):
        assert out in skill, f"SKILL.md should name the deliverable {out}"
    # the docs promise only what the kit does: a card over a still can still measure frozen
    assert "never reads as frozen" not in every, "the docs promise that text cards never measure frozen"
    # a web shot needs real speed: a slow scroll over a page's flat bands measures frozen
    assert re.search(r"`web`[^\n]*px/s", refs["explain.md"]) and "px/s" in skill, "the docs give no minimum web scroll speed"
    # one way to run site.mjs everywhere: from spotlight-output/work, so site/ sits beside scene.html
    runs = re.findall(r"site\.mjs <url> (\S+)", every)
    assert runs and set(runs) == {"."}, f"site.mjs run with workdir {runs}, not ."
    # commands use the run's output folder ($OUT: spotlight-output/ or its timestamped twin), never a hard-coded one,
    # and checking the final video writes its report into work/, not next to the deliverables
    assert not re.search(r"\$F \w+ [^`\n]*spotlight-output/", every), "a footage.py command hard-codes spotlight-output/"
    final = re.findall(r"\$F check \$OUT/video\.mp4[^`\n]*", skill)
    assert final and all("--out $OUT/work" in c for c in final), final
    for stale in ("promo-output", "/promo ", "window.PROMO", "skills/promo", "PROMO_SRGB_ICC"):
        assert stale not in every, f"stale reference: {stale}"
    # P2: sound is a real step, not a promise
    assert "sound.md" in refs, "references/sound.md is missing"
    for flag in ("--voice", "--no-sfx", "--music"):
        assert flag in skill, f"SKILL.md options don't name {flag}"
    assert "music-only.mp4" in skill, "SKILL.md doesn't deliver music-only.mp4"
    assert "phase 2" not in every.lower(), "a doc still says phase 2 is coming"
    # mix.py carries its own dependencies: `uv run <skill-dir>/scripts/mix.py`, never --project (it would put a .venv
    # into the skill folder, which may be read-only)
    mixes = re.findall(r"[^\n`]*scripts/mix\.py[^\n`]*", every)
    assert mixes and all("uv run <skill-dir>/scripts/mix.py" in m and "--project" not in m for m in mixes), mixes
    assert "/// script" in (SK / "scripts/mix.py").read_text() and "/// script" in (SK / "scripts/analyze_music_cues.py").read_text()
    for path in set(re.findall(r"assets/(?:music|sfx)/[\w.-]+\.(?:mp3|ogg|wav|json|md)", every)):
        assert (SK / path).exists(), f"docs name {path}, which doesn't exist"
    sound = refs["sound.md"]
    for p in sorted((SK / "assets/music").glob("*.mp3")) + sorted((SK / "assets/sfx").glob("*.ogg")):
        assert p.name in sound, f"sound.md never offers {p.name}"
    voice = (SK / "scripts/voice.py").read_text()
    assert "voice.py" in sound and "durations.json" in sound and "lines.json" in sound
    for lang in re.findall(r'^\s+"([a-z]{2})": "', voice, re.M):
        assert f"`{lang}`" in sound, f"sound.md's voice table misses {lang}"
    # P3: charts, diagrams and 3D are documented where the agent reads them, and every module named exists
    assert "visuals.md" in refs, "references/visuals.md is missing"
    vis = refs["visuals.md"]
    for kind in ("bar", "line", "donut", "number"):
        assert f"`{kind}`" in vis and kind in kit, f"chart kind {kind} undocumented or missing from kit.js"
    for word in ("three", "params", "data-anchor", "diagram"):
        assert word in kit and word in every, f"{word} undocumented"
    for mod in set(re.findall(r"three/([a-z-]+\.js)", every)):
        assert (SK / "kit/three" / mod).exists(), f"docs name kit/three/{mod}, which doesn't exist"
    assert "phase 3" not in every.lower(), "a doc still says phase 3 is coming"
    print("docs: all checks passed")


if __name__ == "__main__":
    main()
