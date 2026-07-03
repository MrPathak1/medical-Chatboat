from chat import get_bot_response

print("Welcome to the Medical Chatbot. Type 'exit' to end.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: Take care! 😊")
        break
    response = get_bot_response(user_input)
    print(f"Bot: {response}")
