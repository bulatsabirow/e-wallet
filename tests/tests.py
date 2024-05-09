import itertools
import sys
from collections.abc import Iterable
from io import StringIO
from unittest import mock

import pytest
from faker import Faker

from services.enums import Category
from tests.schema import TestFinancialOperation

fake = Faker()


class BaseTestRecord:
    def get_options(self, financial_operation):
        raw_mapping = {
            "-s": financial_operation.summ,
            "-d": financial_operation.description,
            "-c": financial_operation.category,
            "--date": financial_operation.date,
        }
        return (
            (
                key,
                *(
                    val
                    if isinstance(val, Iterable) and not isinstance(val, str)
                    else [val]
                ),
            )
            for key, val in raw_mapping.items()
            if val is not None
        )

    def base_command(
        self,
        command_name: str,
        command_test_manager,
        financial_operation,
        positional_args: Iterable = None,
    ):
        command_test_manager.execute(
            [
                command_name,
                *(positional_args or []),
                *itertools.chain.from_iterable(self.get_options(financial_operation)),
            ]
        )

    def add_record(self, command_test_manager, financial_operation):
        return self.base_command(
            "add_record", command_test_manager, financial_operation
        )

    def filter_record(self, command_test_manager, filter_kwargs):
        return self.base_command("filter_record", command_test_manager, filter_kwargs)

    def edit_record(
        self,
        command_test_manager,
        edited_financial_operation_data,
        financial_operation_id,
    ):
        return self.base_command(
            "edit_record",
            command_test_manager,
            edited_financial_operation_data,
            [financial_operation_id],
        )


class TestAddRecord(BaseTestRecord):
    def test_valid_parameters(
        self, command_test_manager, test_file_manager, financial_operation
    ):
        self.add_record(command_test_manager, financial_operation)
        actual_financial_operation = next(test_file_manager.read())
        # It's not allowed to define id field in financial operation creating command,
        # so id has to be removed in comparison procedure
        for field in financial_operation.fieldnames(exclude=["id"]):
            assert getattr(financial_operation, field) == getattr(
                actual_financial_operation, field
            )

    def test_invalid_summ_parameter(self, command_test_manager, financial_operation):
        with pytest.raises(SystemExit) as exc:
            financial_operation.summ = fake.word()
            self.add_record(command_test_manager, financial_operation)

        assert exc.value.code == 2


class TestEditRecord(BaseTestRecord):
    def test_valid_parameters(
        self,
        command_test_manager,
        test_file_manager,
        edited_financial_operation_data,
        financial_operation,
    ):
        self.add_record(command_test_manager, financial_operation)
        created_financial_operation = next(test_file_manager.read())

        self.edit_record(
            command_test_manager,
            edited_financial_operation_data,
            created_financial_operation.id,
        )
        edited_financial_operation = next(test_file_manager.read())

        for key, val in edited_financial_operation_data.items():
            if val is not None:
                assert val == getattr(edited_financial_operation, key)


class TestFilterRecord(BaseTestRecord):
    def test_valid_parameters(
        self,
        command_test_manager,
        financial_operation,
        financial_operation_filter_kwargs,
        test_file_manager,
    ):
        for _ in range(fake.random_int(100, 1000)):
            self.add_record(command_test_manager, TestFinancialOperation())

        self.filter_record(command_test_manager, financial_operation_filter_kwargs)


class TestShowBalance(BaseTestRecord):
    def test_valid_parameters(self, command_test_manager, test_file_manager, capsys):
        expected_result = 0
        for _ in range(fake.random_int(100, 1000)):
            instance = TestFinancialOperation()
            expected_result += int(instance.summ) * (
                1 if Category.income.value == instance.category else -1
            )

            self.add_record(command_test_manager, instance)

        # intersect console output to check if expected and actual results
        with mock.patch("sys.stdout", new_callable=StringIO):
            command_test_manager.execute(["show_balance"])
            actual_result = int(sys.stdout.getvalue())

            assert abs(expected_result) == actual_result

    def test_incompatible_parameters(self, command_test_manager, test_file_manager):
        with pytest.raises(SystemExit) as exc:
            command_test_manager.execute(
                ["show_balance", "--only-incomes", "--only-expenses"]
            )

        assert exc.value.code == 2
