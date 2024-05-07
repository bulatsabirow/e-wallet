import datetime
from copy import deepcopy
from uuid import uuid4, UUID

from commands.actions import EnumAction
from commands.typing import CommandArguments
from services.enums import Category


def get_filter_record_command_config() -> list[CommandArguments]:
    config = deepcopy(ADD_RECORD_COMMAND_CONFIG)

    for option in config:
        option["required"] = False

    return config


ADD_RECORD_COMMAND_CONFIG: list = [
    {"name_or_flags": ["--summ", "-s"], "type": int, "help": "Sum"},
    {"name_or_flags": ["--category", "-c"], "type": Category, "action": EnumAction},
    {"name_or_flags": ["--description", "-d"], "type": str, "help": "Description"},
    {
        "name_or_flags": ["--date"],
        "type": str,
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

FILTER_RECORD_COMMAND_CONFIG = get_filter_record_command_config()

EDIT_RECORD_COMMAND_CONFIG = [
    {
        "name_or_flags": ["id"],
        "type": UUID,
        "help": "Record ID",
    },
    *FILTER_RECORD_COMMAND_CONFIG,
]
