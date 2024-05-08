import pytest

from tests.commands import CommandTestManager
from tests.schema import TestFinancialOperation, TestFileManager


@pytest.fixture
def financial_operation():
    return TestFinancialOperation()


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
