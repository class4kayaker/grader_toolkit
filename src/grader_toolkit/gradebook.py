import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):  # type: ignore
    __tablename__ = 'student'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)

    def __repr__(self):
        return ('<Student(id={0.id!r},'
                ' name={0.name!r},'
                ' email={0.email!r})>').format(
            self)


class Assignment(Base):  # type: ignore
    __tablename__ = 'assignment'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)
    full_credit = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    def __repr__(self):
        return ('<Assignment(id={0.id!r},'
                ' name={0.name!r},'
                ' full_credit={0.full_credit!r})>')\
            .format(self)


class Grade(Base):  # type: ignore
    __tablename__ = 'grade'
    student_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('student.id'),
                                   primary_key=True)
    student = sqlalchemy.orm.relationship('Student',
                                          back_populates='grades')
    assignment_id = sqlalchemy.Column(sqlalchemy.Integer,
                                      sqlalchemy.ForeignKey('assignment.id'),
                                      primary_key=True)
    assignment = sqlalchemy.orm.relationship('Assignment',
                                             back_populates='grades')
    grade = sqlalchemy.Column(sqlalchemy.Float)
    notes = sqlalchemy.Column(sqlalchemy.String(500))

    def __repr__(self):
        return ('<Grade(student_id={0.student_id!r},'
                ' assignment_id={0.assignment_id!r},'
                ' grade={0.grade!r}),'
                ' notes={0.notes!r}>')\
            .format(self)

Student.grades = sqlalchemy.orm.relationship('Grade',
                                             order_by=Grade.assignment_id,
                                             back_populates='student')
Assignment.grades = sqlalchemy.orm.relationship('Grade',
                                                order_by=Grade.student_id,
                                                back_populates='assignment')


Session = sqlalchemy.orm.sessionmaker()
