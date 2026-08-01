import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()
serper_api_key = os.getenv("SERPER_API_KEY")


def fetch_useful_links(state: dict):
    search = GoogleSerperAPIWrapper(
        serper_api_key=serper_api_key
    )

    preferences = state.get("preferences", {})

    destination = preferences.get(
        "destination",
        ""
    )

    month = preferences.get(
        "month",
        ""
    )

    holiday_type = preferences.get(
        "holiday_type",
        ""
    )

    budget_type = preferences.get(
        "budget_type",
        ""
    )

    duration = preferences.get(
        "duration",
        ""
    )

    query = (
        f"Travel tips, places to visit, and useful travel guides "
        f"for {destination} in {month}. "
        f"Trip type: {holiday_type}. "
        f"Budget: {budget_type}. "
        f"Duration: {duration} days."
    )

    try:
        search_results = search.results(query)

        organic_results = search_results.get(
            "organic",
            []
        )

        links = [
            {
                "title": result.get(
                    "title",
                    "No title"
                ),
                "link": result.get(
                    "link",
                    ""
                )
            }
            for result in organic_results[:5]
        ]

        return {
            "useful_links": links
        }

    except Exception as e:

        return {
            "useful_links": [],
            "warning": f"Failed to fetch links: {str(e)}"
        }


if __name__ == "__main__":
    state = {"destination":""}
    res = fetch_useful_links(state)
    print(res)
