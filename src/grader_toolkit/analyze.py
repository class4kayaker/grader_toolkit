import grader_toolkit  # noqa: F401
import math
try:
    import typing  # noqa: F401
except:
    pass


def analyze_numeric_grades(grades, stream, short=False):
    full = 0.
    s = 0.
    for g in grades:
        full += g.assignment.full_credit
        s += g.grade
    stream.write('Percent Average: {:.2%}\n'.format(s/full))


def analyze_student(student, stream, short=False):
    # type: (grader_toolkit.Student, typing.TextIO, bool) -> None
    stream.write('Name: {}\n'.format(student.name))
    analyze_numeric_grades(student.grades, stream)
    if short:
        return
    for g in student.grades:
        stream.write('Assignment: {}\n'.format(g.assignment.name))
        stream.write('Grade: {}\n'.format(g.grade))
        stream.write('Notes:\n{}\n'.format(g.notes))


def analyze_assignment(assignment, stream, short=False):
    # type: (grader_toolkit.Student, typing.TextIO, bool) -> None
    stream.write('Assignment: {}\n'.format(assignment.name))
    analyze_numeric_grades(assignment.grades, stream, short)
