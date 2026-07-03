import unittest
from unittest.mock import patch, MagicMock
import builtins
import sys

# Import the GUI class and main chatbot function
from gui_chatbot import ModernMedChatBotGUI
import main

import tkinter as tk

class TestModernMedChatBotGUI(unittest.TestCase):
    def setUp(self):
        # Set up a root window for GUI tests
        self.root = tk.Tk()
        self.app = ModernMedChatBotGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('gui_chatbot.get_user_location')
    def test_get_location(self, mock_get_location):
        mock_get_location.return_value = [12.34, 56.78]
        self.app.get_location()
        # Check if the message contains the mocked location
        self.assertIn("12.34", self.app.conversation.get("1.0", tk.END))

    @patch('gui_chatbot.get_user_location')
    @patch('gui_chatbot.find_nearby_places')
    def test_find_stores(self, mock_find_stores, mock_get_location):
        mock_get_location.return_value = [12.34, 56.78]
        mock_find_stores.return_value = [
            {'name': 'Store1', 'address': 'Address1'},
            {'name': 'Store2', 'address': 'Address2'}
        ]
        self.app.find_stores()
        conversation_text = self.app.conversation.get("1.0", tk.END)
        self.assertIn("Store1", conversation_text)
        self.assertIn("Store2", conversation_text)

    @patch('gui_chatbot.simpledialog.askstring')
    @patch('gui_chatbot.get_ayurveda_tip')
    def test_get_ayurveda_tip(self, mock_get_ayurveda_tip, mock_askstring):
        mock_askstring.return_value = "cough"
        mock_get_ayurveda_tip.return_value = "Drink warm water"
        self.app.get_ayurveda_tip()
        conversation_text = self.app.conversation.get("1.0", tk.END)
        self.assertIn("Drink warm water", conversation_text)

    @patch('gui_chatbot.messagebox.showinfo')
    @patch('gui_chatbot.emergency_call')
    def test_trigger_emergency(self, mock_emergency_call, mock_showinfo):
        self.app.trigger_emergency()
        mock_showinfo.assert_called_once()
        mock_emergency_call.assert_called_once()
        conversation_text = self.app.conversation.get("1.0", tk.END)
        self.assertIn("Emergency services contacted", conversation_text)

    @patch('gui_chatbot.simpledialog.askstring')
    @patch('gui_chatbot.get_medicine_details')
    def test_get_medicine_info(self, mock_get_medicine_details, mock_askstring):
        mock_askstring.return_value = "Paracetamol"
        mock_get_medicine_details.return_value = "Used for pain relief"
        self.app.get_medicine_info()
        conversation_text = self.app.conversation.get("1.0", tk.END)
        self.assertIn("Used for pain relief", conversation_text)

    @patch('gui_chatbot.subprocess.Popen')
    @patch('gui_chatbot.messagebox.askyesno')
    @patch('tkinter.Toplevel')
    @patch('reminder_gui.ReminderInputGUI')
    def test_setup_reminder(self, mock_reminder_gui, mock_toplevel, mock_askyesno, mock_popen):
        mock_askyesno.return_value = True
        mock_toplevel.return_value = MagicMock()
        self.app.setup_reminder()
        mock_popen.assert_called_once()

    def test_quit_chat(self):
        self.app.quit_chat()
        # The root window should be scheduled to quit after 1500ms
        self.assertTrue(self.root.tk.call('after', 'info'))

class TestMainChatbot(unittest.TestCase):
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('main.get_user_location')
    @patch('main.find_nearby_places')
    @patch('main.get_ayurveda_tip')
    @patch('main.emergency_call')
    @patch('main.get_medicine_details')
    @patch('main.reminder_input.main')
    @patch('subprocess.Popen')
    def test_chatbot(self, mock_popen, mock_reminder_main, mock_get_medicine_details, mock_emergency_call,
                     mock_get_ayurveda_tip, mock_find_stores, mock_get_location, mock_print, mock_input):
        # Setup mock return values
        mock_get_location.return_value = [12.34, 56.78]
        mock_find_stores.return_value = [{'name': 'Store1', 'address': 'Address1'}]
        mock_get_ayurveda_tip.return_value = "Drink warm water"
        mock_get_medicine_details.return_value = "Used for pain relief"
        mock_reminder_main.return_value = None
        mock_emergency_call.return_value = None

        # Define a sequence of inputs to simulate user interaction
        inputs = iter([
            "location",
            "medical store",
            "ayurveda",
            "cough",
            "emergency",
            "medicine",
            "Paracetamol",
            "reminder",
            "y",
            "exit"
        ])

        def side_effect(prompt=None):
            return next(inputs)

        mock_input.side_effect = side_effect

        # Run chatbot function
        main.chatbot()

        # Check some expected print calls
        mock_print.assert_any_call("🤖 Welcome to the Medical Assistant Chatbot!")
        mock_print.assert_any_call("📍 Your location is approximately: [12.34, 56.78]")
        mock_print.assert_any_call("🩺 Nearby Medical Stores:")
        mock_print.assert_any_call("🌿 Tip:", "Drink warm water")
        mock_print.assert_any_call("📞 Connecting to emergency services...")
        mock_print.assert_any_call("Used for pain relief")
        mock_print.assert_any_call("📝 Launching medicine reminder setup...")
        mock_print.assert_any_call("🔔 Starting reminder notification service in background...")
        mock_print.assert_any_call("👋 Take care! Stay healthy.")

if __name__ == '__main__':
    unittest.main()
