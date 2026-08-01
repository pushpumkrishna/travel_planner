from backend.memory.memory_manager import memory_manager
from backend.src_single_agent import fetch_useful_links


AGENT_NAME = "links_agent"


def links_agent(state):
    """
    Specialist Agent responsible for fetching useful travel links.
    """
    state.setdefault("completed_agents", [])
    state.setdefault("agent_outputs", {})
    state.setdefault("agent_logs", [])
    state.setdefault("reasoning", [])
    state.setdefault("memory", [])

    state["agent_logs"].append("Links Agent started")

    try:
        print("Links agent started")

        result = fetch_useful_links.fetch_useful_links(state)

        print("Links result:", result)

        if not isinstance(result, dict):
            result = {"useful_links": result}

        state.update(result)

        print("Adding links_agent completed")

        if AGENT_NAME not in state["completed_agents"]:
            state["completed_agents"].append(AGENT_NAME)

        print("Completed agents:", state["completed_agents"])

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
        state["reasoning"].append(f"Links Agent failed: {str(e)}")
        state["agent_logs"].append("Links Agent failed")
        return state
