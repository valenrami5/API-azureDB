import uvicorn
import csv
from app.infrastructure.api import app
from app.infrastructure import azure_db_connector
from pydantic import field_validator
from typing import List, Dict
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import field_validator, model_validator
from typing import List, Dict
import pandas as pd
from app.domain.models.jobs import Jobs

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)