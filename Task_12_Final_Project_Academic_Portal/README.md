# Task 12 — Final Project: Academic Portal (Terminal Based)

## Topic
Everything Combined — OOP, File Handling, Exceptions, Decorators,
Generators, Comprehensions, Asyncio, Logging, Modules, .env Config

## What This Task Does
A terminal application to manage student records end to end. It loads data from
CSV files, validates records, flags failed students, calculates late fines, and
generates timestamped reports. All errors are logged through custom exceptions.
Built with OOP, uses decorators, runs concurrently with `asyncio`, and uses a
secure `.env` config.

## File Structure
```
Task_12_Final_Project_Academic_Portal/
├── portal.py              ← MAIN SCRIPT — run this
├── .env                   ← Config: passwords, passing marks, fine rate
├── data/
│   └── cs_students.csv    ← Sample student data (CSV)
├── reports/               ← Auto-created — stores generated reports
└── modules/
    ├── __init__.py        ← Makes modules/ a Python package
    ├── exceptions.py      ← Custom exception classes
    ├── student.py         ← Student + ScholarshipStudent OOP classes
    └── data_loader.py     ← CSV reading with full exception handling
```

## What Each Module File Does

### `modules/exceptions.py`
Contains only custom exception classes:
- `InvalidStudentRecord` — raised for missing name/ID
- `DuplicateStudentError` — raised for repeated roll numbers
- `StudentNotFoundError` — raised when searching for a non-existent student
- `InvalidGradeError` — raised for marks out of 0-100 range

### `modules/student.py`
Contains the OOP class hierarchy:
- `Person` (Abstract Base Class) — name, person_id, abstract methods
- `Student(Person)` — stores private `__grades`, calculates average, determines PASS/FAIL
- `ScholarshipStudent(Student)` — overrides `status` to require 70+ average

### `modules/data_loader.py`
Handles all CSV file reading:
- Reads each row, validates it, creates Student or ScholarshipStudent objects
- Catches corrupted rows, missing fields, invalid marks, duplicates
- Returns a clean list of students + list of error messages

### `modules/__init__.py`
Makes `modules/` a Python package and re-exports key names so `portal.py` can do:
```python
from modules import load_students_from_csv, Student, ScholarshipStudent
```

## Concepts Demonstrated
| Concept | Where Used |
|---|---|
| OOP + Inheritance | `student.py` — Person → Student → ScholarshipStudent |
| Abstract Base Class | `Person` uses `@abstractmethod` |
| Private attributes | `Student.__grades` (double underscore) |
| @property | `Student.average`, `Student.status`, `Student.fine` |
| Custom Exceptions | `exceptions.py`, raised in `data_loader.py` |
| File Handling (CSV) | `data_loader.py` using `csv.DictReader` |
| Decorators | `@log_action`, `@require_admin` in `portal.py` |
| Generators | `failed_students_stream()` using `yield` |
| Comprehensions | Throughout — list, dict, generator expressions |
| asyncio | `load_all_files()` loads CSVs concurrently |
| logging module | DEBUG/INFO/WARNING/ERROR to file + console |
| .env config | `python-dotenv` loads `ADMIN_PASSWORD`, `PASSING_MARKS`, etc. |
| Binary Search | `search_student()` in `portal.py` |
| Sorting | `sorted()` with lambda key for rankings |
| Custom Modules | `modules/` package imported into `portal.py` |

## Setup
```bash
pip install python-dotenv
```

## How to Run
```bash
# IMPORTANT: must run from inside this folder
cd Task_12_Final_Project_Academic_Portal
python portal.py
```

## Menu Options
```
[1] View All Students          — ranked by average
[2] Search Student by Name     — uses binary search
[3] View Failed Students       — streamed via generator
[4] View Fines Report          — shows late day fines
[5] Generate Full Report       — needs admin password (admin123)
[6] Top 5 by Average
[0] Exit
```

## .env Config
```
PORTAL_NAME=University Academic Portal
ADMIN_PASSWORD=admin123
PASSING_MARKS=50
FINE_PER_DAY=10
```
You can change these values without touching any Python code.
