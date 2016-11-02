import click
import click_repl
import grader_toolkit
import yaml
from grader_toolkit import Student, Assignment, Grade
import grader_toolkit.encoder
import sqlalchemy


@click.group()
def cli_main():
    # type: () -> None
    """Utilites useful for entering, tracking, and analysing grades for local
    reference."""
    pass


@cli_main.group(name='gradebook')
@click.option('--dbase', default='sqlite:///./grades.db')
@click.pass_context
def cli_gradebook(ctx, dbase):
    """Access to gradebook utilities"""
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
            click.echo('Done entering students? [yn]', nl=False)
            c = click.getchar()
            click.echo()
            if c == 'y':
                break
            s = Student(
                **get_entries(
                    [('id', 'Student ID:', int),
                     ('name', 'Name:', str),
                     ('email', 'Email:', str)]))
            session.add(s)
        session.commit()
    except:
        session.rollback()
        raise


@cli_gb_add.command(name='assignments')
@click.pass_obj
def cli_gb_add_assignments(session, student_id, name, email):
    """Add assignments to gradebook"""
    try:
        while True:
            click.echo('Done entering assignments? [yn]', nl=False)
            c = click.getchar()
            click.echo()
            if c == 'y':
                break
            a = Assignment(
                **get_entries(
                    [('name', 'Name:', str),
                     ('full_credit', 'Full Credit:', float)]))
            session.add(a)
        session.commit()
    except:
        session.rollback()
        raise


@cli_gradebook.command(name='export')
@click.option('--out', type=click.File(mode='w'))
@click.pass_obj
def cli_gb_export(session, out):
    """Export gradebook"""
    try:
        data = {}
        data['students'] = session.query(Student).all()
        data['assignments'] = session.query(Assignment).all()
        data['grades'] = session.query(Grade).all()
        yaml.dump(data, stream=out)
    except:
        raise


@cli_gradebook.command(name='import')
@click.argument('infile', type=click.File(mode='r'))
@click.pass_obj
def cli_gb_import(session, infile):
    """Import gradebook"""
    try:
        out = yaml.load(infile)
        session.add_all(out['students'])
        session.add_all(out['assignments'])
        session.add_all(out['grades'])
        session.flush()
        session.commit()
    except:
        session.rollback()
        raise


@cli_gradebook.group(name='analyze')
def cli_gb_analyze():
    """Analysis tools"""
    pass


@cli_gb_analyze.command(name='students')
@click.option('--out', type=click.File(mode='w'), default='-')
@click.argument('name')
@click.pass_obj
def cli_gb_analyze_students(session, name, out):
    """Analyze student grades

    NAME"""
    try:
        stList = session.query(Student).filter(Student.name.like(name)).all()
        for st in stList:
            grader_toolkit.analyze.analyze_student(st, stream=out)
    except:
        pass


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
            out.write(repr(st))
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
