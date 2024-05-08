from argparse import Action
from collections.abc import Iterable
from typing import TypedDict, Type, NotRequired, Union, Any


class CommandArguments(TypedDict):
    name_or_flags: Iterable[str]
    type: Type
    help: str
    metavar: NotRequired[str | Iterable[str]]
    nargs: NotRequired[str | int]
    required: NotRequired[bool]
    action: NotRequired[Union[str, Type[Action]]]
    default: NotRequired[Any]
