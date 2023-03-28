from mysql import connector
import datetime


class MySqlConnection:
    connection = None

    @classmethod
    def get_conection_instance(cls):
        """Gets a instance of connection to the MySQL db

        Returns:
            cls.connection (Object): Instance of connection to the MySQL db
        """
        # If not connected
        if not cls.connection or not cls.connection.is_connected():
            cls.connection = connector.connect(
                user="andres",
                password="123456",
                host="127.0.0.1",
                database="habi_db",
                port=3306
            )
        return cls.connection

    @classmethod
    def get_cursor(cls):
        """Gets a cursor object from the connection instance

        Returns:
            cls.connection.cursor (object): MySQLCursor object
        """
        # If not connected, create a connection
        if not cls.connection or not cls.connection.is_connected():
            cls.get_conection_instance()
        # Creates cursor with storage (of rows) in a buffer
        return cls.connection.cursor(buffered=True)

    @classmethod
    def close_conection(cls):
        """Deletes the MySQL database connection instance"""
        if cls.connection:
            cls.connection.close()
            cls.connection = None


class DBHelper:

    query_all = "SELECT * FROM {0};"

    @classmethod
    def get_all(cls, cursor, entity):
        """Gets all records of an 'entity.db_name' table

        Args:
            cursor (object): MySQLCursor object
            entity (object): Property object

        Returns:
            list_object_to_return (list): Records of the 'entity.db_name' table
        """
        cursor.execute(cls.query_all.format(entity.db_name))
        results = cursor.fetchall()
        list_dict_results = []

        # Creates a dictionary, where each row of the table is another
        # dictionary
        for result in results:
            list_dict_results.append(
                {
                    entity.fields[i]: result[i]
                    if not isinstance(result[i], datetime.datetime)
                    else str(result[i])
                    for i in range(len(result))
                }
            )

        # Each element of the dictionary is converted into an object
        list_object_to_return = [entity(**result)
                                 for result in list_dict_results]
        return list_object_to_return

    @classmethod
    def get_by_filter(cls, cursor, entity, **kwargs):
        """Gets the records of a table filtered by **kwargs

        Args:
            cursor (object): MySQLCursor object
            entity (object): Property object
            **kwargs (dictionary): Filter dictionary

        Returns:
            list_object_to_return (list): Records of the 'entity.db_name' table
        """

        query_sentence = cls.query_all.format(entity.db_name)

        # Remove the ";" from the query
        query_sentence = query_sentence.replace(";", " ")
        count = 0
        for key, value in kwargs.items():
            if not isinstance(value, float) and not isinstance(value, int):
                value = f"'{value}'"
            if count == 0:
                query_sentence += f"where {key}={value}"
            else:
                query_sentence += f" and {key}={value}"
            count += 1
        query_sentence += ";"
        cursor.execute(query_sentence)
        results = cursor.fetchall()
        list_dict_results = []
        for result in results:
            list_dict_results.append(
                {
                    entity.fields[i]: result[i]
                    if not isinstance(result[i], datetime.datetime)
                    else str(result[i])
                    for i in range(len(result))
                }
            )
        list_object_to_return = [entity(**result) for result in
                                 list_dict_results]
        return list_object_to_return
