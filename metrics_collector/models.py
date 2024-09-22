from typing import Dict
from threading import Lock
from loguru import logger


class FunctionMetrics:
    """
    Represents the metrics for a function, including the call count, total execution time, and error count.
    
    The `FunctionMetrics` class provides a way to track the metrics for a function, including the number of times the function has been called, the total execution time of the function, and the number of errors that have occurred during function calls.
    
    The `average_execution_time` property calculates the average execution time of the function, or returns 0.0 if the function has not been called.
    """
    def __init__(self):
        self.call_count = 0
        self.total_execution_time = 0.0
        self.error_count = 0

    @property
    def average_execution_time(self) -> float:
        """
        Calculates the average execution time of the function.

        Returns:
            float: The average execution time of the function, or 0.0 if the function has not been called.
        """
        if self.call_count == 0:
            return 0.0
        return self.total_execution_time / self.call_count


class MetricsStore:
    def __init__(self) -> None:
        self.metrics: Dict[str, FunctionMetrics] = {}
        self.lock: Lock = Lock()

    def update_metrics(self, func_name: str, exec_time: float, error_occurred: bool) -> None:
        with self.lock:
            if func_name not in self.metrics:
                self.metrics[func_name] = FunctionMetrics()
                logger.debug(f"Created metrics entry for function '{func_name}'.")
            metric = self.metrics[func_name]
            metric.call_count += 1
            metric.total_execution_time += exec_time
            if error_occurred:
                metric.error_count += 1
            logger.debug(f"Updated metrics for function '{func_name}': {metric}")

    def get_metrics(self, func_name: str) -> FunctionMetrics:
        with self.lock:
            return self.metrics.get(func_name, FunctionMetrics())