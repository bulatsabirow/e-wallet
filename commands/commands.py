import argparse
import datetime
import functools
import sys
from dataclasses import astuple
from functools import reduce
from operator import add, attrgetter, neg, pos
from random import randint
from typing import NoReturn, Any

from attr import asdict

from commands.actions import EnumAction
from commands.config import (
    ADD_RECORD_COMMAND_CONFIG,
    SHOW_BALANCE_COMMAND_CONFIG,
    FILTER_RECORD_COMMAND_CONFIG,
    EDIT_RECORD_COMMAND_CONFIG,
)
from commands.typing import CommandArguments
from services.data import FileManager
from services.enums import Category
from services.schema import FinancialOperation


class BaseCommand:
    file_manager = FileManager()
    arguments_config: list[CommandArguments] = []

    def init_config(self, parser):
        for config in self.arguments_config:
            parser.add_argument(*config.pop("name_or_flags"), **config)

    def __init__(self, parser, *args, **kwargs):
        self.parser = argparse.ArgumentParser(parents=[parser])


class AddRecordCommand(BaseCommand):
    arguments_config = ADD_RECORD_COMMAND_CONFIG

    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.init_config(self.parser)
        self.parser.description = "Adds record to incomes/expenses data storage"

    def __call__(self):
        data = self.parser.parse_args()
        kwargs = {
            field: getattr(data, field)
            for field in FinancialOperation.fieldnames(exclude=("id",))
        }
        instance = FinancialOperation(**kwargs)

        self.file_manager.write(instance)
        sys.stdout.write(str(instance.id))
        sys.stdout.write("\n")


class ShowBalanceCommand(BaseCommand):
    arguments_config = SHOW_BALANCE_COMMAND_CONFIG

    def __init__(self, parser) -> None:
        super().__init__(parser)
        group = self.parser.add_mutually_exclusive_group()
        self.init_config(group)
        self.parser.description = (
            "Shows user current balance or summary incomes/expenses"
        )

    def __call__(self):
        data = self.parser.parse_args()

        def get_summ(operation: FinancialOperation):
            if data.only_incomes:
                return (
                    operation.summ if operation.category == Category.income.value else 0
                )

            if data.only_expenses:
                return (
                    -operation.summ
                    if operation.category == Category.expense.value
                    else 0
                )

            return (
                operation.summ
                if operation.category == Category.income.value
                else -operation.summ
            )

        sys.stdout.write(str(sum(map(get_summ, self.file_manager.read()), 0)))
        sys.stdout.write("\n")


class FilterRecordCommand(BaseCommand):
    arguments_config = FILTER_RECORD_COMMAND_CONFIG

    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.init_config(self.parser)
        self.parser.description = "Adds record to incomes/expenses data storage"

    def __call__(self):
        data = self.parser.parse_args()
        filter_kwargs = vars(data)
        filter_kwargs.pop("command")

        for operation in self.file_manager.filter(**filter_kwargs):
            sys.stdout.write(str(operation))
            sys.stdout.write("\n")
            sys.stdout.write("\n")


class EditRecordCommand(BaseCommand):
    arguments_config = EDIT_RECORD_COMMAND_CONFIG

    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.init_config(self.parser)
        self.parser.description = "Allows edit record data"

    def __call__(self):
        data = self.parser.parse_args()
        edited_fields = {
            key: value
            for key, value in data.__dict__.items()
            if key in FinancialOperation.fieldnames() and value is not None
        }

        result = self.file_manager.edit(edited_fields)
        if not result:
            self.parser.error("Record with entered ID doesn't exist")
        else:
            sys.stdout.write(str(data.id))
            sys.stdout.write("\n")
