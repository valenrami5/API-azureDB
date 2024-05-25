from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import field_validator
from typing import List, Dict
import pandas as pd
from app.domain.models.jobs import Jobs
from app.infrastructure import azure_db_connector

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        print('df okay')
        # if not 1 <= len(df) <= 1000:
        #      raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000 rows")
        jobs_objects = field_validator(List[Jobs], df.to_dict(orient="records"))
        sql_manager = azure_db_connector.SqlManager()
        sql_manager._insert_jobs_batch(jobs_objects)
        return {"message": "CSV data uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")