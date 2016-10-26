import grader_toolkit
import pytest
try:
    import typing  # noqa: F401
except:
    pass  # Only currently using typing for annotations, no action necessary


@pytest.fixture(params=[
    ':memory:',
])
def gbook(request):
    # type: (pytest.Request) -> grader_toolkit.Gradebook
    return grader_toolkit.Gradebook(request.param)


@pytest.fixture(params=[
    0,
    1,
])
def student_set(request):
    # type: (pytest.Request) -> Dict[int, grader_toolkit.Student]
    if request.param == 0:
        return {
            1: grader_toolkit.Student(
                1, 'First', 'Last', 'test@example.com'),
            2: grader_toolkit.Student(
                2, 'First_2', 'Last_2', 'test2@example.com'),
        }
    elif request.param == 1:
        return {
            1: grader_toolkit.Student(
                1, 'First_1', 'Last_1', 'test@example.com'),
            2: grader_toolkit.Student(
                2, 'First_2', 'Last_2', 'test2@example.com'),
        }


@pytest.fixture(params=[
    0,
    1,
])
def assignment_set(request):
    # type: (pytest.Request) -> Dict[int, grader_toolkit.Assignment]
    if request.param == 0:
        return {
            1: grader_toolkit.Assignment(
                1, 'Homework 1'),
            2: grader_toolkit.Assignment(
                2, 'Homework 2'),
        }
    elif request.param == 1:
        return {
            1: grader_toolkit.Assignment(
                1, 'Test 1'),
            2: grader_toolkit.Assignment(
                2, 'Test 2'),
        }


@pytest.fixture
def grade_set(request,  # type: pytest.Request
              student_set,  # type: Dict[int, grader_toolkit.Student]
              assignment_set  # type: Dict[int grader_toolkit.Assignment]
              ):
    # type: (...) -> Dict[typing.Tuple[int, int], grader_toolkit.Grade]
    ret = {}
    for st_id in student_set:
        for a_id in assignment_set:
            ret[(st_id, a_id)] = (
                grader_toolkit.Grade(
                    student_set[st_id],
                    assignment_set[a_id],
                    4.,
                    'Notes'))
    return ret


def test_db_students(gbook,  # type: grader_toolkit.Gradebook
                     student_set  # type: Dict[int, grader_toolkit.Student]
                     ):
    # type: (...) -> None
    for ID in student_set:
        gbook.add_student(student_set[ID])
    for ID in student_set:
        assert student_set[ID] == gbook.get_student_by_id(ID)
        gbook.delete_student(ID)
    assert gbook.get_students() == []
    gbook.add_students([student_set[ID] for ID in student_set])
    for s in gbook.get_students():
        ID = s.student_id
        assert s == student_set[ID]
    for ID in student_set:
        gbook.delete_student(ID)
    assert gbook.get_students() == []


def test_db_assignments(
        gbook,  # type: grader_toolkit.Gradebook
        assignment_set,  # type: Dict[int, grader_toolkit.Assignment]
):
    # type: (...) -> None
    for ID in assignment_set:
        gbook.add_assignment(assignment_set[ID])
    for ID in assignment_set:
        assert assignment_set[ID] == gbook.get_assignment_by_id(ID)
        gbook.delete_assignment(ID)
    assert gbook.get_assignments() == []
    gbook.add_assignments([assignment_set[ID] for ID in assignment_set])
    for s in gbook.get_assignments():
        ID = s.assign_id
        assert s == assignment_set[ID]
    for ID in assignment_set:
        gbook.delete_assignment(ID)
    assert gbook.get_assignments() == []
