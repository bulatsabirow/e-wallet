import csv
from collections.abc import Generator, Iterable
from dataclasses import astuple
from pathlib import Path

from services.schema import FinancialOperation


class FileManager:
    def __init__(self):
        self.path: Path = Path(__file__).parent.parent / "data" / "data.csv"

    def read(self) -> Generator[str, None, None]:
        with open(self.path, "r") as file:
            lines = csv.reader(file)
            # Skip first element as it contains table headers
            next(lines)
            for line in lines:
                yield FinancialOperation(*line)

    def write(self, data: FinancialOperation) -> None:
        with open(self.path, "a+") as file:
            writer = csv.writer(file)
            writer.writerow(astuple(data))
