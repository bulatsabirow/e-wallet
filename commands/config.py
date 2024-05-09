import datetime
from copy import deepcopy

from commands.actions import EnumAction
from commands.argument_types import DateType
from commands.typing import CommandArguments
from services.enums import Category


def get_filter_record_command_config() -> list[CommandArguments]:
    config = deepcopy(ADD_RECORD_COMMAND_CONFIG)
    config.pop()
    config.append(
        {
            "name_or_flags": ["--date"],
            "nargs": 2,
            "type": DateType("YYYY-MM-DD"),
            "metavar": ("date_start", "date_end"),
            "help": "Inclusive date range",
        }
    )

    for option in config:
        option["required"] = False

    return config


def get_edit_record_command_config() -> list[CommandArguments]:
    config = deepcopy(ADD_RECORD_COMMAND_CONFIG)

    for option in config:
        option["required"] = False

    config.append(
        {
            "name_or_flags": ["id"],
            "type": str,
            "help": "Record ID",
        }
    )

    return config


ADD_RECORD_COMMAND_CONFIG: list = [
    {
        "name_or_flags": ["--summ", "-s"],
        "type": int,
        "help": "Sum of the financial operation",
        "required": True,
    },
    {
        "name_or_flags": ["--category", "-c"],
        "type": Category,
        "action": EnumAction,
        "required": True,
        "help": "Financial operation category: income or expense",
    },
    {
        "name_or_flags": ["--description", "-d"],
        "type": str,
        "help": "Financial operation description",
        "required": True,
    },
    {
        "name_or_flags": ["--date"],
        "type": DateType("YYYY-MM-DD"),
        "help": "Financial operation date in 'YYYY-MM-DD' format",
        "required": False,
        "default": datetime.date.today(),
    },
]

SHOW_BALANCE_COMMAND_CONFIG = [
    {
        "name_or_flags": ["--only-incomes"],
        "default": False,
        "help": "Calculate income balance",
        "action": "store_const",
        "const": Category.income.value,
    },
    {
        "name_or_flags": ["--only-expenses"],
        "default": False,
        "help": "Calculate expense balance",
        "action": "store_const",
        "const": Category.expense.value,
    },
]

FILTER_RECORD_COMMAND_CONFIG = get_filter_record_command_config()

EDIT_RECORD_COMMAND_CONFIG = get_edit_record_command_config()
