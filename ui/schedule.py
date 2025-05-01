import customtkinter as ctk
from tkinter import messagebox

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
        time = self.time_entry.get()
        activity = self.activity_entry.get()
        notes = self.notes_entry.get()

        if time and activity:
            result = add_schedule_item(self.event_id, time, activity, notes)
            messagebox.showinfo("Success", result)
            self.load_schedule()
        else:
            messagebox.showerror("Error", "Time and activity are required.")

    def load_schedule(self):
        self.schedule_list.delete("0.0", "end")
        schedule = get_schedule(self.event_id)
        for item in schedule:
            entry = f"{item['time']} - {item['activity']} ({item.get('notes', '')})\n"
            self.schedule_list.insert("end", entry)
