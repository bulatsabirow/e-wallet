import enum


class Category(enum.Enum):
    income = "income"
    expense = "expense"

    @classmethod
    def _missing_(cls, value):
        # case insensitive enum behavior
        return cls(value.lower())
