from backend.memory.memory_manager import memory_manager


AGENT_NAME = "final_response_agent"


def final_response_agent(state):
    """
    Final Response Agent.

    Combines the outputs from all specialist agents and marks the workflow complete.
    Streamlit still displays each section separately from shared state.
    """
    state.setdefault("completed_agents", [])
    state.setdefault("agent_outputs", {})
    state.setdefault("agent_logs", [])
    state.setdefault("reasoning", [])
    state.setdefault("memory", [])

    sections = []

    itinerary = state.get("itinerary", "")
    if itinerary:
        sections.append("## Travel Itinerary\n" + itinerary)

    weather_forecast = state.get("weather_forecast", "")
    if weather_forecast:
        sections.append("## Weather Forecast\n" + weather_forecast)

    activity_suggestions = state.get("activity_suggestions", "")
    if activity_suggestions:
        sections.append("## Activity Suggestions\n" + activity_suggestions)

    packing_list = state.get("packing_list", "")
    if packing_list:
        sections.append("## Packing List\n" + packing_list)

    food_culture_info = state.get("food_culture_info", "")
    if food_culture_info:
        sections.append("## Food & Culture\n" + food_culture_info)

    budget_estimate = state.get("budget_estimate", [])
    if budget_estimate:
        budget_text = "\n".join(budget_estimate)
        sections.append("## Budget Estimate\n" + budget_text)


    final_response = "\n\n".join(sections).strip()

    state["final_response"] = final_response
    state["agent_outputs"][AGENT_NAME] = {"final_response": final_response}

    if AGENT_NAME not in state["completed_agents"]:
        state["completed_agents"].append(AGENT_NAME)

    observation = {
        "agent": AGENT_NAME,
        "status": "SUCCESS",
        "output": {"final_response": final_response},
    }
    memory_manager.add_memory(tool_name=AGENT_NAME, observation=observation)
    state["memory"] = memory_manager.get_memory()
    state["last_observation"] = observation
    state["current_agent"] = ""
    state["is_complete"] = True
    state["reasoning"].append("Final Response Agent completed the multi-agent workflow.")
    state["agent_logs"].append("Final Response Agent completed")
    return state
