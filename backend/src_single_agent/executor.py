from backend.src_single_agent import (
    generate_itinerary,
    recommend_activities,
    weather_forecaster,
    packing_list_generator,
    food_culture_recommender,
    fetch_useful_links,
)

from backend.memory.memory_manager import memory_manager


# ---------------------------------------------------
# Tool Registry
# ---------------------------------------------------

TOOLS = {
    "generate_itinerary": generate_itinerary.generate_itinerary,
    "recommend_activities": recommend_activities.recommend_activities,
    "weather_forecaster": weather_forecaster.weather_forecaster,
    "packing_list_generator": packing_list_generator.packing_list_generator,
    "food_culture_recommender": food_culture_recommender.food_culture_recommender,
    "fetch_useful_links": fetch_useful_links.fetch_useful_links,
}


# ---------------------------------------------------
# Executor Node
# ---------------------------------------------------

def executor(state):
    """
    Executor Node

    Responsibilities:
    1. Read next_action from Planner
    2. Execute the corresponding tool
    3. Store observation in Memory
    4. Update Shared State
    """

    action = state.get("next_action")

    print(f"\n========== EXECUTOR ==========")
    print(f"Executing Tool : {action}")

    # -----------------------------------------
    # Validate Tool
    # -----------------------------------------

    if action not in TOOLS:

        state["last_observation"] = f"Unknown Tool : {action}"

        state["reasoning"].append(
            f"Planner requested an invalid tool: {action}"
        )

        state["is_complete"] = True

        return state

    # -----------------------------------------
    # Execute Tool
    # -----------------------------------------

    tool = TOOLS[action]

    result = tool(state)

    # -----------------------------------------
    # Merge Tool Output
    # -----------------------------------------

    state.update(result)

    # -----------------------------------------
    # Update Completed Actions
    # -----------------------------------------

    if action not in state["completed_actions"]:
        state["completed_actions"].append(action)

    # -----------------------------------------
    # Save Observation
    # -----------------------------------------

    observation = {
        "tool": action,
        "status": "SUCCESS",
        "output": result,
    }

    memory_manager.add_memory(
        tool_name=action,
        observation=observation
    )

    # -----------------------------------------
    # Update GraphState
    # -----------------------------------------

    state["memory"] = memory_manager.get_memory()

    state["last_observation"] = observation

    print(f"{action} completed successfully.")

    return state