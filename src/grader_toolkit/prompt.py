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
        return convert(result)


def long_edit(i_text):
    # type: (typing.Optional[typing.Text]) -> typing.Optional[typing.Text]
    text = click.edit(text=i_text)
    if text is not None:
        lines = [
            (l.strip() if l else '\n\n')
            for l in text.split('\n')
        ]
        text = lines[0]
        for l in lines[1:]:
            if not l == '\n\n':
                text = text.strip() + ' '
            text += l
        return text
    return i_text


def column_prompt(prompt,  # type: typing.Text
                  session,  # type: sqlalchemy.Session
                  column=None,  # type: typing.Optional[sqlalchemy.Column]
                  convert=str):
    # type: (...) -> typing.Any
    c = WordCompleter([r for r, in session.query(column).all()])\
        if column else None
    return convert(prompt_toolkit.prompt(prompt,
                                         completer=c))
