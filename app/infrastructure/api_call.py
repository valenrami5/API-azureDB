import requests
import pandas as pd
from datetime import datetime
path = '/home/valentina_ramirez/Documentos/globant/'


jobs_csv = path + 'jobs.csv'
jobs_url = 'http://127.0.0.1:8000/upload-jobs/'
temp_csv = 'temp.csv'

departments_csv = path + 'departments.csv'
departments_url = 'http://127.0.0.1:8000/upload-departments/'

hired_employees_csv = path + 'hired_employees.csv'
hired_employees_url = 'http://127.0.0.1:8000/upload-hired-employees/'

format_str = "%Y-%m-%dT%H:%M:%SZ"
datetime_obj = datetime.strptime('2021-11-07T02:48:42Z', format_str)
files = {'file': open(hired_employees_csv,'rb')}
df = pd.read_csv(hired_employees_csv)
print(df)

response = requests.post(hired_employees_url, files=files)

print('Response Status Code:', response.status_code)
print('Response Content:', response.text)