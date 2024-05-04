import argparse
import datetime
from dataclasses import astuple
from random import randint
from typing import NoReturn

from services.data import FileManager
from services.enums import Category
from services.schema import FinancialOperation


class BaseCommand:
    file_manager = FileManager()

    def __init__(self) -> NoReturn:
        raise NotImplementedError


class AddRecordCommand(BaseCommand):
    def __init__(self, parser) -> None:
        self.parser = argparse.ArgumentParser(
            description="Example", add_help=False, parents=[parser]
        )
        self.parser.add_argument("--summ", "-s", type=int, help="Sum")
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

        row = astuple(FinancialOperation(**kwargs))
        self.file_manager.write(row)
