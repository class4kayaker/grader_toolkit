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
        return '<Student(id={}, name={}, email={})>'.format(
            self.id,
            self.name,
            self.email)


class Assignment(Base):  # type: ignore
    __tablename__ = 'assignment'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)
    full_credit = sqlalchemy.Column(sqlalchemy.Float, nullable=False)


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

Student.grades = sqlalchemy.orm.relationship('Grade',
                                             order_by=Grade.assignment_id,
                                             back_populates='student')
Assignment.grades = sqlalchemy.orm.relationship('Grade',
                                                order_by=Grade.student_id,
                                                back_populates='assignment')


Session = sqlalchemy.orm.sessionmaker()
