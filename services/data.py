import csv
import os.path
import shutil
from collections.abc import Generator, Iterable
from operator import eq
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from attr import asdict, AttrsInstance

from commands.filter import between
from services.schema import FinancialOperation


class FileManager:
    schema: AttrsInstance = FinancialOperation
    path: Path = Path(__file__).parent.parent / "data" / "data.csv"

    @property
    def filter_criteria(self):
        return {param: eq for param in self.schema.fieldnames(exclude=["date"])} | {
            "date": between
        }

    def filter(self, **kwargs):
        for row in self.read():
            # Each row should correspond all filter parameters
            if all(
                self.filter_criteria.get(filter_kwarg)(
                    getattr(row, filter_kwarg), filter_value
                )
                for filter_kwarg, filter_value in kwargs.items()
                if filter_value is not None
            ):
                yield row

    def read(self) -> Generator[AttrsInstance, None, None]:
        with open(self.path, "r", encoding="utf-8") as file:
            yield from map(lambda row: self.schema(**row), csv.DictReader(file))

    def write(self, data: AttrsInstance) -> None:
        # Check whether file exists before file opening
        is_file_exists = os.path.exists(self.path)

        with open(self.path, "a+", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.schema.fieldnames())

            if not is_file_exists:
                # If data file doesn't exist, its first row should be header
                writer.writeheader()

            writer.writerow(asdict(data))

    def edit(self, edited: dict[str, Any]) -> bool:
        with open(self.path, "r", encoding="utf-8") as file, NamedTemporaryFile(
            "w+", newline="", delete=False, suffix=".csv", encoding="utf-8"
        ) as temp_file:
            reader: Iterable[dict] = csv.DictReader(file)
            writer = csv.DictWriter(temp_file, fieldnames=self.schema.fieldnames())
            writer.writeheader()
            is_row_found = False

            for row in reader:
                if edited["id"] == row["id"]:
                    is_row_found = True
                    row.update(edited)
                    # validate edited data
                    self.schema(**row)

                writer.writerow(row)

        shutil.move(temp_file.name, self.path)
        return is_row_found
