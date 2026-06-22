#!/usr/bin/env python3
"""
Backup Tool
===========
Creates timestamped backups of folders as ZIP archives.

Features:
- Timestamped backup files (e.g., MyFolder_2026-06-22_1430.zip)
- Backup single folder or multiple
- Custom backup destination
- Dry-run mode
- Simple and Pydroid friendly

Author: RetroMatt2077
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def create_backup(source_path: str, backup_dir: str = None, dry_run: bool = False):
    """Create a timestamped ZIP backup of a folder."""
    source = Path(source_path)
    
    if not source.exists():
        print(f"❌ Error: Source path '{source}' does not exist.")
        return False
    if not source.is_dir():
        print(f"❌ Error: '{source}' is not a directory.")
        return False

    # Set backup destination
    if backup_dir:
        dest = Path(backup_dir)
    else:
        dest = source.parent / "Backups"
    
    dest.mkdir(parents=True, exist_ok=True)

    # Create timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    folder_name = source.name
    backup_name = f"{folder_name}_{timestamp}"
    backup_path = dest / backup_name

    print(f"📦 Creating backup of: {source}")
    print(f"📍 Backup location: {dest}")
    print(f"📁 Backup name: {backup_name}.zip")

    if dry_run:
        print("🔍 [DRY RUN] Backup would be created successfully!")
        return True

    try:
        # Create the zip archive
        shutil.make_archive(str(backup_path), 'zip', source)
        final_backup = backup_path.with_suffix('.zip')
        
        print(f"✅ Backup completed successfully!")
        print(f"📁 Backup saved as: {final_backup.name}")
        print(f"📏 Size: {final_backup.stat().st_size / (1024*1024):.2f} MB")
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="📦 Folder Backup Tool")
    parser.add_argument("source", nargs="?", default=".", 
                        help="Folder to backup (default: current directory)")
    parser.add_argument("-d", "--dest", "--backup-dir", 
                        help="Destination folder for backups")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without creating backup")
    parser.add_argument("-p", "--prompt", action="store_true",
                        help="Interactive mode (recommended on Pydroid)")

    args = parser.parse_args()

    if args.prompt or not args.source:
        print("📦 Backup Tool\n")
        source = input("Enter folder path to backup (or press Enter for current): ").strip()
        if not source:
            source = "."
        
        dest = input("Enter backup destination (or press Enter for default 'Backups' folder): ").strip()
        if not dest:
            dest = None
    else:
        source = args.source
        dest = args.dest

    create_backup(source, dest, args.dry_run)


if __name__ == "__main__":
    main()
