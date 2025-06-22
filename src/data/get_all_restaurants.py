from src.data.restaurant_data import RestaurantDatabase

def get_all_restaurants():
    db = RestaurantDatabase()
    return db.get_all_restaurants()
