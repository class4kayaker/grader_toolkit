import pytest
import grader_toolkit
import grader_toolkit.encoder
import io
import sqlalchemy
from ruamel import yaml
import sys
try:
    import typing  # noqa: F401
except:
    pass  # Only currently using typing for annotations, no action necessary


@pytest.fixture(params=[
    'sqlite://'
])
def session(request):
    dbase = request.param
    engine = sqlalchemy.create_engine(dbase)
    grader_toolkit.gradebook.Base.metadata.create_all(engine)
    grader_toolkit.Session.configure(bind=engine)
    yield grader_toolkit.Session()


@pytest.fixture(params=[
    'sqlite://'
])
def session2(request):
    dbase = request.param
    engine = sqlalchemy.create_engine(dbase)
    grader_toolkit.gradebook.Base.metadata.create_all(engine)
    grader_toolkit.Session.configure(bind=engine)
    yield grader_toolkit.Session()


@pytest.fixture
def test_data():
    data = []
    students = []
    s_count = 5
    for i in range(1, s_count):
        students.append(
            grader_toolkit.Student(
                id=i,
                name=u'Student {}'.format(i),
                email=u'test_{}@example.com'.format(i)))
    data.extend(students)
    assignments = []
    for i in range(1, 5):
        assignments.append(
            grader_toolkit.Assignment(
                id=i,
                name=u'Assignment {}'.format(i),
                full_credit=float(2*i)))
    data.extend(assignments)
    for s in students:
        for a in assignments:
            data.append(
                grader_toolkit.Grade(
                    student_id=s.id,
                    assignment_id=a.id,
                    grade=float(s.id)/s_count*a.full_credit,
                    notes=u'Notes {} {}'.format(s.name, a.name)))
    return data


@pytest.fixture
def str_stream():
    if sys.version_info < (3,):
        yield io.BytesIO()
    else:
        yield io.StringIO()


@pytest.mark.parametrize('data', [
    grader_toolkit.Student(
        id=100,
        name=u'Test',
        email=u'test@example.com'),
    grader_toolkit.Assignment(
        id=1,
        name=u'Homework 1',
        full_credit=5.),
    grader_toolkit.Grade(
        student_id=100,
        assignment_id=1,
        grade=4.,
        notes='Long text'),
])
def test_object_roundtrip(session, str_stream, data):
    yaml.dump(data, stream=str_stream)
    str_stream.seek(0)
    data2 = yaml.load(str_stream)
    assert repr(data) == repr(data2)


def test_session_roundtrip(session, session2, str_stream, test_data):
    session.add_all(test_data)
    grader_toolkit.encoder.yaml_dump_session(session, str_stream)
    str_stream.seek(0)
    grader_toolkit.encoder.yaml_load_session(session2, str_stream)
    for s in session.query(grader_toolkit.Student).all():
        s2 = session2.query(grader_toolkit.Student).filter(
            grader_toolkit.Student.id == s.id).one()
        assert repr(s) == repr(s2)
    for a in session.query(grader_toolkit.Assignment).all():
        a2 = session2.query(grader_toolkit.Assignment).filter(
            grader_toolkit.Assignment.id == a.id).one()
        assert repr(a) == repr(a2)
    for g in session.query(grader_toolkit.Grade).all():
        g2 = session2.query(grader_toolkit.Grade).filter(
            sqlalchemy.and_(
                grader_toolkit.Grade.student_id == g.student_id,
                grader_toolkit.Grade.assignment_id == g.assignment_id)
        ).one()
        assert repr(g) == repr(g2)


def test_session_roundtrip_malformed(session, session2, str_stream, test_data):
    session.add_all(test_data)
    grader_toolkit.encoder.yaml_dump_session(session, str_stream)
    str_stream.write('\nmalformed-data[[}}')
    str_stream.seek(0)
    with pytest.raises(yaml.YAMLError):
        grader_toolkit.encoder.yaml_load_session(session2, str_stream)
        assert session.query(grader_toolkit.Student).all() == []
        assert session.query(grader_toolkit.Assignment).all() == []
        assert session.query(grader_toolkit.Grade).all() == []
