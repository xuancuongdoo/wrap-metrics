import time
from functools import wraps
from typing import Any, Callable, Dict

from loguru import logger

from .models import FunctionMetrics

from .models import MetricsStore
from .db_worker import add_metric_to_queue

metrics_store = MetricsStore()


def metrics_collector(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: float = time.perf_counter()
        error_occurred: bool = False
        func_name: str = func.__name__
        try:
            result = func(*args, **kwargs)
            logger.info(f"Function '{func_name}' executed successfully.")
            return result
        except Exception as e:
            error_occurred = True
            logger.exception(f"Exception occurred in function '{func_name}': {e}")
            raise
        finally:
            exec_time: float = time.perf_counter() - start_time
            metrics_store.update_metrics(func_name, exec_time, error_occurred)
            add_metric_to_queue(func_name, exec_time, error_occurred)
            logger.info(
                f"Function '{func_name}' execution time: {exec_time:.6f} seconds."
            )

    return wrapper


def get_metrics(func_name: str) -> Dict[str, Any]:
    metric: FunctionMetrics = metrics_store.get_metrics(func_name)
    return {
        "Function": func_name,
        "Number of calls": metric.call_count,
        "Average execution time": metric.average_execution_time,
        "Number of errors": metric.error_count,
    }