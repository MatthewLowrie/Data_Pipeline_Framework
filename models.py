
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Record:
    """Represents a single data record in the pipeline.

    This class wraps a raw dictionary to demonstrate encapsulation, shielding
    the internal data structure from external direct modification.
    
    Attributes:
        data (dict[str, Any]): The raw key-value pairs representing the record's payload.
    """
    data: dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        """Safely retrieves a value from the internal dictionary.

        This mimics the standard dict.get() behavior, allowing the caller to specify
        a fallback default if the key does not exist.

        Args:
            key (str): The key to look up in the record.
            default (Any, optional): The value to return if key is missing. Defaults to None.

        Returns:
            Any: The value associated with the key, or the default value.
        """
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Allows bracket-notation reading access (e.g., record["key"]).

        This is a magic method (dunder method) that maps index-based bracket lookups
        directly to the internal data dictionary.

        Args:
            key (str): The dictionary key to look up.

        Returns:
            Any: The value stored in the dictionary for the given key.

        Raises:
            KeyError: If the key does not exist in the dictionary.
        """
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Allows bracket-notation writing access (e.g., record["key"] = value).

        This is a magic method (dunder method) that maps index-based assignments
        directly to modify the internal dictionary.

        Args:
            key (str): The key to set or update.
            value (Any): The new value to store.
        """
        self.data[key] = value
        

@dataclass
class StepResult:
    """Result of a single pipeline step execution.

    This data container tracks execution metrics and success/failure status
    for an individual processing component within the pipeline.

    Attributes:
        step_name (str): The descriptive name of the pipeline step (e.g., "Extract CSV").
        records_in (int): The number of records received as input to this step.
        records_out (int): The number of records successfully produced by this step.
        status (str): The completion status, typically "success" or "failed".
        error (str | None, optional): Details of any exception caught during execution. Defaults to None.
    """
    step_name: str
    records_in: int
    records_out: int
    status: str
    error: str | None = None


@dataclass
class PipelineResult:
    """Final result of a complete pipeline run.

    This data container aggregates execution metrics across all pipeline steps,
    offering a summary of the overall execution and filter performance.

    Attributes:
        records_in (int): Total records fed into the start of the pipeline.
        records_out (int): Total clean records successfully loaded at the end.
        success (bool): Indicates if the overall pipeline completed without crashing.
        errors (list[str]): A list of error tracebacks or messages caught during the run.
    """
    records_in: int
    records_out: int
    success: bool
    # We use field(default_factory=list) so every new instance gets its own independent
    # empty list, avoiding the classic Python "shared mutable default argument" bug.
    errors: list[str] = field(default_factory=list)

    @property
    def drop_rate(self) -> float:
        """Calculates the percentage of records filtered out during the run.

        Using the @property decorator allows this dynamically computed value to
        be accessed as a simple attribute (e.g., result.drop_rate) instead of
        requiring a function call (e.g., result.drop_rate()).

        Returns:
            float: The percentage of dropped records (between 0.0 and 1.0).
                   Returns 0.0 if no records entered the pipeline.
        """
        if self.records_in == 0:
            return 0.0
        return (self.records_in - self.records_out) / self.records_in
