import csv
import os.path
from collections.abc import Generator, Iterable
from typing import Union, Any

from attr import asdict
from pathlib import Path

from services.schema import FinancialOperation


class FileManager:
    def __init__(self):
        self.path: Path = Path(__file__).parent.parent / "data" / "data.csv"

    def read(
        self, convert=False
    ) -> Generator[Union[FinancialOperation, dict[str, Any]], None, None]:
        with open(self.path, "r") as file:
            lines: Iterable[dict] = csv.DictReader(file)

            for line in lines:
                if convert:
                    yield FinancialOperation(**line)
                else:
                    yield line

    def write(self, data: FinancialOperation) -> None:
        # Check whether file exists before file opening
        is_file_exists = os.path.exists(self.path)

        with open(self.path, "a+") as file:
            writer = csv.DictWriter(file, fieldnames=FinancialOperation.fieldnames())

            if not is_file_exists:
                # If data file doesn't exist, its first row should be header
                writer.writeheader()

            writer.writerow(asdict(data))
