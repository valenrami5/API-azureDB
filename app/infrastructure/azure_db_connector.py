import os
import pypyodbc as odbc
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv(".env")

class AzureConnector(object):

    def _get_connection(self): 
        driver = os.getenv('driver') 
        server = os.getenv('server')
        user = os.getenv('usr')
        pwd = os.getenv('pwd')
        database = os.getenv('database')
        connection_string = f'Driver={driver};Server={server},1433;Database={database};Uid={user};Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=1000;autocommit=true;enable=true'
        return connection_string
    
    def _establish_connection(self):
        try:
            connection_string = self._get_connection()
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()
            print('..Connection established')
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        return conn, cursor
    
    def _close_connection(self, conn):
        if 'conn' in locals() and conn:
            conn.close()
            print("..Connection closed.")

class SqlManager(AzureConnector):

    def __init__(self):
        self.conn, self.cursor = self._establish_connection()

    def insert_col(self):
        """
    Inserts the integer value 1 into the column named col1 in the Products table in the Azure SQL database.

    This function executes an SQL query to insert a fixed value (1) into the 'col1' column of the 'Products' table.
    After executing the insertion, it closes the database connection.
    Note:
        This function was created for simple connection testing purposes.
    Raises:
        HTTPException: If any error occurs during the query execution.
    """
        insert_query = "INSERT INTO [dbo].[Products] (col1) VALUES (?)"
        self.cursor.execute(insert_query, (1,))
        print("..Row Updated!")
        self._close_connection(self.conn)
