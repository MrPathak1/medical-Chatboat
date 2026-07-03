import unittest
from chat import get_bot_response

class TestChatBot(unittest.TestCase):
    def test_greeting_response(self):
        user_input = "hi"
        response = get_bot_response(user_input)
        expected_responses = [
            "Hello! How can I assist you with your health today?",
            "I'm not sure how to respond to that. Can you tell me more or ask about health topics?"
        ]
        self.assertIn(response, expected_responses)

if __name__ == "__main__":
    unittest.main()
