import datetime
from pathlib import Path

from attr import define, AttrsInstance, field, Factory
from faker import Faker

from services.data import FileManager
from services.enums import Category
from services.schema import FinancialOperation

fake = Faker()


class TestFileManager(FileManager):
    __test__ = False
    path: Path = Path(__file__).parent.parent / "data" / "test_data.csv"


@define
class TestFinancialOperation(FinancialOperation):
    __test__ = False
    summ: str = field(default=Factory(lambda: str(fake.random_int(0, 100000))))
    category: Category = field(default=Factory(lambda: fake.random_element(Category)))
    description: str = field(default=fake.text(max_nb_chars=1000))
    date: datetime.date = field(default=Factory(lambda: fake.date()))
