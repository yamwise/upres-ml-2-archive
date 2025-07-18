#!/usr/bin/env python3
import os
import re
import argparse

def rename_frames(directory):
    # match "<video>_frame<digits>[_anything].png"
    pattern = re.compile(r'^(?P<video>.+?)_frame(?P<frame>\d+)(?:_.*)?\.png$')
    
    for fname in os.listdir(directory):
        src = os.path.join(directory, fname)
        if not os.path.isfile(src):
            continue

        m = pattern.match(fname)
        if not m:
            continue

        video = m.group('video')      # e.g. "CHA121H" or "plant-26637-1080p"
        frame = m.group('frame')      # e.g. "000000"
        new_name = f"{video}.{frame}.png"
        dst = os.path.join(directory, new_name)

        if os.path.exists(dst):
            print(f"Skipping {fname}: {new_name} already exists")
        else:
            print(f"Renaming {fname} → {new_name}")
            os.rename(src, dst)

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Rename <video>_frame<frame>[_…].png → <video>.<frame>.png"
    )
    p.add_argument(
        "dir",
        nargs="?",
        default=".",
        help="Directory containing frames (default: current dir)"
    )
    args = p.parse_args()
    rename_frames(args.dir)
