from typing import Any

from loaders import CSVLoader, DataLoader, JSONLoader
from sources import CSVSource, DataSource, JSONSource
from transforms import FilterNulls, RenameColumns, Transform, TypeCast


class StepFactory:
    """Factory for creating pipeline components from configuration."""

    _source_registry: dict[str, type[DataSource]] = {
        "csv": CSVSource,
        "json": JSONSource,
    }

    _transform_registry: dict[str, type[Transform]] = {
        "filter_nulls": FilterNulls,
        "rename_columns": RenameColumns,
        "type_cast": TypeCast,
    }

    _loader_registry: dict[str, type[DataLoader]] = {
        "json": JSONLoader,
        "csv": CSVLoader,
    }
    
    @classmethod
    def create_source(cls, config: dict[str, Any]) -> DataSource:
        """Create a data source from a config dict."""
        config = dict(config)
        source_type = config.pop("type")
        if source_type not in cls._source_registry:
            raise ValueError(f"Unknown source type: {source_type}")
        source_class = cls._source_registry[source_type]
        return source_class(**config)

    @classmethod
    def create_transform(cls, config: dict[str, Any]) -> Transform:
        """Create a transform from a config dict."""
        config = dict(config)
        transform_type = config.pop("type")
        if transform_type not in cls._transform_registry:
            raise ValueError(f"Unknown transform type: {transform_type}")
        transform_class = cls._transform_registry[transform_type]
        return transform_class(**config)

    @classmethod
    def create_loader(cls, config: dict[str, Any]) -> DataLoader:
        """Create a data loader from a config dict."""
        config = dict(config)
        loader_type = config.pop("type")
        if loader_type not in cls._loader_registry:
            raise ValueError(f"Unknown loader type: {loader_type}")
        loader_class = cls._loader_registry[loader_type]
        return loader_class(**config)
    
    @classmethod
    def register_source(cls, name: str, source_class: type[DataSource]) -> None:
        """Register a new source type."""
        cls._source_registry[name] = source_class

    @classmethod
    def register_transform(cls, name: str, transform_class: type[Transform]) -> None:
        """Register a new transform type."""
        cls._transform_registry[name] = transform_class

    @classmethod
    def register_loader(cls, name: str, loader_class: type[DataLoader]) -> None:
        """Register a new loader type."""
        cls._loader_registry[name] = loader_class