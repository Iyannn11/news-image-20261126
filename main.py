#!/usr/bin/env python3
"""Entry point for the News 26 (news-image-20261126) make.fun entry.

Stdlib only: copies entry.png from this repo into MAKEFUN_OUTPUT_DIR.
Never imports PIL or any third-party module (the grader's Python 3.13
sandbox has no Pillow).
"""
import os
import shutil
import sys
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"

    if not src.is_file():
        print(f"error: {src} not found", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)

    data = dst.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: output is not a PNG", file=sys.stderr)
        return 1
    if len(data) > 1024 * 1024:
        print(f"error: output {len(data)} bytes exceeds 1 MiB",
              file=sys.stderr)
        return 1
    # PNG IHDR: width/height are big-endian uint32 at bytes 16..24.
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (1024, 1024):
        print(f"error: output is {width}x{height}, expected 1024x1024",
              file=sys.stderr)
        return 1
    print(f"copied entry.png -> {dst} ({len(data)} bytes, "
          f"{width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
