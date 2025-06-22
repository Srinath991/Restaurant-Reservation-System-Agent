import json
from src.data.restaurant_data import RestaurantDatabase

def recommend_restaurants(params):
    db = RestaurantDatabase()
    cuisine = params.get("cuisine")
    location = params.get("location")
    group_size = params.get("group_size") or params.get("people")

    restaurants = db.get_all_restaurants()
    filtered = []
    for r in restaurants:
        if cuisine and not any(cuisine.lower() in c.lower() for c in r["cuisine_type"]):
            continue
        if location and location.lower() not in r["location"].get("city", "").lower():
            continue
        if group_size and r["seating_capacity"] < int(group_size):
            continue
        filtered.append(r)
    if not filtered:
        return "No suitable restaurants found. Try changing your preferences."
    top = filtered[:5]
    return "Here are some recommendations:\n" + "\n".join([
        f'{r["name"]} ({", ".join(r["cuisine_type"])} in {r["location"].get("city", "")}, seats: {r["seating_capacity"]})'
        for r in top
    ])
