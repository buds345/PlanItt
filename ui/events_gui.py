# events_gui.py

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from firebase.firebase_config import db
from tkcalendar import DateEntry
from schedule import SchedulePage

def launch_events_gui(user_data):
    app = EventDashboard(user_data)
    app.mainloop()

class EventDashboard(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.master = master
        self.user_data = user_data
        self.user_email = user_data["email"]
        self.username = user_data["username"]
        self.user_id = user_data["id"]  # Firestore doc ID

        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text=f"Welcome, {self.username}", font=("Segoe UI", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Name", "Location", "Date", "Time"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        self.edit_btn = ctk.CTkButton(btn_frame, text="Edit Selected", command=self.edit_event)
        self.delete_btn = ctk.CTkButton(btn_frame, text="Delete Selected", command=self.delete_event)
        self.edit_btn.pack(side="left", padx=10)
        self.delete_btn.pack(side="left", padx=10)


        ctk.CTkButton(self, text="Create Event", command=self.choose_event_type).pack(pady=10)
        ctk.CTkButton(self, text="Manage Schedule", command=lambda: self.open_schedule(event_id)).pack(pady=10)
        self.load_events()

    def open_schedule(self, event_id):
        self.destroy()
        SchedulePage(self.master, event_id)
       
    def edit_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event to edit.")
            return

        item_id = selected[0]
        doc_id = self.event_ids[item_id]
        event_doc = db.collection("events").document(doc_id).get()

        if event_doc.exists:
            data = event_doc.to_dict()
            self.clear_window()

            ctk.CTkLabel(self, text="Edit Event", font=("Segoe UI", 14)).pack(pady=10)

            self.event_name = ctk.CTkEntry(self, placeholder_text="Event Name")
            self.event_location = ctk.CTkEntry(self, placeholder_text="Location")

            self.event_name.insert(0, data["name"])
            self.event_location.insert(0, data["location"])

            self.event_name.pack(pady=5)
            self.event_location.pack(pady=5)

            # Date picker
            ctk.CTkLabel(self, text="Select Date").pack(pady=2)
            self.event_date = DateEntry(self, width=18, background="darkblue", foreground="white", borderwidth=2)
            self.event_date.set_date(data["date"])  # Set current date
            self.event_date.pack(pady=5)

            # Time picker
            ctk.CTkLabel(self, text="Select Time").pack(pady=2)
            time_frame = ctk.CTkFrame(self)
            time_frame.pack(pady=5)

            self.hour_var = tk.StringVar(value=data["time"].split(":")[0])
            self.minute_var = tk.StringVar(value=data["time"].split(":")[1])

            hours = [f"{i:02d}" for i in range(0, 24)]
            minutes = [f"{i:02d}" for i in range(0, 60, 5)]

            self.hour_menu = ctk.CTkOptionMenu(time_frame, variable=self.hour_var, values=hours, width=30)
            self.minute_menu = ctk.CTkOptionMenu(time_frame, variable=self.minute_var, values=minutes, width=30)

            self.hour_menu.pack(side="left", padx=5)
            self.minute_menu.pack(side="left", padx=5)

            ctk.CTkButton(self, text="Update Event", command=lambda: self.update_event(doc_id)).pack(pady=10)
            ctk.CTkButton(self, text="Back to Events", command=self.reset_ui).pack(pady=5)

    def update_event(self, doc_id):
        name = self.event_name.get()
        location = self.event_location.get()
        date = self.event_date.get()
        time = f"{self.hour_var.get()}:{self.minute_var.get()}"

        if not all([name, location, date, time]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        updated_data = {
            "name": name,
            "location": location,
            "date": date,
            "time": time,
        }

        db.collection("events").document(doc_id).update(updated_data)
        messagebox.showinfo("Success", "Event updated successfully!")
        self.reset_ui()

    def delete_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an event to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this event?")
        if not confirm:
            return

        item_id = selected[0]
        doc_id = self.event_ids[item_id]

        db.collection("events").document(doc_id).delete()
        messagebox.showinfo("Deleted", "Event deleted successfully.")
        self.reset_ui()

       
    def choose_event_type(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Choose Event Type", font=("Segoe UI", 14)).pack(pady=10)

        for event_type in ["Birthday", "Wedding", "Conference"]:
            ctk.CTkButton(self, text=event_type, command=lambda t=event_type: self.create_event_form(t)).pack(pady=5)

    def create_event_form(self, event_type):
        self.clear_window()
        ctk.CTkLabel(self, text=f"Create a {event_type}", font=("Segoe UI", 14)).pack(pady=10)

        self.event_name = ctk.CTkEntry(self, placeholder_text="Event Name")
        self.event_location = ctk.CTkEntry(self, placeholder_text="Location")
        self.event_name.pack(pady=5)
        self.event_location.pack(pady=5)

        # Calendar picker for date
        ctk.CTkLabel(self, text="Select Date").pack(pady=2)
        self.event_date = DateEntry(self, width=18, background="darkblue", foreground="white", borderwidth=2)
        self.event_date.pack(pady=5)

        # Time picker using OptionMenu
        ctk.CTkLabel(self, text="Select Time").pack(pady=2)

        time_frame = ctk.CTkFrame(self)
        time_frame.pack(pady=5)

        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")

        hours = [f"{i:02d}" for i in range(0, 24)]
        minutes = [f"{i:02d}" for i in range(0, 60, 5)]  # 5-minute intervals

        self.hour_menu = ctk.CTkOptionMenu(time_frame, variable=self.hour_var, values=hours,width=30)
        self.minute_menu = ctk.CTkOptionMenu(time_frame, variable=self.minute_var, values=minutes,width=30)

        self.hour_menu.pack(side="left", padx=5)
        self.minute_menu.pack(side="left", padx=5)

        ctk.CTkButton(self, text="Save Event", command=lambda: self.save_event(event_type)).pack(pady=10)
        ctk.CTkButton(self, text="Back to Events", command=self.reset_ui).pack(pady=5)

    def save_event(self, event_type):
        name = self.event_name.get()
        location = self.event_location.get()
        date = self.event_date.get()
        time = f"{self.hour_var.get()}:{self.minute_var.get()}"

        if not all([name, location, date, time]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        event_data = {
            "name": name,
            "location": location,
            "date": date,
            "time": time,
            "type": event_type,
            "user_id": self.user_id
        }

        db.collection("events").add(event_data)
        messagebox.showinfo("Success", f"{event_type} created!")
        self.reset_ui()

    def reset_ui(self):
        self.clear_window()
        self.build_ui()

    def load_events(self):
        self.event_ids = {}  # Add this line at the top of load_events()
        for row in self.tree.get_children():
            self.tree.delete(row)

        events_ref = db.collection("events").where("user_id", "==", self.user_id)
        events = events_ref.stream()

        for event in events:
            data = event.to_dict()
            item_id = self.tree.insert("", "end", values=(data["name"], data["location"], data["date"], data["time"]))
            self.event_ids[item_id] = event.id  # Store doc ID using row ID

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
