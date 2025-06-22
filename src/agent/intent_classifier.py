import json
from typing import Dict, List
from src.utils.llm_client import LLMClient

class IntentClassifier:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        
    def classify_intent(self, user_message: str, conversation_history: List[Dict]) -> Dict:
        """Classify user intent using LLM"""
        system_prompt = """
        You are an intent classifier for a restaurant reservation system. 
        Analyze the user's message and classify their intent.
        
        Available intents:
        - search_restaurants: User wants to find restaurants
        - make_reservation: User wants to book a table
        - modify_reservation: User wants to change existing booking
        - cancel_reservation: User wants to cancel booking
        - get_recommendations: User needs suggestions/recommendations
        - get_info: User asks for restaurant details
        - greeting: User is greeting or starting conversation
        - other: Intent doesn't match above categories
        
        Extract relevant entities:
        - date: When they want to dine
        - time: Preferred time
        - party_size: Number of people
        - cuisine: Type of food preference
        - location: Area/neighborhood preference
        - price_range: Budget considerations
        - special_requirements: Dietary restrictions, accessibility needs
        
        Return JSON format:
        {
            "intent": "intent_name",
            "confidence": 0.95,
            "entities": {
                "date": "2024-12-25",
                "time": "19:00",
                "party_size": 4,
                "cuisine": ["Italian", "Mediterranean"],
                "location": "downtown",
                "price_range": "$$",
                "special_requirements": ["vegetarian_options"]
            }
        }
        """
        
        context = f"Conversation history: {json.dumps(conversation_history[-3:])}\n"
        prompt = f"{context}Current message: {user_message}\n\nClassify this intent and extract entities:"
        
        response = self.llm_client.generate_response(system_prompt, prompt)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "intent": "other",
                "confidence": 0.5,
                "entities": {}
            }