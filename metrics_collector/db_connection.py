from threading import Lock
from typing import Optional

import psycopg2
from psycopg2.extensions import connection
from loguru import logger

from .settings import settings


class DatabaseConnection:
    """
    Provides a singleton instance of a database connection, handling connection establishment and reconnection.
    
    The `DatabaseConnection` class is responsible for managing the connection to the PostgreSQL database, as specified by the `settings.postgres_dsn` configuration. It ensures that only a single instance of the connection is created and shared across the application, using the Singleton pattern.
    
    The class provides the following functionality:
    - Establishes a new database connection when the instance is first accessed.
    - Automatically reconnects to the database if the connection is lost or closed.
    - Provides a `connection` property that returns the active database connection.
    - Allows the connection to be explicitly closed using the `close()` method.
    """
    _instance: Optional["DatabaseConnection"] = None
    _lock: Lock = Lock()

    def __init__(self) -> None:
        """
        Initializes the DatabaseConnection class and establishes a new database connection.
        
        This method sets up the initial state of the DatabaseConnection class by initializing the `_conn` attribute to `None` and then calling the `_connect()` method to establish a new database connection.
        """
        self._conn: Optional[connection] = None
        self._connect()

    def _connect(self) -> None:
        """
        Establishes a new database connection.
        
        This method attempts to connect to the PostgreSQL database using the credentials and connection parameters provided in the `settings` module. If the connection is successful, it assigns the connection object to the `_conn` attribute. If the connection fails, it sets the `_conn` attribute to `None`.
        """
        try:
            self._conn = psycopg2.connect(
                user=settings.postgres_user,
                password=settings.postgres_password,
                dbname=settings.postgres_db,
                host=settings.postgres_host,
                port=settings.postgres_port
            )
            logger.info("Database connection established.")
        except Exception as e:
            logger.exception(f"Failed to connect to the database: {e}")
            self._conn = None

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        """
        Returns the singleton instance of the DatabaseConnection class.
        
        This method ensures that only one instance of the DatabaseConnection class is created and returned. It uses a lock to synchronize access to the instance creation process, preventing multiple threads from creating multiple instances.
        
        Returns:
            DatabaseConnection: The singleton instance of the DatabaseConnection class.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    logger.debug("Created new DatabaseConnection instance.")
        return cls._instance

    @property
    def connection(self) -> Optional[connection]:
        """
        Returns the active database connection, reconnecting if necessary.
        
        This property ensures that a valid database connection is available for use. If the connection is `None` or has been closed, it will automatically reconnect to the database using the configured connection parameters.
        
        Returns:
            Optional[connection]: The active database connection, or `None` if a connection could not be established.
        """
        if self._conn is None or self._conn.closed:
            logger.debug("Reconnecting to the database.")
            self._connect()
        return self._conn

    def close(self) -> None:
        """
        Closes the active database connection.
        
        This method ensures that the database connection is properly closed and released. If the connection is already closed, this method does nothing.
        """
        if self._conn and not self._conn.closed:
            self._conn.close()
            logger.info("Database connection closed.")