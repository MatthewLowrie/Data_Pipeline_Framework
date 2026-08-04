from dataclasses import dataclass, field


@dataclass
class StepResult:
    """Result of a single pipeline step execution.

    Attributes:
        step_name: The name of the pipeline step that was executed.
        records_in: The number of input records passed into the step.
        records_out: The number of output records returned by the step.
        status: The execution status (e.g., 'SUCCESS', 'FAILED').
        error: The error message if the step failed, otherwise None.
    """
    step_name: str
    records_in: int
    records_out: int
    status: str
    error: str | None = None


@dataclass
class PipelineResult:
    """Final result of a complete pipeline run.

    Attributes:
        records_in: The total number of records ingested at the start of the pipeline.
        records_out: The total number of records successfully loaded at the end.
        success: Indicates whether the pipeline ran successfully without fatal errors.
        errors: A list of error messages collected during execution. Defaults to an empty list.
    """
    records_in: int
    records_out: int
    success: bool
    errors: list[str] = field(default_factory=list)

    @property
    def drop_rate(self) -> float:
        """Calculates the ratio of records that were filtered or lost.

        Returns:
            The proportion of dropped records as a float between 0.0 and 1.0.
            Returns 0.0 if records_in is 0 to avoid division by zero.
        """
        if self.records_in == 0:
            return 0.0
        return (self.records_in - self.records_out) / self.records_in