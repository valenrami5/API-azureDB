# FastAPI Proyect

This project demonstrates a FastAPI application for uploading CSV files, processing them, and storing the data in an Azure SQL pool within Synapse Analytics.

Table of Contents

- [FastAPI Proyect](#fastapi-proyect)
  - [Installation](#installation)
  - [Usage](#usage)
  - [AzureSynapseSQLPool](#azuresynapsesqlpool)
    - [Database](#database)
  - [AzureSQL database](#azuresql-database)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/valenrami5/globant_assessment.git
    cd main.py

2. **Create and activate a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

## Usage

Endpoints

Assessment 1

    Endpoint: /assessment_1
    Method: GET
    Description: Get the number of employees hired for each job and department in 2021 divided by quarter. The table is ordered alphabetically by department and job.
    Response: HTML response containing the number of employees hired for each job and department in 2021 divided by quarter. The table is ordered alphabetically by department and job.

Assessment 2

    Endpoint: /assessment_2
    Method: GET
    Description: Get the list of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).
    Response: HTML response containing the mean employees hired by departments.

Upload Jobs

    Endpoint: /upload-jobs/
    Method: POST
    Description: Upload job-related data in bulk from a CSV file.
    Parameters:
        file: An UploadFile containing job data in CSV format.
    Response:
        200 OK: { "message": "Batch data uploaded successfully" }
    Raises:
        400 Bad Request: If there is an error processing the file or if the batch size is invalid.

Upload Departments

    Endpoint: /upload-departments/
    Method: POST
    Description: Upload department-related data in bulk from a CSV file.
    Parameters:
        file: An UploadFile containing department data in CSV format.
    Response:
        200 OK: { "message": "Batch data uploaded successfully" }
    Raises:
        400 Bad Request: If there is an error processing the file or if the batch size is invalid.

Upload Hired Employees

    Endpoint: /upload-hired-employees/
    Method: POST
    Description: Upload hired employees-related data in bulk from a CSV file.
    Parameters:
        file: An UploadFile containing hired employees data in CSV format.
    Response:
        200 OK: { "message": "Batch data uploaded successfully" }
    Raises:
        400 Bad Request: If there is an error processing the file or if the batch size is invalid.

Models
Jobs

    id: int
    job: str

Departments

    id: int
    department: str

Hired Employees

    id: int
    name: Optional[str]
    datetime: Optional[datetime]
    department_id: Optional[int]
    job_id: Optional[int]

Error Handling

The application raises HTTPException with status code 400 for errors such as:

    Unsupported model type.
    Data type mismatches.
    Issues in processing the uploaded file.

## AzureSynapseSQLPool

### Database

1. First, an Azure SQL Synapse pool database called HR Management was created with Locally Redundant Storage (LRS) due to cost considerations. However, it was later decided that an Azure SQL Database would be a better fit. This decision was based on several factors:

2. Column Constraints: Azure SQL Database supports column constraints such as primary and foreign keys, which are essential for maintaining data integrity in relational databases.

3. Performance and Architecture: While the Massively Parallel Processing (MPP) architecture of Azure Synapse allows workloads to be spread across multiple virtual processors, providing excellent performance for processing massive enterprise datasets, it is more suited for large-scale data warehousing.

4. Concurrency: Azure SQL Database supports up to 6,400 concurrent queries, compared to Azure Synapse's limit of 128 concurrent queries. This makes Azure SQL Database a better fit for smaller, transactional workloads that require high concurrency, often with thousands of concurrent users.

In summary, the Azure SQL Database offers better support for transactional workloads with high concurrency and the necessary database constraints, making it more suitable for the HR Management application.

## AzureSQL database

Database Schema
The HR Management database is hosted on Azure SQL and comprises three tables: hired_employees, jobs, and departments. The departments table acts as the fact table in this schema. Here is an overview of each table:

Departments Table

    Columns:

        id (INT, Primary Key): Unique identifier for the department.
        department (VARCHAR, NOT NULL): Name of the department.

Jobs Table

    Columns:

        id (INT, Primary Key): Unique identifier for the job.
        job (VARCHAR, NOT NULL, Unique): Name of the job.

Hired Employees Table

    Columns:

        id (INT, Primary Key): Unique identifier for the hired employee.
        name (VARCHAR): Name of the hired employee.
        datetime (DATETIME): Date and time when the employee was hired.
        department_id (INT, Foreign Key): References id in the departments table.
        job_id (INT, Foreign Key): References id in the jobs table.

Database Connection

The database connection is managed by the AzureConnector class and the SqlManager class, which handle establishing and closing connections, as well as executing various database operations. The connection uses credentials and parameters stored in environment variables.

AzureConnector Class

    Methods:

        _get_connection(): Constructs the connection string from environment variables.
        _establish_connection(): Establishes the connection to the Azure SQL database and returns the connection and cursor.
        _close_connection(conn): Closes the given database connection.
        SqlManager Class

    Methods:
    
        __init__(): Initializes the connection and cursor.
        show_tables(): Displays the names of all tables in the database.
        create_departments_table(): Creates the departments table if it does not exist.
        create_jobs_table(): Creates the jobs table if it does not exist.
        create_hired_employees_table(): Creates the hired_employees table if it does not exist.
        _insert_jobs_batch(jobs_objects): Inserts a batch of job records into the jobs table.
        _insert_departments_batch(departments_objects): Inserts a batch of department records into the departments table.
        _insert_hired_employees_batch(hired_employees_objects): Inserts a batch of hired employee records into the hired_employees table.
        read_table(table_name): Reads all records from the specified table and loads them into a DataFrame.
        close_connection(): Closes the database connection.
