# modules/exceptions.py - Custom exception classes

class InvalidStudentRecord(Exception):
    pass

class DuplicateStudentError(Exception):
    pass

class StudentNotFoundError(Exception):
    pass

class InvalidGradeError(Exception):
    pass
