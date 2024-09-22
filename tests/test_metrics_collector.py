# tests/test_metrics_collector.py
import time

from metrics_collector.collector import metrics_collector, get_metrics


def test_metrics_collector():
    @metrics_collector
    def test_function():
        time.sleep(0.1)

    @metrics_collector
    def test_function_with_error():
        time.sleep(0.1)
        raise ValueError("Test error")

    # Call the functions
    test_function()
    try:
        test_function_with_error()
    except ValueError:
        pass

    # Get metrics
    metrics1 = get_metrics('test_function')
    metrics2 = get_metrics('test_function_with_error')

    # Assertions
    assert metrics1['Number of calls'] == 1
    assert metrics1['Number of errors'] == 0
    assert metrics1['Average execution time'] > 0

    assert metrics2['Number of calls'] == 1
    assert metrics2['Number of errors'] == 1
    assert metrics2['Average execution time'] > 0