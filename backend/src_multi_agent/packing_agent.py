from backend.memory.memory_manager import memory_manager
from backend.src_single_agent import packing_list_generator


AGENT_NAME = "packing_agent"


def packing_agent(state):
    """
    Specialist Agent responsible for generating a packing list.
    It can use itinerary and weather already present in shared state.
    """
    state.setdefault("completed_agents", [])
    state.setdefault("agent_outputs", {})
    state.setdefault("agent_logs", [])
    state.setdefault("reasoning", [])
    state.setdefault("memory", [])

    state["agent_logs"].append("Packing Agent started")

    try:
        result = packing_list_generator.packing_list_generator(state)
        if not isinstance(result, dict):
            result = {"packing_list": str(result)}

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
        state["agent_logs"].append("Packing Agent completed")
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
        state["reasoning"].append(f"Packing Agent failed: {str(e)}")
        state["agent_logs"].append("Packing Agent failed")
        return state
