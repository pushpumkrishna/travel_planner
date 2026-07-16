import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()
serper_api_key = os.getenv("SERPER_API_KEY")


def fetch_useful_links():
    search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
    # destination = state["preferences"].get("destination", "")
    # month = state["preferences"].get("month", "")
    destination = "Goa"
    month = "June"
    query = f"Travel tips and guides for {destination} in {month}"
    try:
        search_results = search.results(query)
        organic_results = search_results.get("organic", [])
        links = [
            {"title": result.get("title", "No title"),
             "link": result.get("link", "")}
            for result in organic_results[:5]
        ]
        print(links)

        if isinstance(links, list):
            links = "\n".join(str(item) for item in links)

        elif isinstance(links, dict):
            links = str(links)

        else:
            links = str(links)

        return {"useful_links": links}
    except Exception as e:
        return {"useful_links": [], "warning": f"Failed to fetch links: {str(e)}"}


if __name__ == "__main__":
    res = fetch_useful_links()
    print(res)
