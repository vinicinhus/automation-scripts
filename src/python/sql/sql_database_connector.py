"""
Module: sql_database_connector

This module provides a class for connecting to a Microsoft SQL Server database using PyMSSQL and executing queries.

Classes:
    SQLDatabaseConnector: A class for connecting to a SQL Server database and executing queries.

Dependencies:
    pymssql 2.2.7: A simple database interface for Python that builds on top of FreeTDS to provide a Python DB-API (PEP-249) interface to Microsoft SQL Server.

Usage Example:
    >>> from sql_database_connector import SQLDatabaseConnector

    >>> # Initialize a SQLDatabaseConnector object
    >>> connector = SQLDatabaseConnector(server='localhost', username='user', password='password', database='example_db')

    >>> # Connect to the database
    >>> connector.connect()

    >>> # Execute a query
    >>> query = "SELECT * FROM table_name"
    >>> result_df = connector.execute_query(query)

    >>> # Disconnect from the database
    >>> connector.disconnect()
"""

from typing import Optional

import pandas as pd
import pymssql
from loguru import logger


class SQLDatabaseConnector:
    """
    A class to connect to a Microsoft SQL Server database using PyMSSQL and execute queries.

    Args:
        server (str): The server name or IP address of the SQL Server instance.
        username (str): The username for authentication.
        password (str): The password for authentication.
        database (str, optional): The name of the database to connect to.

    Attributes:
        server (str): The server name or IP address of the SQL Server instance.
        username (str): The username for authentication.
        password (str): The password for authentication.
        database (str): The name of the database to connect to.
        connection: The connection object to the database.
    """

    def __init__(
            self, server: str, username: str, password: str, database: Optional[str] = None
    ) -> None:
        """
        Initialize a DatabaseConnector object.

        Args:
            server (str): The server address or hostname.
            username (str): The username for authentication.
            password (str): The password for authentication.
            database (Optional[str], optional): The name of the database to connect to. Defaults to None.
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
            pymssql.InterfaceError: If there is an interface error connecting to the database.
            pymssql.DatabaseError: If there is a database error connecting to the database.
            Exception: If an unexpected error occurs while connecting.
        """
        try:
            if self.database:
                connection_string = {
                    "server": self.server,
                    "user": self.username,
                    "password": self.password,
                    "database": self.database,
                }
            else:
                connection_string = {
                    "server": self.server,
                    "user": self.username,
                    "password": self.password,
                }
            self.connection = pymssql.connect(**connection_string)
            logger.info("Connected to the SQL database")
        except pymssql.InterfaceError as e:
            logger.error(f"InterfaceError connecting to database: {e}")
            raise
        except pymssql.DatabaseError as e:
            logger.error(f"DatabaseError connecting to database: {e}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while connecting to database: {e}"
            )
            raise

    def disconnect(self) -> None:
        """
        Disconnects from the SQL Server database.

        Raises:
            pymssql.DatabaseError: If there is a database error disconnecting from the database.
            pymssql.InterfaceError: If there is an interface error disconnecting from the database.
            Exception: If an unexpected error occurs while disconnecting.
        """
        try:
            if self.connection:
                self.connection.close()
                logger.info("Disconnected from the database")
        except pymssql.DatabaseError as e:
            logger.error(f"DatabaseError disconnecting from database: {e}")
            raise
        except pymssql.InterfaceError as e:
            logger.error(f"InterfaceError disconnecting from database: {e}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while disconnecting from database: {e}"
            )
            raise

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executes a SQL query and returns the result as a DataFrame.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pd.DataFrame: A DataFrame containing the result of the query, or None if an error occurs.

        Raises:
            pymssql.ProgrammingError: If there is a programming error executing the query.
            pymssql.DatabaseError: If there is a database error executing the query.
            pymssql.InterfaceError: If there is an interface error executing the query.
            Exception: If an unexpected error occurs while executing the query.
        """
        try:
            cursor = self.connection.cursor()
            logger.info("Retrieving query data")
            dataframe = pd.read_sql(query, self.connection)
            logger.info(f"Dataframe retrieved, length: {len(dataframe)}")
            return dataframe
        except pymssql.ProgrammingError as e:
            logger.error(f"ProgrammingError executing query: {e}")
            raise
        except pymssql.DatabaseError as e:
            logger.error(f"DatabaseError executing query: {e}")
            raise
        except pymssql.InterfaceError as e:
            logger.error(f"InterfaceError executing query: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while executing query: {e}")
            raise
