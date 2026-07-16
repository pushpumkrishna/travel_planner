from langchain_core.messages import HumanMessage
# from langchain_ollama import ChatOllama
from backend.src_multi_agent import llm
import json


def generate_itinerary(state):
    # llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    # prompt = f"""
    # Using the following preferences, create a detailed itinerary:
    # {json.dumps(state["preferences"], indent=2)}
    #
    # Include sections for each day, dining options, and downtime.
    # """

    prompt = f"""
    You are an expert travel itinerary planner.

    Create a detailed, practical, and user-friendly travel itinerary based on the user's preferences.
    Do not add any message or comment in the start/end of the output.

    User Preferences:
    {json.dumps(state["preferences"], indent=2)}

    Important Instructions:
    - Create a realistic itinerary based on destination, duration, month, budget, holiday type, and number of people.
    - Make the plan easy to follow for travelers.
    - Include morning, afternoon, evening, and night sections for each day.
    - Add dining options where useful.
    - Add downtime/rest breaks so the itinerary does not feel rushed.
    - Consider weather, travel time, crowd levels, and comfort.
    - If exact live data is not available, give practical general recommendations.
    - Avoid overloading the day with too many activities.
    - Keep the output clean and presentable.
    - Use headings, bullet points, and tables wherever helpful.

    Output Format:

    1. Trip Summary
    - Destination
    - Duration
    - Travel month
    - Holiday type
    - Budget type
    - Best travel style for this trip

    3. Day-wise Itinerary
    For each day, use this format:

    Day 1: Short Day Theme

    | Time | Plan | Notes |
    |---|---|---|
    | Morning | Activity/place | Why it is good |
    | Afternoon | Activity/place + lunch | Keep it practical |
    | Evening | Activity/place | Relaxed suggestion |
    | Night | Dinner / leisure | Food or downtime idea |
    
    Important:
    * Use bullet points wherever necessary.
    * Give bit detailed knowledge in 2nd and 3rd columns above.

    """
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        if isinstance(result, list):
            result = "\n".join(
                str(item.get("text", item)) if isinstance(item, dict) else str(item)
                for item in result
            )

        elif isinstance(result, dict):
            result = str(result.get("text", ""))

        else:
            result = str(result)
        return {"itinerary": result.strip()}
    except Exception as e:
        return {"itinerary": "", "warning": str(e)}
