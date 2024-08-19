from sql_database_connector import SQLDatabaseConnector


def main():
    # Initialize the SQLDatabaseConnector object with connection details
    sql_connector = SQLDatabaseConnector(
        server="localhost",
        username="your_username",
        password="your_password",
        database="example_db",
    )

    try:
        # Connect to the database
        sql_connector.connect()

        # Execute a SELECT query
        query = "SELECT * FROM table_name"
        result_df = sql_connector.execute_query(query)

        # Print the result
        if result_df is not None:
            print("Query Result:")
            print(result_df)

        # Execute an INSERT query
        insert_query = """
            INSERT INTO table_name (column1, column2)
            VALUES (%s, %s)
        """
        params = ["value1", 123]
        sql_connector.execute_query(insert_query, params)
        print("Data inserted successfully.")

        # Execute an UPDATE query
        update_query = """
            UPDATE table_name
            SET column1 = %s
            WHERE column2 = %s
        """
        update_params = ["new_value", 123]
        sql_connector.execute_query(update_query, update_params)
        print("Data updated successfully.")

        # Execute a DELETE query
        delete_query = """
            DELETE FROM table_name
            WHERE column2 = %s
        """
        delete_params = [123]
        sql_connector.execute_query(delete_query, delete_params)
        print("Data deleted successfully.")

    finally:
        # Disconnect from the database
        sql_connector.disconnect()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
