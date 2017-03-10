import click
import click_repl
import grader_toolkit
import grader_toolkit.interface
from grader_toolkit import Student, Assignment, Grade
import grader_toolkit.encoder
import grader_toolkit.prompt
import sqlalchemy


@click.group()
def cli_main():
    # type: () -> None
    """Utilites useful for entering, tracking, and analysing grades for local
    reference."""
    pass


@cli_main.group(name='gradebook')
@click.option('--dbase', default='sqlite://')
@click.pass_context
def cli_gradebook(ctx, dbase):
    """Access to gradebook utilities"""
    if ctx.obj is None:
        engine = sqlalchemy.create_engine(dbase)
        grader_toolkit.gradebook.Base.metadata.create_all(engine)
        grader_toolkit.Session.configure(bind=engine)
        ctx.obj = grader_toolkit.Session()


click_repl.register_repl(cli_gradebook)


@cli_gradebook.group(name='add')
def cli_gb_add():
    """Add objects to gradebook"""
    pass


def get_entries(kws):
    ret = {}
    for kw, prompt, t in kws:
        ret[kw] = click.prompt(prompt, type=t)
    return ret


@cli_gb_add.command(name='students')
@click.pass_obj
def cli_gb_add_students(session):
    """Add students to gradebook"""
    try:
        while True:
            s = Student(
                **get_entries(
                    [('id', 'Student ID:', int),
                     ('name', 'Name:', str),
                     ('email', 'Email:', str)]))
            session.add(s)
            session.commit()
            click.echo('Done entering students? [yn]', nl=False)
            c = click.getchar()
            click.echo()
            if c == 'y':
                break
    except:
        session.rollback()
        raise


@cli_gb_add.command(name='assignments')
@click.pass_obj
def cli_gb_add_assignments(session):
    """Add assignments to gradebook"""
    try:
        while True:
            a = Assignment(
                **get_entries(
                    [('name', 'Name:', str),
                     ('full_credit', 'Full Credit:', float)]))
            session.add(a)
            session.commit()
            click.echo('Done entering assignments? [yn]', nl=False)
            c = click.getchar()
            click.echo()
            if c == 'y':
                break
    except:
        session.rollback()
        raise


@cli_gradebook.group(name='edit')
def cli_gb_edit():
    pass


@cli_gb_edit.command(name='grades')
@click.option('--grade/--no-grade', default=True,
              help='Edit grades')
@click.option('--notes/--no-notes', default=True,
              help='Edit notes')
@click.pass_obj
def cli_gb_edit_grades(session, grade, notes):
    """Edit grades"""
    try:
        while True:
            sname = grader_toolkit.prompt.column_prompt(
                'Student name: ',
                session,
                column=Student.name)
            if not sname:
                break
            s = session.query(Student).filter(Student.name == sname).one()
            aname = grader_toolkit.prompt.column_prompt(
                'Assignment name: ',
                session,
                column=Assignment.name)
            a = session.query(Assignment)\
                .filter(Assignment.name == aname).one()
            try:
                g = session.query(Grade).filter(
                    sqlalchemy.and_(
                        Grade.student_id == s.id,
                        Grade.assignment_id == a.id)).one()
            except sqlalchemy.orm.exc.NoResultFound:
                g = Grade(
                    student_id=s.id,
                    assignment_id=a.id)
                session.add(g)
                session.commit()
            if notes:
                g.notes = grader_toolkit.prompt.long_edit(
                    g.notes)
            if grade:
                g_in = str(g.grade) if (g.grade is not None) else ''
                g.grade = grader_toolkit.prompt.short_edit_prompt(
                    'Grade: ',
                    default=g_in,
                    convert=float)
            session.commit()
    except:
        session.rollback()
        raise


@cli_gradebook.group(name='view')
def cli_gb_view():
    pass


@cli_gb_view.command(name='grades')
@click.pass_obj
def cli_gb_view_grades(session):
    """View grades"""
    while True:
        sname = grader_toolkit.prompt.column_prompt(
            'Student name:',
            session,
            column=Student.name)
        if not sname:
            break
        s = session.query(Student).filter(Student.name == sname).one()
        aname = grader_toolkit.prompt.column_prompt(
            'Assignment name:',
            session,
            column=Assignment.name)
        a = session.query(Assignment)\
            .filter(Assignment.name == aname).one()
        try:
            g = session.query(Grade).filter(
                sqlalchemy.and_(
                    Grade.student_id == s.id,
                    Grade.assignment_id == a.id)).one()
        except sqlalchemy.orm.exc.NoResultFound:
            g = Grade(
                student_id=s.id,
                assignment_id=a.id)
            session.add(g)
            session.commit()
        click.echo_via_pager(
            text='Grade: {0.grade}\nNotes:\n{0.notes}'.format(g))


@cli_gradebook.command(name='export')
@click.argument('out', type=click.File(mode='w'))
@click.pass_obj
def cli_gb_export(session, out):
    """Export gradebook"""
    grader_toolkit.encoder.yaml_dump_session(session, out)


@cli_gradebook.group(name='interface')
@click.pass_obj
def cli_gb_interface(session):
    pass


@cli_gb_interface.command(name='upload')
@click.argument('aname')
@click.option('--out', type=click.Path())
@click.option('--fmt',
              type=click.Choice(grader_toolkit.interface.upload_formats.keys())
              )
@click.option('--gtemplate', type=click.File(mode='r'))
@click.pass_obj
def cli_gb_interface_upload(session, aname, out, fmt, gtemplate):
    """Generate """
    try:
        a = (session.query(Assignment)
             .filter(Assignment.name == aname).one())
        grader_toolkit.interface.upload_formats[fmt](a, gtemplate, out)
    except sqlalchemy.orm.exc.NoResultFound:
        print('Assignment "{}" not found'.format(aname))
    except sqlalchemy.orm.exc.MultipleResultsFound:
        print('Unique record for "{}" not found'.format(aname))


@cli_gradebook.command(name='import')
@click.argument('infile', type=click.File(mode='r'))
@click.pass_obj
def cli_gb_import(session, infile):
    """Import gradebook"""
    grader_toolkit.encoder.yaml_load_session(session, infile)


@cli_gradebook.group(name='analyze')
def cli_gb_analyze():
    """Analysis tools"""
    pass


@cli_gb_analyze.command(name='students')
@click.option('--out', type=click.File(mode='w'), default='-')
@click.option('--short/--no-short', default=False)
@click.pass_obj
def cli_gb_analyze_students(session, out, short):
    """Analyze student grades

    NAME"""
    while True:
        sname = grader_toolkit.prompt.column_prompt(
            'Student name:',
            session,
            column=Student.name)
        if sname == '':
            break
        try:
            s = session.query(Student).filter(Student.name == sname).one()
            grader_toolkit.analyze_student(s, out, short)
        except sqlalchemy.orm.exc.NoResultFound:
            print('Student "{}" not found'.format(sname))
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Unique record for "{}" not found'.format(sname))


@cli_gb_analyze.command(name='assignments')
@click.option('--out', type=click.File(mode='w'), default='-')
@click.option('--short/--no-short', default=False)
@click.pass_obj
def cli_gb_analyze_assignments(session, out, short):
    """Analyze assignment results

    NAME"""
    while True:
        aname = grader_toolkit.prompt.column_prompt(
            'Assignment name:',
            session,
            column=Assignment.name)
        if aname == '':
            break
        try:
            a = (session.query(Assignment)
                 .filter(Assignment.name == aname).one())
            grader_toolkit.analyze_assignment(a, out, short)
        except sqlalchemy.orm.exc.NoResultFound:
            print('Assignment "{}" not found'.format(aname))
        except sqlalchemy.orm.exc.MultipleResultsFound:
            print('Unique record for "{}" not found'.format(aname))


@cli_gradebook.group(name='list')
def cli_gb_list():
    """Listing tools"""
    pass


@cli_gb_list.command(name='students')
@click.option('--out', type=click.File(mode='w'), default='-')
@click.pass_obj
def cli_gb_list_students(session, out):
    """List students"""
    try:
        stList = session.query(Student).all()
        for st in stList:
            out.write('{0.name}[{0.id}]: {0.email}\n'.format(st))
    except:
        pass


@cli_gb_list.command(name='assignments')
@click.option('--out', type=click.File(mode='w'), default='-')
@click.pass_obj
def cli_gb_list_assignments(session, out):
    """List assignments"""
    try:
        stList = session.query(Student).all()
        for st in stList:
            out.write(repr(st))
    except:
        pass


@cli_gb_list.command(name='grades')
@click.option('--out', type=click.File(mode='w'), default='-')
@click.pass_obj
def cli_gb_list_grades(session, out):
    """List assignments"""
    try:
        gList = session.query(Grade).all()
        for g in gList:
            out.write(
                '''Student: {0.student.name}
Assignment: {0.assignment.name}
Grade: {0.grade}
Notes:
{0.notes}\n\n'''.format(g))
    except:
        pass


@cli_main.group(name='util')
def cli_util():
    # type: () -> None
    """General cli utilities that are not directly tied to recording
    anything"""
    pass


@cli_util.command()
def totaling():
    # type: () -> None
    """Sum lines of entered integers and display count and total for totalling
    grades"""
    for line in click.get_text_stream('stdin'):
        line = line.strip()
        if not line:
            break
        try:
            arr = [int(v) for v in line.split()]
            count = len(arr)
            total = sum(arr)
            click.echo('[{:2d}] {:d}'.format(count, total))
        except:
            click.secho('Error', fg='red')
