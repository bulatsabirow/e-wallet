from datetime import datetime
from typing import Union


def date_converter(date_str: Union[str, datetime.date]) -> datetime.date:
    try:
        if isinstance(date_str, str):
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_str
    except ValueError:
        raise ValueError(
            f"Invalid date string: {date_str}. It must follow format YYYY-MM-DD"
        )
