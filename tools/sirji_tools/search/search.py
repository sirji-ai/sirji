import os
import requests
from sirji_tools.config.config_loader import load_config
from sirji_tools.logger import r_logger as logger

# Now you can access the environment variables using os.getenv
GOOGLE_SEARCH_API_KEY = os.environ.get("SIRJI_GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.environ.get("SIRJI_GOOGLE_SEARCH_ENGINE_ID")



def search_for(query):
    logger.info(f"Started searching for query term: {query}")

    if not query:
        raise KeyError("Query is empty")
    
    google_config = load_config("google_config.json")


    if (query == ''):
        return KeyError("Query is empty")

    search_url = google_config['google_search_url']
    params = {
        'q': query,
        'key': GOOGLE_SEARCH_API_KEY,
        'cx': GOOGLE_SEARCH_ENGINE_ID,
        'num': google_config['search_results_per_page']
    }

    response = requests.get(search_url, params=params)
    response.raise_for_status()  # Raises an exception for HTTP errors
    search_results = response.json()

    urls = [item['link'] for item in search_results.get('items', [])]

    logger.info(f"Completed searching for query term: {query}")

    return urls

# Example usage:
# search_term = ''
# urls = search_for(search_term)
# print(urls)
