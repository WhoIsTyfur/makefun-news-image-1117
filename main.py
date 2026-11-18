"""make.fun news-image-20261117 entry: write the front page for Tuesday 17 November 2026.

The picture is drawn ahead of time by art/draw.py and committed as entry.png; this program
copies those bytes unchanged to /output/entry.png (or $MAKEFUN_OUTPUT_DIR), so both runs
write identical bytes and no network is needed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def check_png(data: bytes) -> None:
    """Fail loudly if the committed image would not pass the contest's gate."""
    if not data.startswith(PNG_SIG):
        raise SystemExit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over 1 MiB")
    w = int.from_bytes(data[16:20], "big")
    h = int.from_bytes(data[20:24], "big")
    if not (0 < w <= MAX_SIDE and 0 < h <= MAX_SIDE):
        raise SystemExit(f"entry.png is {w}x{h}, over {MAX_SIDE}x{MAX_SIDE}")
    if not data.endswith(b"IEND\xaeB`\x82"):
        raise SystemExit("entry.png is truncated (no IEND chunk)")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    with open(os.path.join(HERE, "entry.png"), "rb") as f:
        data = f.read()
    check_png(data)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
