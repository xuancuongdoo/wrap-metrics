import time
import sys
from loguru import logger

from metrics_collector.collector import metrics_collector, get_metrics
from metrics_collector.db_connection import DatabaseConnection
from metrics_collector.settings import settings


logger.remove()
logger.add(
    sink=sys.stderr,
    level=settings.log_level,
    format="<green>{time}</green> | <level>{level}</level> | <cyan>{name}</cyan> | <level>{message}</level>",
)


@metrics_collector
def example_function() -> None:
    """A sample function to demonstrate metrics collection."""
    time.sleep(0.5)
    logger.info("example_function executed.")


@metrics_collector
def error_function() -> None:
    """A sample function that raises an exception."""
    time.sleep(0.2)
    logger.info("error_function about to raise an exception.")
    raise ValueError("An error occurred in error_function")


def main() -> None:
    """Main function to run the example."""
    logger.info("Starting the metrics collection example.")

    for _ in range(3):
        example_function()

    try:
        error_function()
    except ValueError:
        logger.warning("Caught an exception from error_function.")

    # Retrieve and display metrics
    metrics = get_metrics('example_function')
    logger.info(f"Metrics for example_function: {metrics}")

    metrics_error = get_metrics('error_function')
    logger.info(f"Metrics for error_function: {metrics_error}")

    db_conn_instance: DatabaseConnection = DatabaseConnection.get_instance()
    db_conn_instance.close()


if __name__ == "__main__":
    main()