from collections.abc import Iterable

from commands.argument_types import DateType


def between(value: str, dates: Iterable[str]):
    date_start, date_end = map(DateType("YYYY-MM-DD"), dates)

    return date_start <= value <= date_end
