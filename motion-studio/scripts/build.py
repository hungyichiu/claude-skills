#!/usr/bin/env python3
"""Build a Motion Studio page from a scene spec.

Usage:
    python3 build.py spec.json OUT_DIR

Writes OUT_DIR/index.html (player + editor, spec embedded as a fallback)
and OUT_DIR/spec.json (the copy the published page loads and saves).
Publish index.html as the artifact with spec.json as a supporting file.
"""
import html
import json
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent / "assets" / "engine.html"


def build_html(spec: dict) -> str:
    title = (spec.get("meta") or {}).get("title") or "未命名動畫"
    spec_txt = json.dumps(spec, ensure_ascii=False).replace("</", "<\\/")
    page = ENGINE.read_text(encoding="utf-8")
    page = page.replace("__MOTION_TITLE__", html.escape(title), 1)
    page = page.replace("__MOTION_SPEC__", spec_txt, 1)
    return page


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    spec_path, out = Path(sys.argv[1]), Path(sys.argv[2])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if not spec.get("scenes"):
        sys.exit("spec has no scenes")
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(build_html(spec), encoding="utf-8")
    (out / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(float(s.get("duration", 4)) for s in spec["scenes"])
    print(f"built {out/'index.html'} — {len(spec['scenes'])} scenes, {total:.1f}s")


if __name__ == "__main__":
    main()
