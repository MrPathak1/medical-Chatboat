import unittest
from unittest.mock import patch, MagicMock
import main

class TestChatbot(unittest.TestCase):
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.get_user_location')
    def test_location_command(self, mock_get_location, mock_print, mock_input):
        mock_get_location.return_value = [12.34, 56.78]
        mock_input.side_effect = ["location", "exit"]
        main.chatbot()
        mock_print.assert_any_call("📍 Your location is approximately: [12.34, 56.78]")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.get_user_location')
    @patch('main.find_nearby_places')
    def test_medical_store_command(self, mock_find_stores, mock_get_location, mock_print, mock_input):
        mock_get_location.return_value = [12.34, 56.78]
        mock_find_stores.return_value = [{'name': 'Store1', 'address': 'Address1'}]
        mock_input.side_effect = ["medical store", "exit"]
        main.chatbot()
        mock_print.assert_any_call("🩺 Nearby Medical Stores:")
        mock_print.assert_any_call("• Store1 - Address1")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.get_user_location')
    def test_medical_store_no_location(self, mock_get_location, mock_print, mock_input):
        mock_get_location.return_value = None
        mock_input.side_effect = ["medical store", "exit"]
        main.chatbot()
        mock_print.assert_any_call("❌ Cannot fetch nearby stores without location.")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.get_ayurveda_tip')
    def test_ayurveda_command(self, mock_get_tip, mock_print, mock_input):
        mock_get_tip.return_value = "Drink warm water"
        mock_input.side_effect = ["ayurveda", "cough", "exit"]
        main.chatbot()
        mock_print.assert_any_call("🌿 Tip:", "Drink warm water")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.emergency_call')
    def test_emergency_command(self, mock_emergency_call, mock_print, mock_input):
        mock_input.side_effect = ["emergency", "exit"]
        main.chatbot()
        mock_emergency_call.assert_called_once()
        mock_print.assert_any_call("📞 Connecting to emergency services...")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.get_medicine_details')
    def test_medicine_command(self, mock_get_details, mock_print, mock_input):
        mock_get_details.return_value = "Used for pain relief"
        mock_input.side_effect = ["medicine", "Paracetamol", "exit"]
        main.chatbot()
        mock_print.assert_any_call("Used for pain relief")

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.reminder_input.main')
    @patch('subprocess.Popen')
    def test_reminder_command_start_notify(self, mock_popen, mock_reminder_main, mock_print, mock_input):
        mock_input.side_effect = ["reminder", "n", "exit"]
        main.chatbot()
        mock_reminder_main.assert_called_once()
        mock_popen.assert_not_called()

        mock_input.side_effect = ["reminder", "y", "exit"]
        main.chatbot()
        mock_reminder_main.assert_called()
        mock_popen.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_unknown_command(self, mock_print, mock_input):
        mock_input.side_effect = ["unknown", "exit"]
        main.chatbot()
        mock_print.assert_any_call("🤔 I didn't understand that. You can ask about location, medical stores, ayurveda tips, emergency, medicine info, or reminders.")

if __name__ == "__main__":
    unittest.main()
