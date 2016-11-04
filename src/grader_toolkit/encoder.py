from __future__ import unicode_literals
from ruamel import yaml
from grader_toolkit import Student, Assignment, Grade  # noqa: F401
import sqlalchemy  # noqa: F401
import typing  # noqa: F401
import sys


if sys.version_info < (3,):
    text_type = unicode  # noqa: F821
else:
    text_type = str


class folded_str(str):
    pass


def represent_folded(dumper, data):
    # type: (yaml.Dumper, folded_str) -> yaml.Node
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')

yaml.add_representer(folded_str, represent_folded)


def represent_student(dumper, data):
    # type: (yaml.Dumper, Student) -> yaml.Node
    return dumper.represent_mapping(
        u'!Student',
        {u'id': data.id,
         u'name': data.name,
         u'email': data.email})


def construct_student(loader, node):
    # type: (yaml.Loader, yaml.Node) -> Student
    return Student(**loader.construct_mapping(node))

yaml.add_representer(Student, represent_student)
yaml.add_constructor(u'!Student', construct_student)


def represent_assignment(dumper, data):
    # type: (yaml.Dumper, Assignment) -> yaml.Node
    return dumper.represent_mapping(
        u'!Assignment',
        {u'id': data.id,
         u'name': data.name,
         u'full_credit': data.full_credit})


def construct_assignment(loader, node):
    # type: (yaml.Loader, yaml.Node) -> Assignment
    return Assignment(**loader.construct_mapping(node))

yaml.add_representer(Assignment, represent_assignment)
yaml.add_constructor(u'!Assignment', construct_assignment)


def represent_grade(dumper, data):
    # type: (yaml.Dumper, Grade) -> yaml.Node
    return dumper.represent_mapping(
        '!Grade',
        {'student_id': data.student_id,
         'assignment_id': data.assignment_id,
         'grade': data.grade,
         'notes': folded_str(data.notes)})


def construct_grade(loader, node):
    # type: (yaml.Loader, yaml.Node) -> Grade
    return Grade(**loader.construct_mapping(node))

yaml.add_representer(Grade, represent_grade)
yaml.add_constructor('!Grade', construct_grade)


def yaml_dump_session(session, stream):
    # type: (sqlalchemy.orm.Session, typing.TextIO) -> None
    """Dump data from session as yaml"""
    data = {}
    data['students'] = session.query(Student).all()
    data['assignments'] = session.query(Assignment).all()
    data['grades'] = session.query(Grade).all()
    yaml.dump(data, stream=stream)


def yaml_load_session(session, stream):
    # type: (sqlalchemy.orm.Session, typing.TextIO) -> None
    """Load yaml data into session"""
    try:
        out = yaml.load(stream)
        session.add_all(out['students'])
        session.add_all(out['assignments'])
        session.add_all(out['grades'])
        session.flush()
        session.commit()
    except:
        session.rollback()
        raise
