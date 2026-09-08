import csv
import json
from abc import ABC, abstractmethod

from models import Record


class DataSource(ABC):
    """Abstract base class for all data sources."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._records: list[Record] = []

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def extract(self) -> list[Record]:
        """Extract records from the data source."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}')"
    
class CSVSource(DataSource):
    """Extracts data from a CSV file."""

    def __init__(self, name: str, filepath: str) -> None:
        super().__init__(name)
        self._filepath = filepath

    def extract(self) -> list[Record]:
        records: list[Record] = []
        with open(self._filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(Record(data=dict(row)))
        self._records = records
        return records
    
    
class JSONSource(DataSource):
    """Extracts data from a JSON file."""

    def __init__(self, name: str, filepath: str) -> None:
        super().__init__(name)
        self._filepath = filepath

    def extract(self) -> list[Record]:
        records: list[Record] = []
        with open(self._filepath, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    records.append(Record(data=item))
            else:
                records.append(Record(data=data))
        self._records = records
        return records