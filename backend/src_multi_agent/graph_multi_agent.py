from typing import TypedDict
from langgraph.graph import StateGraph, END
from backend.src_multi_agent import (
    budget_agent,
    supervisor_agent,
    itinerary_agent,
    weather_agent,
    activity_agent,
    packing_agent,
    food_culture_agent,
    final_response_agent,
)


class ChatMessage(TypedDict):
    question: str
    response: str


class GraphState(TypedDict, total=False):
    preferences_text: str
    preferences: dict
    itinerary: str
    activity_suggestions: str
    budget_estimate: str
    weather_forecast: str
    packing_list: str
    food_culture_info: str
    chat_history: list[ChatMessage]
    user_question: str
    chat_response: str

    memory: list
    reasoning: list[str]
    last_observation: dict
    agent_logs: list[str]

    # Multi-agent fields
    current_agent: str
    completed_agents: list[str]
    agent_outputs: dict
    final_response: str
    is_complete: bool

    # Backward-compatible fields from the single-agent version
    next_action: str
    completed_actions: list[str]
    planner_confidence: float


def supervisor_router(state: GraphState):

    completed_agents = state.get(
        "completed_agents",
        []
    )

    current_agent = state.get(
        "current_agent",
        ""
    )

    print("Current Agent:", current_agent)
    print("Completed Agents:", completed_agents)

    # Do not run an agent again if it is already completed
    if current_agent in completed_agents:
        if len(completed_agents) == 6:
            return "final_response_agent"                                                    
        return END

    if current_agent == "itinerary_agent":
        return "itinerary_agent"

    if current_agent == "weather_agent":
        return "weather_agent"

    if current_agent == "activity_agent":
        return "activity_agent"

    if current_agent == "packing_agent":
        return "packing_agent"

    if current_agent == "food_culture_agent":
        return "food_culture_agent"

    if current_agent == "budget_agent":
        return "budget_agent"

    if current_agent == "final_response_agent":
        return "final_response_agent"

    return END

workflow = StateGraph(GraphState)

workflow.add_node("supervisor", supervisor_agent.supervisor_agent)
workflow.add_node("itinerary_agent", itinerary_agent.itinerary_agent)
workflow.add_node("weather_agent", weather_agent.weather_agent)
workflow.add_node("activity_agent", activity_agent.activity_agent)
workflow.add_node("packing_agent", packing_agent.packing_agent)
workflow.add_node("food_culture_agent", food_culture_agent.food_culture_agent)
workflow.add_node("budget_agent", budget_agent.budget_agent)
workflow.add_node("final_response_agent", final_response_agent.final_response_agent)

workflow.set_entry_point("supervisor")
workflow.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "itinerary_agent": "itinerary_agent",
        "weather_agent": "weather_agent",
        "activity_agent": "activity_agent",
        "packing_agent": "packing_agent",
        "food_culture_agent": "food_culture_agent",
        "budget_agent": "budget_agent",
        "final_response_agent": "final_response_agent",
        END: END,
    },
)

workflow.add_edge("itinerary_agent", "supervisor")
workflow.add_edge("weather_agent", "supervisor")
workflow.add_edge("activity_agent", "supervisor")
workflow.add_edge("packing_agent", "supervisor")
workflow.add_edge("food_culture_agent", "supervisor")
workflow.add_edge("budget_agent", "supervisor")
workflow.add_edge("final_response_agent", END)

graph = workflow.compile()
