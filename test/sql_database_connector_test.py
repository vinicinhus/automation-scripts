import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import MagicMock

import pandas as pd

from src.python.sql.sql_database_connector import SQLDatabaseConnector


@pytest.fixture
def mock_connection():
    connection_mock = MagicMock()
    cursor_mock = MagicMock()
    connection_mock.cursor.return_value = cursor_mock
    return connection_mock


@pytest.fixture
def connector(mock_connection):
    return SQLDatabaseConnector(
        server="localhost", username="user", password="password", database="example_db"
    )


def test_connect_success(connector, mock_connection):
    connector.connection = None
    connector.connect()
    assert connector.connection == mock_connection
    mock_connection.connect.assert_called_once()


def test_connect_without_database_success():
    connector = SQLDatabaseConnector(
        server="localhost", username="user", password="password"
    )
    connector.connect()
    assert connector.connection is not None


def test_connect_interface_error(connector, mock_connection):
    mock_connection.connect.side_effect = Exception("Mock interface error")
    with pytest.raises(Exception):
        connector.connect()


def test_disconnect_success(connector, mock_connection):
    connector.connection = mock_connection
    connector.disconnect()
    mock_connection.close.assert_called_once()
    assert connector.connection is None


def test_disconnect_no_connection(connector, mock_connection):
    connector.connection = None
    connector.disconnect()
    mock_connection.close.assert_not_called()


def test_execute_query_success(connector, mock_connection):
    query = "SELECT * FROM table_name"
    mock_dataframe = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    mock_connection.cursor.return_value.execute.return_value.fetchall.return_value = (
        mock_dataframe.values.tolist()
    )
    result = connector.execute_query(query)
    assert result.equals(mock_dataframe)


def test_execute_query_programming_error(connector, mock_connection):
    query = "SELECT * FROM non_existent_table"
    mock_connection.cursor.return_value.execute.side_effect = Exception(
        "Mock programming error"
    )
    with pytest.raises(Exception):
        connector.execute_query(query)


def test_execute_query_database_error(connector, mock_connection):
    query = "SELECT * FROM table_name"
    mock_connection.cursor.return_value.execute.side_effect = Exception(
        "Mock database error"
    )
    with pytest.raises(Exception):
        connector.execute_query(query)


def test_execute_query_interface_error(connector, mock_connection):
    query = "SELECT * FROM table_name"
    mock_connection.cursor.return_value.execute.side_effect = Exception(
        "Mock interface error"
    )
    with pytest.raises(Exception):
        connector.execute_query(query)


def test_execute_query_unexpected_error(connector, mock_connection):
    query = "SELECT * FROM table_name"
    mock_connection.cursor.return_value.execute.side_effect = Exception(
        "Mock unexpected error"
    )
    with pytest.raises(Exception):
        connector.execute_query(query)
