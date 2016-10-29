import yaml
from grader_toolkit import Student, Assignment, Grade  # noqa: F401


class folded_str(str):
    pass


def represent_folded(dumper, data):
    # type: (yaml.Dumper, folded_str) -> yaml.Node
    return dumper.represent_scalar(u'tag:yaml:org,2002:str', data, style='>')

yaml.add_representer(folded_str, represent_folded)


def represent_student(dumper, data):
    # type: (yaml.Dumper, Student) -> yaml.Node
    return dumper.represent_mapping(
        '!Student',
        {'id': data.id,
         'name': data.name,
         'email': data.email})


def construct_student(loader, node):
    # type: (yaml.Loader, yaml.Node) -> Student
    return Student(**loader.construct_mapping(node))

yaml.add_representer(Student, represent_student)
yaml.add_constructor('!Student', construct_student)


def represent_assignment(dumper, data):
    # type: (yaml.Dumper, Assignment) -> yaml.Node
    return dumper.represent_mapping(
        '!Assignment',
        {'id': data.id,
         'name': data.name,
         'full_credit': data.full_credit})


def construct_assignment(loader, node):
    # type: (yaml.Loader, yaml.Node) -> Assignment
    return Assignment(**loader.construct_mapping(node))

yaml.add_representer(Assignment, represent_assignment)
yaml.add_constructor('!Assignment', construct_assignment)


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
