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