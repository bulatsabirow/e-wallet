import pytest
from attr import asdict
from faker import Faker

from tests.commands import CommandTestManager
from tests.schema import (
    TestFinancialOperation,
    TestFileManager,
    TestFinancialOperationFilterKwargs,
)
from utils import AttrDict

fake = Faker()


@pytest.fixture
def financial_operation():
    return TestFinancialOperation()


@pytest.fixture
def financial_operation_filter_kwargs():
    return TestFinancialOperationFilterKwargs()


@pytest.fixture
def edited_financial_operation_data(financial_operation):
    return AttrDict(
        {
            key: None
            if fake.random_int(0, 9) < 5
            else getattr(TestFinancialOperation(), key)
            for key in asdict(financial_operation)
            if key in financial_operation.fieldnames(exclude=["id"])
        }
    )


@pytest.fixture
def test_file_manager():
    return TestFileManager()


@pytest.fixture
def command_test_manager():
    return CommandTestManager()


@pytest.fixture(scope="function", autouse=True)
def delete_test_csv_file():
    yield

    try:
        TestFileManager.path.unlink()
    except FileNotFoundError:
        pass
