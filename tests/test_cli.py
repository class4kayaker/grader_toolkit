import pytest
import grader_toolkit.cli
from click.testing import CliRunner
try:
    import typing  # noqa: F401
except:
    pass  # Only currently using typing for annotations, no action necessary


@pytest.mark.parametrize('text, out', [
    ('', ''),
    ('5 6 4', '[ 3] 15\n'),
    ('5 6 4\n3 4 7 8', '[ 3] 15\n[ 4] 22\n'),
    ('5 e6 4\n3 4 7 8', 'Error\n[ 4] 22\n'),
    ('\n5 e6 4\n3 4 7 8', ''),
])
def test_totaling(text, out):
    # type: (typing.Text, typing.Text) -> None
    runner = CliRunner()
    result = runner.invoke(grader_toolkit.cli.cli_main,
                           ['util', 'totaling'],
                           input=text)
    assert result.exit_code == 0
    assert result.output == out
