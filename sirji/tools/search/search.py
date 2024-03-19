import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the environment variables using os.getenv
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

def get_search_result_urls(query, num_results=10):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': GOOGLE_SEARCH_API_KEY,
        'cx': GOOGLE_SEARCH_ENGINE_ID,
        'num': min(num_results, 10)  # API allows up to 10 results at a time
    }

    response = requests.get(search_url, params=params)
    response.raise_for_status()  # Raises an exception for HTTP errors
    search_results = response.json()
    
    urls = [item['link'] for item in search_results.get('items', [])]
    return urls

# Example usage:
# search_term = 'OpenAI'
# urls = get_search_result_urls(search_term)
# print(urls)

