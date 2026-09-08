from abc import ABC, abstractmethod

from models import Record


class Transform(ABC):
    """Abstract base class for all transforms (Strategy pattern)."""

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def apply(self, records: list[Record]) -> list[Record]:
        """Apply the transformation to a list of records."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}')"
    
    
class FilterNulls(Transform):
    """Removes records where specified fields are null or empty."""

    def __init__(self, name: str, fields: list[str]) -> None:
        super().__init__(name)
        self._fields = fields

    def apply(self, records: list[Record]) -> list[Record]:
        result: list[Record] = []
        for record in records:
            if all(
                record.get(field) not in (None, "", "null", "None")
                for field in self._fields
            ):
                result.append(record)
        return result
    

class RenameColumns(Transform):
    """Renames fields in each record."""

    def __init__(self, name: str, mapping: dict[str, str]) -> None:
        super().__init__(name)
        self._mapping = mapping

    def apply(self, records: list[Record]) -> list[Record]:
        result: list[Record] = []
        for record in records:
            new_data = {}
            for key, value in record.data.items():
                new_key = self._mapping.get(key, key)
                new_data[new_key] = value
            result.append(Record(data=new_data))
        return result
    
    
class TypeCast(Transform):
    """Casts specified fields to given types."""

    def __init__(self, name: str, schema: dict[str, type]) -> None:
        super().__init__(name)
        self._schema = schema

    def apply(self, records: list[Record]) -> list[Record]:
        result: list[Record] = []
        for record in records:
            new_data = dict(record.data)
            for field_name, target_type in self._schema.items():
                if field_name in new_data:
                    try:
                        new_data[field_name] = target_type(new_data[field_name])
                    except (ValueError, TypeError):
                        new_data[field_name] = None
            result.append(Record(data=new_data))
        return result