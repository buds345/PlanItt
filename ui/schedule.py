import customtkinter as ctk
from tkinter import messagebox

# Mock schedule storage (in-memory)
schedule_db = {}

def add_schedule_item(event_id, time_str, activity, notes):
    if event_id not in schedule_db:
        schedule_db[event_id] = []

    for item in schedule_db[event_id]:
        if item["time"] == time_str and item["activity"].lower() == activity.lower():
            return "This schedule item already exists."

    schedule_db[event_id].append({
        "time": time_str,
        "activity": activity,
        "notes": notes
    })
    return "Schedule item added successfully."


def get_schedule(event_id):
    return schedule_db.get(event_id, [])


class SchedulePage(ctk.CTkFrame):
    def __init__(self, master, event_id):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.event_id = event_id

        ctk.CTkLabel(self, text="Event Schedule", font=("Segoe UI", 20)).pack(pady=10)

        self.time_entry = ctk.CTkEntry(self, placeholder_text="Time (e.g. 10:00 AM)")
        self.time_entry.pack(pady=5)

        self.activity_entry = ctk.CTkEntry(self, placeholder_text="Activity")
        self.activity_entry.pack(pady=5)

        self.notes_entry = ctk.CTkEntry(self, placeholder_text="Notes (optional)")
        self.notes_entry.pack(pady=5)

        ctk.CTkButton(self, text="Add Schedule Item", command=self.add_item).pack(pady=10)
        ctk.CTkButton(self, text="Load Schedule", command=self.load_schedule).pack(pady=5)

        self.schedule_list = ctk.CTkTextbox(self, width=300, height=200)
        self.schedule_list.pack(pady=10)

    def add_item(self):
        time_str = self.time_entry.get()
        activity = self.activity_entry.get()
        notes = self.notes_entry.get()

        if time_str and activity:
            result = add_schedule_item(self.event_id, time_str, activity, notes)
            messagebox.showinfo("Success", result)

            # Clear input fields
            self.time_entry.delete(0, "end")
            self.activity_entry.delete(0, "end")
            self.notes_entry.delete(0, "end")
        else:
            messagebox.showerror("Error", "Time and activity are required.")

    def load_schedule(self):
        self.schedule_list.delete("0.0", "end")
        schedule = get_schedule(self.event_id)
        if not schedule:
            self.schedule_list.insert("end", "No schedule items found.\n")
        else:
            for item in schedule:
                entry = f"{item['time']} - {item['activity']} ({item.get('notes', '')})\n"
                self.schedule_list.insert("end", entry)
        messagebox.showinfo("Info", "Schedule loaded.")
