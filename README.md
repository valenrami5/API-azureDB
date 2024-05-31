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

**API Endpoints**
**GET /**

    Description: Returns a welcome message.
    Response:
        200 OK: {"message": "Welcome to the FastAPI application"}

**POST /upload-csv/**

    Description: Receives a CSV file, processes it, and stores the data in the Azure SQL pool.
    Request:
        Header: Content-Type: multipart/form-data
        Body: A file field named file containing the CSV file.
    Response:
        200 OK: File uploaded successfully with a preview of the data.
        400 Bad Request: Error processing file.

## AzureSynapseSQLPool

### Database

1. First, an Azure SQL Synapse pool database called HR Management was created with Locally Redundant Storage (LRS) due to cost considerations. However, it was later decided that an Azure SQL Database would be a better fit. This decision was based on several factors:

2. Column Constraints: Azure SQL Database supports column constraints such as primary and foreign keys, which are essential for maintaining data integrity in relational databases.

3. Performance and Architecture: While the Massively Parallel Processing (MPP) architecture of Azure Synapse allows workloads to be spread across multiple virtual processors, providing excellent performance for processing massive enterprise datasets, it is more suited for large-scale data warehousing.

4. Concurrency: Azure SQL Database supports up to 6,400 concurrent queries, compared to Azure Synapse's limit of 128 concurrent queries. This makes Azure SQL Database a better fit for smaller, transactional workloads that require high concurrency, often with thousands of concurrent users.

In summary, the Azure SQL Database offers better support for transactional workloads with high concurrency and the necessary database constraints, making it more suitable for the HR Management application.

## AzureSQL database

An single SQL database in azure was created called HR Management was created