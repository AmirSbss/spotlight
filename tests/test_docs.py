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
    for field in ("clip", "still", "web", "scroll", "panel", "push", "origin", "filter", "drift", "grade", "grain"):
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
    print("docs: all checks passed")


if __name__ == "__main__":
    main()
