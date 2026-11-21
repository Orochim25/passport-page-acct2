"""Republic of Dunvar -- Salt-Flat Boatman's Passport.

Entry for make.fun "The Passport Page of a Country That Isn't There".
The program copies the pre-rendered passport spread (entry.png, 1024x1024)
to the output directory required by the harness.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

ENTRY_NAME = "entry.png"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path: Path) -> tuple[int, int]:
    """Read width and height from a PNG IHDR chunk (stdlib only)."""
    with path.open("rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def output_dir() -> Path:
    """Resolve the harness output directory, falling back to /output."""
    raw = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip()
    return Path(raw) if raw else Path("/output")


def main() -> int:
    source = Path(__file__).resolve().parent / ENTRY_NAME
    if not source.is_file():
        print(f"missing {ENTRY_NAME} next to main.py (looked in {source.parent})", file=sys.stderr)
        return 1
    if source.stat().st_size > MAX_BYTES:
        print(f"{ENTRY_NAME} exceeds {MAX_BYTES} bytes", file=sys.stderr)
        return 1
    width, height = png_dimensions(source)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"{ENTRY_NAME} is {width}x{height}, expected 1024x1024", file=sys.stderr)
        return 1
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / ENTRY_NAME
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
