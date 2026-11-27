
import os

from dotenv import load_dotenv
from tavily import TavilyClient


# Load environment variables from .env
load_dotenv()

# Get Tavily API key
api_key = os.getenv("TAVILY_API_KEY")

# Create Tavily client
tavily = TavilyClient(api_key=api_key)


def search_web(query: str):

    response = tavily.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    results = []

    for item in response["results"]:

        results.append({
            "title": item["title"],
            "url": item["url"],
            "content": item["content"]
        })

    return results
if __name__ == "__main__":

    results = search_web("Latest React features")

    for result in results:
        print(result["title"])
        print(result["url"])
        print(result["content"])
        print("--------------------")