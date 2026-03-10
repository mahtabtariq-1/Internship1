# modules/student.py - Student OOP classes with inheritance

from abc import ABC, abstractmethod
from modules.exceptions import InvalidStudentRecord, InvalidGradeError
import os

PASSING_MARKS = float(os.getenv("PASSING_MARKS", 50))

class Person(ABC):
    """Base class for any person in the system."""
    def __init__(self, name, person_id):
        if not name or not person_id:
            raise InvalidStudentRecord("Name and ID cannot be empty")
        self.name = name.strip()
        self.person_id = str(person_id).strip()

    @abstractmethod
    def get_summary(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}[{self.person_id}] - {self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id='{self.person_id}', name='{self.name}')"

    def __eq__(self, other):
        return isinstance(other, Person) and self.person_id == other.person_id

    def __hash__(self):
        return hash(self.person_id)


class Student(Person):
    """Regular student with subjects and grades."""
    def __init__(self, name, student_id, department, semester):
        super().__init__(name, student_id)
        self.department = department.strip()
        self.semester = semester
        self.__grades = {}   # subject -> marks (private)
        self.late_days = 0

    def add_grade(self, subject, marks):
        try:
            marks = float(marks)
        except (ValueError, TypeError):
            raise InvalidGradeError(f"Invalid marks '{marks}' for subject '{subject}'")
        if not (0 <= marks <= 100):
            raise InvalidGradeError(f"Marks must be between 0-100, got {marks}")
        self.__grades[subject.strip()] = marks

    @property
    def grades(self):
        return dict(self.__grades)   # return copy

    @property
    def average(self):
        if not self.__grades:
            return 0.0
        return round(sum(self.__grades.values()) / len(self.__grades), 2)

    @property
    def status(self):
        # fail if any subject below passing or average below passing
        if not self.__grades:
            return "No Grades"
        failed_subjects = [s for s, m in self.__grades.items() if m < PASSING_MARKS]
        if failed_subjects:
            return f"FAIL ({', '.join(failed_subjects)})"
        return "PASS"

    @property
    def fine(self):
        fine_per_day = float(os.getenv("FINE_PER_DAY", 10))
        return self.late_days * fine_per_day

    def get_summary(self):
        lines = [
            f"  Name       : {self.name}",
            f"  ID         : {self.person_id}",
            f"  Dept       : {self.department} | Semester: {self.semester}",
            f"  Average    : {self.average}",
            f"  Status     : {self.status}",
        ]
        if self.fine > 0:
            lines.append(f"  Fine       : Rs. {self.fine} ({self.late_days} late days)")
        for subj, marks in self.__grades.items():
            lines.append(f"    {subj:<20}: {marks}")
        return "\n".join(lines)

    def __lt__(self, other):
        return self.average < other.average

    def __gt__(self, other):
        return self.average > other.average

    def __len__(self):
        return len(self.__grades)


class ScholarshipStudent(Student):
    """Student with scholarship — higher passing threshold."""
    def __init__(self, name, student_id, department, semester, scholarship_amount):
        super().__init__(name, student_id, department, semester)
        self.scholarship_amount = scholarship_amount

    @property
    def status(self):
        # scholarship students must maintain 70+ average
        if self.average < 70:
            return "SCHOLARSHIP AT RISK"
        return super().status

    def get_summary(self):
        base = super().get_summary()
        return base + f"\n  Scholarship: Rs. {self.scholarship_amount:,}"
