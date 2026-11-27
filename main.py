"""News 26 R3 entrypoint: copies entry.png to the output directory.

Stdlib only. Never imports PIL or render.py: the grader's sandbox has no
Pillow, and this program must run there.
"""

import os
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    bot_dir = Path(os.environ.get("MAKEFUN_BOT_DIR", Path(__file__).resolve().parent))
    src = bot_dir / "entry.png"
    if not src.is_file():
        print(f"entry.png not found in {bot_dir}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    data = dst.read_bytes()
    if data[:8] != PNG_MAGIC:
        print("output is not a PNG", file=sys.stderr)
        return 1
    if len(data) < 10_000:
        print(f"output suspiciously small: {len(data)} bytes", file=sys.stderr)
        return 1
    if len(data) != src.stat().st_size:
        print("output size differs from entry.png", file=sys.stderr)
        return 1
    print(f"copied {src} -> {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
