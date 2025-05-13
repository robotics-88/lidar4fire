#!/usr/bin/env python3
"""
truncate_laz.py: Truncate a LAZ file by extracting a bounding-box segment of given size
from the lower-right corner of its total bounding box.

Usage:
    python truncate_laz.py input.laz --x_len 50 --y_len 30

This script renames the original file to add `_original` before the extension,
then writes the truncated result back to the original filename.

Dependencies:
    pip install laspy numpy
"""
import argparse
import laspy
import numpy as np
import sys
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser(
        description="Truncate a LAZ file to a box of given X and Y size from its lower-right corner, renaming the original file and saving the result under the original name."
    )
    p.add_argument('input', help='Input LAZ/LAS file path')
    p.add_argument('--x_len', type=float, required=True,
                   help='Box width in meters (X direction)')
    p.add_argument('--y_len', type=float, required=True,
                   help='Box height in meters (Y direction)')
    return p.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Compute the new name for the original file
    suffix = input_path.suffix
    stem = input_path.stem
    original_path = input_path.with_name(f"{stem}_original{suffix}")

    # Rename the original file
    try:
        input_path.rename(original_path)
    except Exception as e:
        print(f"Error renaming '{input_path}' to '{original_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Read the renamed original file
    try:
        las = laspy.read(original_path)
    except Exception as e:
        print(f"Error reading '{original_path}': {e}", file=sys.stderr)
        sys.exit(1)

    xs = las.x
    ys = las.y

    # Compute total bounds
    min_x, max_x = float(xs.min()), float(xs.max())
    min_y, max_y = float(ys.min()), float(ys.max())

    # Compute truncation box from lower-right corner (max_x, min_y)
    x0 = max_x - args.x_len
    x1 = max_x
    y0 = min_y
    y1 = min_y + args.y_len

    # Warn if box extends beyond original bounds
    if x0 < min_x:
        print(f"Warning: requested x_len ({args.x_len}) exceeds total X range ({max_x-min_x}); cropping at min_x.")
        x0 = min_x
    if y1 > max_y:
        print(f"Warning: requested y_len ({args.y_len}) exceeds total Y range ({max_y-min_y}); cropping at max_y.")
        y1 = max_y

    # Create boolean mask of points inside the box
    mask = (xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1)
    count = mask.sum()

    if count == 0:
        print("No points found in the specified box; no output written.")
        sys.exit(0)

    # Slice LAS data by mask
    truncated = las[mask]

    # Write out truncated data to the original filename
    try:
        truncated.write(input_path)
        print(f"Wrote {count} points to '{input_path}' (original moved to '{original_path}')")
    except Exception as e:
        print(f"Error writing '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
