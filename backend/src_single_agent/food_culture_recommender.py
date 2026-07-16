from langchain_core.messages import HumanMessage
# from langchain_ollama import ChatOllama
from backend.src_multi_agent import llm


def food_culture_recommender(state):
    # llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    # prompt = f"""
    # For a trip to {state["preferences"].get("destination", "")} with a
    # {state["preferences"].get("budget_type", "mid-range")} budget:
    # 1. Suggest popular local dishes and recommended dining options.
    # 2. Provide important cultural norms, etiquette tips, and things travelers should be aware of.
    # Format the response with clear sections for 'Food & Dining' and 'Culture & Etiquette'.
    # """

    prompt = f"""
    You are a local food and culture travel guide.

    Create a clear, practical, and user-friendly guide for food, dining, culture, and etiquette.
    Do not add any message or comment in the start/end of the output.

    Trip Details:
    - Destination: {state["preferences"].get("destination", "")}
    - Budget Type: {state["preferences"].get("budget_type", "mid-range")}
    - Holiday Type: {state["preferences"].get("holiday_type", "general")}
    - Duration: {state["preferences"].get("duration", "")} days
    - Number of People: {state["preferences"].get("num_people", "")}
    - Travel Month: {state["preferences"].get("month", "")}

    Important Instructions:
    - Suggest food and dining options suitable for the destination and budget.
    - Include local dishes, street food, restaurants/cafes style, and meal suggestions.
    - Include culture, etiquette, local behavior, dress code, and safety awareness.
    - Keep the language simple and useful for travelers.
    - Do not give fake restaurant names if exact data is not available.
    - If exact places are not known, suggest the type of area/place to search for.
    - Make the output clean and presentable.
    - Use headings, bullet points, and tables wherever helpful.

    Output Format:

    1. Food & Dining Summary
    - Give a 2-3 line summary of what food experience the traveler can expect.

    2. Day-wise Food & Dining Plan
    
    Create a separate table for each day of the trip.
    
    For each day, use this format:
    
    Day 1: Food & Dining Plan
    
    | Time of Day | Suggested Food / Meal | Recommended Restaurants|
    |---|---|---|
    | Morning / Breakfast | Mention breakfast dishes or food type | - Restaurant Name — Rating: 4.x/5<br>- Restaurant Name — Rating: 4.x/5 |
    | Afternoon / Lunch | Mention lunch dishes or food type | - Restaurant Name — Rating: 4.x/5<br>- Restaurant Name — Rating: 4.x/5 |
    | Evening Snacks | Mention snacks, cafes, street food | - Restaurant Name — Rating: 4.x/5<br>- Restaurant Name — Rating: 4.x/5 |
    | Night / Dinner | Mention dinner dishes or food type | - Restaurant Name — Rating: 4.x/5<br>- Restaurant Name — Rating: 4.x/5 |
    
    Repeat the same table for each day of the trip:
    - Day 1
    - Day 2
    - Day 3
    - Continue based on trip duration.
    
    Rules:
    - Recommend restaurants based on destination, budget, trip type, and local food culture.
    - Include restaurant names in bullet points inside the table.
    - Include ratings where available.
    - If exact ratings are not available, mention "rating not verified" instead of creating fake ratings.
    - Keep restaurant suggestions practical and realistic.
    - Include a mix of local restaurants, cafes, street food areas, and family-friendly places where suitable.
    - Avoid repeating the same restaurant too many times unless it is highly relevant.

    3. Culture & Etiquette
    Create a table with these columns:
    | Topic | What to Know | Traveler Tip |

    Include:
    - Local manners
    - Dress code
    - Temple/religious places if relevant
    - Tipping/payment habits
    - Photography rules
    - Food habits
    - Safety and crowd awareness

    4. Things to Avoid
    - Mention food, behavior, or travel mistakes to avoid.
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
        return {"food_culture_info": result.strip()}
    except Exception as e:
        return {"food_culture_info": "", "warning": str(e)}
