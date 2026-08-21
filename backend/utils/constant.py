# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

MONTHS = [
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
]

HOLIDAY_TYPES = [
    "Family",
    "Couple",
    "Solo",
    "Friends",
    "Adventure",
    "Beach",
    "Religious",
    "Festival",
    "Business",
]

BUDGET_TYPES = [
    "Budget",
    "Moderate",
    "Luxury",
]

INITIAL_STATE_DICT = {
        "preferences_text": "",
        "preferences": {},
        "itinerary": "",
        "activity_suggestions": "",
        "budget_estimate": [],
        "weather_forecast": "",
        "packing_list": "",
        "food_culture_info": "",
        "chat_history": [],
        "user_question": "",
        "chat_response": "",

        # Memory and observation fields
        "memory": [],
        "reasoning": [],
        "last_observation": {},
        "agent_logs": [],

        # Multi-agent fields
        "current_agent": "",
        "completed_agents": [],
        "agent_outputs": {},
        "final_response": "",
        "is_complete": False,

        # Old single-agent fields kept for compatibility
        "next_action": "",
        "completed_actions": [],
        "planner_confidence": 0.0,
    }
