import datetime
from copy import deepcopy
from uuid import uuid4, UUID

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
            "help": "Date range",
        }
    )

    for option in config:
        option["required"] = False

    return config


ADD_RECORD_COMMAND_CONFIG: list = [
    {"name_or_flags": ["--summ", "-s"], "type": int, "help": "Sum", "required": True},
    {
        "name_or_flags": ["--category", "-c"],
        "type": Category,
        "action": EnumAction,
        "required": True,
    },
    {
        "name_or_flags": ["--description", "-d"],
        "type": str,
        "help": "Description",
        "required": True,
    },
    {
        "name_or_flags": ["--date"],
        "type": DateType("YYYY-MM-DD"),
        "help": "Date",
        "required": False,
        "default": datetime.date.today(),
    },
]

SHOW_BALANCE_COMMAND_CONFIG = [
    {
        "name_or_flags": ["--only-incomes"],
        "default": False,
        "help": "Consider only incomes",
        "action": "store_true",
    },
    {
        "name_or_flags": ["--only-expenses"],
        "default": False,
        "help": "Consider only expenses",
        "action": "store_true",
    },
]

# TODO filter date range
FILTER_RECORD_COMMAND_CONFIG = get_filter_record_command_config()

EDIT_RECORD_COMMAND_CONFIG = [
    {
        "name_or_flags": ["id"],
        "type": str,
        "help": "Record ID",
    },
    *FILTER_RECORD_COMMAND_CONFIG,
]