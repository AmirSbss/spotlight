#!/usr/bin/env python3
"""Footage plumbing for spotlight: the steps with sharp edges, done the same way every run.

  prep   <work> <files...>                        manifest.jsonl + upright stills + contact sheets
  shot   <clip> <start> <dur> <WxH> <cx> <outdir>  one clip shot as exactly round(dur*30) JPGs
  encode <frames-dir> <mix.wav|none> <out.mp4> [--poster img]
                                                   PNG/JPG frames + mix -> BT.709 H.264/AAC mp4 at -14 LUFS (two-pass),
                                                   with the poster embedded as cover art
  check  <video> [--end-card s] [--target LUFS] [--out dir]    frozen holds, loudness, frames, contact sheet -> check.json
  track  <audio> [--json]                                     per-second loudness (+ tempo, strong cues) for picking a music window

Needs ffmpeg/ffprobe (with zscale) and ImageMagick 6 or 7. Python stdlib only.
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FPS = 30
PHOTO = {".jpg", ".jpeg", ".jfif", ".png", ".webp", ".heic", ".heif", ".avif", ".tif", ".tiff", ".bmp", ".gif"}
VIDEO = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".3gp", ".mts", ".m2ts", ".ts", ".mpg", ".mpeg", ".wmv"}
AUDIO = {".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac", ".opus"}
HDR = {"arib-std-b67", "smpte2084"}  # HLG (iPhone), PQ
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
# iPhone photos are Display P3; stripping the profile without converting washes them out next to the video
SRGB_ICC = next((p for p in (os.environ.get("SPOTLIGHT_SRGB_ICC", ""), "/usr/share/color/icc/sRGB.icc",
                             "/usr/share/color/icc/colord/sRGB.icc", "/usr/share/color/icc/ghostscript/srgb.icc",
                             "/System/Library/ColorSync/Profiles/sRGB Profile.icc") if p and os.path.exists(p)), None)


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{Path(str(cmd[0])).name} failed: {r.stderr.strip()[-600:]}")
    return r.stdout


def im(tool, *args):
    # ImageMagick 7 ships `magick <tool>`; 6 (Debian 12) ships the bare tools.
    return (["magick", tool] if shutil.which("magick") else [tool]) + [str(a) for a in args]


def im_read(path):
    # read a user file literally ('%d' in a name is not a frame pattern) and keep its first image (HEIC, GIF)
    return ["-define", "filename:literal=true", path, "-delete", "1--1"]


def kind(path):
    ext = Path(path).suffix.lower()
    return "photo" if ext in PHOTO else "video" if ext in VIDEO else "audio" if ext in AUDIO else "other"


def frames_in(folder, ext):
    # only numbered frames (00001.jpg ...): never touch or count anything else in the folder
    return sorted(p for p in Path(folder).glob(f"[0-9][0-9][0-9][0-9][0-9].{ext}"))


def pattern(folder, ext):
    # image2 treats '%' in the path as a format directive, so a folder like "50% off" needs it doubled
    return str(folder).replace("%", "%%") + f"/%05d.{ext}"


def probe(path):
    info = {"file": str(path), "kind": kind(path)}
    if info["kind"] == "photo":
        w, h = run(im("convert", *im_read(path), "-auto-orient", "-format", "%w %h", "info:")).split()
        info.update(width=int(w), height=int(h))
    elif info["kind"] in ("video", "audio"):
        data = json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-show_streams", "-show_format", path]))
        streams = data.get("streams", [])
        info["duration"] = round(float(data.get("format", {}).get("duration", 0)), 3)
        info["has_audio"] = any(s.get("codec_type") == "audio" for s in streams)
        if info["kind"] == "video":
            v = next((s for s in streams if s.get("codec_type") == "video"
                      and not s.get("disposition", {}).get("attached_pic")), None)
            if v is None:
                raise RuntimeError("no video stream")
            rot = int(float(v.get("tags", {}).get("rotate", 0)))
            for sd in v.get("side_data_list", []):
                rot = int(sd.get("rotation", rot))
            w, h = (v["height"], v["width"]) if rot % 180 else (v["width"], v["height"])
            num, den = (v.get("avg_frame_rate") or "0/0").split("/")
            info.update(width=w, height=h, rotation=rot, fps=round(int(num) / int(den), 3) if int(den) else 0,
                        transfer=v.get("color_transfer", ""), hdr=v.get("color_transfer") in HDR)
    return info


def skipped(path, root):
    # dotfiles and hidden folders (._IMG_0001.HEIC, DCIM/.thumbnails) and earlier spotlight output never enter
    # the inventory; judged relative to the media folder, which may itself sit under ~/.cache or spotlight-output-*
    return any(part.startswith((".", "spotlight-output")) for part in Path(os.path.abspath(path)).relative_to(root).parts)


def cuts(path):
    # hard cuts inside a clip, so in/out points can avoid them
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:v:0", "-vf",
                        "select='gt(scene,0.3)',showinfo", "-f", "null", "-"], capture_output=True, text=True)
    return [round(float(t), 2) for t in re.findall(r"pts_time:\s*([0-9.]+)", r.stderr)]


def sheet_frames(info, cut_list):
    # 12 tiles: the opening frame, the scene cuts (up to 11), then evenly spaced frames far from those
    fps, dur = info["fps"] or FPS, max(info["duration"], 0.1)
    picked = {0} | {round(c * fps) for c in cut_list[:11]}
    even = {round(dur * k / 12 * fps) for k in range(12)} - picked
    while len(picked) < 12 and even:
        far = max(even, key=lambda f: min(abs(f - g) for g in picked))
        picked.add(far)
        even.discard(far)
    return "+".join(f"eq(n,{f})" for f in sorted(picked))  # quoted in the filter, so commas need no escape


def passthrough(version):
    # -fps_mode arrived in ffmpeg 5.1 and -vsync goes away after 8.x: pick what this ffmpeg has
    return ["-fps_mode:v:0", "passthrough"] if version >= (5, 1) else ["-vsync", "0"]


def ffmpeg_version():
    m = re.search(r"ffmpeg version n?(\d+)\.(\d+)", run(["ffmpeg", "-version"]))
    return (int(m[1]), int(m[2])) if m else (99, 0)  # git builds report a hash: treat as new


def prep(work, files):
    root = os.path.commonpath([os.path.dirname(os.path.abspath(f)) for f in files]) if files else "/"
    dropped = [f for f in files if skipped(f, root)]
    files = [f for f in files if f not in dropped]
    if dropped:
        print("skipped (hidden or earlier spotlight output):", ", ".join(map(str, dropped)), file=sys.stderr)
    if SRGB_ICC is None and any(kind(f) == "photo" for f in files):
        print("warning: no sRGB ICC profile found (set SPOTLIGHT_SRGB_ICC); wide-gamut photos will look washed out", file=sys.stderr)
    if not files:
        raise RuntimeError("nothing to use: every file was skipped (dotfiles, hidden folders, earlier spotlight-output)")
    work = Path(work)
    stills, sheets = work / "stills", work / "sheets"
    stills.mkdir(parents=True, exist_ok=True)
    sheets.mkdir(exist_ok=True)
    items = []
    for i, f in enumerate(files, 1):
        try:
            info = {"index": i, **probe(f)}
            if info["kind"] == "photo":
                info["still"] = str(stills / f"{i:03d}.jpg")
                srgb = ["-profile", SRGB_ICC] if SRGB_ICC else []
                run(im("convert", *im_read(f), "-auto-orient", *srgb, "-strip", "-resize", "4096x4096>", "-quality", "92", info["still"]))
            elif info["kind"] == "video":
                info["cuts"] = cuts(f)
                vf = [f"select='{sheet_frames(info, info['cuts'])}'"] + ([TONEMAP] if info["hdr"] else []) + [
                    "scale=480:-2",
                    f"drawtext=text='#{i} %{{pts\\:hms}}':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6",
                    "tile=4x3"]
                info["sheet"] = str(sheets / f"video-{i:03d}.jpg")
                run(["ffmpeg", "-y", "-v", "error", "-i", f, "-vf", ",".join(vf), "-frames:v", "1", "-update", "1", info["sheet"]])
        except Exception as e:  # one unreadable file must not sink the whole folder
            info = {"index": i, "file": str(f), "kind": kind(f), "error": str(e)}
        items.append(info)
    # the manifest first: a failed contact sheet must not lose the inventory
    (work / "manifest.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in items))
    ok = [x for x in items if "still" in x]
    for n in range(0, len(ok), 12):
        labelled = [a for x in ok[n:n + 12] for a in ("-label", x["index"], x["still"])]
        run(im("montage", "-pointsize", "28", *labelled, "-tile", "4x3", "-geometry", "360x360+6+6",
               sheets / f"photos-{n // 12 + 1:02d}.jpg"))
    return items


def shot(clip, start, dur, size, cx, outdir):
    if not 0 <= cx <= 1:
        raise ValueError("cx must be between 0 (left) and 1 (right)")
    w, h = (int(v) for v in size.split("x"))
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    for old in frames_in(out, "jpg"):
        old.unlink()
    n = round(dur * FPS)
    vf = [f"fps={FPS}"] + ([TONEMAP] if probe(clip).get("hdr") else []) + [
        f"scale={w}:{h}:force_original_aspect_ratio=increase", f"crop={w}:{h}:(iw-{w})*{cx}:(ih-{h})/2"]
    run(["ffmpeg", "-y", "-v", "error", "-ss", start, "-i", clip, "-vf", ",".join(vf),
         "-frames:v", n, "-q:v", "2", pattern(out, "jpg")])
    got = len(frames_in(out, "jpg"))
    if got != n:
        raise RuntimeError(f"{clip}: got {got} of {n} frames; start+dur is past the end of the clip")
    return n


def loudnorm(mix, fit):
    # two-pass: one-pass (dynamic) loudnorm drifts ~0.5-1 LU on beds that start soft and lift
    target = "I=-14:TP=-2.5:LRA=11"  # AAC overshoots ~0.7 dB on real mixes; -2.5 in lands under -1.5 out
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mix), "-af",
                        f"{fit},loudnorm={target}:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"ffmpeg loudness measure failed: {r.stderr.strip()[-600:]}")
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    if "inf" in m["input_i"]:  # silent mix: nothing to normalize
        return fit
    return (f"{fit},loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")


def encode(frames, mix, dst, poster=None):
    frames = Path(frames)
    png, jpg = frames_in(frames, "png"), frames_in(frames, "jpg")
    if png and jpg:
        raise RuntimeError(f"{frames} mixes PNG and JPG frames (a stale earlier render?); keep one kind")
    files, ext = (png, "png") if png else (jpg, "jpg")
    if not files:
        raise RuntimeError(f"no NNNNN.png or NNNNN.jpg frames in {frames}")
    nums = [int(f.stem) for f in files]
    if nums[0] not in (0, 1) or nums != list(range(nums[0], nums[0] + len(nums))):
        raise RuntimeError(f"{frames}: frame numbers have a gap or don't start at 00000/00001")
    magic = b"\x89PNG" if ext == "png" else b"\xff\xd8"
    for f in files:
        with open(f, "rb") as fh:
            if not fh.read(4).startswith(magic):
                raise RuntimeError(f"{f.name} is not a real {ext.upper()} (a copied still in the wrong format?); frames would be dropped")
    n, dur = len(files), len(files) / FPS
    inputs = ["-framerate", FPS, "-start_number", nums[0], "-i", pattern(frames, ext)]
    # BT.709 end to end: convert the frames' matrix and say so, instead of leaving players to guess
    graph = "[0:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]"
    if mix != "none":
        # pad or trim the mix to the picture so a short track never shortens the video
        inputs += ["-i", mix]
        graph += f";[1:a]{loudnorm(mix, f'apad,atrim=0:{dur}')},aformat=sample_rates=48000:channel_layouts=stereo[a]"
        maps = ["-map", "[v]", "-map", "[a]"]
    else:
        # a silent track, not none: Telegram and others treat audio-less MP4s as GIFs
        # through the graph like a real mix: mapped straight in, it fell behind the video and the frame limit
        # closed the file with seconds of it unwritten
        inputs += ["-f", "lavfi", "-t", dur, "-i", "anullsrc=r=48000:cl=stereo"]
        graph += ";[1:a]anull[a]"
        maps = ["-map", "[v]", "-map", "[a]"]
    if poster:
        # cover art: players and file browsers show it without a poster frame flashing inside the video
        inputs += ["-i", poster]
        maps += ["-map", "2:v", "-c:v:1", "mjpeg", "-disposition:v:1", "attached_pic"]
    # passthrough: a frame that fails to decode must show up as missing, not be papered over by duplication
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, *maps, *passthrough(ffmpeg_version()),
           "-c:a", "aac", "-b:a", "192k", "-c:v:0", "libx264", "-crf", 18, "-preset", "medium",
           "-colorspace:v:0", "bt709", "-color_primaries:v:0", "bt709", "-color_trc:v:0", "bt709", "-color_range:v:0", "tv",
           "-movflags", "+faststart", "-frames:v:0", n, dst]
    run(cmd)
    got = int(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                   "stream=nb_read_packets", "-of", "csv=p=0", dst]).strip() or 0)
    if got != n:
        raise RuntimeError(f"encoded {got} of {n} frames; is every frame file a real {ext.upper()}?")


def frozen_samples(video, threshold=0.35):
    # luma difference between consecutive frames sampled at 10 fps (approach from motion-video-kit, MIT):
    # a sample under the threshold means nothing visible moved in that 0.1 s
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-map", "0:v:0", "-vf",
                        "fps=10,scale=320:-2,format=gray,tblend=all_mode=difference,signalstats,"
                        "metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    values = [float(v) for v in re.findall(r"YAVG=([0-9.]+)", r.stderr)]
    return [round((i + 1) / 10, 2) for i, v in enumerate(values) if v < threshold]


def holds(times, step=0.1):
    # consecutive frozen samples -> [start, end] stretches
    out = []
    for t in times:
        if out and t - out[-1][1] <= step + 1e-6:
            out[-1][1] = t
        else:
            out.append([round(t - step, 2), t])
    return out


def loudness(video):
    data = json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-show_streams", video]))
    if not any(s.get("codec_type") == "audio" for s in data.get("streams", [])):
        return None
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-map", "0:a:0", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    grab = lambda k: float(re.search(rf"{k}:\s+(-?[0-9.]+|-inf)", tail).group(1).replace("-inf", "-99"))
    return {"I": grab("I"), "LRA": grab("LRA"), "TP": grab("Peak")}


def check(video, end_card=0.0, target=-14.0, out=None):
    video = Path(video)
    out = Path(out) if out else video.parent
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-count_packets", "-show_streams", video]))
    v = next(s for s in data["streams"] if s["codec_type"] == "video" and not s.get("disposition", {}).get("attached_pic"))
    a = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    num, den = (v.get("avg_frame_rate") or "0/0").split("/")
    fps = int(num) / int(den) if int(den) else FPS
    frames = int(v["nb_read_packets"])
    dur = float(v.get("duration") or frames / fps)
    stretches = [h for h in holds(frozen_samples(video)) if h[0] < dur - end_card - 1e-6]
    stretches = [[s, min(e, dur - end_card)] for s, e in stretches]
    total = round(sum(e - s for s, e in stretches), 2)
    long_holds = [[s, e] for s, e in stretches if e - s > 0.6]
    budget = round(max(dur - end_card, 0) / 30, 2)
    loud = loudness(video)
    warnings, failures = [], []
    if abs(frames - round(dur * fps)) > 1:
        failures.append(f"frame count {frames} doesn't match {dur:.3f}s at {fps:g} fps")
    if loud:
        if loud["TP"] > -1.0:
            failures.append(f"true peak {loud['TP']} dBTP is above -1")
        if loud["I"] <= -69.9:  # ebur128's floor: a silent track (encode's mix=none) or audio shorter than its 400 ms gate
            warnings.append("audio is silent or too short to measure (integrated loudness at the -70 LUFS floor)")
        else:
            if abs(loud["I"] - target) > 1.0:
                failures.append(f"integrated loudness {loud['I']} LUFS is more than 1 LU from {target}")
            if loud["LRA"] < 3:
                warnings.append(f"loudness range {loud['LRA']} LU is under 3 (fine for calm pieces, flat for energetic ones)")
    if end_card >= dur / 2:
        warnings.append(f"--end-card {end_card:g} exempts {end_card:g} of {dur:.1f}s from the frozen check; it is the end card's "
                        f"length (duration minus SPOTLIGHT.end), not the time it starts")
    if total > budget:
        warnings.append(f"frozen {total}s, over the budget of {budget}s (1s per 30s)")
    for s, e in long_holds:
        warnings.append(f"hold without motion {s:.1f}-{e:.1f}s ({e - s:.1f}s > 0.6s)")
    sheet = out / "check-sheet.jpg"
    vf = (f"fps={24 / max(dur, 0.1)},scale=270:-2,"
          "drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=6x4")
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-map", "0:v:0", "-vf", vf, "-frames:v", "1", "-update", "1", sheet])
    result = {"file": str(video), "duration": round(dur, 3), "fps": round(fps, 3), "frames": frames,
              "size": [v["width"], v["height"]], "video_codec": v.get("codec_name"), "audio_codec": a and a.get("codec_name"),
              "loudness": loud, "frozen": {"total": total, "holds": stretches, "long_holds": long_holds, "budget": budget},
              "warnings": warnings, "failures": failures, "sheet": str(sheet)}
    (out / "check.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def track(audio):
    # loudness of every whole second: where a track is soft, where it lifts. The power mean of the momentary (400 ms)
    # values ending in that second, so a lift shows in the second it happens; the first windows, not full yet, are skipped
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(audio), "-map", "0:a:0", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    power = {}
    for t, m in re.findall(r"t:\s*([0-9.]+)\s.*?M:\s*(-?[0-9.]+|-inf)", r.stderr):
        t = round(float(t), 1)
        if t >= 0.4:
            power.setdefault(int(t - 1e-6), []).append(10 ** (float(m.replace("-inf", "-120.7")) / 10))
    per_second = [round(10 * math.log10(sum(v) / len(v)), 1) for _, v in sorted(power.items())]
    result = {"duration": round(float(json.loads(run(["ffprobe", "-v", "error", "-of", "json", "-show_format", audio]))["format"]["duration"]), 3),
              "per_second": per_second}
    analyzer = Path(__file__).with_name("analyze_music_cues.py")
    if shutil.which("uv") and analyzer.exists():
        with tempfile.TemporaryDirectory() as tmp:
            cue = subprocess.run(["uv", "run", "--project", str(analyzer.parent), "python", str(analyzer), str(audio),
                                  "--output-json", f"{tmp}/c.json", "--output-md", f"{tmp}/c.md", "--window-duration", "60"],
                                 capture_output=True, text=True)
            if cue.returncode == 0:
                c = json.loads(Path(f"{tmp}/c.json").read_text())
                result["tempo"] = c.get("tempo")
                result["strong_cues"] = sorted(round(x["time"], 2) for x in c.get("strongCues", []) if x["time"] < 60)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep")
    p.add_argument("work")
    p.add_argument("files", nargs="+")
    p = sub.add_parser("shot")
    for name, typ in (("clip", str), ("start", float), ("dur", float), ("size", str), ("cx", float), ("outdir", str)):
        p.add_argument(name, type=typ)
    p = sub.add_parser("encode")
    for name in ("frames", "mix", "dst"):
        p.add_argument(name)
    p.add_argument("--poster", help="image embedded as MP4 cover art")
    p = sub.add_parser("check", help="measure a render: frozen holds, loudness, frames, contact sheet")
    p.add_argument("video")
    p.add_argument("--end-card", type=float, default=0.0, help="the end card's length in seconds (duration minus SPOTLIGHT.end), exempt from the frozen check")
    p.add_argument("--target", type=float, default=-14.0)
    p.add_argument("--out")
    p = sub.add_parser("track", help="per-second loudness (+ tempo and strong cues with uv) of a music track")
    p.add_argument("audio")
    p.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        if a.cmd == "prep":
            items = prep(a.work, a.files)
            print(f"{len(items)} files, {sum('error' in x for x in items)} unreadable -> {a.work}/manifest.jsonl")
        elif a.cmd == "shot":
            print(shot(a.clip, a.start, a.dur, a.size, a.cx, a.outdir), "frames")
        elif a.cmd == "check":
            r = check(a.video, a.end_card, a.target, a.out)
            loud = r["loudness"] or {}
            print(f"{r['duration']}s {r['frames']} frames {r['size'][0]}x{r['size'][1]} · I {loud.get('I')} LRA {loud.get('LRA')} "
                  f"TP {loud.get('TP')} · frozen {r['frozen']['total']}s (budget {r['frozen']['budget']}s) · sheet {r['sheet']}")
            for w in r["warnings"]:
                print("warning:", w)
            for f in r["failures"]:
                print("FAIL:", f)
            if r["failures"]:
                raise SystemExit(1)
        elif a.cmd == "track":
            r = track(a.audio)
            if a.json:
                print(json.dumps(r))
            else:
                print(" ".join(f"{i}:{v:.0f}" for i, v in enumerate(r["per_second"])))
                if "tempo" in r:
                    print("tempo", r["tempo"], "strong cues", r["strong_cues"])
        elif a.cmd == "encode":
            encode(a.frames, a.mix, a.dst, a.poster)
            print(a.dst)
    except (RuntimeError, ValueError) as e:
        raise SystemExit(f"footage.py {a.cmd}: {e}")


if __name__ == "__main__":
    main()
