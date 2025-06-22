import streamlit as st
import json
from datetime import datetime, timedelta
from src.agent.conversation_handler import ConversationHandler
from src.data.restaurant_data import RestaurantDatabase

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_handler" not in st.session_state:
        st.session_state.conversation_handler = ConversationHandler()
    if "restaurant_db" not in st.session_state:
        st.session_state.restaurant_db = RestaurantDatabase()

def main():
    st.set_page_config(
        page_title="GoodFoods Reservation Assistant",
        page_icon="🍽️",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("🍽️ GoodFoods Reservation Assistant")
    st.markdown("Find and book the perfect dining experience across our restaurant network!")
    
    # Sidebar with restaurant stats
    with st.sidebar:
        st.header("📊 Quick Stats")
        total_restaurants = len(st.session_state.restaurant_db.get_all_restaurants())
        st.metric("Total Locations", total_restaurants)
        st.metric("Cities Covered", "12")
        st.metric("Cuisine Types", "15+")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("How can I help you with your dining plans?"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("Finding the best options for you..."):
                    response = st.session_state.conversation_handler.handle_message(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()