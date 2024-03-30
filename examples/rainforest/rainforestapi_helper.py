import os
import requests
import json
from dotenv import load_dotenv
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

# Update API key and base URL (if necessary)
api_key = os.environ.get("NEWS_API_KEY", "86839fb89b9c4286810e7d5f1cb30e54")
base_url = "https://newsapi.org/v1/sources"  # Updated base URL

# Update base parameters for the News API
base_params = {
    "apiKey": api_key,
    # Add more parameters as needed
}

# Update URL construction function
def get_url(params):
    query_parameters = {**base_params, **params}
    encoded_parameters = urlencode(query_parameters)
    return f"{base_url}?{encoded_parameters}"

# Update response processing to handle News API response structure
def send_request(data_dir, params):
    response = requests.get(get_url(params))

    if response.status_code == 200:
        data = response.json()
        sources = data.get('sources', [])

        with open(data_dir + "/news_sources.jsonl", 'w') as file:
            for source in sources:
                # Extract relevant data fields from the source
                source_data = {
                    "id": source.get("id", ""),
                    "name": source.get("name", ""),
                    "description": source.get("description", ""),
                    "url": source.get("url", ""),
                    "category": source.get("category", ""),
                    "language": source.get("language", ""),
                    "country": source.get("country", "")
                }
                # Format the data as a JSON object
                file.write(json.dumps({"doc": source_data}) + '\n')
    else:
        print(f"Failed to fetch data from News API. Status code: {response.status_code}")

# Example usage:
# send_request("data", {})  # Replace {} with additional parameters if needed
