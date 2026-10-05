
from dataclasses import dataclass, field

# Import our custom components to enforce type safety across our orchestrator.
# These act as structural type declarations so Python knows what objects we are tracking.
from loaders import DataLoader
from models import PipelineResult, Record, StepResult
from sources import DataSource
from transforms import Transform


@dataclass
class PipelineLog:
    """Tracks execution results for each pipeline step.

    This helper class collects StepResult objects dynamically as each pipeline
    stage completes, allowing us to generate a clean final run report.
    """

    # We use field(default_factory=list) to ensure every instance of PipelineLog
    # gets a brand new, independent list. This prevents shared state bugs.
    steps: list[StepResult] = field(default_factory=list)

    def add(self, result: StepResult) -> None:
        """Appends a single step execution result to our run history log.

        Args:
            result (StepResult): The structured result of an executed step.
        """
        # Save the StepResult object directly into our memory list
        self.steps.append(result)

    def summary(self) -> str:
        """Generates a clean, formatted text report of the pipeline's execution.

        Iterates through all recorded steps and outputs a developer-friendly
        ASCII summary showing successes, failures, and record counts.

        Returns:
            str: A multi-line string containing the execution summary.
        """
        # We start by initializing a list of strings with our report header.
        # Constructing a list of lines is much faster and cleaner in Python 
        # than repeatedly adding string fragments with the '+' operator.
        lines = ["Pipeline Execution Summary", "=" * 40]

        # Loop through each captured step execution result
        for step in self.steps:
            # Dynamically determine the status icon to print
            status_icon = "OK" if step.status == "success" else "FAIL"

            # Format and add a clean row showing input vs. output throughput
            lines.append(
                f"  [{status_icon}] {step.step_name}: "
                f"{step.records_in} in -> {step.records_out} out"
            )

            # If an error traceback exists for this step, print it directly below
            if step.error:
                lines.append(f"        Error: {step.error}")

        # Append the footer boundary line to close out our ASCII table
        lines.append("=" * 40)

        # Merge our list of string lines together using a standard newline character
        return "\n".join(lines)

class Pipeline:
    """Orchestrates data pipeline execution using composition."""

    def __init__(self, name: str) -> None:
        # We store the pipeline's name with a single leading underscore.
        # In Python, this signals that the variable is intended for internal use only.
        self._name = name

        # We initialize the source variable as None.
        # The type hint 'DataSource | None' means it can hold a DataSource object or stay empty.
        self._source: DataSource | None = None

        # We set up an empty list to store our transformation strategies.
        # They will be executed sequentially when the pipeline runs.
        self._transforms: list[Transform] = []

        # We initialize the loader variable as None.
        # This will eventually hold our concrete file loader (like a CSV or JSON writer).
        self._loader: DataLoader | None = None

        # We create an instance of a logging helper right inside our constructor.
        # This is a classic example of COMPOSITION: the Pipeline 'has a' log recorder.
        self._log = PipelineLog()

    @property
    def name(self) -> str:
        """Provides controlled, read-only access to the internal pipeline name."""
        # The @property decorator lets external code read 'self._name' safely 
        # by simply writing 'pipeline.name' as if it were a standard attribute.
        return self._name

    def set_source(self, source: DataSource) -> "Pipeline":
        """Set the data source. Returns self for method chaining."""
        self._source = source
        return self

    def add_transform(self, transform: Transform) -> "Pipeline":
        """Add a transform step. Returns self for method chaining."""
        self._transforms.append(transform)
        return self

    def set_loader(self, loader: DataLoader) -> "Pipeline":
        """Set the data loader. Returns self for method chaining."""
        self._loader = loader
        return self
    
    def run(self) -> PipelineResult:
        """Execute the pipeline end-to-end."""
        if not self._source:
            raise ValueError("Pipeline has no data source configured")
        if not self._loader:
            raise ValueError("Pipeline has no data loader configured")

        errors: list[str] = []
        

#         Extract
#         The method first validates that both a source and loader are configured. Then it tries to extract records. \
#         If extraction fails, it logs the failure and immediately returns a failed PipelineResult. 

#         The records_in variable captures the starting count so the final result can calculate a drop rate.
        try:
            records = self._source.extract()
            self._log.add(StepResult(
                step_name=f"Extract: {self._source.name}",
                records_in=0,
                records_out=len(records),
                status="success"
            ))
        except Exception as e:
            self._log.add(StepResult(
                step_name=f"Extract: {self._source.name}",
                records_in=0,
                records_out=0,
                status="failed",
                error=str(e)
            ))
            return PipelineResult(
                records_in=0, records_out=0,
                success=False, errors=[str(e)]
            )

        records_in = len(records)
        
        # Transform
        # Unlike the Extract phase, a failed transform does not abort the pipeline. \
        # It logs the error and continues with whatever records survived.
        for transform in self._transforms:
            count_before = len(records)
            try:
                records = transform.apply(records)
                self._log.add(StepResult(
                    step_name=f"Transform: {transform.name}",
                    records_in=count_before,
                    records_out=len(records),
                    status="success"
                ))
            except Exception as e:
                errors.append(f"{transform.name}: {str(e)}")
                self._log.add(StepResult(
                    step_name=f"Transform: {transform.name}",
                    records_in=count_before,
                    records_out=len(records),
                    status="failed",
                    error=str(e)
                ))
        
        # Load
        try:
            loaded_count = self._loader.load(records)
            self._log.add(StepResult(
                step_name=f"Load: {self._loader.name}",
                records_in=len(records),
                records_out=loaded_count,
                status="success"
            ))
        except Exception as e:
            errors.append(f"Load failed: {str(e)}")
            self._log.add(StepResult(
                step_name=f"Load: {self._loader.name}",
                records_in=len(records),
                records_out=0,
                status="failed",
                error=str(e)
            ))
            return PipelineResult(
                records_in=records_in, records_out=0,
                success=False, errors=errors
            )

        return PipelineResult(
            records_in=records_in,
            records_out=loaded_count,
            success=len(errors) == 0,
            errors=errors
        )

    def get_log(self) -> PipelineLog:
        """Return the execution log."""
        return self._log