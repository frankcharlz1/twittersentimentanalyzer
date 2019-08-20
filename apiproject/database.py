from psycopg2 import pool


class Database:
    __connectionpool = None

    @classmethod
    def initialise(cls, **kwargs):
        Database.__connectionpool = pool.SimpleConnectionPool(1, 10, **kwargs)
        # kwargs: keyword arguments. Accept any number of named parameters
        # Named parameters have a name and a value e.g: database='learning'

    @classmethod
    def get_connection(cls):
        return cls.__connectionpool.getconn()

    @classmethod
    def return_connection(cls, connection):
        Database.__connectionpool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        Database.__connectionpool.closeall()


class CursorconnectionFromPool:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)
