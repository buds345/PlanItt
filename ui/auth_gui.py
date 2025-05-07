import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox

from auth.register import register_user
from auth.login import login_user
from events_gui import EventDashboard
import firebase_admin
from firebase_admin import firestore

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # Optional custom theme later

class AuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PlanIt - Event App")
        self.geometry("400x500")
        self.resizable(True, True)

        self.mode = "login"
        self.build_login_ui()

    def build_profile_ui(self):
        self.clear_ui()

        ctk.CTkLabel(self, text="Profile", font=("Segoe UI", 22)).pack(pady=20)

        name = self.logged_in_user.get("name", "No Name")
        user_email = self.logged_in_user.get("email", "No Email")

        ctk.CTkLabel(self, text=f"Name: {name}").pack(pady=10)
        ctk.CTkLabel(self, text=f"Email: {user_email}").pack(pady=10)

        ctk.CTkButton(self, text="Edit Profile", command=self.edit_profile_ui).pack(pady=20)
        ctk.CTkButton(self, text="Back to Dashboard", command=lambda: self.show_event_dashboard(self.logged_in_user), fg_color="transparent", border_color="#ff007f", border_width=2, text_color="#ff007f").pack()

        ctk.CTkButton(self, text="Log Out", command=self.logout_user, fg_color="red").pack(pady=10)
        ctk.CTkButton(self, text="Delete Account", command=self.delete_account, fg_color="darkred").pack(pady=10)

    def edit_profile_ui(self):
        self.clear_ui()

        ctk.CTkLabel(self, text="Edit Profile", font=("Segoe UI", 22)).pack(pady=20)

        self.new_name_entry = ctk.CTkEntry(self, placeholder_text="New Name")
        self.new_name_entry.pack(pady=10)

        self.new_email_entry = ctk.CTkEntry(self, placeholder_text="New Email")
        self.new_email_entry.pack(pady=10)

        ctk.CTkButton(self, text="Save Changes", command=self.save_profile_changes, fg_color="#ff007f").pack(pady=20)
        ctk.CTkButton(self, text="Back to Profile", command=self.build_profile_ui, fg_color="transparent", border_color="#ff007f", border_width=2, text_color="#ff007f").pack()

    def save_profile_changes(self):
        new_name = self.new_name_entry.get()
        new_email = self.new_email_entry.get()

        if new_name and new_email:
            self.logged_in_user['name'] = new_name
            self.logged_in_user['email'] = new_email
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.build_profile_ui()  # Go back to profile page
        else:
            messagebox.showerror("Error", "Please fill out both fields.")

    def change_password_ui(self):
        self.clear_ui()

        ctk.CTkLabel(self, text="Change Password", font=("Segoe UI", 22)).pack(pady=20)

        self.current_password_entry = ctk.CTkEntry(self, placeholder_text="Current Password", show="*")
        self.current_password_entry.pack(pady=10)

        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        self.new_password_entry.pack(pady=10)

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirm New Password", show="*")
        self.confirm_password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Save New Password", command=self.save_new_password, fg_color="#ff007f").pack(pady=20)
        ctk.CTkButton(self, text="Back to Profile", command=self.build_profile_ui, fg_color="transparent", border_color="#ff007f", border_width=2, text_color="#ff007f").pack()

    def save_new_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password == confirm_password:
            if current_password == self.logged_in_user.get("password"):
                self.logged_in_user['password'] = new_password
                messagebox.showinfo("Success", "Password changed successfully!")
                self.build_profile_ui()
            else:
                messagebox.showerror("Error", "Current password is incorrect.")
        else:
            messagebox.showerror("Error", "New passwords do not match.")

    def logout_user(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if confirm:
            self.logged_in_user = None
            self.build_login_ui()
            
    def delete_account(self):
        from tkinter import messagebox
        from google.cloud import firestore

        confirm = messagebox.askyesno("Confirm Deletion", "This will permanently delete your account. Continue?")
        if confirm:
            try:
                db = firestore.client()
                user_email = self.logged_in_user.get("email")
                users_ref = db.collection("users")
                query = users_ref.where("email", "==", user_email).get()
                for doc in query:
                    doc.reference.delete()

                messagebox.showinfo("Deleted", "Your account has been deleted.")
                self.logged_in_user = None
                self.build_login_ui()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete account: {e}")   

    def clear_ui(self):
        for widget in self.winfo_children():
            widget.destroy()


    def build_login_ui(self):
        self.clear_ui()
        ctk.CTkLabel(self, text="Sign In", font=("Segoe UI", 22)).pack(pady=20)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.handle_login, fg_color="#ff007f").pack(pady=20)

        ctk.CTkButton(self, text="No account? Register", command=self.build_register_ui, fg_color="transparent", border_color="#ff007f", border_width=2, text_color="#ff007f").pack()

    def build_register_ui(self):
        self.clear_ui()
        ctk.CTkLabel(self, text="Register", font=("Segoe UI", 22)).pack(pady=20)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Name")
        self.name_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Register", command=self.handle_register, fg_color="#ff007f").pack(pady=20)

        ctk.CTkButton(self, text="Already registered? Sign In", command=self.build_login_ui, fg_color="transparent", border_color="#ff007f", border_width=2, text_color="#ff007f").pack()

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = login_user(email, password)

        if user == "unverified":
            messagebox.showwarning("Verify Email", "Please verify your email before logging in.")
        elif user:
            messagebox.showinfo("Success", "Login successful!")
            self.show_event_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def show_event_dashboard(self, user_data):
        self.clear_ui()
        self.dashboard = EventDashboard(self, user_data)

    def handle_register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        if register_user(name, email, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.build_login_ui()
        else:
            messagebox.showerror("Error", "Registration failed.")

if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()
