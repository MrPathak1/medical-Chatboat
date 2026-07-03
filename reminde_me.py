import json
import datetime
import time
import pywhatkit
import threading
import os

REMINDERS_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

def input_medicine_reminder():
    medicine_name = input("Enter the name of the medicine: ").strip()
    
    times = []
    print("Enter reminder times in 24-hour HH:MM format. Type 'done' when finished:")
    while True:
        t = input("Time: ").strip()
        if t.lower() == "done":
            break
        try:
            datetime.datetime.strptime(t, "%H:%M")
            times.append(t)
        except ValueError:
            print("Invalid time format. Please enter time as HH:MM.")
    
    days = []
    print("Enter days to remind (e.g. Monday, Tuesday) or number of days (e.g. 4days). Type 'done' when finished:")
    while True:
        d = input("Day or number of days: ").strip()
        if d.lower() == "done":
            break
        if d.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            days.append(d.capitalize())
        elif d.lower().endswith("days") and d[:-4].isdigit():
            days.append(d.lower())
        else:
            print("Invalid input. Enter a day name or number of days like '4days'.")
    
    reminder = {
        "medicine": medicine_name,
        "times": times,
        "days": days
    }
    return reminder

def get_current_day_name():
    return datetime.datetime.now().strftime("%A")

def is_reminder_due(reminder):
    current_day = get_current_day_name()
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    # Check if current day matches reminder days
    if any(day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] for day in reminder["days"]):
        if current_day not in reminder["days"]:
            return False
    else:
        # Handle number of days like '4days'
        for day in reminder["days"]:
            if day.endswith("days"):
                num_days = int(day[:-4])
                # Check if today is within num_days from the reminder creation date
                # For simplicity, assume reminder was created today and count days from then
                # This can be improved by storing creation date in reminder
                # Here, we just allow reminder for num_days from now
                # So we consider reminder valid for num_days days from now
                # We will skip this check for now as no creation date is stored
                pass
    
    # Check if current time matches any reminder time
    if current_time in reminder["times"]:
        return True
    return False

def send_whatsapp_message(medicine):
    # User must be logged into WhatsApp Web on their computer
    # The message will be sent to the user's own WhatsApp number
    # User needs to input their phone number here in international format
    phone_number = input("Enter your WhatsApp phone number with country code (e.g. +1234567890): ").strip()
    message = f"Reminder: It's time to take your medicine: {medicine}"
    # Send message immediately (delay 0)
    pywhatkit.sendwhatmsg_instantly(phone_number, message)
    print(f"WhatsApp reminder sent for medicine: {medicine}")

def reminder_loop():
    reminders = load_reminders()
    print("Reminder service started. Press Ctrl+C to stop.")
    try:
        while True:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.strftime("%A")
            for reminder in reminders:
                # Check if reminder is due
                if current_day in reminder["days"] or any(day.endswith("days") for day in reminder["days"]):
                    if current_time in reminder["times"]:
                        # Send WhatsApp message in a separate thread to avoid blocking
                        threading.Thread(target=send_whatsapp_message, args=(reminder["medicine"],)).start()
                        # To avoid multiple sends in the same minute, sleep for 60 seconds
                        time.sleep(60)
            time.sleep(20)
    except KeyboardInterrupt:
        print("Reminder service stopped.")

def main():
    print("Medicine Reminder Setup")
    reminders = load_reminders()
    while True:
        reminder = input_medicine_reminder()
        reminders.append(reminder)
        save_reminders(reminders)
        more = input("Add another reminder? (y/n): ").strip().lower()
        if more != "y":
            break
    print("Starting reminder service...")
    reminder_loop()

if __name__ == "__main__":
    main()
