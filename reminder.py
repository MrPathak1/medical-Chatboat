import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import datetime
import time
import threading
import pywhatkit
import os

class ReminderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder GUI")
        self.root.geometry("400x300")
        self.reminders = self.load_reminders()

        self.title_label = tk.Label(root, text="Reminder GUI", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.medicine_label = tk.Label(root, text="Medicine Name:")
        self.medicine_label.pack()
        self.medicine_entry = tk.Entry(root, font=("Helvetica", 12))
        self.medicine_entry.pack()

        self.time_label = tk.Label(root, text="Reminder Time (HH:MM):")
        self.time_label.pack()
        self.time_entry = tk.Entry(root, font=("Helvetica", 12))
        self.time_entry.pack()

        self.day_label = tk.Label(root, text="Reminder Day (e.g., Monday, Tuesday):")
        self.day_label.pack()
        self.day_entry = tk.Entry(root, font=("Helvetica", 12))
        self.day_entry.pack()

        self.set_reminder_button = tk.Button(root, text="Set Reminder", command=self.set_reminder)
        self.set_reminder_button.pack(pady=20)

        self.start_notification_button = tk.Button(root, text="Start Notification Service", command=self.start_notification_service)
        self.start_notification_button.pack()

    def load_reminders(self):
        if os.path.exists("reminders.json"):
            with open("reminders.json", "r") as f:
                return json.load(f)
        return []

    def save_reminders(self, reminders):
        with open("reminders.json", "w") as f:
            json.dump(reminders, f, indent=4)

    def set_reminder(self):
        medicine_name = self.medicine_entry.get()
        reminder_time = self.time_entry.get()
        reminder_day = self.day_entry.get()

        if medicine_name and reminder_time and reminder_day:
            reminder = {
                "medicine": medicine_name,
                "time": reminder_time,
                "day": reminder_day,
                "created_on": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            self.reminders.append(reminder)
            self.save_reminders(self.reminders)
            messagebox.showinfo("Reminder Set", "Reminder set successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def start_notification_service(self):
        threading.Thread(target=self.notification_loop).start()

    def notification_loop(self):
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M")
            current_day = datetime.datetime.now().strftime("%A")
            for reminder in self.reminders:
                if reminder["time"] == current_time and reminder["day"] == current_day:
                    phone_number = input("Enter your WhatsApp phone number with country code (e.g. +1234567890): ").strip()
                    message = f"Reminder: It's time to take your medicine: {reminder['medicine']}"
                    try:
                        pywhatkit.sendwhatmsg_instantly(phone_number, message)
                        print(f"WhatsApp reminder sent for medicine: {reminder['medicine']}")
                    except Exception as e:
                        print(f"Failed to send message: {e}")
            time.sleep(60)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderGUI(root)
    root.mainloop()