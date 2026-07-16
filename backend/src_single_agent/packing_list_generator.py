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
    Do not add any message or comment in the start/end of the output.

    Trip Details:
    - Destination: {state["preferences"].get("destination", "")}
    - Travel Month: {state["preferences"].get("month", "")}
    - Duration: {state["preferences"].get("duration", 0)} days
    - Holiday Type: {state["preferences"].get("holiday_type", "general")}
    - Budget Type: {state["preferences"].get("budget_type", "")}
    - Number of People: {state["preferences"].get("num_people", "")}

    Weather Information:
    {state.get("weather_forecast", 
               "Weather information not available. Use seasonal estimate based on destination and month.")}

    Important Instructions:
    - Make the packing list practical for real travelers.
    - Consider destination, month, duration, weather, and holiday type.
    - If weather data is missing, use a realistic seasonal assumption.
    - Keep the output clean and presentable.
    - Use headings, bullet points, and tables wherever helpful.
    - Avoid unnecessary items.
    - Mention must-carry items separately.

    Output Format:

    1. Complete Packing Table
    
    Create one combined packing table with these columns:
    
    | Category | Items to Pack | Notes |
    |---|---|---|
    
    Include all these categories in the same table:
    - Clothes
    - Daywear
    - Nightwear
    - Trip-specific clothes
    - Footwear
    - Toiletries
    - Medicines / First Aid
    - Electronics
    - Documents
    - Weather Protection
    - Rain items if rainy
    - Warm clothes if cold
    - Sun protection if hot
    - Comfortable items if humid
    - Trip-specific items
    
    Rules:
    - In the "Items to Pack" column, mention item names.
    - Use bullet points inside the table cells.
    - Keep the packing list practical and easy to understand.
    - Avoid unnecessary items.
    - Customize items based on destination, month, duration, weather, and holiday type.
    
    - For Trip-specific Items Packing Instructions:
        - If it is a beach trip, suggest items useful for water activities, beach comfort, sun protection, and wet clothes management.
        - If it is an adventure trip, suggest items useful for outdoor movement, safety, rough terrain, and changing weather.
        - If it is a family trip, suggest items useful for comfort, health, snacks, children/elderly needs, and emergency support.
        - If it is a festival or cultural trip, suggest items useful for local customs, modest dressing, long walking, crowd management, and temple/religious visits if relevant.
        - If the holiday type is general or unclear, suggest only common practical travel items.
        - Do not add unnecessary items.
        - Keep suggestions suitable for the destination, weather, duration, and budget.

    6. Do Not Carry / Avoid
    - Mention items that are unnecessary or risky to carry.
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
