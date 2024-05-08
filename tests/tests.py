import itertools
from argparse import ArgumentError
from collections.abc import Iterable

import pytest
from attr import asdict
from faker import Faker
from tests.commands import CommandTestManager

fake = Faker()


class BaseTestRecord:
    def get_options_to_values_mapping(self, financial_operation):
        raw_mapping = {
            "-s": financial_operation.summ,
            "-d": financial_operation.description,
            "-c": financial_operation.category,
            "--date": financial_operation.date,
        }
        return ((key, val) for key, val in raw_mapping.items() if val is not None)

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
                *itertools.chain.from_iterable(
                    self.get_options_to_values_mapping(financial_operation)
                ),
            ]
        )

    def add_record(self, command_test_manager, financial_operation):
        return self.base_command(
            "add_record", command_test_manager, financial_operation
        )

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
        assert financial_operation == next(test_file_manager.read())

    def test_invalid_summ_parameter(self, command_test_manager, financial_operation):
        with pytest.raises((ArgumentError, SystemExit)) as exc:
            command_test_manager.execute(
                [
                    "add_record",
                    "-s",
                    fake.word(),
                    "-d",
                    financial_operation.description,
                    "-c",
                    financial_operation.category,
                    "--date",
                    financial_operation.date,
                ]
            )

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
        self.edit_record(
            command_test_manager,
            edited_financial_operation_data,
            financial_operation.id,
        )
        edited_financial_operation = next(test_file_manager.read())

        for key, val in edited_financial_operation_data.items():
            if val is not None:
                assert val == getattr(edited_financial_operation, key)
