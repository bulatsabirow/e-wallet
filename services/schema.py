import datetime
from uuid import uuid4, UUID

from attr import define, field, Factory, fields, AttrsInstance

from services.converters import date_converter
from services.enums import Category


@define
class FinancialOperation(AttrsInstance):
    summ: int = field(converter=int)
    category: Category
    description: str
    date: datetime.date = field(
        default=Factory(datetime.date.today), converter=date_converter
    )
    id: UUID = field(default=Factory(uuid4))

    @summ.validator
    def check(self, attribute, value):
        if value < 0:
            raise ValueError("Operation sum must be greater than zero")

    def __str__(self):
        return "\n".join(
            "%(field)s: %(value)s" % {"field": f.name, "value": getattr(self, f.name)}
            for f in fields(self.__class__)
        )

    @classmethod
    def fieldnames(cls):
        return [f.name for f in fields(cls)]
