import customtkinter as ctk
from tkinter import messagebox
from firebase.firebase_config import db

# Define a custom color theme
PRIMARY_COLOR = "#4f46e5"  # Indigo
SECONDARY_COLOR = "#6366f1"  # Light Indigo
BACKGROUND_COLOR = "#f9fafb"  # Light Gray
TEXT_COLOR = "#1f2937"  # Dark Gray
ERROR_COLOR = "#dc2626"  # Red
SCHEDULE_FRAME_COLOR = "#2d2d2d"  # Dark Gray for schedule display area

class SchedulePage(ctk.CTkFrame):
    def __init__(self, master, event_id, back_callback):
        super().__init__(master, fg_color=BACKGROUND_COLOR)
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.event_id = event_id
        self.back_callback = back_callback

        # Back Button (Positioned at top left)
        button_font = ("Segoe UI", 14)
        self.back_button = ctk.CTkButton(self, text="Back", font=button_font, fg_color="gray", hover_color="darkgray", command=self.back_to_events)
        self.back_button.place(x=10, y=10, anchor="nw")

        # Title
        ctk.CTkLabel(self, text="Event Schedule", font=("Segoe UI", 28, "bold"), text_color=PRIMARY_COLOR).pack(pady=(0, 20), anchor="center")

        # Input fields (Decreasing the width of textboxes)
        entry_font = ("Segoe UI", 14)
        self.time_entry = ctk.CTkEntry(self, placeholder_text="Time (e.g. 10:00 AM)", font=entry_font, width=300)  # Smaller width
        self.time_entry.pack(pady=4, anchor="center")

        self.activity_entry = ctk.CTkEntry(self, placeholder_text="Activity", font=entry_font, width=300)  # Smaller width
        self.activity_entry.pack(pady=4, anchor="center")

        self.notes_entry = ctk.CTkEntry(self, placeholder_text="Notes (optional)", font=entry_font, width=300)  # Smaller width
        self.notes_entry.pack(pady=4, anchor="center")

        # Buttons
        button_font = ("Segoe UI", 14)

        # Smaller buttons
        ctk.CTkButton(self, text="Add Schedule Item", font=button_font, fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR, command=self.add_item, width=20, height=20).pack(pady=5, anchor="center")
        ctk.CTkButton(self, text="Load Schedule", font=button_font, fg_color=PRIMARY_COLOR, hover_color=SECONDARY_COLOR, command=self.load_schedule, width=20, height=20).pack(pady=5, anchor="center")

        # Schedule Frame (Now dark gray)
        self.schedule_frame = ctk.CTkScrollableFrame(self, width=50, height=40, fg_color=SCHEDULE_FRAME_COLOR, corner_radius=20)
        self.schedule_frame.pack(pady=20, fill="both", expand=True, anchor="center")

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

            # Reload the schedule frame to show the newly added item
            self.load_schedule()

        else:
            messagebox.showerror("Error", "Time and activity are required.")

    def load_schedule(self):
        # Clear previous schedule display
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()

        schedule = get_schedule(self.event_id)
        if not schedule:
            label = ctk.CTkLabel(self.schedule_frame, text="No schedule items found.", text_color=TEXT_COLOR)
            label.pack(anchor="w", pady=2)
        else:
            for item in schedule:
                item_frame = ctk.CTkFrame(self.schedule_frame, fg_color="#f3f4f6", corner_radius=8)
                item_frame.pack(fill="x", pady=5, padx=5)

                text = f"{item['time']} - {item['activity']} ({item.get('notes', '')})"
                var = ctk.BooleanVar()
                checkbox = ctk.CTkCheckBox(item_frame, text=text, font=("Segoe UI", 12), text_color=TEXT_COLOR, variable=var)
                checkbox.pack(side="left", fill="x", expand=True, padx=5, pady=5)

                delete_button = ctk.CTkButton(
                    item_frame,
                    text="Delete",
                    font=("Segoe UI", 12),
                    width=70,
                    height=30,
                    fg_color=ERROR_COLOR,
                    hover_color="#b91c1c",
                    command=lambda doc_id=item['id']: self.delete_item(doc_id)
                )
                delete_button.pack(side="right", padx=5, pady=5)

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

# Helper functions (assuming these are already implemented)
def add_schedule_item(event_id, time, activity, notes):
    schedule_item = {"time": time, "activity": activity, "notes": notes, "event_id": event_id}
    db.collection("schedules").add(schedule_item)
    return "Schedule item added successfully."

def get_schedule(event_id):
    schedule_ref = db.collection("schedules").where("event_id", "==", event_id)
    schedule_items = schedule_ref.stream()
    schedule_list = []
    for item in schedule_items:
        data = item.to_dict()
        data['id'] = item.id
        schedule_list.append(data)
    return schedule_list

def delete_schedule_item(doc_id):
    db.collection("schedules").document(doc_id).delete()
    return "Schedule item deleted successfully."

