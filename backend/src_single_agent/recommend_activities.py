from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from backend.src_multi_agent import llm
import json


def recommend_activities(state):
    llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    # prompt = f"""
    # Based on the following preferences and itinerary, suggest unique local activities:
    # Preferences: {json.dumps(state["preferences"], indent=2)}
    # Itinerary: {state["itinerary"]}
    #
    # Provide suggestions in bullet points for each day if possible.
    # """

    prompt = f"""
    You are a local travel activity expert.

    Based on the user's preferences and itinerary, suggest unique and practical local activities.
    Do not add any message or comment in the start/end of the output.

    User Preferences:
    {json.dumps(state["preferences"], indent=2)}

    Current Itinerary:
    {state["itinerary"]}

    Important Instructions:
    - Suggest activities that match the destination, trip type, budget, duration, and traveler preferences.
    - Prefer local, unique, and experience-based activities instead of generic tourist suggestions.
    - If the itinerary has day-wise details, give activity suggestions day-wise.
    - If day-wise itinerary is not clear, group suggestions by activity type.
    - Avoid repeating activities already mentioned in the itinerary.
    - Keep the language simple and useful for travelers.
    - Make the output presentable using headings, bullet points, and tables if helpful.

    Output Format:

    1. Day-wise Activity Suggestions
    Use this format if itinerary has days:

    Day 1:
    - Activity:
    - Why it is good:
    - Best time:
    - Approx. cost:
    - Travel tip:

    Day 2:
    - Activity:
    - Why it is good:
    - Best time:
    - Approx. cost:
    - Travel tip:

    3. Extra Local Experiences
    Suggest 3-5 unique local experiences, such as:
    - Local markets
    - Food walks
    - Cultural experiences
    - Nature spots
    - Adventure activities
    - Family-friendly activities if applicable

    4. Activities to Avoid
    Mention activities that may not fit due to:
    - Weather
    - Budget
    - Travel group
    - Time limit
    - Safety
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
        return {"activity_suggestions": result.strip()}
    except Exception as e:
        return {"activity_suggestions": "", "warning": str(e)}
