
from backend.memory.memory_manager import memory_manager
from backend.mcp_multi_agent.tool_registry import TOOLS
from backend.mcp_multi_agent.client_mcp import mcp_client

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
    result = mcp_client.execute(
            action,
            state,
        )

    # -----------------------------------------
    # Merge Tool Output
    # -----------------------------------------

    tool_output = result.content[0].text

    print(tool_output)

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
