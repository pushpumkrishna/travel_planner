import streamlit as st
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
# from langchain_core.messages import HumanMessage
# from langchain_ollama import ChatOllama
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from backend.src_single_agent import (
    planner,
    chat_agent,
)
import google.generativeai as genai
from backend.memory.memory_manager import memory_manager
from backend.utils.util import export_to_pdf
from backend.src_single_agent import executor
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Initialize LLM
st.set_page_config(page_title="AI Travel Planner", layout="wide")
try:
    # llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    print(llm)
except Exception as e:
    st.error(f"LLM initialization failed: {str(e)}")
    st.stop()


key = "AQ.Ab8RN6JwGuXFn5HYQj1C0ijm4Lx6C8ifI__HUl0tYJyxDZTbiQ"


# 1. Provide your VIP pass (API Key)
genai.configure(api_key=key)

# Initialize GoogleSerperAPIWrapper
try:
    search = GoogleSerperAPIWrapper()
except Exception as e:
    st.error(f"Serper API initialization failed: {str(e)}")
    st.stop()


class ChatMessage(TypedDict):
    question: str
    response: str


# Define state
class GraphState(TypedDict):
    preferences_text: str
    preferences: dict
    itinerary: str
    activity_suggestions: str
    useful_links: list[dict]
    weather_forecast: str
    packing_list: str
    food_culture_info: str
    # chat_history: Annotated[list[dict], "List of question-response pairs"]
    chat_history: list[ChatMessage]
    user_question: str
    chat_response: str

    # -------- ReAct Fields --------
    memory: list
    next_action: str
    last_observation: dict
    reasoning: list[str]
    completed_actions: list[str]
    planner_confidence: float
    is_complete: bool
    agent_logs: list[str]


# ------------------- LangGraph -------------------
workflow = StateGraph(GraphState)
workflow.add_node("planner", planner.planner)
workflow.add_node("executor", executor.executor)
workflow.add_node("chat", chat_agent.chat_node)
workflow.set_entry_point("planner")


def planner_router(state):
    if state["is_complete"]:
        return END

    return "executor"


# Connect Planner to Executor
workflow.add_conditional_edges("planner", planner_router)
workflow.add_edge("executor", "planner")
workflow.add_edge("chat", END)
graph = workflow.compile()

# ------------------- UI -------------------
st.markdown("# AI-Powered Travel Itinerary Planner")

if "state" not in st.session_state:
    st.session_state.state = {
        "memory": [],
        "next_action": "",
        "last_observation": {},
        "reasoning": [],
        "completed_actions": [],
        "planner_confidence": 1.0,
        "is_complete": False,
        "agent_logs": [],
    }

with st.form("travel_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination")
        month = st.selectbox(
            "Month of Travel",
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
        )
        duration = st.slider("Number of Days", 1, 30, 7)
        num_people = st.selectbox(
            "Number of People", ["1", "2", "3", "4-6", "7-10", "10+"]
        )
    with col2:
        holiday_type = st.selectbox(
            "Holiday Type",
            [
                "Any",
                "Party",
                "Skiing",
                "Backpacking",
                "Family",
                "Beach",
                "Festival",
                "Adventure",
                "City Break",
                "Romantic",
                "Cruise",
            ],
        )
        budget_type = st.selectbox(
            "Budget Type", ["Budget", "Mid-Range", "Luxury", "Backpacker", "Family"]
        )
        comments = st.text_area("Additional Comments")
    submit_btn = st.form_submit_button("Generate Itinerary")

if submit_btn:
    # Clear previous trip memory
    memory_manager.clear()

    preferences_text = (f"Destination: {destination}\nMonth: {month}\nDuration: {duration} days\n"
                        f"People: {num_people}\nType: {holiday_type}\nBudget: {budget_type}\nComments: {comments}")
    preferences = {
        "destination": destination,
        "month": month,
        "duration": duration,
        "num_people": num_people,
        "holiday_type": holiday_type,
        "budget_type": budget_type,
        "comments": comments,
    }

    st.session_state.state.update(
        {
            "preferences_text": preferences_text,
            "preferences": preferences,
            # Existing fields
            "itinerary": "",
            "activity_suggestions": "",
            "useful_links": [],
            "weather_forecast": "",
            "packing_list": "",
            "food_culture_info": "",
            "chat_history": [],
            "user_question": "",
            "chat_response": "",
            # Agent State
            "memory": [],
            "next_action": "",
            "last_observation": {},
            "reasoning": [],
            "completed_actions": [],
            "planner_confidence": 1.0,
            "is_complete": False,
        }
    )

    with st.spinner("Generating itinerary..."):
        result = graph.invoke(st.session_state.state)
        st.session_state.state.update(result)

        if result.get("itinerary"):
            st.success("Itinerary Created")
        else:
            st.error("Failed to generate itinerary.")

# Layout
if st.session_state.state.get("itinerary"):
    col_itin, col_chat = st.columns([3, 2])

    with col_itin:
        st.markdown("### Travel Itinerary")
        st.markdown(st.session_state.state["itinerary"])

    # Export PDF button
    if st.button("Export as PDF"):
        pdf_path = export_to_pdf(st.session_state.state["itinerary"])
        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download Itinerary PDF", f, file_name="itinerary.pdf"
                )

    with col_chat:
        st.markdown("### Chat About Your Itinerary")
        for chat in st.session_state.state["chat_history"]:
            with st.chat_message("user"):
                st.markdown(chat["question"])
            with st.chat_message("assistant"):
                st.markdown(chat["response"])

        if user_input := st.chat_input("Ask something about your itinerary"):
            st.session_state.state["user_question"] = user_input
            with st.spinner("Generating response..."):
                result = chat_agent.chat_node(st.session_state.state)
                st.session_state.state.update(result)
                st.rerun()
else:
    st.info("Fill the form and generate an itinerary to begin.")
