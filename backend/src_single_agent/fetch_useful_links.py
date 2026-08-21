# import os
# from dotenv import load_dotenv
# from langchain_community.utilities import GoogleSerperAPIWrapper

# load_dotenv()
# serper_api_key = os.getenv("SERPER_API_KEY")


# def fetch_useful_links(state: dict):
#     search = GoogleSerperAPIWrapper(
#         serper_api_key=serper_api_key
#     )

#     preferences = state.get("preferences", {})

#     destination = preferences.get(
#         "destination",
#         ""
#     )

#     month = preferences.get(
#         "month",
#         ""
#     )

#     holiday_type = preferences.get(
#         "holiday_type",
#         ""
#     )

#     budget_type = preferences.get(
#         "budget_type",
#         ""
#     )

#     duration = preferences.get(
#         "duration",
#         ""
#     )

#     query = (
#         f"Travel tips, places to visit, and useful travel guides "
#         f"for {destination} in {month}. "
#         f"Trip type: {holiday_type}. "
#         f"Budget: {budget_type}. "
#         f"Duration: {duration} days."
#     )

#     try:
#         search_results = search.results(query)

#         organic_results = search_results.get(
#             "organic",
#             []
#         )

#         links = [
#             {
#                 "title": result.get(
#                     "title",
#                     "No title"
#                 ),
#                 "link": result.get(
#                     "link",
#                     ""
#                 )
#             }
#             for result in organic_results[:5]
#         ]

#         return {
#             "useful_links": links
#         }

#     except Exception as e:

#         return {
#             "useful_links": [],
#             "warning": f"Failed to fetch links: {str(e)}"
#         }


# if __name__ == "__main__":
#     state = {"destination":"Goa"}
#     res = fetch_useful_links(state)
#     print(res)

from backend.src_multi_agent import llm


def estimate_budget(state):
    """
    Generates an estimated travel budget based on user preferences.
    """

    preferences = state.get("preferences", {})

    prompt = f"""
You are a travel budget planning assistant.

Create an estimated budget for the trip using the following preferences:

Destination: {preferences.get("destination", "")}
Month: {preferences.get("month", "")}
Duration: {preferences.get("duration", 0)} days
Number of Travellers: {preferences.get("num_people", 0)}
Holiday Type: {preferences.get("holiday_type", "")}
Budget Type: {preferences.get("budget_type", "")}
Additional Preferences: {preferences.get("comments", "")}

Provide the estimate in these categories:

1. Accommodation
2. Food
3. Local Transport
4. Activities
5. Miscellaneous
6. Total Estimated Budget

Keep the estimate practical and clearly mention that it is approximate.
"""

    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        response = response.content

    return {
        "budget_estimate": str(response)
    }