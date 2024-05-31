import os
from typing import List

import pypyodbc as odbc
from fastapi import HTTPException
from dotenv import load_dotenv
import pandas as pd

from app.domain.models.jobs import Jobs
from app.domain.models.departments import Departments
from app.domain.models.hired_employees import HiredEmployees


load_dotenv(".env")
class AzureConnector(object):

    def _get_connection(self): 
        driver = os.getenv('driver') 
        server = os.getenv('server')
        user = os.getenv('usr', '{ODBC Driver 17 for SQL Server}')
        pwd = os.getenv('pwd')
        database = os.getenv('database')
        connection_string = f'Driver={driver};Server={server};Database={database};Uid={user};Pwd={pwd};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=;'
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

    def show_tables(self):
        query = """SELECT name FROM sys.tables;"""
        self.cursor.execute(query)
        tables = self.cursor.fetchall() 
        if not tables:
            print('vacio')
        else:
            for table in tables:
                print(table[0])     

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
        
    def create_departments_table(self):
        query = """
            IF NOT EXISTS (
        SELECT * FROM sys.tables WHERE name = 'Departments'
    )
    BEGIN
        CREATE TABLE [dbo].[Departments] (
            [id]         INT  NOT NULL,
            [department] VARCHAR(255) NOT NULL,
            CONSTRAINT [PK_Departments] PRIMARY KEY CLUSTERED ([id] ASC),
        );
    END
        """
        self.cursor.execute(query)
        self.conn.commit()
        print("..Departments table created!")

    def create_jobs_table(self):
        query = """
            IF NOT EXISTS (
            SELECT * FROM sys.tables WHERE name = 'jobs'
        )
        BEGIN
            CREATE TABLE [dbo].[jobs] (
                [id]  INT  NOT NULL,
                [job] VARCHAR(255) NOT NULL, 
                CONSTRAINT [PK_jobs] PRIMARY KEY CLUSTERED ([id] ASC),
                CONSTRAINT [UK_jobs_job] UNIQUE ([job])
            );
        END"""
        self.cursor.execute(query)
        self.conn.commit()
        print("..Jobs employees table created!")


    def create_hired_employees_table(self):
        query = """
            IF NOT EXISTS (
                SELECT * FROM sys.tables WHERE name = 'hired_employees'
            )
            BEGIN
                CREATE TABLE [dbo].[hired_employees] (
                    [id]            INT      NOT NULL,
                    [name]          VARCHAR(255)     NULL,
                    [datetime]      DATETIME NULL,
                    [department_id] INT      NULL,
                    [job_id]        INT      NULL,
                    CONSTRAINT [PK_Hired_employees] PRIMARY KEY CLUSTERED ([id] ASC),
                    CONSTRAINT [FK_Departments_hired_employees] FOREIGN KEY ([department_id]) REFERENCES [dbo].[Departments] ([id]),
                    CONSTRAINT [FK_jobs_hired_employees] FOREIGN KEY ([job_id]) REFERENCES [dbo].[jobs] ([id])
                );
            END
        """
        self.cursor.execute(query)
        self.conn.commit()
        print("..hired employees table created!")

    def _insert_jobs_batch(self, jobs_objects: List[Jobs]):
        query = """
            INSERT INTO [dbo].[jobs] ([id], [job])
            VALUES (?, ?);
        """
        try:
            values = [(job.id, job.job) for job in jobs_objects]
            print(values)
            self.cursor.executemany(query, values)
            self.conn.commit()
            print('..DB Updated')
            self.cursor.close()
        except Exception as e:
            self.conn.rollback()
            raise e
        
    def _insert_departments_batch(self, departments_objects: List[Departments]):
        query = """
            INSERT INTO [dbo].[departments] ([id], [department])
            VALUES (?, ?);
        """
        try:
            values = [(dept.id, dept.department) for dept in departments_objects]
            self.cursor.executemany(query, values)
            self.conn.commit()
            self.cursor.close()
        except Exception as e:
            self.conn.rollback()
            raise e
        
    def _insert_hired_employees_batch(self, hired_employees_objects: List[HiredEmployees]):
        query = """
            INSERT INTO [dbo].[hired_employees] ([id], [name], [datetime], [department_id], [job_id])
            VALUES (?, ?, ?, ?, ?);
        """
        try:
            values = [(emp.id, emp.name, emp.datetime, emp.department_id, emp.job_id) for emp in hired_employees_objects]
            self.cursor.executemany(query, values)
            self.conn.commit()
            self.cursor.close()
            print('Database Updated')
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def read_table(self, table_name: str):
        query = f" SELECT * FROM {table_name}"
        try:
            df = pd.read_sql(query, self.conn)
            print("Data loaded into DataFrame successfully.")
        except Exception as e:
            print("Error loading data into DataFrame:", e)
        return df

    def close_connection(self):
        return self._close_connection(self.conn)
        
