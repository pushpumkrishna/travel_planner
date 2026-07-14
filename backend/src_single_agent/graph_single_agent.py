from typing import TypedDict
from langgraph.graph import StateGraph, END
from backend.src_single_agent import planner_LLM, executor, chat_agent


class ChatMessage(TypedDict):
    question: str
    response: str


class GraphState(TypedDict, total=False):
    preferences_text: str
    preferences: dict
    itinerary: str
    activity_suggestions: str
    useful_links: list[dict]
    weather_forecast: str
    packing_list: str
    food_culture_info: str
    chat_history: list[ChatMessage]
    user_question: str
    chat_response: str

    memory: list
    next_action: str
    last_observation: dict
    reasoning: list[str]
    completed_actions: list[str]
    planner_confidence: float
    is_complete: bool
    agent_logs: list[str]


def planner_router(state: GraphState):
    if state.get("is_complete", False):
        return END
    return "executor"


workflow = StateGraph(GraphState)
workflow.add_node("planner", planner_LLM.planner)
workflow.add_node("executor", executor.executor)
workflow.add_node("chat", chat_agent.chat_node)

workflow.set_entry_point("planner")
workflow.add_conditional_edges("planner", planner_router)
workflow.add_edge("executor", "planner")
workflow.add_edge("chat", END)

graph = workflow.compile()
