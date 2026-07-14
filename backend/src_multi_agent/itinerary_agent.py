from backend.memory.memory_manager import memory_manager
from backend.src_single_agent import generate_itinerary


AGENT_NAME = "itinerary_agent"


def itinerary_agent(state):
    """
    Specialist Agent responsible for generating the base travel itinerary.
    """
    state.setdefault("completed_agents", [])
    state.setdefault("agent_outputs", {})
    state.setdefault("agent_logs", [])
    state.setdefault("reasoning", [])
    state.setdefault("memory", [])

    state["agent_logs"].append("Itinerary Agent started")

    try:
        result = generate_itinerary.generate_itinerary(state)
        if not isinstance(result, dict):
            result = {"itinerary": str(result)}

        state.update(result)
        state["agent_outputs"][AGENT_NAME] = result

        if AGENT_NAME not in state["completed_agents"]:
            state["completed_agents"].append(AGENT_NAME)

        observation = {
            "agent": AGENT_NAME,
            "status": "SUCCESS",
            "output": result,
        }
        memory_manager.add_memory(tool_name=AGENT_NAME, observation=observation)
        state["memory"] = memory_manager.get_memory()
        state["last_observation"] = observation
        state["agent_logs"].append("Itinerary Agent completed")
        return state

    except Exception as e:
        observation = {
            "agent": AGENT_NAME,
            "status": "FAILED",
            "error": str(e),
        }
        memory_manager.add_memory(tool_name=AGENT_NAME, observation=observation)
        state["memory"] = memory_manager.get_memory()
        state["last_observation"] = observation
        state["reasoning"].append(f"Itinerary Agent failed: {str(e)}")
        state["agent_logs"].append("Itinerary Agent failed")
        return state
