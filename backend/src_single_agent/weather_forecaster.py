from langchain_core.messages import HumanMessage
# from langchain_ollama import ChatOllama
from backend.src_multi_agent import llm


def weather_forecaster(state):
    # llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    # prompt = f"""
    # Based on the destination and month, provide a detailed weather forecast including temperature, precipitation,
    # and advice for travelers:
    # Destination: {state["preferences"].get("destination", "")}
    # Month: {state["preferences"].get("month", "")}
    # """

    prompt = f"""
    You are a travel weather assistant.

    Create a clear and user-friendly weather guide for the trip.

    Trip Details:
    - Destination: {state["preferences"].get("destination", "")}
    - Travel Month: {state["preferences"].get("month", "")}
    - Duration: {state["preferences"].get("duration", "")} days
    - Trip Type: {state["preferences"].get("holiday_type", "")}
    - Budget Type: {state["preferences"].get("budget_type", "")}

    Important Instructions:
    - If exact live weather data is not available, give a realistic seasonal weather estimate for that destination and month.
    - Do not make fake exact daily forecasts.
    - Keep the language simple and useful for travelers.
    - Make the output clean and presentable.
    - Use headings, bullet points, and tables wherever useful.
    - Focus on practical travel advice.

    Output Format:

    1. Short Weather Summary
    - Give a simple 3-4 line summary of expected weather in bullet points.

    2. Weather Table
    Create a table with these columns:
    | Weather Factor | Expected Condition | Travel Advice |

    Include:
    - Temperature range
    - Rain / precipitation chance
    - Humidity
    - Wind / storm possibility
    - Day vs night comfort
    
    3. Day-wise Weather Table

    Create a day-wise weather table for the trip duration.
    
    Use this table format:
    
    | Day | Expected Weather | Temperature Range | Rain Chance | Humidity / Wind |
    |---|---|---|---|---|
    
    Rules:
    - Create rows from Day 1 to Day {state["preferences"].get("duration", 0)}.
    - If exact daily forecast is not available, provide realistic seasonal estimates for the destination and month.
    - Do not create fake exact live forecast values.
    
    """
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        print(type(result))

        if isinstance(result, list):
            result = "\n".join(
                str(item.get("text", item)) if isinstance(item, dict) else str(item)
                for item in result
            )

        elif isinstance(result, dict):
            result = str(result.get("text", ""))

        else:
            result = str(result)

        return {"weather_forecast": result.strip()}

    except Exception as e:
        return {"weather_forecast": "", "warning": str(e)}
