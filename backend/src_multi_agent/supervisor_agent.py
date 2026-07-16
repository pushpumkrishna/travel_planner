MULTI_AGENT_ORDER = [
    "weather_agent",
    "packing_agent",
    "itinerary_agent",
    "activity_agent",
    "food_culture_agent",
    "links_agent",
]


def supervisor_agent(state):
    """
    Supervisor Agent.

    Decides which specialist agent should run next.
    This is the coordinator in the multi-agent architecture.
    """
    state.setdefault("completed_agents", [])
    state.setdefault("agent_outputs", {})
    state.setdefault("agent_logs", [])
    state.setdefault("reasoning", [])
    state.setdefault("current_agent", "")
    state.setdefault("is_complete", False)

    completed_agents = state.get("completed_agents", [])

    for agent_name in MULTI_AGENT_ORDER:
        if agent_name not in completed_agents:
            state["current_agent"] = agent_name
            state["is_complete"] = False
            state["reasoning"].append(f"Supervisor selected {agent_name}.")
            state["agent_logs"].append(f"Supervisor routed to: {agent_name}")
            return state

    state["current_agent"] = "final_response_agent"
    state["is_complete"] = False
    state["reasoning"].append("Supervisor selected final_response_agent.")
    state["agent_logs"].append("Supervisor routed to: final_response_agent")
    return state
