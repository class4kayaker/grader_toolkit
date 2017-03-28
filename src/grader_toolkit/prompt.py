import click
import prompt_toolkit
from prompt_toolkit.contrib.completers import WordCompleter
# Typing imports
import sqlalchemy  # noqa: F401
from prompt_toolkit.document import Document  # noqa: F401
from prompt_toolkit.completion import CompleteEvent, Completion  # noqa: F401
try:
    import typing  # noqa: F401
    T = typing.TypeVar('T')
except:
    pass


def short_edit_prompt(
        prompt,  # type: typing.Text
        default=u'',  # type: typing.Optional[typing.Text]
        convert=str,
        allow_none=True):
    # type: (...) -> T
    result = prompt_toolkit.prompt(prompt, default=default)
    if allow_none and result == '':
        return None
    else:
        try:
            return convert(result)
        except ValueError:
            return None


def long_edit(i_text):
    # type: (typing.Optional[typing.Text]) -> typing.Optional[typing.Text]
    text = click.edit(text=i_text)
    if text is not None:
        return text
    return i_text


def column_prompt(prompt,  # type: typing.Text
                  session,  # type: sqlalchemy.Session
                  column=None,  # type: typing.Optional[sqlalchemy.Column]
                  convert=str):
    # type: (...) -> typing.Any
    if column:
        c = WordCompleter([r for r, in session.query(column).all()],
                          match_middle=True)
    else:
        c = None
    return convert(prompt_toolkit.prompt(prompt,
                                         completer=c))
