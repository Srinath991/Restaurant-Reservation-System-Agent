import os
import json
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Restaurant:
    id: str
    name: str
    cuisine_type: List[str]
    location: Dict[str, str]
    price_range: str
    seating_capacity: int
    rating: float
    features: List[str]
    ambiance: str

class RestaurantDatabase:
    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), 'sample_restaurants.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                self.restaurants = [self._normalize_restaurant(r) for r in json.load(f)]
        else:
            self.restaurants = [self._normalize_restaurant(r) for r in self._generate_sample_data()]
    
    def _generate_sample_data(self) -> List[Dict]:
        """Generate 50-100 sample restaurants"""
        cuisines = [
            "Italian", "Chinese", "Mexican", "Indian", "Japanese", "Thai", 
            "American", "French", "Mediterranean", "Korean", "Vietnamese", 
            "Greek", "Spanish", "Lebanese", "Ethiopian"
        ]
        
        cities = [
            "Downtown", "Midtown", "Uptown", "Westside", "Eastside", 
            "Northshore", "Southbay", "Old Town", "Financial District", 
            "Arts District", "Little Italy", "Chinatown"
        ]
        
        features_pool = [
            "outdoor_seating", "parking", "wheelchair_accessible", "kids_friendly", 
            "romantic", "live_music", "bar", "private_dining", "delivery", 
            "takeout", "brunch", "late_night", "rooftop", "waterfront"
        ]
        
        restaurants = []
        
        for i in range(75):  # Generate 75 restaurants
            restaurant = {
                "id": f"rest_{i+1:03d}",
                "name": self._generate_restaurant_name(cuisines),
                "cuisine_type": random.sample(cuisines, random.randint(1, 2)),
                "location": {
                    "address": f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Park Blvd', 'First St'])}",
                    "city": random.choice(cities),
                    "coordinates": [
                        round(random.uniform(37.7, 37.8), 6),  # SF-like coordinates
                        round(random.uniform(-122.5, -122.4), 6)
                    ]
                },
                "price_range": random.choice(["$", "$$", "$$$", "$$$$"]),
                "seating_capacity": random.randint(30, 200),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "features": random.sample(features_pool, random.randint(3, 6)),
                "ambiance": random.choice(["casual", "fine_dining", "family_friendly", "romantic", "trendy"])
            }
            restaurants.append(restaurant)
        
        return restaurants
    
    def _generate_restaurant_name(self, cuisines: List[str]) -> str:
        """Generate realistic restaurant names"""
        prefixes = ["The", "Chez", "Casa", "Little", "Golden", "Royal", "Blue", "Red"]
        suffixes = ["Bistro", "Kitchen", "Grill", "House", "Garden", "Corner", "Table", "Place"]
        
        if random.random() > 0.5:
            return f"{random.choice(prefixes)} {random.choice(suffixes)}"
        else:
            return f"{random.choice(['Mario', 'Giuseppe', 'Chen', 'Sakura', 'Taj', 'Elena'])}s {random.choice(suffixes)}"
    
    def search_restaurants(
        self,
        cuisine: Optional[List[str]] = None,
        location: Optional[str] = None,
        party_size: Optional[int] = None,
        price_range: Optional[str] = None,
        features: Optional[List[str]] = None
    ) -> List[Dict]:
        """Search restaurants with filters"""
        filtered = self.restaurants.copy()
        
        if cuisine:
            filtered = [r for r in filtered if any(c in r['cuisine_type'] for c in cuisine)]
        
        if location:
            filtered = [r for r in filtered if location.lower() in r['location']['city'].lower()]
        
        if price_range:
            filtered = [r for r in filtered if r['price_range'] == price_range]
        
        if features:
            filtered = [r for r in filtered if any(f in r['features'] for f in features)]
        
        if party_size:
            filtered = [r for r in filtered if r['seating_capacity'] >= party_size]
        
        # Sort by rating
        filtered.sort(key=lambda x: x['rating'], reverse=True)
        
        return filtered
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Optional[Dict]:
        """Get restaurant by ID"""
        for restaurant in self.restaurants:
            if restaurant['id'] == restaurant_id:
                return restaurant
        return None
    
    def get_all_restaurants(self) -> List[Dict]:
        """Get all restaurants"""
        return self.restaurants

    def find_restaurant_by_name(self, name: str) -> Optional[Dict]:
        """Find a restaurant by its name (case-insensitive)"""
        for restaurant in self.restaurants:
            if restaurant["name"].lower() == name.lower():
                return restaurant
        return None

    def _normalize_restaurant(self, r):
        # Normalize both formats to a common schema
        return {
            "id": r.get("id", r.get("name", "")[:8]),
            "name": r.get("name"),
            "cuisine_type": r.get("cuisine_type") or ([r["cuisine"]] if r.get("cuisine") else []),
            "location": r.get("location") if isinstance(r.get("location"), dict) else {"city": r.get("location", "")},
            "price_range": r.get("price_range", "$$"),
            "seating_capacity": r.get("seating_capacity") or r.get("capacity", 0),
            "rating": r.get("rating", 4.0),
            "features": r.get("features", []),
            "ambiance": r.get("ambiance", "casual")
        }
