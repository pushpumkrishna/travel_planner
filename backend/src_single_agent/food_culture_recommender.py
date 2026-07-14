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

    2. Must-Try Local Dishes
    Create a table with these columns:
    | Dish / Food Item | Why Try It | Best Time / Place Type |

    3. Dining Options by Budget
    Create a table with these columns:
    | Budget Level | Recommended Dining Style | Tips |

    Include:
    - Budget-friendly
    - Mid-range
    - Premium / special meal

    4. Suggested Meal Plan
    - Breakfast ideas
    - Lunch ideas
    - Evening snacks
    - Dinner ideas

    5. Culture & Etiquette
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

    6. Things to Avoid
    - Mention food, behavior, or travel mistakes to avoid.

    7. Final Local Tip
    - Give one short practical local tip for the traveler.
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
