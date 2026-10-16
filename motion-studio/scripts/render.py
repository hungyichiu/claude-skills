#!/usr/bin/env python3
"""Render a Motion Studio spec to MP4 (or GIF / still frames).

Usage:
    python3 render.py spec.json out.mp4 [--scale 1.5] [--fps 30]
    python3 render.py spec.json out.gif [--scale 0.6] [--fps 15]
    python3 render.py spec.json frames_dir --stills 0.5,3.2,7   # PNG stills at those seconds

The spec may also be an index.html built by build.py (its embedded spec is used).
Needs: playwright (python) with a Chromium install, and ffmpeg.
Frames are rendered deterministically: the page is seeked to each frame time,
so the video timing never depends on machine speed.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import build_html  # noqa: E402


def load_spec(path: Path) -> dict:
    txt = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".html", ".htm"):
        m = re.search(r'<script type="application/json" id="motion-spec">(.*?)</script>', txt, re.S)
        if not m:
            sys.exit("no embedded motion-spec found in the html")
        txt = m.group(1).replace("<\\/", "</")
    return json.loads(txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=1.5, help="pixel scale (1.5 on 1280x720 = 1920x1080)")
    ap.add_argument("--fps", type=int, default=None)
    ap.add_argument("--stills", default=None, help="comma separated seconds; writes PNGs into OUT dir")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright

    spec = load_spec(Path(a.spec))
    out = Path(a.out)
    with tempfile.TemporaryDirectory() as td:
        page_path = Path(td) / "render.html"
        page_path.write_text(
            '<!doctype html><html><head><meta charset="utf-8"></head><body>' + build_html(spec) + "</body></html>",
            encoding="utf-8",
        )
        with sync_playwright() as p:
            browser = p.chromium.launch()
            meta = spec.get("meta", {})
            w, h = int(meta.get("width", 1280)), int(meta.get("height", 720))
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=a.scale)
            # no network in the sandbox: skip web fonts, the local Noto CJK fallback is used
            ctx.route(re.compile(r"^https?://"), lambda route: route.abort())
            pg = ctx.new_page()
            pg.add_init_script("window.__MOTION_RENDER=true;")
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.goto(page_path.as_uri())
            pg.wait_for_function("window.__motion !== undefined", timeout=15000)
            pg.evaluate("window.__motion.ready")
            if errors:
                sys.exit("page error: " + "; ".join(errors))
            info = pg.evaluate("({d: window.__motion.duration, fps: window.__motion.fps})")
            fps = a.fps or int(info["fps"] or 30)
            dur = float(info["d"])
            clip = {"x": 0, "y": 0, "width": w, "height": h}

            if a.stills:
                out.mkdir(parents=True, exist_ok=True)
                for t in [float(x) for x in a.stills.split(",") if x.strip()]:
                    pg.evaluate(f"window.__motion.seek({t})")
                    pg.screenshot(path=str(out / f"still_{t:06.2f}.png"), clip=clip)
                browser.close()
                print(f"stills written to {out}")
                return

            n = max(1, round(dur * fps))
            ow, oh = round(w * a.scale) // 2 * 2, round(h * a.scale) // 2 * 2
            if out.suffix.lower() == ".gif":
                vf = f"scale={ow}:{oh}:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4"
                cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
                       "-vf", vf, "-loop", "0", str(out)]
            else:
                cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
                       "-vf", f"scale={ow}:{oh}:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                       "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
            ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            for i in range(n):
                pg.evaluate(f"window.__motion.seek({i / fps})")
                ff.stdin.write(pg.screenshot(clip=clip, type="png"))
            ff.stdin.close()
            if ff.wait() != 0:
                sys.exit("ffmpeg failed")
            browser.close()
    print(f"rendered {out} — {dur:.1f}s, {n} frames @ {fps}fps, {ow}x{oh}")


if __name__ == "__main__":
    main()
