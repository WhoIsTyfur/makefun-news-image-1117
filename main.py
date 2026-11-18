"""make.fun news-image-20261117 entry: write the front page for Tuesday 17 November 2026.

The picture is drawn ahead of time by art/draw.py and committed as entry.png; this program
copies those bytes unchanged to /output/entry.png (or $MAKEFUN_OUTPUT_DIR), so both runs
write identical bytes and no network is needed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    with open(os.path.join(HERE, "entry.png"), "rb") as f:
        data = f.read()
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
