import datetime
from argparse import Namespace
from collections.abc import Iterable, Collection
from typing import Self
from uuid import uuid4, UUID

import arrow.arrow
from attr import define, field, Factory, fields, AttrsInstance

from services.enums import Category
from services.errors import ValidationErrorMessages


@define
class FinancialOperation(AttrsInstance):
    summ: int = field(converter=int)
    category: Category
    description: str
    date: datetime.date = field(default=Factory(arrow.now().date))
    id: UUID = field(default=Factory(uuid4))

    @summ.validator
    def check(self, attribute, value):
        if value < 0:
            raise ValueError(ValidationErrorMessages.INTEGER_LESS_THAN_ZERO)

    def __str__(self):
        return "\n".join(
            "%(field)s: %(value)s" % {"field": f.name, "value": getattr(self, f.name)}
            for f in fields(self.__class__)
        )

    @classmethod
    def fieldnames(cls, exclude: Iterable[str] = tuple()) -> Collection[str]:
        return [f.name for f in fields(cls) if f.name not in exclude]

    @classmethod
    def from_args(cls, args: Namespace) -> Self:
        return cls(
            **{
                field: vars(args).get(field)
                for field in FinancialOperation.fieldnames(exclude=("id",))
            }
        )
