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


def edit_prompt(prompt,  # type: typing.Text
                default=u'',  # type: typing.Text
                convert=str,
                allow_none=True):
    # type: (...) -> T
    result = prompt_toolkit.prompt(prompt, default=default)
    if allow_none and result == '':
        return None
    else:
        return convert(result)


def column_prompt(prompt,  # type: typing.Text
                  session,  # type: sqlalchemy.Session
                  column=None,  # type: typing.Optional[sqlalchemy.Column]
                  convert=str):
    # type: (...) -> typing.Any
    c = WordCompleter([r for r, in session.query(column).all()])\
        if column else None
    return convert(prompt_toolkit.prompt(prompt,
                                         completer=c))
