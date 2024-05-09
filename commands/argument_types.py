from argparse import ArgumentTypeError

import arrow


class DateType:
    def __init__(self, date_format: str):
        self.format = date_format

    def __call__(self, value: str):
        try:
            return arrow.get(value).format(self.format)
        except arrow.ParserError:
            raise ArgumentTypeError(
                f"Date {value} has unrecognized format. "
                f"Expected value should have {self.format} format"
            )
        except ValueError:
            raise ArgumentTypeError(f"Invalid date value: {value}.")
