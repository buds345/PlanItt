import customtkinter as ctk
from tkinter import messagebox
from firebase.firebase_config import db

def add_schedule_item(event_id, time, activity, notes):
    schedule_item = {
        "time": time,
        "activity": activity,
        "notes": notes,
        "event_id": event_id,
    }
    db.collection("schedules").add(schedule_item)
    return "Schedule item added successfully."
 
def get_schedule(event_id):
    schedule_ref = db.collection("schedules").where("event_id", "==", event_id)
    schedule_items = schedule_ref.stream()

    schedule_list = []
    for item in schedule_items:
        data = item.to_dict()
        data['id'] = item.id   # <--- Add Firestore document ID
        schedule_list.append(data)

    return schedule_list

def delete_schedule_item(doc_id):
    db.collection("schedules").document(doc_id).delete()
    return "Schedule item deleted successfully."

class SchedulePage(ctk.CTkFrame):
    def __init__(self, master, event_id, back_callback):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.event_id = event_id
        self.back_callback = back_callback
 
        ctk.CTkLabel(self, text="Event Schedule", font=("Segoe UI", 20)).pack(pady=10)
 
        self.time_entry = ctk.CTkEntry(self, placeholder_text="Time (e.g. 10:00 AM)")
        self.time_entry.pack(pady=5)
 
        self.activity_entry = ctk.CTkEntry(self, placeholder_text="Activity")
        self.activity_entry.pack(pady=5)
 
        self.notes_entry = ctk.CTkEntry(self, placeholder_text="Notes (optional)")
        self.notes_entry.pack(pady=5)
 
        ctk.CTkButton(self, text="Add Schedule Item", command=self.add_item).pack(pady=10)
        ctk.CTkButton(self, text="Load Schedule", command=self.load_schedule).pack(pady=5)
 
        self.schedule_frame = ctk.CTkScrollableFrame(self, width=300, height=300)
        self.schedule_frame.pack(pady=10)

        ctk.CTkButton(self, text="Back to Events", command=self.back_to_events).pack(pady=10)

        self.checkbox_vars = []

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
        # Clear previous schedule display
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()

        schedule = get_schedule(self.event_id)
        if not schedule:
            label = ctk.CTkLabel(self.schedule_frame, text="No schedule items found.")
            label.pack(anchor="w", pady=2)
        else:
            for item in schedule:
                item_frame = ctk.CTkFrame(self.schedule_frame)
                item_frame.pack(fill="x", pady=2, padx=5)

                text = f"{item['time']} - {item['activity']} ({item.get('notes', '')})"
                var = ctk.BooleanVar()
                checkbox = ctk.CTkCheckBox(item_frame, text=text, variable=var)
                checkbox.pack(side="left", fill="x", expand=True)

                delete_button = ctk.CTkButton(item_frame, text="Delete", width=60, fg_color="red", hover_color="darkred", command=lambda doc_id=item['id']: self.delete_item(doc_id))
                delete_button.pack(side="right", padx=5)

                self.checkbox_vars.append(var)

        messagebox.showinfo("Info", "Schedule loaded.")

    def delete_item(self, doc_id):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?")
        if confirm:
            result = delete_schedule_item(doc_id)
            messagebox.showinfo("Deleted", result)
            self.load_schedule()

    def back_to_events(self):
        self.destroy()
        self.back_callback()
