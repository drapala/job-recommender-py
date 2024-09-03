def close_connections(mysql_connection, mongo_client, producer):
    """Function to close connections when terminating the application."""
    mysql_connection.close()
    mongo_client.close()
    producer.close()
