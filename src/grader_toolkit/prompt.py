import prompt_toolkit
import sqlalchemy  # noqa: F401
import grader_toolkit
from prompt_toolkit.document import Document  # noqa: F401
from prompt_toolkit.completion import CompleteEvent, Completion  # noqa: F401
try:
    import typing  # noqa: F401
except:
    pass


class GraderCompleter(prompt_toolkit.completion.Completer):
    def __init__(self, dbase_session):
        # type: (sqlalchemy.Session) -> None
        pass

    def get_completions(self, document, complete_event):
        # type: (Document, CompleteEvent) -> typing.Iterator[Completion]
        yield Completion()
