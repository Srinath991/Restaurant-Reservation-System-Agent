from src.tools.restaurant_search import search_restaurants
from src.tools.recommendation_engine import recommend_restaurants
from src.tools.booking_manager import book_table
from src.utils.llm_client import GeminiClient

class ToolRouter:
    def __init__(self):
        self.llm = GeminiClient()

    def route(self, intent, params):
        if intent == "search_restaurant":
            return search_restaurants(params)
        elif intent == "recommend_restaurant":
            return recommend_restaurants(params)
        elif intent == "book_table":
            return book_table(params)
        else:
            return "Sorry, I didn't understand your request. Can you rephrase?"
