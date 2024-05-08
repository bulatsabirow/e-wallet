import argparse
from copy import deepcopy

from commands.commands import (
    BaseCommand,
    AddRecordCommand,
    ShowBalanceCommand,
    FilterRecordCommand,
    EditRecordCommand,
)
from commands.config import (
    ADD_RECORD_COMMAND_CONFIG,
    EDIT_RECORD_COMMAND_CONFIG,
    SHOW_BALANCE_COMMAND_CONFIG,
    FILTER_RECORD_COMMAND_CONFIG,
)
from managers import CommandManager
from tests.schema import TestFileManager, TestFinancialOperation


class BaseTestCommandMixin:
    file_manager = TestFileManager()
    schema = TestFinancialOperation


class AddRecordTestCommand(BaseTestCommandMixin, AddRecordCommand):
    pass


class EditRecordTestCommand(BaseTestCommandMixin, EditRecordCommand):
    pass


class ShowBalanceTestCommand(BaseTestCommandMixin, ShowBalanceCommand):
    pass


class FilterRecordTestCommand(BaseTestCommandMixin, FilterRecordCommand):
    pass


class CommandTestManager(CommandManager):
    command_list = {
        "add_record": AddRecordTestCommand,
        "edit_record": EditRecordTestCommand,
        "show_balance": ShowBalanceTestCommand,
        "filter_record": FilterRecordTestCommand,
    }
