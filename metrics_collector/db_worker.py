import threading
import queue
import time
from typing import Optional, Callable
from functools import wraps

from loguru import logger
from psycopg2.extensions import connection
from psycopg2.extras import execute_values

from .db_connection import DatabaseConnection


metrics_queue: queue.Queue = queue.Queue()


def retry_on_exception(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 3
        delay = 5
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Error in '{func.__name__}': {e}")
                logger.info(f"Retrying in {delay} seconds... ({attempt + 1}/{retries})")
                time.sleep(delay)
        logger.error(f"Failed to execute '{func.__name__}' after {retries} attempts.")

    return wrapper


@retry_on_exception
def db_worker() -> None:
    db_conn_instance: DatabaseConnection = DatabaseConnection.get_instance()
    conn: Optional[connection] = db_conn_instance.connection
    if conn is None:
        logger.error("Database connection is unavailable. Exiting db_worker.")
        return

    while True:
        metrics_batch: list = []
        try:
            while not metrics_queue.empty():
                metric = metrics_queue.get_nowait()
                metrics_batch.append(metric)
            if metrics_batch:
                with conn.cursor() as cursor:
                    insert_query = """
                    INSERT INTO function_metrics (function_name, execution_time, error_occurred, timestamp)
                    VALUES %s
                    """
                    execute_values(
                        cursor,
                        insert_query,
                        metrics_batch,
                        template=None,
                        page_size=100,
                    )
                    conn.commit()
                    logger.debug(
                        f"Inserted {len(metrics_batch)} metrics into the database."
                    )
            time.sleep(1)
        except Exception as e:
            logger.exception(f"DB Worker Error: {e}")
            conn.rollback()
            time.sleep(5)
            continue


worker_thread = threading.Thread(target=db_worker, daemon=True)
worker_thread.start()


def add_metric_to_queue(func_name: str, exec_time: float, error_occurred: bool) -> None:
    """
    Adds a new metric to the metrics queue for processing by the database worker.

    Args:
        func_name (str): The name of the function that generated the metric.
        exec_time (float): The execution time of the function in seconds.
        error_occurred (bool): Whether an error occurred during the function execution.

    Returns:
        None
    """
    timestamp: float = time.time()
    metrics_queue.put((func_name, exec_time, error_occurred, timestamp))
    logger.debug(f"Metric added to queue for function '{func_name}'.")
