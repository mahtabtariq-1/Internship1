# modules/data_loader.py - Handles CSV reading with exception handling

import csv
import os
import logging
from modules.student import Student, ScholarshipStudent
from modules.exceptions import InvalidStudentRecord, InvalidGradeError, DuplicateStudentError

logger = logging.getLogger("portal.loader")

def load_students_from_csv(filepath):
    """Reads a CSV file and returns a list of Student objects."""
    students = []
    errors = []
    seen_ids = set()

    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return students, errors

    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                logger.warning(f"Empty file: {filepath}")
                return students, errors

            for i, row in enumerate(reader, 1):
                try:
                    student_id = row.get("student_id", "").strip()
                    name       = row.get("name", "").strip()
                    dept       = row.get("department", "").strip()
                    semester   = row.get("semester", "").strip()
                    late_days  = row.get("late_days", "0").strip()
                    scholarship= row.get("scholarship", "").strip()

                    if not student_id or not name:
                        raise InvalidStudentRecord(f"Row {i}: Missing ID or name")

                    if student_id in seen_ids:
                        raise DuplicateStudentError(f"Row {i}: Duplicate ID {student_id}")
                    seen_ids.add(student_id)

                    late_days_val = int(late_days) if late_days.isdigit() else 0

                    if scholarship:
                        s = ScholarshipStudent(name, student_id, dept, semester, float(scholarship))
                    else:
                        s = Student(name, student_id, dept, semester)

                    s.late_days = late_days_val

                    # load subject grades (any extra columns are subjects)
                    skip_cols = {"student_id","name","department","semester","late_days","scholarship"}
                    for col in reader.fieldnames:
                        if col not in skip_cols:
                            val = row.get(col, "").strip()
                            if val:
                                try:
                                    s.add_grade(col, val)
                                except InvalidGradeError as e:
                                    logger.warning(f"  Grade issue for {name}: {e}")

                    students.append(s)
                    logger.info(f"Loaded: {name} ({student_id})")

                except (InvalidStudentRecord, DuplicateStudentError, InvalidGradeError) as e:
                    logger.error(f"Skipped row {i} in {os.path.basename(filepath)}: {e}")
                    errors.append(str(e))

    except Exception as e:
        logger.error(f"Could not read {filepath}: {e}")
        errors.append(str(e))

    return students, errors
