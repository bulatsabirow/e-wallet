import datetime
from operator import attrgetter
from pathlib import Path
from typing import Optional

import arrow
from attr import define, AttrsInstance, field, Factory
from faker import Faker

from services.data import FileManager
from services.enums import Category
from services.schema import FinancialOperation

fake = Faker()


# TODO replace
def generate_date_between() -> tuple[str, str]:
    # randomly create date range within given date boundaries
    start = fake.date()
    return (start, str(fake.date_between_dates(date_start=arrow.get(start).date())))


@define
class TestFinancialOperationFilterKwargs:
    __test__ = False
    summ: str = field(default=Factory(lambda: str(fake.random_int(0, 100000))))
    category: Category = field(
        default=Factory(
            lambda: fake.random_element([category.value for category in Category])
        )
    )
    description: str = field(default=Factory(lambda: fake.text(max_nb_chars=1000)))
    date: tuple[str, str] = field(default=Factory(generate_date_between))


@define
class TestFinancialOperation(FinancialOperation):
    __test__ = False
    summ: str = field(default=Factory(lambda: str(fake.random_int(0, 100000))))
    category: Category = field(
        default=Factory(
            lambda: fake.random_element([category.value for category in Category])
        )
    )
    description: str = field(default=Factory(lambda: fake.text(max_nb_chars=1000)))
    date: str = field(default=Factory(fake.date))
    id: str = field(default=Factory(fake.uuid4))


class TestFileManager(FileManager):
    __test__ = False
    schema = TestFinancialOperation
    path: Path = Path(__file__).parent.parent / "data" / "test_data.csv"
