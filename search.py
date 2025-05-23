from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from typing import Dict, List, Tuple

# Load environment variables
load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")
if not API_KEY:
    raise ValueError("SERPAPI_KEY environment variable is not set")

def google_dork_search(dork: str) -> Tuple[int, List[Dict]]:
    """
    Perform a Google dork search and return the total number of results and search results.
    
    Args:
        dork (str): The Google dork query string
        
    Returns:
        Tuple[int, List[Dict]]: Number of results found and list of search results with URLs and snippets
    """
    if not API_KEY:
        raise ValueError("SERPAPI_KEY is not set")
        
    params = {
        "engine": "google",
        "q": dork,
        "api_key": API_KEY,
        "num": 10  # Limit to 10 results per search
    }
    try:
        search = GoogleSearch(params)
        result = search.get_dict()
        
        # Extract total results count
        total_results = int(result.get("search_information", {}).get("total_results", 0))
        
        # Extract organic results (actual search results)
        organic_results = result.get("organic_results", [])
        
        # Format results to include only relevant information
        formatted_results = [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("source", "")
            }
            for item in organic_results
        ]
        
        return total_results, formatted_results
    except Exception as e:
        print(f"Error performing search: {str(e)}")
        return 0, [] 