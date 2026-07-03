import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import gui_chatbot

class TestModernMedChatBotGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = gui_chatbot.ModernMedChatBotGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_display_message(self):
        self.app.display_message("Test message")
        content = self.app.conversation.get("1.0", tk.END)
        self.assertIn("Test message", content)

    @patch('gui_chatbot.get_user_location')
    def test_get_location_with_location(self, mock_get_location):
        mock_get_location.return_value = [12.34, 56.78]
        self.app.display_message = MagicMock()
        self.app.get_location()
        self.app.display_message.assert_called_with("Bot: 📍 Your location is approximately: [12.34, 56.78]")

    @patch('gui_chatbot.get_user_location')
    def test_get_location_without_location(self, mock_get_location):
        mock_get_location.return_value = None
        self.app.display_message = MagicMock()
        self.app.get_location()
        self.app.display_message.assert_called_with("Bot: ❌ Unable to get location.")

    @patch('gui_chatbot.find_nearby_places')
    @patch('gui_chatbot.get_user_location')
    def test_find_stores_with_stores(self, mock_get_location, mock_find_stores):
        mock_get_location.return_value = [12.34, 56.78]
        mock_find_stores.return_value = [{'name': 'Store1', 'address': 'Address1'}]
        self.app.display_message = MagicMock()
        self.app.find_stores()
        self.app.display_message.assert_any_call("Bot: 🏥 Nearby Medical Stores:")
        self.app.display_message.assert_any_call("• Store1 - Address1")

    @patch('gui_chatbot.find_nearby_places')
    @patch('gui_chatbot.get_user_location')
    def test_find_stores_no_stores(self, mock_get_location, mock_find_stores):
        mock_get_location.return_value = [12.34, 56.78]
        mock_find_stores.return_value = []
        self.app.display_message = MagicMock()
        self.app.find_stores()
        self.app.display_message.assert_called_with("Bot: ❌ No nearby medical stores found.")

    @patch('gui_chatbot.get_user_location')
    def test_find_stores_no_location(self, mock_get_location):
        mock_get_location.return_value = None
        self.app.display_message = MagicMock()
        self.app.find_stores()
        self.app.display_message.assert_called_with("Bot: ❌ Cannot fetch nearby stores without location.")

    @patch('gui_chatbot.simpledialog.askstring')
    @patch('gui_chatbot.get_ayurveda_tip')
    def test_get_ayurveda_tip_with_issue(self, mock_get_tip, mock_askstring):
        mock_askstring.return_value = "cough"
        mock_get_tip.return_value = "Drink warm water"
        self.app.display_message = MagicMock()
        self.app.get_ayurveda_tip()
        self.app.display_message.assert_called_with("Bot: 🌿 Tip for cough - Drink warm water")

    @patch('gui_chatbot.simpledialog.askstring')
    def test_get_ayurveda_tip_no_issue(self, mock_askstring):
        mock_askstring.return_value = None
        self.app.display_message = MagicMock()
        self.app.get_ayurveda_tip()
        self.app.display_message.assert_called_with("Bot: ❌ No health issue entered.")

    @patch('gui_chatbot.messagebox.showinfo')
    @patch('gui_chatbot.emergency_call')
    def test_trigger_emergency(self, mock_emergency_call, mock_showinfo):
        self.app.display_message = MagicMock()
        self.app.trigger_emergency()
        mock_showinfo.assert_called_once()
        mock_emergency_call.assert_called_once()
        self.app.display_message.assert_called_with("Bot: 📞 Emergency services contacted.")

    @patch('gui_chatbot.simpledialog.askstring')
    @patch('gui_chatbot.get_medicine_details')
    def test_get_medicine_info_with_name(self, mock_get_details, mock_askstring):
        mock_askstring.return_value = "Paracetamol"
        mock_get_details.return_value = "Used for pain relief"
        self.app.display_message = MagicMock()
        self.app.get_medicine_info()
        self.app.display_message.assert_called_with("Bot: 💊 Used for pain relief")

    @patch('gui_chatbot.simpledialog.askstring')
    def test_get_medicine_info_no_name(self, mock_askstring):
        mock_askstring.return_value = None
        self.app.display_message = MagicMock()
        self.app.get_medicine_info()
        self.app.display_message.assert_called_with("Bot: ❌ No medicine name entered.")

    @patch('gui_chatbot.subprocess.Popen')
    @patch('gui_chatbot.messagebox.askyesno')
    @patch('reminder_gui.ReminderInputGUI')
    def test_setup_reminder_start_notify(self, mock_reminder_gui, mock_askyesno, mock_popen):
        mock_askyesno.return_value = True
        self.app.display_message = MagicMock()
        self.app.setup_reminder()
        self.app.display_message.assert_any_call("Bot: 📝 Launching medicine reminder setup...")
        self.app.display_message.assert_any_call("Bot: 🔔 Starting reminder notification service in background...")
        mock_popen.assert_called_once()

    @patch('gui_chatbot.messagebox.askyesno')
    @patch('reminder_gui.ReminderInputGUI')
    def test_setup_reminder_no_start_notify(self, mock_reminder_gui, mock_askyesno):
        mock_askyesno.return_value = False
        self.app.display_message = MagicMock()
        self.app.setup_reminder()
        self.app.display_message.assert_any_call("Bot: 📝 Launching medicine reminder setup...")


    def test_quit_chat(self):
        self.app.display_message = MagicMock()
        self.app.root.after = MagicMock()
        self.app.quit_chat()
        self.app.display_message.assert_called_with("Bot: 👋 Take care! Stay healthy.")
        self.app.root.after.assert_called()

if __name__ == "__main__":
    unittest.main()
