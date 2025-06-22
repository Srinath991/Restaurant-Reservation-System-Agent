from typing import List, Dict, Optional
from datetime import datetime
from src.data.restaurant_data import RestaurantDatabase

class RestaurantSearchTool:
    def __init__(self):
        self.db = RestaurantDatabase()
    
    def search_restaurants(
        self,
        cuisine: Optional[List[str]] = None,
        location: Optional[str] = None,
        date: Optional[str] = None,
        party_size: Optional[int] = None,
        price_range: Optional[str] = None,
        features: Optional[List[str]] = None
    ) -> Dict:
        """Search restaurants based on criteria"""
        try:
            restaurants = self.db.search_restaurants(
                cuisine=cuisine,
                location=location,
                party_size=party_size,
                price_range=price_range,
                features=features
            )
            
            # Filter by availability if date provided
            if date and restaurants:
                available_restaurants = []
                for restaurant in restaurants:
                    if self._check_availability(restaurant['id'], date, party_size):
                        available_restaurants.append(restaurant)
                restaurants = available_restaurants
            
            return {
                "success": True,
                "restaurants": restaurants[:10],  # Limit to top 10
                "total_found": len(restaurants)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "restaurants": []
            }
    
    def _check_availability(self, restaurant_id: str, date: str, party_size: int) -> bool:
        """Check if restaurant has availability (simplified logic)"""
        # In real implementation, this would check actual booking database
        # For demo, we'll assume 80% availability
        import random
        return random.random() > 0.2

def search_restaurants(params):
    db = RestaurantDatabase()
    cuisine = params.get("cuisine")
    location = params.get("location")
    party_size = params.get("party_size") or params.get("people")
    
    restaurants = db.get_all_restaurants()
    filtered = []
    for r in restaurants:
        if cuisine and not any(cuisine.lower() in c.lower() for c in r["cuisine_type"]):
            continue
        if location and location.lower() not in r["location"].get("city", "").lower():
            continue
        if party_size and r["seating_capacity"] < int(party_size):
            continue
        filtered.append(r)
    if not filtered:
        return "No restaurants found matching your criteria."
    top = filtered[:10]
    return "Found these restaurants:\n" + "\n".join([f'{r["name"]} ({", ".join(r["cuisine_type"])} in {r["location"].get("city", "")}, seats: {r["seating_capacity"]})' for r in top])