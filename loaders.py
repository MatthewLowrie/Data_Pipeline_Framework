import csv
import json
from abc import ABC, abstractmethod

from models import Record


class DataLoader(ABC):
    """Abstract base class for all data loaders."""

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def load(self, records: list[Record]) -> int:
        """Load records to destination. Returns count of records loaded."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}')"
    
    
class JSONLoader(DataLoader):
    """Loads records to a JSON file."""

    def __init__(self, name: str, filepath: str) -> None:
        super().__init__(name)
        self._filepath = filepath

    def load(self, records: list[Record]) -> int:
        data = [record.data for record in records]
        with open(self._filepath, "w") as f:
            json.dump(data, f, indent=2)
        return len(data)
    
    
class CSVLoader(DataLoader):
    """Loads records to a CSV file."""

    def __init__(self, name: str, filepath: str) -> None:
        super().__init__(name)
        self._filepath = filepath

    def load(self, records: list[Record]) -> int:
        if not records:
            return 0
        fieldnames = list(records[0].data.keys())
        with open(self._filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow(record.data)
        return len(records)