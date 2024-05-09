from collections.abc import Generator
from typing import Any

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
def financial_operation() -> TestFinancialOperation:
    return TestFinancialOperation()


@pytest.fixture
def financial_operation_filter_kwargs() -> TestFinancialOperationFilterKwargs:
    return TestFinancialOperationFilterKwargs()


@pytest.fixture
def edited_financial_operation_data(
    financial_operation: TestFinancialOperation,
) -> AttrDict[str, Any]:
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
def test_file_manager() -> TestFileManager:
    return TestFileManager()


@pytest.fixture
def command_test_manager() -> CommandTestManager:
    return CommandTestManager()


@pytest.fixture(scope="function", autouse=True)
def delete_test_csv_file() -> Generator[None, None, None]:
    yield

    # delete testing .csv file after every test
    try:
        TestFileManager.path.unlink()
    except FileNotFoundError:
        pass
