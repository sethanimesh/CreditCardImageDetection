import requests
import os
from tqdm import tqdm

# Define the API URL
url = "https://www.moneyhero.com.hk/api/credit-card/v2/cards/all?lang=en&pageSize=1000"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: The response is not in JSON format.")
        print("Response content:", response.content)
else:
    print(f"Error: Failed to fetch data. Status code: {response.status_code}")