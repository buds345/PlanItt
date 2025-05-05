# ui/guest_gui.py

import customtkinter as ctk
from tkinter import ttk, messagebox
from firebase.firebase_config import db
from utils.email_sender import send_invite_email  # Add at the top
import uuid  # Add at the top


class GuestManager(ctk.CTkFrame):
    def __init__(self, master, event_id):
        super().__init__(master)
        self.master = master
        self.event_id = event_id
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Guest List", font=("Segoe UI", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Name", "Email"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill="both", expand=True)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10)

        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Guest Name")
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="Guest Email")
        self.name_entry.pack(side="left", padx=5)
        self.email_entry.pack(side="left", padx=5)

        ctk.CTkButton(self, text="Add Guest", command=self.add_guest).pack(pady=10)
        ctk.CTkButton(self, text="Delete Selected Guest", command=self.delete_guest).pack(pady=5)
        ctk.CTkButton(self, text="Send Invite Email", command=self.send_invite).pack(pady=5)
        ctk.CTkButton(self, text="Back to Events", command=self.go_back).pack(pady=10)

        self.load_guests()

    def load_guests(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        guests_ref = db.collection("events").document(self.event_id).collection("guests")
        guests = guests_ref.stream()

        self.guest_ids = {}

        for guest in guests:
            data = guest.to_dict()
            item_id = self.tree.insert("", "end", values=(data["name"], data["email"]))
            self.guest_ids[item_id] = guest.id

    def add_guest(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name or not email:
            messagebox.showerror("Error", "Both name and email are required.")
            return

        # Generate a unique RSVP token
        rsvp_token = str(uuid.uuid4())

        guest_data = {
            "name": name,
            "email": email,
            "rsvp": "pending",
            "rsvp_token": rsvp_token
        }

        db.collection("events").document(self.event_id).collection("guests").add(guest_data)

        messagebox.showinfo("Success", "Guest added.")
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.load_guests()


    def delete_guest(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a guest to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Delete selected guest?")
        if not confirm:
            return

        item_id = selected[0]
        guest_id = self.guest_ids[item_id]

        db.collection("events").document(self.event_id).collection("guests").document(guest_id).delete()
        messagebox.showinfo("Deleted", "Guest deleted.")
        self.load_guests()

    def go_back(self):
        self.destroy()
        self.master.reset_ui()
    
    def send_invite(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a guest.")
            return

        item_id = selected[0]
        guest_id = self.guest_ids[item_id]
        name, email = self.tree.item(item_id, "values")

        # Fetch RSVP token from Firestore
        guest_doc = db.collection("events").document(self.event_id).collection("guests").document(guest_id).get()
        guest_data = guest_doc.to_dict()
        rsvp_token = guest_data.get("rsvp_token")

        # Construct the RSVP link (assuming you're hosting at http://localhost:5000)
        rsvp_url = f"http://localhost:5000/rsvp/{rsvp_token}"

        # Send the invite with the RSVP link
        success = send_invite_email(email, name, self.event_id, "Your Event Name", rsvp_url)

        if success:
            messagebox.showinfo("Success", "Invitation email sent.")
        else:
            messagebox.showerror("Error", "Failed to send invitation.")
