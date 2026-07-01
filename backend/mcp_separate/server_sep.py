"""
FastMCP Server
--------------

This server exposes all Travel Planner tools through
the Model Context Protocol (MCP).

Run:
    python backend/mcp_single_client/server.py
"""

from mcp.server.fastmcp import FastMCP

from backend_single_agent.src import (
    generate_itinerary,
    recommend_activities,
    fetch_useful_links,
    weather_forecaster,
    packing_list_generator,
    food_culture_recommender,
)

# ---------------------------------------------------
# Create MCP Server
# ---------------------------------------------------

mcp = FastMCP("AI Travel Planner")


# ---------------------------------------------------
# Generate Itinerary
# ---------------------------------------------------

@mcp.tool(name="generate_itinerary")
def generate_itinerary_tool(state: dict) -> dict:
    """
    Generate travel itinerary.
    """
    return generate_itinerary.generate_itinerary(state)


# ---------------------------------------------------
# Weather Forecast
# ---------------------------------------------------

@mcp.tool(name="weather_forecaster")
def weather_forecaster_tool(state: dict) -> dict:
    """
    Generate destination weather forecast.
    """
    return weather_forecaster.weather_forecaster(state)


# ---------------------------------------------------
# Activity Suggestions
# ---------------------------------------------------

@mcp.tool(name="recommend_activities")
def recommend_activities_tool(state: dict) -> dict:
    """
    Recommend tourist activities.
    """
    return recommend_activities.recommend_activities(state)


# ---------------------------------------------------
# Packing List
# ---------------------------------------------------

@mcp.tool(name="packing_list_generator")
def packing_list_generator_tool(state: dict) -> dict:
    """
    Generate the packing list.
    """
    return packing_list_generator.packing_list_generator(state)


# ---------------------------------------------------
# Food & Culture
# ---------------------------------------------------

@mcp.tool(name="food_culture_recommender")
def food_culture_recommender_tool(state: dict) -> dict:
    """
    Recommend food and cultural experiences.
    """
    return food_culture_recommender.food_culture_recommender(state)


# ---------------------------------------------------
# Useful Links
# ---------------------------------------------------

@mcp.tool(name="fetch_useful_links")
def fetch_useful_links_tool(state: dict) -> dict:
    """
    Fetch useful travel links.
    """
    return fetch_useful_links.fetch_useful_links(state)


# ---------------------------------------------------
# Start MCP Server
# ---------------------------------------------------

if __name__ == "__main__":
    mcp.run()
