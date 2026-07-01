from backend_single_agent.memory.memory_manager import memory_manager

from langchain_ollama import ChatOllama
import json

from backend_single_agent.memory.memory_manager import memory_manager

llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434"
)


def planner(state):
    """
    Planner Node

    Responsibilities:
    1. Read current shared state
    2. Read historical memory
    3. Decide the next tool
    4. Explain why it selected that tool
    """

    completed = state.get("completed_actions", [])

    # Read Memory
    memory = memory_manager.get_memory()

    # Keep latest memory inside GraphState (optional but useful)
    state["memory"] = memory

    # -----------------------------
    # Rule-based Planning (Temporary)
    # Later this entire section will
    # be replaced by an LLM call.
    # -----------------------------

    if "generate_itinerary" not in completed:

        state["next_action"] = "generate_itinerary"

        state["reasoning"].append(
            "Trip itinerary is required before calling other tools."
        )

        return state

    if "weather_forecaster" not in completed:

        state["next_action"] = "weather_forecaster"

        state["reasoning"].append(
            "Weather information helps improve later recommendations."
        )

        return state

    if "recommend_activities" not in completed:

        state["next_action"] = "recommend_activities"

        state["reasoning"].append(
            "Recommend activities after itinerary is available."
        )

        return state

    if "packing_list_generator" not in completed:

        state["next_action"] = "packing_list_generator"

        state["reasoning"].append(
            "Packing list depends on itinerary and weather."
        )

        return state

    if "food_culture_recommender" not in completed:

        state["next_action"] = "food_culture_recommender"

        state["reasoning"].append(
            "Recommend local food and culture information."
        )

        return state

    if "fetch_useful_links" not in completed:

        state["next_action"] = "fetch_useful_links"

        state["reasoning"].append(
            "Collect useful travel resources before finishing."
        )

        return state

    # -----------------------------
    # No more work left
    # -----------------------------

    state["next_action"] = ""

    state["is_complete"] = True

    state["reasoning"].append(
        "All required tools have been executed."
    )

    return state
