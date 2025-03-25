"""
Module: sql_server_pyodbc_dict

This module provides the `SQLDatabaseConnectorDict` class for connecting to and interacting with a Microsoft SQL Server database using PyODBC, returning results as dictionaries instead of pandas DataFrames for better performance.

The class allows for establishing a connection to the database, executing SQL queries, and closing the connection.

Dependencies:
    pyodbc: A Python DB-API module for ODBC.

Classes:
    SQLDatabaseConnectorDict: A class that handles connection to a SQL Server database and supports executing SQL queries, returning results as dictionaries.

Usage Example:
    >>> from sql_server_pyodbc_dict import SQLDatabaseConnectorDict

    >>> # Initialize a SQLDatabaseConnectorDict object for Windows Authentication
    >>> sql_connector = SQLDatabaseConnectorDict(server='localhost', database='example_db', use_windows_auth=True)

    >>> # Or for SQL Server Authentication with username and password
    >>> sql_connector = SQLDatabaseConnectorDict(server='localhost', database='example_db', use_windows_auth=False, username='user', password='password')

    >>> # Connect to the database
    >>> sql_connector.connect()

    >>> # Execute a query
    >>> query = "SELECT * FROM table_name WHERE column = ?"
    >>> result = sql_connector.execute_query(query, params=[value])  # Returns list of dicts

    >>> # Disconnect from the database
    >>> sql_connector.disconnect()
"""

from typing import Any, Dict, List, Optional, Union

import pyodbc
from loguru import logger


class SQLDatabaseConnectorDict:
    """
    A class to manage connection to a Microsoft SQL Server database using PyODBC and to execute SQL queries,
    returning results as dictionaries for better performance.

    Args:
        server (str): The server name or IP address of the SQL Server instance.
        database (str): The name of the database to connect to.
        use_windows_auth (bool): Whether to use Windows Authentication (True) or SQL Server Authentication (False).
        username (str, optional): The username for SQL Server Authentication. Required if use_windows_auth is False.
        password (str, optional): The password for SQL Server Authentication. Required if use_windows_auth is False.

    Attributes:
        server (str): The server name or IP address of the SQL Server instance.
        database (str): The name of the database to connect to.
        use_windows_auth (bool): Indicates if Windows Authentication is used.
        username (Optional[str]): Username for SQL Server Authentication.
        password (Optional[str]): Password for SQL Server Authentication.
        connection (Optional[pyodbc.Connection]): The connection object to the database. Initially None.
    """

    def __init__(
        self,
        server: str,
        database: str,
        use_windows_auth: bool,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """
        Initialize the SQLDatabaseConnectorDict object.

        Args:
            server (str): The server address or hostname.
            database (str): The name of the database.
            use_windows_auth (bool): Whether to use Windows Authentication or not.
            username (Optional[str]): The username for SQL Server Authentication.
            password (Optional[str]): The password for SQL Server Authentication.
        """
        self.server = server
        self.database = database
        self.use_windows_auth = use_windows_auth
        self.username = username
        self.password = password
        self.connection = None

    def connect(self) -> None:
        """
        Establishes a connection to the SQL Server database.

        Raises:
            pyodbc.Error: If there is an error with the database connection.
        """
        try:
            if self.use_windows_auth:
                # Connection string using Windows Authentication
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                if not self.username or not self.password:
                    raise ValueError(
                        "Username and password are required for SQL Server Authentication."
                    )
                # Connection string for SQL Server Authentication
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={self.username};"
                    f"PWD={self.password};"
                )

            self.connection = pyodbc.connect(connection_string)
            logger.info("Successfully connected to the SQL database.")
        except pyodbc.Error as e:
            logger.exception("Failed to connect to the database.")
            raise RuntimeError(
                "Database connection failed. Check logs for details."
            ) from e

    def disconnect(self) -> None:
        """
        Closes the connection to the SQL Server database.

        Raises:
            pyodbc.Error: If there is an error with the database during disconnection.
        """
        try:
            if self.connection:
                self.connection.close()
                logger.info("Successfully disconnected from the SQL database.")
        except pyodbc.Error as e:
            logger.exception("Failed to disconnect from the database.")
            raise RuntimeError("Failed to disconnect from the database.") from e

    def execute_query(
        self, query: str, params: Optional[List[Union[str, int]]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Executes a SQL query on the connected database and returns the results as a list of dictionaries
        if the query is a SELECT statement.

        Args:
            query (str): The SQL query to execute, with `?` placeholders for parameters.
            params (Optional[List[Union[str, int]]]): The parameters to pass with the query. Defaults to None.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of dictionaries containing the query results for SELECT statements,
            or None for other types of queries.

        Raises:
            pyodbc.Error: If there is an error with the SQL query execution.
        """
        try:
            logger.debug(f"Executing query: {query} with parameters: {params}")
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or [])

                if "SELECT" in query.upper():
                    columns = [column[0] for column in cursor.description]
                    rows = cursor.fetchall()

                    # Convert rows to list of dictionaries
                    result = [dict(zip(columns, row)) for row in rows]

                    logger.info(
                        f"Query executed successfully. Retrieved {len(result)} rows."
                    )
                    return result
                else:
                    self.connection.commit()
                    logger.info("Query executed successfully.")
                    return None
        except pyodbc.Error as e:
            logger.exception("Query execution failed.")
            raise RuntimeError("Query execution failed. Check logs for details.") from e

    def execute_query_from_file(
        self, file_path: str, params: Optional[List[Union[str, int]]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Executes a SQL query from a file and returns the results as a list of dictionaries if the query is a SELECT statement.

        Args:
            file_path (str): The path to the SQL file containing the query.
            params (Optional[List[Union[str, int]]]): The parameters to pass with the query. Defaults to None.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of dictionaries containing the query results for SELECT statements,
            or None for other types of queries.

        Raises:
            FileNotFoundError: If the SQL file does not exist.
            pyodbc.Error: If there is an error with the SQL query execution.
        """
        try:
            logger.debug(f"Reading SQL query from file: {file_path}")
            with open(file_path, "r", encoding="utf-8") as file:
                query = file.read()

            logger.debug(
                f"Executing query from file: {file_path} with parameters: {params}"
            )

            with self.connection.cursor() as cursor:
                cursor.execute(query, params or [])

                if "SELECT" in query.upper():
                    columns = [column[0] for column in cursor.description]
                    rows = cursor.fetchall()

                    # Convert rows to list of dictionaries
                    result = [dict(zip(columns, row)) for row in rows]

                    logger.info(
                        f"Query from file executed successfully. Retrieved {len(result)} rows."
                    )
                    return result
                else:
                    self.connection.commit()
                    logger.info("Query from file executed successfully.")
                    return None

        except FileNotFoundError as e:
            logger.exception(f"SQL file not found: {file_path}")
            raise e
        except pyodbc.Error as e:
            logger.exception("Query execution from file failed.")
            raise RuntimeError(
                "Query execution from file failed. Check logs for details."
            ) from e
