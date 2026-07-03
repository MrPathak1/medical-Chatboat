# Creating a redesigned and fully-featured GUI for the updated chatbot functionality.
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
from location import get_user_location
from store_finder import find_nearby_places
from ayurveda_helper import load_ayurveda_data, get_ayurveda_tip
from emergency import emergency_call
from medicine_info import get_medicine_details
import reminder_input
import subprocess
import os
from chat import get_bot_response

class ModernMedChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🩺 MED-CHAT-BOT")
        self.root.geometry("800x700")
        self.root.configure(bg="#1F2937")

        self.ayurveda_data = load_ayurveda_data()

        self.title_label = tk.Label(root, text="MED-CHAT-BOT", font=("Helvetica", 26, "bold"),
                                    bg="#111827", fg="white", pady=10)
        self.title_label.pack(fill=tk.X)

        self.conversation = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD,
                                                      bg="#F9FAFB", fg="#111827", font=("Helvetica", 12),
                                                      bd=0, padx=10, pady=10)
        self.conversation.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(root, bg="#1F2937")
        self.input_frame.pack(pady=10, padx=20, fill=tk.X)

        self.user_input = tk.Entry(self.input_frame, font=("Helvetica", 12),
                                   bg="#E5E7EB", fg="#111827", bd=0, relief=tk.FLAT)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message,
                                     bg="#3B82F6", fg="white", font=("Helvetica", 11, "bold"),
                                     bd=0, relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.send_button.pack(side=tk.RIGHT)

        # Quick command buttons
        self.command_frame = tk.Frame(root, bg="#111827")
        self.command_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        commands = [
            ("📍 Location", self.get_location),
            ("🏥 Stores", self.find_stores),
            ("🌿 Ayurveda", self.get_ayurveda_tip),
            ("📞 Emergency", self.trigger_emergency),
            ("💊 Medicine Info", self.get_medicine_info),
            ("⏰ Reminder", self.setup_reminder),
            ("❌ Exit", self.quit_chat)
        ]

        for text, command in commands:
            btn = tk.Button(self.command_frame, text=text, command=command,
                            bg="#4B5563", fg="white", font=("Helvetica", 10),
                            relief=tk.FLAT, padx=10, pady=5, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5)

        self.display_message("🤖 Welcome to the Medical Assistant Chatbot!")

    def display_message(self, message):
        self.conversation.config(state='normal')
        self.conversation.insert(tk.END, message + "\n")
        self.conversation.config(state='disabled')
        self.conversation.see(tk.END)

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return
        self.display_message(f"You: {user_text}")
        self.user_input.delete(0, tk.END)
        self.process_input(user_text.lower())

    def process_input(self, user_input):
        if "location" in user_input:
            self.get_location()
        elif "store" in user_input or "pharmacy" in user_input:
            self.find_stores()
        elif "ayurveda" in user_input or "tip" in user_input:
            self.get_ayurveda_tip()
        elif "emergency" in user_input:
            self.trigger_emergency()
        elif "medicine" in user_input:
            self.get_medicine_info()
        elif "reminder" in user_input or "remind" in user_input:
            self.setup_reminder()
        elif "exit" in user_input or "quit" in user_input:
            self.quit_chat()
        else:
            # Use chat.py's get_bot_response for other inputs
            bot_response = get_bot_response(user_input)
            self.display_message(f"Bot: {bot_response}")

    def get_location(self):
        loc = get_user_location()
        msg = f"📍 Your location is approximately: {loc}" if loc else "❌ Unable to get location."
        self.display_message(f"Bot: {msg}")

    def find_stores(self):
        loc = get_user_location()
        if loc:
            stores = find_nearby_places(loc[0], loc[1])
            if stores:
                self.display_message("Bot: 🏥 Nearby Medical Stores:")
                for store in stores:
                    self.display_message(f"• {store['name']} - {store['address']}")
            else:
                self.display_message("Bot: ❌ No nearby medical stores found.")
        else:
            self.display_message("Bot: ❌ Cannot fetch nearby stores without location.")

    def get_ayurveda_tip(self):
        issue = simpledialog.askstring("Ayurveda Tip", "Enter your health issue (e.g., cough, cold):", parent=self.root)
        if issue:
            tip = get_ayurveda_tip(issue, self.ayurveda_data)
            self.display_message(f"Bot: 🌿 Tip for {issue} - {tip}")
        else:
            self.display_message("Bot: ❌ No health issue entered.")

    def trigger_emergency(self):
        messagebox.showinfo("Emergency", "📞 Connecting to emergency services...")
        emergency_call()
        self.display_message("Bot: 📞 Emergency services contacted.")

    def get_medicine_info(self):
        medicine_name = simpledialog.askstring("Medicine Info", "Enter the medicine name:", parent=self.root)
        if medicine_name:
            details = get_medicine_details(medicine_name)
            self.display_message(f"Bot: 💊 {details}")
        else:
            self.display_message("Bot: ❌ No medicine name entered.")

    def setup_reminder(self):
        self.display_message("Bot: 📝 Launching medicine reminder setup...")
        import reminder_gui
        reminder_window = tk.Toplevel(self.root)
        reminder_app = reminder_gui.ReminderInputGUI(reminder_window)
        reminder_window.grab_set()
        reminder_window.wait_window()
        self.root.focus_set()

        start_notify = messagebox.askyesno("Reminder Service", "Start reminder notification service now?")
        if start_notify:
            self.display_message("Bot: 🔔 Starting reminder notification service in background...")
            subprocess.Popen(["python", "reminder_notify.py"],
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)

    def quit_chat(self):
        self.display_message("Bot: 👋 Take care! Stay healthy.")
        self.root.after(1500, self.root.quit)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMedChatBotGUI(root)
    root.mainloop()
