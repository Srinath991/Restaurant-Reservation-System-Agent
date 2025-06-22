from src.data.restaurant_data import RestaurantDatabase
from datetime import datetime
import random

# In-memory booking store for demo (could be replaced with DB/file)
bookings = []

def get_restaurant_info(name):
    db = RestaurantDatabase()
    restaurant = db.find_restaurant_by_name(name)
    if not restaurant:
        return f"Sorry, I couldn't find information for '{name}'."
    info = []
    info.append(f"**{restaurant.get('name', 'N/A')}**")
    cuisine = ', '.join(restaurant.get('cuisine_type', [])) if restaurant.get('cuisine_type') else restaurant.get('cuisine', 'N/A')
    info.append(f"Cuisine: {cuisine}")
    location = restaurant.get('location', {})
    if isinstance(location, dict):
        address = location.get('address', 'N/A')
        city = location.get('city', 'N/A')
    else:
        address = 'N/A'
        city = location
    info.append(f"Location: {address}, {city}")
    info.append(f"Seating Capacity: {restaurant.get('seating_capacity', restaurant.get('capacity', 'N/A'))}")
    info.append(f"Price Range: {restaurant.get('price_range', 'N/A')}")
    info.append(f"Rating: {restaurant.get('rating', 'N/A')}")
    features = ', '.join(restaurant.get('features', []))
    if features:
        info.append(f"Features: {features}")
    info.append(f"Ambiance: {restaurant.get('ambiance', 'N/A')}")
    return '\n'.join(info)

def list_restaurants_by_cuisine(cuisine):
    db = RestaurantDatabase()
    matches = [r for r in db.get_all_restaurants() if cuisine.lower() in ','.join([c.lower() for c in (r.get('cuisine_type', []) or [r.get('cuisine','')])])]
    if not matches:
        return f"No restaurants found for cuisine: {cuisine}."
    return '\n'.join([f"{r['name']} ({r.get('location', {}).get('city', r.get('location', ''))})" for r in matches])

def list_restaurants_by_location(location):
    db = RestaurantDatabase()
    matches = [r for r in db.get_all_restaurants() if location.lower() in (r.get('location', {}).get('city', r.get('location', ''))).lower()]
    if not matches:
        return f"No restaurants found in {location}."
    return '\n'.join([f"{r['name']} ({', '.join(r.get('cuisine_type', [])) if r.get('cuisine_type') else r.get('cuisine', '')})" for r in matches])

def book_table(params):
    db = RestaurantDatabase()
    name = params.get("name")
    date = params.get("date")
    time = params.get("time")
    people = int(params.get("people", 2))
    
    restaurant = next((r for r in db.get_all_restaurants() if r["name"].lower() == (name or "").lower()), None)
    if not restaurant:
        return f"Restaurant '{name}' not found."
    # For demo, assume all bookings succeed
    return f"Table for {people} booked at {restaurant['name']} on {date} at {time}. Enjoy your meal!"
