# Metrics Collector Project

This project collects metrics from Python functions and stores them in a PostgreSQL database. It provides a decorator `@metrics_collector` that can be used to track the execution time and error occurrences of functions.

## Prerequisites

- Docker (for Docker usage)
- Python 3.12 (for local usage)
- Poetry (for dependency management)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/metrics-collector-project.git
   cd metrics-collector-project
   ```

2. Install Poetry if you haven't already:

   ```bash
   pip install poetry
   ```

3. Install the project dependencies:

   ```bash
   poetry install
   ```

4. Create a `.env` file in the project root directory with the following environment variables:

   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=metrics_collector
   POSTGRES_PORT=5432
   POSTGRES_HOST=localhost
   LOG_LEVEL=INFO
   ```

5. Make sure you have a running PostgreSQL database with the specified credentials.

6. Run the application locally:

   ```bash
   make run
   ```

   This command will start the Docker containers, initialize the database, and run the application locally. It will also install any missing dependencies using Poetry.

7. To check the Docker logs, use the following command:

   ```bash
   make logs
   ```
   This command will start the application and collect metrics from the example functions.

## Project Structure

- `main.py`: The main entry point of the application.
- `metrics_collector/`: The package containing the metrics collector implementation.
  - `collector.py`: Defines the `@metrics_collector` decorator and related functions.
  - `db_connection.py`: Handles the database connection using the Singleton pattern.
  - `db_worker.py`: Implements the worker thread for inserting metrics into the database.
  - `settings.py`: Defines the application settings using Pydantic.
- `Dockerfile`: Dockerfile for building the application image.
- `docker-compose.yml`: Docker Compose configuration for running the application and database containers.
- `pyproject.toml`: Poetry configuration file for managing dependencies.
- `Makefile`: Makefile with convenient commands for Docker usage.

## License

This project is licensed under the [MIT License](LICENSE).