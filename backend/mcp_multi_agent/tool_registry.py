from backend.src_single_agent import (
    generate_itinerary,
    recommend_activities,
    weather_forecaster,
    packing_list_generator,
    food_culture_recommender,
    budget_estimate,
)

TOOLS = {

    "generate_itinerary": generate_itinerary.generate_itinerary,

    "recommend_activities": recommend_activities.recommend_activities,

    "weather_forecaster": weather_forecaster.weather_forecaster,

    "packing_list_generator": packing_list_generator.packing_list_generator,

    "food_culture_recommender": food_culture_recommender.food_culture_recommender,

    "budget_estimate": budget_estimate.estimate_budget,

}
