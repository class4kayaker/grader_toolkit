import click


@click.group()
def cli_main():
    # type: () -> None
    """Utilites useful for entering, tracking, and analysing grades for local
    reference."""
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
            click.echo('Error', color='red')
