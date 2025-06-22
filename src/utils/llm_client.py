import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def classify_intent(self, message):
        prompt = f"""
        Classify the user's intent from the following message. Choose one of: search_restaurant, recommend_restaurant, book_table.
        Message: {message}
        Intent:
        """
        response = self.model.generate_content(prompt)
        return response.text.strip().split("\n")[0]

    def extract_params(self, message):
        prompt = f"""
        Extract relevant parameters (name, cuisine, location, date, time, people, group_size) from the following message as a JSON object.
        Message: {message}
        JSON:
        """
        response = self.model.generate_content(prompt)
        import json
        try:
            return json.loads(response.text.strip().split("\n")[0])
        except Exception:
            return {}

    def generate_response(self, system_prompt, user_prompt):
        prompt = f"""
        {system_prompt}
        {user_prompt}
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()