import csv
from collections.abc import Generator, Iterable
from pathlib import Path


class FileManager:
    def __init__(self):
        self.path: Path = Path(__file__).parent.parent / "data" / "data.csv"

    def read(self) -> Generator[str, None, None]:
        with open(self.path, "r") as file:
            for line in csv.reader(file):
                yield line

    def write(self, data: Iterable[Iterable[str]]) -> None:
        with open(self.path, "a+") as file:
            writer = csv.writer(file)
            writer.writerow(data)
