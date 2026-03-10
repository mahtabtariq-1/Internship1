# Task 03 — Project Directory Auditor

## Topic
Modules: Built-in & Custom

## What This Task Does
The DevOps team needs a tool that scans a given project folder,
collects each file's name, size, type, and last modified date,
then generates a timestamped audit report. Files not modified in
over 30 days are flagged, and a separate penalties report lists
calculated overage fines.

## File Structure
```
Task_03_Project_Directory_Auditor/
├── audit.py               ← Main script — run this
└── scanner/
    ├── __init__.py        ← Makes scanner a Python package
    └── file_scanner.py    ← Custom module with scanning logic
```

## Concepts Used
- `os` module: `getcwd`, `listdir`, `path.join`, `path.exists`, `stat`, `walk`
- `math` module: `ceil`
- `datetime` module: `datetime`, `timedelta`, `strftime`
- Custom importable module (the `scanner` package)
- `import`, `from...import`
- `__init__.py` to create a package
- `__name__ == '__main__'` guard

## How to Run
```bash
# IMPORTANT: must be run from inside this folder
cd Task_03_Project_Directory_Auditor
python audit.py
```

## Output
- Prints audit table in terminal
- Creates `audit_report_TIMESTAMP.txt`
- Creates `penalties_TIMESTAMP.txt`
