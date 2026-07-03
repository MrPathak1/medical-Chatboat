import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import reminder
import tkinter as tk

class TestReminderGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = reminder.ReminderGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_reminders_file_exists(self, mock_file):
        reminders = self.app.load_reminders()
        self.assertEqual(reminders, [])

    @patch('os.path.exists')
    def test_load_reminders_file_not_exists(self, mock_exists):
        mock_exists.return_value = False
        reminders = self.app.load_reminders()
        self.assertEqual(reminders, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_save_reminders(self, mock_file):
        reminders = [{"medicine": "Med1", "time": "10:00", "day": "Monday"}]
        self.app.save_reminders(reminders)
        mock_file().write.assert_called()

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_set_reminder_valid(self, mock_showerror, mock_showinfo):
        self.app.medicine_entry.insert(0, "Med1")
        self.app.time_entry.insert(0, "10:00")
        self.app.day_entry.insert(0, "Monday")
        self.app.set_reminder()
        mock_showinfo.assert_called_once()
        mock_showerror.assert_not_called()

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_set_reminder_invalid(self, mock_showerror, mock_showinfo):
        self.app.medicine_entry.delete(0, tk.END)
        self.app.time_entry.delete(0, tk.END)
        self.app.day_entry.delete(0, tk.END)
        self.app.set_reminder()
        mock_showerror.assert_called_once()
        mock_showinfo.assert_not_called()

    @patch('threading.Thread')
    def test_start_notification_service(self, mock_thread):
        self.app.start_notification_service()
        mock_thread.assert_called_once()

    @patch('reminder.pywhatkit.sendwhatmsg_instantly')
    @patch('builtins.input', return_value='+1234567890')
    @patch('time.sleep', return_value=None)
    def test_notification_loop_send_message(self, mock_sleep, mock_input, mock_send):
        self.app.reminders = [{
            "medicine": "Med1",
            "time": "12:00",
            "day": "Monday"
        }]
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.side_effect = ["12:00", "Monday"]
            # Run only one iteration of loop by patching while True to False
            with patch('builtins.print') as mock_print:
                # To avoid infinite loop, patch time.sleep to raise exception after first call
                def side_effect(seconds):
                    raise KeyboardInterrupt
                mock_sleep.side_effect = side_effect
                try:
                    self.app.notification_loop()
                except KeyboardInterrupt:
                    pass
                mock_send.assert_called_once()
