import datetime

from attr import define, field, Factory, fields

from services.enums import Category


@define
class FinancialOperation:
    summ: int = field(converter=int)
    category: Category
    description: str
    date: datetime.date = Factory(datetime.date.today)

    @summ.validator
    def check(self, attribute, value):
        if value < 0:
            raise ValueError("Operation sum must be greater than zero")

    def __str__(self):
        return "\n".join(
            "%s: %s" % (field.name, getattr(self, field.name))
            for field in fields(self.__class__)
        )
