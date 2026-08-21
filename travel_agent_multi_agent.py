import os
from copy import deepcopy
import streamlit as st
from dotenv import load_dotenv
from backend.src_multi_agent.graph_multi_agent import graph
from backend.utils.constant import *
# from backend.utils.util import export_to_pdf


load_dotenv()
st.set_page_config(
    page_title="Multi-Agent AI Travel Planner",
    page_icon="✈️",
    layout="wide",
)


def create_initial_state():
    return deepcopy(INITIAL_STATE_DICT)


def normalize_multi_agent_state(state):
    """
    Ensures UI fields are available at top level.
    Sometimes multi-agent outputs are inside agent_outputs.
    """

    agent_outputs = state.get("agent_outputs", {})

    mapping = {
        "itinerary_agent": "itinerary",
        "weather_agent": "weather_forecast",
        "activity_agent": "activity_suggestions",
        "packing_agent": "packing_list",
        "food_culture_agent": "food_culture_info",
        "budget_agent": "budget_estimate",
        "final_response_agent": "final_response",
    }

    for agent_name, state_key in mapping.items():
        agent_result = agent_outputs.get(agent_name, {})

        if isinstance(agent_result, dict):
            if not state.get(state_key) and agent_result.get(state_key):
                state[state_key] = agent_result[state_key]

    return state


if "travel_state" not in st.session_state:
    st.session_state.travel_state = create_initial_state()


st.title("✈️ Multi-Agent AI Travel Planner")


with st.form("travel_form"):

    col1, col2 = st.columns(2)

    with col1:

        destination = st.text_input(
            "Destination"
        )

        month = st.selectbox(
            "Travel Month",
            MONTHS,
        )

        duration = st.number_input(
            "Trip Duration (days)",
            min_value=1,
            value=5,
        )

        num_people = st.number_input(
            "Number of Travellers",
            min_value=1,
            value=2,
        )

    with col2:

        holiday_type = st.selectbox(
            "Holiday Type",
            HOLIDAY_TYPES,
        )

        budget_type = st.selectbox(
            "Budget Type",
            BUDGET_TYPES,
        )

        comments = st.text_area(
            "Additional Preferences"
        )

    submit_button = st.form_submit_button(
        "Generate Travel Plan"
    )


if submit_button:

    if not destination.strip():

        st.warning(
            "Please enter a destination."
        )

    else:

        preferences = {
            "destination": destination.strip(),
            "month": month,
            "duration": int(duration),
            "num_people": int(num_people),
            "holiday_type": holiday_type,
            "budget_type": budget_type,
            "comments": comments.strip(),
        }

        state = create_initial_state()

        state["preferences"] = preferences

        state["preferences_text"] = (
            f"Destination: {destination.strip()}\n"
            f"Month: {month}\n"
            f"Duration: {duration} days\n"
            f"Number of travellers: {num_people}\n"
            f"Holiday type: {holiday_type}\n"
            f"Budget type: {budget_type}\n"
            f"Additional preferences: {comments}"
        )

        try:
            with st.spinner(
                "Generating your travel plan..."
            ):
                result = graph.invoke(
                    state,
                )

            result = normalize_multi_agent_state(result)
            st.session_state.travel_state = result

            st.success(
                "Travel plan generated successfully."
            )

        except Exception as error:

            st.error(
                f"Travel plan generation failed: {error}"
            )


state = st.session_state.travel_state

with st.expander("Debug State"):
    st.json(state)


if state.get("itinerary"):

    st.header("Travel Plan: ")

    st.subheader("Travel Itinerary:")

    st.markdown(
        state["itinerary"]
    )


if state.get("weather_forecast"):

    st.subheader("🌤️ Weather Forecast:")

    st.markdown(
        state["weather_forecast"]
    )


if state.get("activity_suggestions"):

    st.subheader("🎯 Activity Suggestions:")

    st.markdown(
        state["activity_suggestions"]
    )


if state.get("budget_estimate"):

    st.subheader("� Budget Estimate:")

    st.markdown(
            state["budget_estimate"]
        )

if state.get("packing_list"):

    st.subheader("🎒 Packing List:")

    st.markdown(
        state["packing_list"]
    )


if state.get("food_culture_info"):

    st.subheader("🍽️ Food & Culture:")

    st.markdown(
        state["food_culture_info"]
    )




# if state.get("final_response"):
#
#     st.header("Final Travel Plan")
#     st.markdown(state["final_response"])
#
#     pdf_path = export_to_pdf(
#         state["final_response"]
#     )
#
#     with open(pdf_path, "rb") as pdf_file:
#
#         pdf_data = pdf_file.read()
#
#     st.download_button(
#         label="Download Travel Plan as PDF",
#         data=pdf_data,
#         file_name="travel_plan.pdf",
#         mime="application/pdf",
#     )

    # os.remove(pdf_path)
