# Task 3: Project Directory Auditor
# Approach: We use a custom module (scanner package) to scan a given folder.
# It collects file name, size, type, last modified date, flags old files (>30 days),
# calculates fines, and writes a timestamped audit report.

import os
import math
from datetime import datetime
from scanner import scan_folder, get_flagged, get_total_fines

# ---- Setup: create a fake project folder with some test files ----
def make_test_project():
    os.makedirs("sample_project/src", exist_ok=True)
    os.makedirs("sample_project/docs", exist_ok=True)

    files = [
        ("sample_project/src/main.py", "print('hello world')"),
        ("sample_project/src/utils.py", "# utility functions"),
        ("sample_project/docs/readme.txt", "Project readme file content here."),
        ("sample_project/docs/notes.md", "# Notes\n- todo list"),
        ("sample_project/config.json", '{"debug": true}'),
    ]
    for fpath, content in files:
        with open(fpath, "w") as f:
            f.write(content)

make_test_project()

# ---- Run the audit ----
target_folder = "sample_project"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("=" * 58)
print("         PROJECT DIRECTORY AUDITOR")
print("=" * 58)
print(f"Scanning: {os.path.abspath(target_folder)}")
print(f"Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

files = scan_folder(target_folder)
flagged = get_flagged(files)
total_fine = get_total_fines(files)

# print all files
print(f"{'File':<25} {'Type':<12} {'Size':>8}  {'Last Modified':<18} {'Days':>5}  {'Flag'}")
print("-" * 85)
for f in files:
    size_kb = math.ceil(f["size_bytes"] / 1024) if f["size_bytes"] > 0 else 0
    flag_txt = "*** FLAGGED ***" if f["flagged"] else ""
    print(f"{f['name']:<25} {f['type']:<12} {str(size_kb)+'KB':>8}  {f['last_modified']:<18} {f['days_old']:>5}  {flag_txt}")

# ---- Write main audit report ----
report_name = f"audit_report_{timestamp}.txt"
with open(report_name, "w") as rep:
    rep.write(f"AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    rep.write(f"Target: {target_folder}\n")
    rep.write("=" * 60 + "\n")
    rep.write(f"Total files scanned : {len(files)}\n")
    rep.write(f"Flagged (>30 days)  : {len(flagged)}\n")
    rep.write(f"Total fines         : Rs. {total_fine}\n\n")
    rep.write(f"{'File':<25} {'Type':<10} {'Size':>8} {'Days':>5}  {'Status'}\n")
    rep.write("-" * 65 + "\n")
    for f in files:
        size_kb = math.ceil(f["size_bytes"] / 1024)
        status = "FLAGGED" if f["flagged"] else "OK"
        rep.write(f"{f['name']:<25} {f['type']:<10} {size_kb:>7}KB {f['days_old']:>5}  {status}\n")

# ---- Write penalties report ----
penalties_name = f"penalties_{timestamp}.txt"
with open(penalties_name, "w") as pf:
    pf.write(f"PENALTIES REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    pf.write("=" * 45 + "\n")
    if flagged:
        for f in flagged:
            pf.write(f"File  : {f['name']}\n")
            pf.write(f"Days  : {f['days_old']} (over by {f['days_old']-30} days)\n")
            pf.write(f"Fine  : Rs. {f['fine']}\n\n")
        pf.write(f"TOTAL FINE: Rs. {total_fine}\n")
    else:
        pf.write("No penalties. All files are within 30-day limit.\n")

print("\n" + "=" * 58)
print(f"Flagged files : {len(flagged)}")
print(f"Total fines   : Rs. {total_fine}")
print(f"\nReports saved:")
print(f"  - {report_name}")
print(f"  - {penalties_name}")

if __name__ == '__main__':
    pass
