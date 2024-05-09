import argparse
import datetime
import functools
import sys
from collections.abc import Iterable
from copy import deepcopy
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
    schema = FinancialOperation

    def init_config(self, parser):
        for config in self.arguments_config:
            parser.add_argument(*config.pop("name_or_flags"), **config)

    def __init__(self, parser, arguments_config=None, *args, **kwargs):
        self.parser = argparse.ArgumentParser(parents=[parser])
        self.arguments_config: list[CommandArguments] = deepcopy(arguments_config) or []

    def parse_args(self, *args, **kwargs):
        return self.parser.parse_args(*args, **kwargs)


class AddRecordCommand(BaseCommand):
    def __init__(self, parser) -> None:
        super().__init__(parser, ADD_RECORD_COMMAND_CONFIG)
        self.init_config(self.parser)
        self.parser.description = "Adds record to incomes/expenses data storage"

    def __call__(self, *args, **kwargs):
        data = self.parse_args(*args, **kwargs)
        instance = self.schema.from_args(data)

        self.file_manager.write(instance)
        sys.stdout.write(str(instance.id))
        sys.stdout.write("\n")


class ShowBalanceCommand(BaseCommand):
    def __init__(self, parser) -> None:
        super().__init__(parser, SHOW_BALANCE_COMMAND_CONFIG)
        group = self.parser.add_mutually_exclusive_group()
        self.init_config(group)
        self.parser.description = (
            "Shows user current balance or summary incomes/expenses"
        )

    def calculate_balance(self, category: bool | Category):
        rows: Iterable[FinancialOperation] = (
            self.file_manager.read()
            if not category
            else self.file_manager.filter(category=category)
        )

        return sum(map(lambda row: int(row.summ), rows))

    def __call__(self, *args, **kwargs):
        data = self.parse_args(*args, **kwargs)

        category = data.only_incomes or data.only_expenses
        # TODO beautify
        sys.stdout.write(str(self.calculate_balance(category)))
        sys.stdout.write("\n")


class FilterRecordCommand(BaseCommand):
    def __init__(self, parser) -> None:
        super().__init__(parser, FILTER_RECORD_COMMAND_CONFIG)
        self.init_config(self.parser)
        self.parser.description = "Adds record to incomes/expenses data storage"

    def __call__(self, *args, **kwargs):
        data = self.parse_args(*args, **kwargs)
        filter_kwargs = vars(data)
        filter_kwargs.pop("command")

        for operation in self.file_manager.filter(**filter_kwargs):
            sys.stdout.write(str(operation))
            sys.stdout.write("\n")
            sys.stdout.write("\n")


class EditRecordCommand(BaseCommand):
    def __init__(
        self,
        parser,
    ) -> None:
        super().__init__(parser, EDIT_RECORD_COMMAND_CONFIG)
        self.init_config(self.parser)
        self.parser.description = "Allows edit record data"

    def __call__(self, *args, **kwargs):
        data = self.parse_args(*args, **kwargs)
        edited_fields = {
            key: value
            for key, value in data.__dict__.items()
            if key in self.schema.fieldnames() and value is not None
        }

        result = self.file_manager.edit(edited_fields)
        if not result:
            self.parser.error("Record with entered ID doesn't exist")
        else:
            sys.stdout.write(str(data.id))
            sys.stdout.write("\n")
