import datetime
from operator import attrgetter
from pathlib import Path

from attr import define, AttrsInstance, field, Factory
from faker import Faker

from services.data import FileManager
from services.enums import Category
from services.schema import FinancialOperation

fake = Faker()


@define
class TestFinancialOperation(FinancialOperation):
    __test__ = False
    summ: str = field(default=Factory(lambda: str(fake.random_int(0, 100000))))
    category: Category = field(
        default=Factory(
            lambda: fake.random_element([category.value for category in Category])
        )
    )
    description: str = field(default=fake.text(max_nb_chars=1000))
    date: datetime.date = field(default=Factory(lambda: fake.date()))
    id: str = field(default=fake.uuid4())


class TestFileManager(FileManager):
    __test__ = False
    schema = TestFinancialOperation
    path: Path = Path(__file__).parent.parent / "data" / "test_data.csv"
