# GoodFoods Reservation Assistant

A conversational AI agent for restaurant search, recommendation, and booking, powered by Google Gemini.

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Copy `.env.example` to `.env` and add your Gemini API key:
   ```bash
   cp .env.example .env
   # Edit .env and set GEMINI_API_KEY=your_actual_key
   ```
4. Run the app:
   ```bash
   uv run streamlit run app.py
   ```

## Prompt Engineering Approach
- The agent uses Google Gemini for all intent classification, parameter extraction, and response generation.
- Prompts are designed to:
  - Extract user intent (search, recommend, book)
  - Extract relevant parameters (cuisine, location, date, etc.)
  - Generate natural, context-aware responses
- See `src/utils/llm_client.py` for prompt templates.

## Example Conversations
- **User:** I want to book a table for 4 at an Italian restaurant in Uptown tomorrow at 7pm.
- **Assistant:** Here are some Italian restaurants in Uptown: Bella Pasta, Pizza Palace, Pasta Fresca. Would you like to book at one of these?
- **User:** Book at Bella Pasta.
- **Assistant:** Table for 4 booked at Bella Pasta tomorrow at 7pm. Enjoy your meal!
- **User:** Show me vegan options in Midtown.
- **Assistant:** Here are some recommendations: Vegan Vibes, Herbivore.
- **User:** Book a table for 2 at Vegan Vibes tonight at 8pm.
- **Assistant:** Table for 2 booked at Vegan Vibes tonight at 8pm. Enjoy your meal!

## Troubleshooting
- If you see an error about missing API key, ensure `.env` is present and contains `GEMINI_API_KEY`.
- If you see a KeyError, ensure your data files are present and up to date.
- For any other issues, check the logs or contact the author.

## Business Strategy Summary
See `docs/business_strategy.md` for a detailed use case and business strategy document.

## Assumptions, Limitations, and Future Enhancements
- Assumes all bookings succeed (demo mode).
- No user authentication or payment integration.
- Future: Add real-time availability, user profiles, and feedback collection.
