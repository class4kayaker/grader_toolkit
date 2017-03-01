from __future__ import division
import grader_toolkit  # noqa: F401
import math
try:
    import typing  # noqa: F401
except:
    pass


def analyze_numeric_grades(grades, stream):
    # type: (List[grader_toolkit.Grade], typing.TextIO) -> None
    full = 0.
    s = 0.
    var = 0.
    for g in grades:
        grade = g.grade
        credit = g.assignment.full_credit
        perc = grade/credit
        full += credit
        s += grade
        var += credit*perc**2
    avg = s/full
    var = math.sqrt(var/full - avg**2)
    stream.write('Percent Average: {:.2%}\n'.format(avg))
    stream.write('Percent Variance: {:.2%}\n'.format(var))


def freq_grades(grades, stream, bins=10):
    # type: (List[float], typing.TextIO, int) -> None
    if bins < 0:
        raise ValueError("Argument bins={} not valid (<0)".format(bins))
    if bins == 0:
        return
    mxgrade = max(grades)
    mngrade = min(grades)
    gset = set(grades)
    if len(gset) < bins:
        stream.write("{:^21s}|{:^10s}\n".format("Grade", "Count"))
        for grade in gset:
            count = len([g for g in grades if g == grade])
            stream.write("{:^21.4g}|{:^10.4g}\n".format(grade, count))
    else:
        binsize = (mxgrade-mngrade)/bins
        stream.write('{:^21s}|{:^10s}\n'.format("Band", "Count"))
        for i in range(bins):
            count = len([g for g in grades if (i == int((g-mngrade)/binsize))])
            stream.write("{:^10.4g}-{:^10.4g}|{:^10d}\n".format(
                mngrade+i*binsize, mngrade+(i+1)*binsize, count))


def analyze_student(student, stream, short=False):
    # type: (grader_toolkit.Student, typing.TextIO, bool) -> None
    stream.write('Name: {}\n'.format(student.name))
    analyze_numeric_grades(student.grades, stream)
    if short:
        return
    for g in student.grades:
        stream.write('Assignment: {}\n'.format(g.assignment.name))
        stream.write('Grade: {0.grade}/{0.assignment.full_credit}\n'
                     .format(g))
        stream.write('Notes:\n{}\n'.format(g.notes))


def analyze_assignment(assignment, stream, short=False):
    # type: (grader_toolkit.Student, typing.TextIO, bool) -> None
    stream.write('Assignment: {}\n'.format(assignment.name))
    analyze_numeric_grades(assignment.grades, stream)
    freq_grades([g.grade for g in assignment.grades], stream)
    if short:
        return
    for g in assignment.grades:
        stream.write('Student: {}\n'.format(g.student.name))
        stream.write('Grade: {0.grade}/{0.assignment.full_credit}\n'
                     .format(g))
        stream.write('Notes:\n{}\n'.format(g.notes))
