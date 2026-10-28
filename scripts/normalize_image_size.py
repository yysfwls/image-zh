#!/usr/bin/env python3
"""Check a localized image against its source and normalize pixel dimensions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print(
        "Pillow is required. Install it with: python3 -m pip install Pillow",
        file=sys.stderr,
    )
    raise SystemExit(2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare a localized image with its original and resize the localized "
            "image to the original pixel dimensions when needed."
        )
    )
    parser.add_argument("original", type=Path, help="Original image used as the size reference")
    parser.add_argument("localized", type=Path, help="Localized image to check")
    parser.add_argument(
        "--output",
        type=Path,
        help="Destination for the normalized image; defaults to a -normalized sibling",
    )
    return parser.parse_args()


def default_output(path: Path) -> Path:
    return path.with_name(f"{path.stem}-normalized{path.suffix}")


def main() -> int:
    args = parse_args()
    original = args.original.expanduser().resolve()
    localized = args.localized.expanduser().resolve()

    for label, path in (("original", original), ("localized", localized)):
        if not path.is_file():
            print(f"{label} image not found: {path}", file=sys.stderr)
            return 2

    with Image.open(original) as original_image:
        target_size = original_image.size

    with Image.open(localized) as localized_image:
        current_size = localized_image.size
        print(f"original:  {target_size[0]}x{target_size[1]}  {original}")
        print(f"localized: {current_size[0]}x{current_size[1]}  {localized}")

        if current_size == target_size:
            print("size check: OK; no normalization needed")
            return 0

        output = (args.output or default_output(localized)).expanduser().resolve()
        if output == localized:
            print("refusing to overwrite the localized input; choose a new --output path", file=sys.stderr)
            return 2
        if output.exists():
            print(f"output already exists: {output}", file=sys.stderr)
            return 2

        output.parent.mkdir(parents=True, exist_ok=True)
        normalized = localized_image.resize(target_size, Image.Resampling.LANCZOS)
        normalized.save(output)

    with Image.open(output) as result:
        if result.size != target_size:
            print(f"normalization verification failed: {result.size}", file=sys.stderr)
            return 1

    print(f"normalized: {target_size[0]}x{target_size[1]}  {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
