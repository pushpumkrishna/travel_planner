import json
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from backend_single_agent.memory.memory_manager import memory_manager
from backend_single_agent.src.executor import TOOLS


llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434"
)

parser = JsonOutputParser()


def planner(state):
    """
    Planner Node

    Responsibilities
    ----------------
    1. Read current shared state
    2. Read memory
    3. Decide the next tool
    4. Return reasoning
    """

    memory = memory_manager.get_memory()

    completed = state.get("completed_actions", [])

    available_tools = [
        tool
        for tool in TOOLS.keys()
        if tool not in completed
    ]

    prompt = f"""
You are an AI Travel Planning Agent.

Your responsibility is to decide ONLY ONE next action.

Current User Request
--------------------
{state["preferences_text"]}

Completed Actions
-----------------
{completed}

Previous Observation
--------------------
{state.get("last_observation")}

Relevant Memory
---------------
{memory}

Available Tools
---------------
{available_tools}

Instructions
------------
- Think step by step.
- Execute ONLY ONE tool.
- Never repeat completed tools.
- If all required work is complete,
  set is_complete=true.
- Return JSON only.

Output Format

{{
    "reason":"...",
    "next_action":"...",
    "confidence":0.95,
    "is_complete":false
}}

"""

    try:

        response = llm.invoke(prompt)

        plan = parser.parse(response.content)

        state["reasoning"].append(
            plan["reason"]
        )

        state["next_action"] = plan.get(
            "next_action",
            ""
        )

        state["planner_confidence"] = plan.get(
            "confidence",
            1.0
        )

        state["is_complete"] = plan.get(
            "is_complete",
            False
        )

    except Exception as e:

        state["reasoning"].append(
            f"Planner Error : {str(e)}"
        )

        state["is_complete"] = True

    return state
