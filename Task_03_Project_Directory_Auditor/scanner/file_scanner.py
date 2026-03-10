# scanner/file_scanner.py
# Custom module that does the actual scanning of files in a directory

import os
from datetime import datetime, timedelta

FINE_PER_DAY = 10  # Rs. 10 per day after 30-day limit

def scan_folder(path):
    """Scans a folder and returns info about each file."""
    results = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"Folder not found: {path}")

    for root, dirs, files in os.walk(path):
        for fname in files:
            full_path = os.path.join(root, fname)
            try:
                stat = os.stat(full_path)
                size = stat.st_size
                last_modified = datetime.fromtimestamp(stat.st_mtime)
                days_old = (datetime.now() - last_modified).days
                file_ext = os.path.splitext(fname)[1] or "no extension"

                flagged = days_old > 30
                fine = (days_old - 30) * FINE_PER_DAY if flagged else 0

                results.append({
                    "name": fname,
                    "path": full_path,
                    "size_bytes": size,
                    "type": file_ext,
                    "last_modified": last_modified.strftime("%Y-%m-%d %H:%M"),
                    "days_old": days_old,
                    "flagged": flagged,
                    "fine": fine
                })
            except Exception as e:
                print(f"  [WARN] Could not stat {fname}: {e}")

    return results


def get_flagged(file_list):
    return [f for f in file_list if f["flagged"]]


def get_total_fines(file_list):
    return sum(f["fine"] for f in file_list)
