from future import raise_from
import prompt_toolkit
import sqlalchemy  # noqa: F401
from prompt_toolkit.document import Document  # noqa: F401
from prompt_toolkit.completion import CompleteEvent, Completion  # noqa: F401
try:
    import typing  # noqa: F401
except:
    pass


def column_prompt(prompt,  # type: typing.Text
                  session,  # type: sqlalchemy.Session
                  column=None,  # type: typing.Optional[sqlalchemy.Column]
                  unique=False,  # type: bool
                  convert=str,
                  ccount=10):
    # type: (...) -> typing.Any
    c = ColumnCompleter(session, column, mxcount=10) if column else None
    v = ExistanceValidator(session, column, convert=convert)\
        if unique else None
    return convert(prompt_toolkit.prompt(prompt,
                                         completer=c,
                                         validator=v))


class ColumnCompleter(prompt_toolkit.completion.Completer):
    def __init__(self, session, entity, mxcount=10):
        # type: (sqlalchemy.Session, sqlalchemy.Column, int) -> None
        self.session = session
        self.entity = entity
        self.mxcount = mxcount

    def get_completions(self, document, complete_event):
        # type: (Document, CompleteEvent) -> typing.Iterator[Completion]
        cQ = self.session.query(self.entity)\
            .filter(sqlalchemy.cast(self.entity, sqlalchemy.String)
                    .like(document.text))
        if cQ.count() <= self.mxcount:
            for e in cQ.all():
                yield Completion(str(e))


class ExistanceValidator(prompt_toolkit.validation.Validator):
    def __init__(self,
                 session,  # type: sqlalchemy.Session
                 entity,  # type: sqlalchemy.Column
                 convert=str
                 ):
        # type: (...) -> None
        self.session = session
        self.entity = entity
        self.convert = convert

    def validate(self, document):
        # type: (Document) -> None
        try:
            value = self.convert(document.text)
        except Exception as e:
            raise_from(
                prompt_toolkit.validation.ValidationError(
                    message='Invalid text'),
                e)
        cQ = self.session.query(self.entity)\
            .filter(self.entity == value)
        count = cQ.count()
        if not count == 1:
            raise prompt_toolkit.validation.ValidationError(
                message='Item does not exist or is not unique')
