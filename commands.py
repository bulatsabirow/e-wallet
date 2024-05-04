import argparse
import datetime
import sys
from dataclasses import astuple
from functools import reduce
from operator import add, attrgetter, neg, pos
from random import randint
from typing import NoReturn

from attrs import asdict

from services.data import FileManager
from services.enums import Category
from services.schema import FinancialOperation


class BaseCommand:
    file_manager = FileManager()

    def __init__(self, parser, *args, **kwargs):
        self.parser = argparse.ArgumentParser(parents=[parser])


class AddRecordCommand(BaseCommand):
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.parser.description = "Adds record to incomes/expenses data storage"
        self.parser.add_argument("--summ", "-s", type=int, help="Sum")
        # TODO enum action
        self.parser.add_argument(
            "--category",
            "-c",
            choices=[Category.income.value, Category.expense.value],
            help="Category",
        )
        self.parser.add_argument("--description", "-d", type=str, help="Description")
        self.parser.add_argument(
            "--date",
            required=False,
            default=datetime.date.today(),
            type=str,
            help="Date",
        )

    def __call__(self):
        data = self.parser.parse_args()
        kwargs = {
            "summ": data.summ,
            "category": data.category,
            "description": data.description,
            "date": data.date,
        }

        instance = FinancialOperation(**kwargs)
        self.file_manager.write(instance)


class ShowBalanceCommand(BaseCommand):
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.parser.description = (
            "Shows user current balance or summary incomes/expenses"
        )
        self.parser.add_argument("--only-incomes", default=False, action="store_true")
        self.parser.add_argument("--only-expenses", default=False, action="store_true")

    def __call__(self):
        data = self.parser.parse_args()

        def get_summ(operation: FinancialOperation):
            if data.only_incomes and data.only_expenses:
                raise self.parser.error(
                    "--only-incomes and --only-expenses are incompatible arguments "
                )

            # TODO consider --only-incomes and --only-expenses case
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

        return reduce(add, map(get_summ, self.file_manager.read()))


class FilterRecordCommand(BaseCommand):
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.parser.description = "Adds record to incomes/expenses data storage"
        self.parser.add_argument("--summ", "-s", type=int, help="Sum")
        # TODO enum action
        self.parser.add_argument(
            "--category",
            "-c",
            choices=[Category.income.value, Category.expense.value],
            help="Category",
        )
        self.parser.add_argument("--description", "-d", type=str, help="Description")
        self.parser.add_argument(
            "--date",
            required=False,
            type=str,
            help="Date",
        )

    def __call__(self):
        data = self.parser.parse_args()
        filter_kwargs = vars(data)
        filter_kwargs.pop("command")

        for operation in self.file_manager.read():
            operation_dict = asdict(operation)
            # TODO filtering in other function
            if all(
                filter_value is None
                or filter_value == operation_dict.get(filter_kwarg, None)
                for filter_kwarg, filter_value in filter_kwargs.items()
            ):
                sys.stdout.write(str(operation))
                sys.stdout.write("\n")
                sys.stdout.write("\n")
