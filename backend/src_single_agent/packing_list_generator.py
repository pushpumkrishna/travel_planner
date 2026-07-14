from langchain_core.messages import HumanMessage
# from langchain_ollama import ChatOllama
from backend.src_multi_agent import llm


def packing_list_generator(state):
    # llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    # prompt = f"""
    # Generate a comprehensive packing list for a {state["preferences"].get("holiday_type", "general")} holiday in
    # {state["preferences"].get("destination", "")} during {state["preferences"].get("month", "")} for
    # {state["preferences"].get("duration", 0)} days.
    # Include essentials based on expected weather and trip type.
    # """

    prompt = f"""
    You are a smart travel packing assistant.

    Generate a clear, practical, and easy-to-follow packing list for the trip.

    Trip Details:
    - Destination: {state["preferences"].get("destination", "")}
    - Travel Month: {state["preferences"].get("month", "")}
    - Duration: {state["preferences"].get("duration", 0)} days
    - Holiday Type: {state["preferences"].get("holiday_type", "general")}
    - Budget Type: {state["preferences"].get("budget_type", "")}
    - Number of People: {state["preferences"].get("num_people", "")}

    Weather Information:
    {state.get("weather_forecast", "Weather information not available. Use seasonal estimate based on destination and month.")}

    Important Instructions:
    - Make the packing list practical for real travelers.
    - Consider destination, month, duration, weather, and holiday type.
    - If weather data is missing, use a realistic seasonal assumption.
    - Keep the output clean and presentable.
    - Use headings, bullet points, and tables wherever helpful.
    - Avoid unnecessary items.
    - Mention must-carry items separately.

    Output Format:

    1. Short Packing Summary
    - Give a 2-3 line summary of what kind of packing is needed.

    2. Essential Packing Table
    Create a table with these columns:
    | Category | Items to Pack | Why Needed |

    Include these categories:
    - Clothes
    - Footwear
    - Toiletries
    - Medicines / First Aid
    - Electronics
    - Documents
    - Weather Protection
    - Trip-specific Items

    3. Clothes Recommendation
    - Mention daywear
    - Nightwear
    - Extra clothes based on duration
    - Special clothes based on trip type

    4. Weather-Based Items
    - Rain items if rainy
    - Warm clothes if cold
    - Sun protection if hot
    - Comfortable items if humid

    5. Trip-Type Specific Packing
    - Beach trip: swimwear, flip-flops, sunscreen
    - Adventure trip: trekking shoes, torch, quick-dry clothes
    - Family trip: extra medicines, snacks, comfort items
    - Festival/cultural trip: modest clothes, comfortable footwear

    6. Do Not Carry / Avoid
    - Mention items that are unnecessary or risky to carry.

    7. Final Packing Tip
    - Give one short practical tip for the traveler.
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
        return {"packing_list": result.strip()}
    except Exception as e:
        return {"packing_list": "", "warning": str(e)}
