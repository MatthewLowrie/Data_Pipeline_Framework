import time
from abc import ABC, abstractmethod


class Observer(ABC):
    """Abstract base class for pipeline event observers."""

    @abstractmethod
    def on_step_start(self, step_name: str) -> None:
        """Called before a pipeline step begins."""
        ...

    @abstractmethod
    def on_step_complete(self, step_name: str, records_out: int) -> None:
        """Called after a pipeline step completes successfully."""
        ...

    @abstractmethod
    def on_error(self, step_name: str, error: str) -> None:
        """Called when a pipeline step encounters an error."""
        ...
        
        
class ConsoleObserver(Observer):
    """Prints pipeline events to the console."""

    def on_step_start(self, step_name: str) -> None:
        print(f"  [EVENT] Starting: {step_name}")

    def on_step_complete(self, step_name: str, records_out: int) -> None:
        print(f"  [EVENT] Completed: {step_name} ({records_out} records)")

    def on_error(self, step_name: str, error: str) -> None:
        print(f"  [EVENT] ERROR in {step_name}: {error}")
        
class TimingObserver(Observer):
    """Tracks execution time for each pipeline step."""

    def __init__(self) -> None:
        self._timings: dict[str, float] = {}
        self._current_step: str = ""
        self._start_time: float = 0.0

    def on_step_start(self, step_name: str) -> None:
        self._current_step = step_name
        self._start_time = time.time()

    def on_step_complete(self, step_name: str, records_out: int) -> None:
        elapsed = time.time() - self._start_time
        self._timings[step_name] = elapsed

    def on_error(self, step_name: str, error: str) -> None:
        elapsed = time.time() - self._start_time
        self._timings[f"{step_name} (FAILED)"] = elapsed

    def summary(self) -> str:
        lines = ["Timing Summary", "-" * 30]
        total = 0.0
        for step_name, elapsed in self._timings.items():
            lines.append(f"  {step_name}: {elapsed:.4f}s")
            total += elapsed
        lines.append(f"  Total: {total:.4f}s")
        lines.append("-" * 30)
        return "\n".join(lines)