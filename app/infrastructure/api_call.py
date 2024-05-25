import requests
import pandas as pd

data = {
    'id': [1, 2],
    'job': ['Software Engineer', 'Data Scientist']
}

url = 'http://localhost:8000/upload-csv/'

df = pd.DataFrame(data)
csv_file = "temp.csv"
df.to_csv(csv_file, index=False)
print('df from api.. ok')
with open(csv_file, 'rb') as f:
    files = {'file': ('temp.csv', f)}
# Send a POST request to the endpoint
response = requests.post(url, files=files)

# Print response status code and content
print('Response Status Code:', response.status_code)
print('Response Content:', response.text)