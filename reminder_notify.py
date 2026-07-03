import json
import datetime
import time
import threading
import pywhatkit
import os

REMINDERS_FILE = "reminders.json"
phone_number = None  # Global to avoid asking repeatedly

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return []

def get_current_day_name():
    return datetime.datetime.now().strftime("%A")

def is_reminder_due(reminder):
    current_day = get_current_day_name()
    current_time = datetime.datetime.now().strftime("%H:%M")
    today = datetime.datetime.now().date()

    if any(day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] for day in reminder["days"]):
        if current_day not in reminder["days"]:
            return False

    for day in reminder["days"]:
        if day.endswith("days") and day[:-4].isdigit():
            num_days = int(day[:-4])
            creation_date = datetime.datetime.strptime(reminder["created_on"], "%Y-%m-%d").date()
            if (today - creation_date).days >= num_days:
                return False

    return current_time in reminder["times"]

def send_whatsapp_message(medicine):
    global phone_number
    if not phone_number:
        phone_number = input("Enter your WhatsApp phone number with country code (e.g. +1234567890): ").strip()
    message = f"Reminder: It's time to take your medicine: {medicine}"
    try:
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        print(f"WhatsApp reminder sent for medicine: {medicine}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def reminder_loop():
    reminders = load_reminders()
    sent_flags = set()
    print("Reminder service started. Press Ctrl+C to stop.")
    try:
        while True:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            for reminder in reminders:
                if is_reminder_due(reminder):
                    flag = (reminder["medicine"], current_time)
                    if flag not in sent_flags:
                        threading.Thread(target=send_whatsapp_message, args=(reminder["medicine"],)).start()
                        sent_flags.add(flag)
            if datetime.datetime.now().second == 0:
                sent_flags.clear()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Reminder service stopped.")

if __name__ == "__main__":
    reminder_loop()
