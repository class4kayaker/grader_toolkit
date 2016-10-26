import sqlite3
try:
    import typing  # noqa: F401
except:
    pass


class Student:
    __slots__ = ('student_id', 'f_name', 'l_name', 'email')

    def __init__(self, student_id, f_name, l_name, email):
        # type: (int, typing.Text, typing.Text, typing.Text) -> None
        self.student_id = student_id
        self.f_name = f_name
        self.l_name = l_name
        self.email = email

    def get_name(self, order='lf'):
        # type: (typing.Text) -> typing.Text
        if order == 'lf':
            fmt = '{l}, {f}'
        elif order == 'fl':
            fmt = '{f} {l}'
        else:
            raise ValueError('Invalid order value')
        return fmt.format(f=self.f_name, l=self.l_name)

    def __repr__(self):
        # type: () -> str
        return '{f} {l}[{ID}]: {email}'.format(
            f=self.f_name,
            l=self.l_name,
            ID=self.student_id,
            email=self.email)

    def __eq__(self, other):
        # type: (typing.Any) -> bool
        if not isinstance(other, Student):
            return False
        return (self.f_name == other.f_name and
                self.l_name == other.l_name and
                self.student_id == other.student_id and
                self.email == other.email)


class Assignment:
    __slots__ = ('assign_id', 'assign_name')

    def __init__(self, assign_id, assign_name):
        # type: (int, typing.Text) -> None
        self.assign_id = assign_id
        self.assign_name = assign_name

    def __repr__(self):
        # type: () -> str
        return '{name}[{ID}]'.format(
            name=self.assign_name,
            ID=self.assign_id)

    def __eq__(self, other):
        # type: (typing.Any) -> bool
        if not isinstance(other, Assignment):
            return False
        return (self.assign_name == other.assign_name and
                self.assign_id == other.assign_id)


class Grade:
    __slots__ = ('student', 'assignment', 'grade', 'notes')

    def __init__(self, student, assignment, grade, notes):
        # type: (Student, Assignment, float, typing.Text) -> None
        self.student = student
        self.assignment = assignment
        self.grade = grade
        self.notes = notes

    def __repr__(self):
        # type: () -> str
        return '({st}) ({a}): {grade} - {notes}'.format(
            st=repr(self.student),
            a=repr(self.assignment),
            grade=self.grade,
            notes=self.notes)

    def __eq__(self, other):
        # type: (typing.Any) -> bool
        if not isinstance(other, Grade):
            return False
        return (self.student == other.student and
                self.assignment == other.assignment and
                self.grade == other.grade and
                self.notes == other.notes)


class Gradebook:
    def __init__(self, dbase=':memory:'):
        # type: (typing.Text) -> None
        self.conn = None
        self.conn = sqlite3.connect(dbase)
        cur = self.conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS
            Students(student_id INTEGER PRIMARY KEY,
            f_name TEXT, l_name TEXT, email TEXT)""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS
            Assignments(assign_id INTEGER PRIMARY KEY ASC,
            name TEXT)""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS
            Grades(assign_id INTEGER,
            student_id INTEGER,
            grade REAL,
            notes TEXT,
            PRIMARY KEY (assign_id, student_id))""")
        self.conn.commit()
        cur.close()

    def close(self):
        self.conn.close()

    def add_student(self, student):
        # type: (Student) -> None
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO Students VALUES (?, ?, ?, ?)',
            (student.student_id,
             student.f_name,
             student.l_name,
             student.email))
        self.conn.commit()
        cur.close()

    def add_students(self, students):
        # type: (List[Student]) -> None
        cur = self.conn.cursor()
        stList = [
            (student.student_id,
             student.f_name,
             student.l_name,
             student.email)
            for student in students]
        cur.executemany(
            'INSERT INTO Students VALUES ' +
            '(:student_id, :f_name, :l_name, :email)',
            stList)
        self.conn.commit()
        cur.close()

    def get_students(self):
        # type: () -> List[Student]
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM Students')
        stList = [
            Student(e[0], e[1], e[2], e[3])
            for e in cur.fetchall()
        ]
        cur.close()
        return stList

    def get_student_by_id(self, student_id):
        # type: (int) -> Student
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM Students WHERE student_id=?', (student_id,))
        e = cur.fetchone()
        cur.close()
        return Student(e[0], e[1], e[2], e[3])

    def delete_student(self, student_id):
        # type: (int) -> None
        cur = self.conn.cursor()
        cur.execute('DELETE FROM Students WHERE student_id=?', (student_id,))
        self.conn.commit()
        cur.close()

    def add_assignment(self, assignment):
        # type: (Assignment) -> None
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO Assignments VALUES (?, ?)',
            (assignment.assign_id,
             assignment.assign_name))
        self.conn.commit()
        cur.close()

    def add_assignments(self, assignments):
        # type: (List[Assignment]) -> None
        cur = self.conn.cursor()
        aList = [
            (assignment.assign_id,
             assignment.assign_name)
            for assignment in assignments]
        cur.executemany(
            'INSERT INTO Assignments VALUES (?, ?)',
            aList)
        self.conn.commit()
        cur.close()

    def get_assignments(self):
        # type: () -> List[Assignment]
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM Assignments')
        stList = [
            Assignment(e[0], e[1])
            for e in cur.fetchall()
        ]
        cur.close()
        return stList

    def get_assignment_by_id(self, assign_id):
        # type: (int) -> Assignment
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM Assignments WHERE assign_id=?',
                    (assign_id,))
        e = cur.fetchone()
        cur.close()
        return Assignment(e[0], e[1])

    def delete_assignment(self, assign_id):
        # type: (int) -> Assignment
        cur = self.conn.cursor()
        cur.execute('DELETE FROM Assignments WHERE assign_id=?',
                    (assign_id,))
        self.conn.commit()
        cur.close()

    def add_grade(self, grade):
        # type: (Grade) -> None
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO Grades VALUES (?, ?, ?, ?)',
            (grade.assignment.assign_id,
             grade.student.student_id,
             grade.grade,
             grade.notes))
        self.conn.commit()
        cur.close()

    def add_grades(self, gradeList):
        # type: (List[Grade]) -> None
        cur = self.conn.cursor()
        gList = [
            (grade.assignment.assign_id,
             grade.student.student_id,
             grade.grade,
             grade.notes)
            for grade in gradeList]
        cur.executemany(
            'INSERT INTO Grades VALUES (?, ?, ?, ?)',
            gList)
        self.conn.commit()
        cur.close()

    def get_grades(self):
        # type: () -> List[Grade]
        cur = self.conn.cursor()
        cur.execute('SELECT s.student_id, FROM Grades g '
                    'JOIN Students s ON g.student_id = s.student_id '
                    'JOIN Assignments a ON a.assign_id = a.assign_id')
        stList = [
            Grade(Student(e[0], e[1], e[2], e[3]),
                  Assignment(e[4], e[5]),
                  e[6], e[7])
            for e in cur.fetchall()
        ]
        cur.close()
        return stList

    def get_grade_by_id(self, assign_id, student_id):
        # type: (int, int) -> Grade
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM Grades WHERE'
                    'assign_id=? AND student_id=?',
                    (assign_id, student_id))
        e = cur.fetchone()
        cur.close()
        return Grade(e[0], e[1], e[2], e[3])

    def delete_grade(self, assign_id, student_id):
        # type: (int, int) -> None
        cur = self.conn.cursor()
        cur.execute('DELETE FROM Grades WHERE'
                    'assign_id=? AND student_id=?',
                    (assign_id, student_id))
        self.conn.commit()
        cur.close()
