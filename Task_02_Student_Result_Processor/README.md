# Task 02 — Student Result Processor

## Topic
File Handling & Exception Handling

## What This Task Does
The academic department has CSV files of student records in a folder.
Some files are corrupted, some are missing, and some have invalid data.
This script reads all files safely, flags failed students (marks < 50),
and writes a clean results CSV without ever crashing.

## Concepts Used
- `open()` with `with` statement
- CSV module: `csv.DictReader`, `csv.DictWriter`
- `try / except / else / finally`
- Custom exception class: `InvalidRecordError`
- `os.makedirs()`, `os.listdir()`
- Catching: `FileNotFoundError`, `ValueError`, `TypeError`

## Files Created by the Script
- `student_files/` — folder with sample CSV files (auto-created)
- `clean_results.csv` — the cleaned output file

## How to Run
```bash
python student_result_processor.py
```

## Sample Output
```
Reading: class_A.csv
  -> Ali Hassan (101): 78.0 [PASS]
  -> Sara Khan (102): 45.0 [FAIL]
  ...

SUMMARY
Total processed : 6
Passed          : 4
Failed          : 2
```
