import json
import datetime
import os

REMINDERS_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return []
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
        "days": days,
        "created_on": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    return reminder

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
    print("Reminders saved successfully!")

def save_reminder_from_gui(reminder):
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)

if __name__ == "__main__":
    main()
