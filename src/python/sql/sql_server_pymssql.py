"""
Module: sql_server_pymssql

This module provides the `SQLDatabaseConnector` class for connecting to and interacting with a Microsoft SQL Server database using PyMSSQL.

The class allows for establishing a connection to the database, executing SQL queries, and closing the connection.

Dependencies:
    pymssql 2.2.7: A simple database interface for Python that builds on top of FreeTDS to provide a Python DB-API (PEP-249) interface to Microsoft SQL Server.
    pandas: A data analysis and manipulation library that provides data structures and functions needed to work with structured data.

Classes:
    SQLDatabaseConnector: A class that handles connection to a SQL Server database and supports executing SQL queries.

Usage Example:
    >>> from sql_server_pymssql import SQLDatabaseConnector

    >>> # Initialize a SQLDatabaseConnector object
    >>> sql_connector = SQLDatabaseConnector(server='localhost', username='user', password='password', database='example_db')

    >>> # Connect to the database
    >>> sql_connector.connect()

    >>> # Execute a query
    >>> query = "SELECT * FROM table_name"
    >>> result_df = sql_connector.execute_query(query)

    >>> # Disconnect from the database
    >>> sql_connector.disconnect()
"""

from typing import List, Optional, Union

import pandas as pd
import pymssql
from loguru import logger


class SQLDatabaseConnector:
    """
    A class to manage connection to a Microsoft SQL Server database using PyMSSQL and to execute SQL queries.

    Args:
        server (str): The server name or IP address of the SQL Server instance.
        username (str): The username for authentication.
        password (str): The password for authentication.
        database (str, optional): The name of the database to connect to. Defaults to None.

    Attributes:
        server (str): The server name or IP address of the SQL Server instance.
        username (str): The username for authentication.
        password (str): The password for authentication.
        database (Optional[str]): The name of the database to connect to.
        connection (Optional[pymssql.Connection]): The connection object to the database. Initially None.
    """

    def __init__(
        self, server: str, username: str, password: str, database: Optional[str] = None
    ) -> None:
        """
        Initialize the SQLDatabaseConnector object.

        Args:
            server (str): The server address or hostname.
            username (str): The username for authentication.
            password (str): The password for authentication.
            database (Optional[str]): The name of the database to connect to. Defaults to None.
        """
        self.server = server
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> None:
        """
        Establishes a connection to the SQL Server database.

        Raises:
            pymssql.InterfaceError: If there is an error with the interface connection.
            pymssql.DatabaseError: If there is an error with the database connection.
            Exception: For any other unexpected errors.
        """
        try:
            connection_params = (
                {
                    "server": self.server,
                    "user": self.username,
                    "password": self.password,
                    "database": self.database,
                }
                if self.database
                else {
                    "server": self.server,
                    "user": self.username,
                    "password": self.password,
                }
            )
            self.connection = pymssql.connect(**connection_params)
            logger.info("Successfully connected to the SQL database.")
        except pymssql.InterfaceError as e:
            logger.error(f"Failed to connect to database: InterfaceError - {e}")
            raise
        except pymssql.DatabaseError as e:
            logger.error(f"Failed to connect to database: DatabaseError - {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error occurred while connecting to database: {e}")
            raise

    def disconnect(self) -> None:
        """
        Closes the connection to the SQL Server database.

        Raises:
            pymssql.DatabaseError: If there is an error with the database during disconnection.
            pymssql.InterfaceError: If there is an error with the interface during disconnection.
            Exception: For any other unexpected errors.
        """
        try:
            if self.connection:
                self.connection.close()
                logger.info("Successfully disconnected from the SQL database.")
        except pymssql.DatabaseError as e:
            logger.error(f"Failed to disconnect from database: DatabaseError - {e}")
            raise
        except pymssql.InterfaceError as e:
            logger.error(f"Failed to disconnect from database: InterfaceError - {e}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while disconnecting from database: {e}"
            )
            raise

    def execute_query(
        self, query: str, params: Optional[List[Union[str, int]]] = None
    ) -> Optional[pd.DataFrame]:
        """
        Executes a SQL query on the connected database and returns the results as a pandas DataFrame if the query is a SELECT statement.

        Args:
            query (str): The SQL query to execute.
            params (Optional[List[Union[str, int]]]): The parameters to pass with the query. Defaults to None.

        Returns:
            Optional[pd.DataFrame]: A DataFrame containing the query results for SELECT statements, or None for other types of queries.

        Raises:
            pymssql.ProgrammingError: If there is an error with the SQL query syntax.
            pymssql.DatabaseError: If there is a database error during query execution.
            pymssql.InterfaceError: If there is an error with the interface during query execution.
            Exception: For any other unexpected errors.
        """
        try:
            logger.debug(f"Executing query: {query} with params: {params}")
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)

                if "SELECT" in query.upper():
                    data = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    dataframe = pd.DataFrame(data, columns=columns)
                    logger.info(
                        f"Query executed successfully. Data retrieved: {len(dataframe)} rows."
                    )
                    return dataframe
                else:
                    self.connection.commit()
                    if "INSERT" in query.upper():
                        logger.info("Data inserted successfully.")
                    elif "UPDATE" in query.upper():
                        logger.info("Data updated successfully.")
                    elif "DELETE" in query.upper():
                        logger.info("Data deleted successfully.")
                    return None
        except pymssql.ProgrammingError as e:
            logger.error(f"Failed to execute query: ProgrammingError - {e}")
            raise
        except pymssql.DatabaseError as e:
            logger.error(f"Failed to execute query: DatabaseError - {e}")
            raise
        except pymssql.InterfaceError as e:
            logger.error(f"Failed to execute query: InterfaceError - {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error occurred while executing query: {e}")
            raise
