#!/usr/bin/env python3
"""
Bulk File Renamer
=================
A flexible tool to rename multiple files at once with various patterns.

Features:
- Add prefix/suffix
- Numbering (sequential)
- Replace text in filenames
- Convert case (lower/upper/title)
- Remove specific text
- Dry-run mode for safety

Author: RetroMatt2077
"""

import os
import argparse
from pathlib import Path
from datetime import datetime


def rename_files(directory: str, 
                 prefix: str = "", 
                 suffix: str = "", 
                 numbering: bool = False,
                 start_num: int = 1,
                 replace_old: str = None,
                 replace_new: str = None,
                 case: str = None,
                 remove_text: str = None,
                 dry_run: bool = False):
    
    path = Path(directory)
    if not path.exists():
        print(f"❌ Error: Directory '{directory}' does not exist.")
        return

    files = sorted([f for f in path.iterdir() if f.is_file()])
    
    if not files:
        print("No files found in the directory.")
        return

    print(f"📂 Found {len(files)} files to rename in: {path.resolve()}\n")

    for i, file_path in enumerate(files, start=start_num):
        old_name = file_path.name
        name, ext = file_path.stem, file_path.suffix

        new_name = name

        # Replace text
        if replace_old is not None and replace_new is not None:
            new_name = new_name.replace(replace_old, replace_new)

        # Remove text
        if remove_text:
            new_name = new_name.replace(remove_text, "")

        # Add prefix and suffix
        new_name = f"{prefix}{new_name}{suffix}"

        # Add numbering
        if numbering:
            new_name = f"{new_name}_{i:03d}"  # e.g., file_001

        # Case conversion
        if case == "lower":
            new_name = new_name.lower()
        elif case == "upper":
            new_name = new_name.upper()
        elif case == "title":
            new_name = new_name.title()

        new_filename = new_name + ext
        old_path = file_path
        new_path = file_path.parent / new_filename

        if old_path == new_path:
            print(f"⏭️  Skipped (no change): {old_name}")
            continue

        if not dry_run:
            try:
                old_path.rename(new_path)
                print(f"✅ Renamed: {old_name} → {new_filename}")
            except Exception as e:
                print(f"❌ Failed: {old_name} → {new_filename} | Error: {e}")
        else:
            print(f"[DRY RUN] Would rename: {old_name} → {new_filename}")


def main():
    parser = argparse.ArgumentParser(description="Bulk File Renamer Tool")
    parser.add_argument("directory", nargs="?", default=".", 
                        help="Directory containing files to rename (default: current)")
    
    parser.add_argument("-p", "--prefix", type=str, default="", 
                        help="Add prefix to filenames")
    parser.add_argument("-s", "--suffix", type=str, default="", 
                        help="Add suffix to filenames (before extension)")
    
    parser.add_argument("-n", "--numbering", action="store_true",
                        help="Add sequential numbering (e.g., _001, _002)")
    parser.add_argument("--start", type=int, default=1,
                        help="Starting number for numbering (default: 1)")
    
    parser.add_argument("--replace", nargs=2, metavar=('OLD', 'NEW'),
                        help="Replace OLD text with NEW text in filename")
    parser.add_argument("--remove", type=str,
                        help="Remove specific text from filename")
    
    parser.add_argument("--case", choices=["lower", "upper", "title"],
                        help="Convert filename case")
    
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without actually renaming")

    args = parser.parse_args()

    replace_old, replace_new = None, None
    if args.replace:
        replace_old, replace_new = args.replace

    rename_files(
        directory=args.directory,
        prefix=args.prefix,
        suffix=args.suffix,
        numbering=args.numbering,
        start_num=args.start,
        replace_old=replace_old,
        replace_new=replace_new,
        case=args.case,
        remove_text=args.remove,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
