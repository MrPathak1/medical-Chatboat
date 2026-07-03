import tkinter as tk
from tkinter import messagebox
import datetime
import reminder_input

class ReminderInputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Set Medicine Reminder")
        self.root.geometry("350x300")
        self.root.resizable(False, False)

        tk.Label(root, text="Medicine Name:").pack(pady=(10, 0))
        self.medicine_entry = tk.Entry(root, font=("Helvetica", 12))
        self.medicine_entry.pack(pady=5, fill=tk.X, padx=20)

        tk.Label(root, text="Reminder Times (HH:MM, 24-hour):").pack(pady=(10, 0))
        self.times_entry = tk.Entry(root, font=("Helvetica", 12))
        self.times_entry.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(root, text="Separate multiple times with commas").pack()

        tk.Label(root, text="Reminder Days (e.g. Monday, Tuesday or 4days):").pack(pady=(10, 0))
        self.days_entry = tk.Entry(root, font=("Helvetica", 12))
        self.days_entry.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(root, text="Separate multiple days with commas").pack()

        self.submit_button = tk.Button(root, text="Set Reminder", command=self.submit_reminder)
        self.submit_button.pack(pady=20)

    def submit_reminder(self):
        medicine = self.medicine_entry.get().strip()
        times_text = self.times_entry.get().strip()
        days_text = self.days_entry.get().strip()

        if not medicine:
            messagebox.showerror("Error", "Please enter the medicine name.")
            return

        times = [t.strip() for t in times_text.split(",") if t.strip()]
        for t in times:
            try:
                datetime.datetime.strptime(t, "%H:%M")
            except ValueError:
                messagebox.showerror("Error", f"Invalid time format: {t}. Use HH:MM 24-hour format.")
                return

        days = [d.strip() for d in days_text.split(",") if d.strip()]
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for d in days:
            if d not in valid_days and not (d.endswith("days") and d[:-4].isdigit()):
                messagebox.showerror("Error", f"Invalid day format: {d}. Use day names or number of days like '4days'.")
                return

        reminder = {
            "medicine": medicine,
            "times": times,
            "days": days,
            "created_on": datetime.datetime.now().strftime("%Y-%m-%d")
        }

        reminder_input.save_reminder_from_gui(reminder)
        messagebox.showinfo("Success", "Reminder saved successfully!")
        self.root.destroy()
