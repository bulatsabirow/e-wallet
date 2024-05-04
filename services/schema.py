import datetime
from dataclasses import dataclass, field

from services.enums import Category


@dataclass
class FinancialOperation:
    summ: int
    category: Category
    description: str
    date: datetime.date = field(init=True, default_factory=datetime.date.today)

    def __post_init__(self):
        if self.summ < 0:
            raise ValueError("Operation sum must be greater than zero")
