import json
from typing import Dict, List, Any
from src.agent.tool_router import ToolRouter
from src.utils.llm_client import GeminiClient

class ConversationHandler:
    def __init__(self):
        self.tool_router = ToolRouter()
        self.llm = GeminiClient()
        self.conversation_history = []
        
    def handle_message(self, user_message: str) -> str:
        """Process user message and return appropriate response"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Classify intent
            intent = self.llm.classify_intent(user_message)
            params = self.llm.extract_params(user_message)
            
            # Route to appropriate tool
            tool_response = self.tool_router.route(intent, params)
            
            # Generate natural language response
            response = self._generate_response(user_message, intent, tool_response)
            
            # Add to conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error. Please try rephrasing your request. ({str(e)})"
    
    def _generate_response(self, user_message: str, intent: str, tool_response: Dict) -> str:
        """Generate natural language response based on tool results"""
        system_prompt = """
        You are a helpful restaurant reservation assistant. Generate a natural, conversational response
        based on the user's message and the tool results provided.
        
        Guidelines:
        - Be friendly and helpful
        - If showing restaurant options, mention key details (cuisine, price, location)
        - If booking is successful, confirm all details
        - If there are issues, offer alternatives
        - Keep responses concise but informative
        """
        
        prompt = f"""
        User Message: {user_message}
        Intent: {intent}
        Tool Results: {json.dumps(tool_response, indent=2)}
        
        Generate a helpful response to the user.
        """
        
        return self.llm.generate_response(system_prompt, prompt)