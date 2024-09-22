CREATE TABLE IF NOT EXISTS function_metrics (
    id SERIAL PRIMARY KEY,
    function_name VARCHAR(255),
    execution_time DOUBLE PRECISION,
    error_occurred BOOLEAN,
    timestamp DOUBLE PRECISION
);