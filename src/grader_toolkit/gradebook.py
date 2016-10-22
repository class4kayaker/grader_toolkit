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

    def __str__(self):
        # type: () -> typing.Text
        return '{f_name} {l_name}({ID}): {email}'.format_map(self.__dict__)

    def __getitem__(self, name):
        # type: (typing.Text) -> typing.Any
        return self.__dict__[name]


class Assignment:
    __slots__ = ('assign_id', 'name')

    def __init__(self, assign_id, name):
        # type: (int, typing.Text) -> None
        self.assign_id = assign_id
        self.name = name

    def __str__(self):
        # type: () -> typing.Text
        return '{name}[{ID}]'.format_map(self.__dict__)

    def __getitem__(self, name):
        # type: (typing.Text) -> typing.Any
        return self.__dict__[name]


class Gradebook:
    def __init__(self, dbase=':memory:'):
        # type: (typing.Text) -> None
        self.conn = None
        try:
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
                Grades(assign_id INT PRIMARY KEY,
                name TEXT)""")
            self.conn.commit()
            cur.close()
        finally:
            if self.conn:
                self.conn.close()

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

    def add_assignment(self, assignment):
        # type: (Assignment) -> None
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO Assignments VALUES (?, ?)',
            (assignment.assign_id,
             assignment.name))
        self.conn.commit()
        cur.close()

    def add_assignments(self, assignments):
        # type: (List[Assignment]) -> None
        cur = self.conn.cursor()
        aList = [
            (assignment.assign_id,
             assignment.name)
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
