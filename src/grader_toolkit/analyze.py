import grader_toolkit  # noqa: F401
import math
try:
    import typing  # noqa: F401
except:
    pass


def analyze_numeric_grades(grades, stream, short=False):
    full = 0.
    s = 0.
    sq = 0.
    for g in grades:
        full += g.assignment.full_credit
        s += g.grade
        sq += g.grade**2
    stream.write('Percent Average: {:%}'.format(s/full))
    stream.write('Percent Dev: {:%}'.format(math.sqrt((sq-s**2)/full**2)))


def analyze_student(student, stream, short=False):
    # type: (grader_toolkit.Student, typing.TextIO, bool) -> None
    stream.write('Name: {}'.format(student.name))
    analyze_numeric_grades(student.grades, stream)
    if short:
        return
    for g in student.grades:
        stream.write('Assignment: {}'.format(g.assignment.name))
        stream.write('Grade: {}'.format(g.grade))
        stream.write('Notes: {}'.format(g.notes))


def analyze_assignment(assignment, stream, short=False):
    # type: (grader_toolkit.Student, typing.TextIO, bool) -> None
    stream.write('Assignment: {}'.format(assignment.name))
    analyze_numeric_grades(assignment.grades, stream, short)
