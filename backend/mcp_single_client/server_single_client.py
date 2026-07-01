from fastmcp import FastMCP

from backend_single_agent.src.agent import run_travel_agent

mcp = FastMCP("AI Travel Planner")


@mcp.tool
def travel_planner(state: dict) -> dict:
    """
    Runs the complete LangGraph-based AI Travel Planning Agent.
    """
    return run_travel_agent(state)


if __name__ == "__main__":
    mcp.run()
