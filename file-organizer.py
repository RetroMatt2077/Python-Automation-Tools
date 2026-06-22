#!/usr/bin/env python3
"""
File Organizer
==============
Automatically organizes files in a directory into categorized folders
by file type, creation date, or both.

Author: RetroMatt2077
"""

import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# File type categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
    "Executables": [".exe", ".app", ".msi", ".deb", ".rpm"],
    "Other": []  # Catch-all
}

def get_category(extension: str) -> str:
    """Return the category for a given file extension."""
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize_by_type(source_dir: str, dry_run: bool = False):
    """Organize files by their type (extension)."""
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"❌ Error: Directory '{source_dir}' does not exist.")
        return

    moved = defaultdict(int)

    for file_path in source_path.iterdir():
        if file_path.is_file():
            category = get_category(file_path.suffix)
            dest_dir = source_path / category

            if not dry_run:
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(dest_dir / file_path.name))

            moved[category] += 1
            print(f"{'[DRY RUN] ' if dry_run else ''}Moved: {file_path.name} → {category}/")

    print("\n✅ Organization complete!")
    for category, count in moved.items():
        print(f"   {category}: {count} files")


def organize_by_date(source_dir: str, dry_run: bool = False):
    """Organize files into Year/Month folders based on creation date."""
    source_path = Path(source_dir)
    moved = 0

    for file_path in source_path.iterdir():
        if file_path.is_file():
            # Get file creation/modification date
            timestamp = file_path.stat().st_mtime
            date = datetime.fromtimestamp(timestamp)
            year_month = date.strftime("%Y/%B")  # e.g., 2026/June

            dest_dir = source_path / year_month

            if not dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest_dir / file_path.name))

            print(f"{'[DRY RUN] ' if dry_run else ''}Moved: {file_path.name} → {year_month}/")
            moved += 1

    print(f"\n✅ Date organization complete! {moved} files moved.")


def main():
    parser = argparse.ArgumentParser(description="File Organizer Tool")
    parser.add_argument("directory", nargs="?", default=".", 
                        help="Directory to organize (default: current)")
    parser.add_argument("-t", "--type", action="store_true",
                        help="Organize by file type")
    parser.add_argument("-d", "--date", action="store_true",
                        help="Organize by creation date (Year/Month)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without moving files")

    args = parser.parse_args()

    print(f"📂 Organizing files in: {Path(args.directory).resolve()}\n")

    if args.type:
        organize_by_type(args.directory, args.dry_run)
    elif args.date:
        organize_by_date(args.directory, args.dry_run)
    else:
        # Default: organize by type
        organize_by_type(args.directory, args.dry_run)


if __name__ == "__main__":
    main()
