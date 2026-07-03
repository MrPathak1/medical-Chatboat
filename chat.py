# chat.py
import json
import random

try:
    with open("conversations.json", "r") as f:
        conversation_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading conversation data: {e}")
    conversation_data = []

def get_bot_response(user_input):
    user_input = user_input.lower().strip()
    # Improved matching: check if user input is substring of any user phrase or vice versa
    matches = [pair for pair in conversation_data if user_input in pair["user"].lower() or pair["user"].lower() in user_input]
    if matches:
        return random.choice(matches)["bot"]
    return "I'm not sure how to respond to that. Can you tell me more or ask about health topics?"
