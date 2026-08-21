from backend_single_agent.src import (
    generate_itinerary,
    recommend_activities,
    weather_forecaster,
    packing_list_generator,
    food_culture_recommender,
    fetch_useful_links,
)

TOOLS = {

    "generate_itinerary": generate_itinerary.generate_itinerary,

    "recommend_activities": recommend_activities.recommend_activities,

    "weather_forecaster": weather_forecaster.weather_forecaster,

    "packing_list_generator": packing_list_generator.packing_list_generator,

    "food_culture_recommender": food_culture_recommender.food_culture_recommender,

    "fetch_useful_links": fetch_useful_links.fetch_useful_links,

}
